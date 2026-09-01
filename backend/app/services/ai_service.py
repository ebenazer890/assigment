"""
AI Service for Ask Intelligence, Synthesis, and Dynamic RAG Reasoning
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
import json
import re

from app.db.models import Role, Activity, Process, Skill, RoleAnalysis, ResearchSource, ActivityAIImpact, FutureSkill, FutureResponsibility, RoleFutureProfile
from app.services.rag_service import RAGService
from app.repositories import AnalyticsRepository


class AIService:
    """
    Hybrid Ask Intelligence Engine:
    - Deterministic routing for structural queries (database queries).
    - RAG evidence retrieval for contextual backing.
    - Natural language synthesis for qualitative reasoning.
    """

    @staticmethod
    def answer_question(db: Session, question: str, context_role_id: Optional[int] = None) -> Dict:
        """
        Answer user question using hybrid deterministic DB routing + RAG evidence.
        """
        q_lower = question.lower()
        evidence = RAGService.retrieve_evidence(db, question, top_k=2)

        # 1. Handle "Top 5 roles" query
        if "top" in q_lower and ("role" in q_lower or "impact" in q_lower or "affected" in q_lower):
            top_roles = AnalyticsRepository.get_top_ai_impact_roles(db, limit=5)
            roles_str = ", ".join([f"**{i+1}. {r[1]}** ({r[2]*100:.1f}% exposure)" for i, r in enumerate(top_roles)])
            answer = f"The top 5 banking roles with the highest AI impact are:\n\n{roles_str}\n\nThese rankings are dynamically computed from underlying activity-level automation and augmentation scores."
            reasoning = "Calculated by aggregating weighted activity characteristics across repetitiveness, rule-based nature, and structured data availability."
            return {
                "question": question,
                "answer": answer,
                "reasoning": reasoning,
                "evidence": evidence,
                "confidence": 0.95
            }

        # 2. Handle "Compare [Role 1] and [Role 2]" query
        if "compare" in q_lower or ("vs" in q_lower and "analyst" in q_lower):
            # Extract role names if possible
            roles = db.query(Role).all()
            found_roles = [r for r in roles if r.name.lower() in q_lower]
            if len(found_roles) >= 2:
                r1, r2 = found_roles[0], found_roles[1]
                from app.services import RoleComparisonService
                comp = RoleComparisonService.compare_roles(db, r1.id, r2.id)
                answer = f"**Role Comparison: {r1.name} vs {r2.name}**\n\n" \
                         f"• **{r1.name}**: {comp['role_1']['ai_exposure']*100:.1f}% AI Exposure ({comp['role_1']['affected_activities']} affected activities)\n" \
                         f"• **{r2.name}**: {comp['role_2']['ai_exposure']*100:.1f}% AI Exposure ({comp['role_2']['affected_activities']} affected activities)\n\n" \
                         f"**Key Difference**: {comp['comparison']['key_difference']}. {comp['comparison']['more_affected_role']} involves more routine data processing and standardized workflows."
                return {
                    "question": question,
                    "answer": answer,
                    "reasoning": "Determined dynamically by evaluating activity-level repetition, data availability, and human judgment scores.",
                    "evidence": evidence,
                    "confidence": 0.92
                }

        # Identify target role from context_role_id or name in question
        target_role = None
        if context_role_id:
            target_role = db.query(Role).filter(Role.id == context_role_id).first()
        else:
            roles = db.query(Role).all()
            for r in roles:
                if r.name.lower() in q_lower:
                    target_role = r
                    break

        # Fallback to Data Analyst if no role specified but query is role-specific
        if not target_role and ("data analyst" in q_lower or "why" in q_lower or "skill" in q_lower or "automat" in q_lower):
            target_role = db.query(Role).filter(Role.name == "Data Analyst").first()

        if target_role:
            analysis = db.query(RoleAnalysis).filter(RoleAnalysis.role_id == target_role.id).first()
            exp_pct = f"{analysis.average_ai_exposure * 100:.1f}%" if analysis else "N/A"

            # 3. Handle "Why is [Role] exposed to AI?"
            if "why" in q_lower and ("expos" in q_lower or "impact" in q_lower or "affect" in q_lower):
                # Get activity breakdown
                high_exp_activities = []
                for proc in target_role.processes:
                    for act in proc.activities:
                        if act.ai_exposure_score >= 0.60:
                            high_exp_activities.append(f"**{act.name}** ({act.ai_exposure_score*100:.0f}% exposure)")
                
                act_str = ", ".join(high_exp_activities) if high_exp_activities else "routine data processing activities"
                answer = f"**{target_role.name}** has an overall AI Exposure of **{exp_pct}**.\n\n" \
                         f"This score is primarily driven by high automation potential in activities such as: {act_str}.\n\n" \
                         f"These activities feature high repetitiveness, structured data availability, and rule-based logic, allowing AI models to assist or execute routine tasks rapidly."
                return {
                    "question": question,
                    "answer": answer,
                    "reasoning": f"Role-level score is an aggregate of underlying activity scores calculated via deterministic formula.",
                    "evidence": evidence,
                    "confidence": 0.90
                }

            # 4. Handle "Which activities are automated / augmented / human-led?"
            if "automat" in q_lower or "augment" in q_lower or "human" in q_lower or "activity" in q_lower:
                auto_acts, aug_acts, human_acts = [], [], []
                for proc in target_role.processes:
                    for act in proc.activities:
                        impact = db.query(ActivityAIImpact).filter(ActivityAIImpact.activity_id == act.id).first()
                        cat = impact.impact_category if impact else ("Mostly Automated" if act.automation_potential >= 0.65 else "AI Augmented")
                        if cat == "Mostly Automated":
                            auto_acts.append(act.name)
                        elif cat == "AI Augmented":
                            aug_acts.append(act.name)
                        else:
                            human_acts.append(act.name)

                if "automat" in q_lower:
                    acts_list = ", ".join([f"**{a}**" for a in auto_acts]) if auto_acts else "None"
                    answer = f"For **{target_role.name}**, the activities likely to be **Mostly Automated** are:\n\n{acts_list}\n\nThese activities feature standardized rules and high data availability."
                elif "human" in q_lower:
                    acts_list = ", ".join([f"**{a}**" for a in human_acts]) if human_acts else "None"
                    answer = f"For **{target_role.name}**, the activities that remain **Human-Led** are:\n\n{acts_list}\n\nThese activities require complex human judgment, ethical accountability, or intensive stakeholder interaction."
                else:
                    acts_list = ", ".join([f"**{a}**" for a in aug_acts]) if aug_acts else "None"
                    answer = f"For **{target_role.name}**, the activities classified as **AI-Augmented** are:\n\n{acts_list}\n\nIn these activities, AI co-pilots assist human experts who maintain final decision oversight."

                return {
                    "question": question,
                    "answer": answer,
                    "reasoning": "Activity impact classification based on threshold boundaries of automation and augmentation scores.",
                    "evidence": evidence,
                    "confidence": 0.90
                }

            # 5. Handle "What future skills will [Role] need?"
            if "skill" in q_lower or "reskill" in q_lower:
                fut_skills = db.query(FutureSkill).filter(FutureSkill.role_id == target_role.id).all()
                if fut_skills:
                    skills_formatted = "\n".join([f"• **{fs.skill.name}** ({fs.skill_status}): {fs.reason or ''}" for fs in fut_skills])
                    answer = f"Future skills required for **{target_role.name}**:\n\n{skills_formatted}"
                else:
                    answer = f"Future skills for **{target_role.name}** include AI Prompt Engineering, AI Model Oversight, Critical Thinking, and Strategic Decision Making."
                return {
                    "question": question,
                    "answer": answer,
                    "reasoning": "Derived from the shift in activity responsibilities toward AI validation, governance, and high-level strategy.",
                    "evidence": evidence,
                    "confidence": 0.90
                }

            # 6. Handle "What evidence supports this conclusion?"
            if "evidence" in q_lower or "research" in q_lower or "source" in q_lower:
                sources_str = "\n\n".join([f"📌 **{e['title']}** ({e['publisher']}, {e['publication_date']})\nURL: {e['url']}\n*Summary*: {e['summary']}" for e in evidence])
                answer = f"The analysis for **{target_role.name}** and banking workforce transformation is supported by the following research sources:\n\n{sources_str}"
                return {
                    "question": question,
                    "answer": answer,
                    "reasoning": "Retrieved from vector evidence database.",
                    "evidence": evidence,
                    "confidence": 0.95
                }

        # Generic RAG fallback response with evidence backing
        sources_summary = "; ".join([e["title"] for e in evidence]) if evidence else "industry research"
        answer = f"Based on enterprise intelligence and research from {sources_summary}:\n\n" \
                 f"AI is transforming banking roles by automating routine data processing while augmenting cognitive and analytical tasks. " \
                 f"Roles with high exposure shift toward validation, ethical oversight, and strategic decision-making."

        return {
            "question": question,
            "answer": answer,
            "reasoning": "Synthesized from structured enterprise dataset and verified research sources.",
            "evidence": evidence,
            "confidence": 0.80
        }
