"""
Business services for role analysis, comparison, analytics, and dynamic role creation
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import json
from datetime import datetime

from app.repositories import (
    RoleRepository, ProcessRepository, ActivityRepository,
    SkillRepository, AIImpactRepository, RoleAnalysisRepository,
    AnalyticsRepository
)
from app.db.models import (
    Role, Activity, RoleAnalysis, Skill, Process, RoleProcess, RoleActivity,
    ActivitySkill, RoleSkill, ActivityAIImpact, FutureResponsibility,
    FutureSkill, RoleFutureProfile, ResearchSource
)
from app.scoring import AIScoringEngine
from app.rag_service import RAGService


class RoleAnalysisService:
    """Service for analyzing roles and calculating AI impact"""
    
    @staticmethod
    def analyze_role(db: Session, role_id: int) -> Dict:
        """
        Perform comprehensive AI impact analysis on a role
        """
        role = RoleRepository.get_by_id(db, role_id)
        if not role:
            return None
        
        # Get all processes and activities
        processes = ProcessRepository.get_by_role_id(db, role_id)
        
        activities = []
        for process in processes:
            activities.extend(ActivityRepository.get_by_process_id(db, process.id))
        
        if not activities:
            return None
        
        # Calculate aggregated metrics
        ai_exposures = [a.ai_exposure_score for a in activities]
        automation_potentials = [a.automation_potential for a in activities]
        augmentation_potentials = [a.augmentation_potential for a in activities]
        
        avg_ai_exposure = sum(ai_exposures) / len(ai_exposures) if ai_exposures else 0.0
        avg_automation = sum(automation_potentials) / len(automation_potentials) if automation_potentials else 0.0
        avg_augmentation = sum(augmentation_potentials) / len(augmentation_potentials) if augmentation_potentials else 0.0
        
        # Classify activities based on 0-100 scale impact categories
        activities_automated = []
        activities_augmented = []
        activities_human_led = []

        for a in activities:
            impact = db.query(ActivityAIImpact).filter(ActivityAIImpact.activity_id == a.id).first()
            category = impact.impact_category if impact else ("Mostly Automated" if a.automation_potential >= 0.65 else "AI Augmented")
            
            act_info = {
                "id": a.id,
                "name": a.name,
                "score": round(a.ai_exposure_score * 100, 1),
                "automation_score": round(a.automation_potential * 100, 1),
                "augmentation_score": round(a.augmentation_potential * 100, 1),
                "category": category,
                "reasoning": impact.reasoning if impact else ""
            }

            if category == "Mostly Automated" or a.automation_potential >= 0.65:
                activities_automated.append(act_info)
            elif category == "AI Augmented" or a.augmentation_potential >= 0.35 or a.ai_exposure_score >= 0.45:
                activities_augmented.append(act_info)
            else:
                activities_human_led.append(act_info)

        # Retrieve future responsibilities & future skills from explicit tables if present
        fut_resps = db.query(FutureResponsibility).filter(FutureResponsibility.role_id == role_id).all()
        resp_list = [fr.responsibility for fr in fut_resps] if fut_resps else [
            "Validating AI-generated analytical outputs and query logic",
            "Designing human-in-the-loop AI operational workflows",
            "Monitoring enterprise data quality and synthetic data integrity",
            "Interpreting complex business problems with senior leadership",
            "Supervising continuous AI agents and governance frameworks"
        ]

        fut_sks = db.query(FutureSkill).filter(FutureSkill.role_id == role_id).all()
        skill_list = [f"{fs.skill.name} ({fs.skill_status})" for fs in fut_sks] if fut_sks else [
            "AI Prompt Engineering (Emerging)",
            "AI Model Oversight (Increasing)",
            "SQL (AI-Augmented)",
            "Critical Thinking (Enduring Human Capability)"
        ]

        profile_entry = db.query(RoleFutureProfile).filter(RoleFutureProfile.role_id == role_id).first()
        profile_summary = profile_entry.future_role_summary if profile_entry else (
            f"The {role.name} role will evolve into an AI-augmented specialist position. "
            f"{avg_automation*100:.0f}% of routine activities face automation, while {avg_augmentation*100:.0f}% can be augmented. "
            f"Core responsibility shifts heavily toward validation, interpretation, and strategic decision making."
        )

        # Store analysis
        analysis_data = {
            "average_ai_exposure": round(avg_ai_exposure, 3),
            "average_automation_potential": round(avg_automation, 3),
            "average_augmentation_potential": round(avg_augmentation, 3),
            "activities_likely_automated": len(activities_automated),
            "activities_likely_augmented": len(activities_augmented),
            "activities_human_led": len(activities_human_led),
            "new_responsibilities": json.dumps(resp_list),
            "future_skills": json.dumps(skill_list),
            "future_role_profile": profile_summary
        }
        
        stored_analysis = RoleAnalysisRepository.create_or_update(db, role_id, analysis_data)
        
        return {
            "role": {
                "id": role.id,
                "name": role.name,
                "department": role.department,
                "description": role.description
            },
            "analysis": analysis_data,
            "activities_summary": {
                "automated": activities_automated,
                "augmented": activities_augmented,
                "human_led": activities_human_led
            }
        }
    
    @staticmethod
    def get_role_detail(db: Session, role_id: int) -> Dict:
        """Get comprehensive role detail with all related data"""
        role = RoleRepository.get_by_id(db, role_id)
        if not role:
            return None
        
        processes = ProcessRepository.get_by_role_id(db, role_id)
        
        # Build process hierarchy with 0-100 scores
        processes_data = []
        for process in processes:
            activities = ActivityRepository.get_by_process_id(db, process.id)
            act_list = []
            for a in activities:
                impact = db.query(ActivityAIImpact).filter(ActivityAIImpact.activity_id == a.id).first()
                act_list.append({
                    "id": a.id,
                    "name": a.name,
                    "description": a.description,
                    "ai_exposure_score": round(a.ai_exposure_score * 100, 1),
                    "automation_potential": round(a.automation_potential * 100, 1),
                    "augmentation_potential": round(a.augmentation_potential * 100, 1),
                    "impact_category": impact.impact_category if impact else "AI Augmented",
                    "reasoning": impact.reasoning if impact else ""
                })

            processes_data.append({
                "id": process.id,
                "name": process.name,
                "department": process.department,
                "description": process.description,
                "activities": act_list
            })
        
        # Get analysis
        analysis = RoleAnalysisRepository.get_by_role(db, role_id)
        if not analysis:
            RoleAnalysisService.analyze_role(db, role_id)
            analysis = RoleAnalysisRepository.get_by_role(db, role_id)

        analysis_data = None
        if analysis:
            analysis_data = {
                "average_ai_exposure": analysis.average_ai_exposure,
                "average_automation_potential": analysis.average_automation_potential,
                "average_augmentation_potential": analysis.average_augmentation_potential,
                "activities_likely_automated": analysis.activities_likely_automated,
                "activities_likely_augmented": analysis.activities_likely_augmented,
                "activities_human_led": analysis.activities_human_led,
                "new_responsibilities": json.loads(analysis.new_responsibilities) if analysis.new_responsibilities else [],
                "future_skills": json.loads(analysis.future_skills) if analysis.future_skills else [],
                "future_role_profile": analysis.future_role_profile,
                "analyzed_at": analysis.analyzed_at.isoformat()
            }

        # Fetch future profile entity details
        profile_entity = db.query(RoleFutureProfile).filter(RoleFutureProfile.role_id == role_id).first()
        profile_details = None
        if profile_entity:
            profile_details = {
                "future_role_title": profile_entity.future_role_title,
                "future_role_summary": profile_entity.future_role_summary,
                "key_changes": profile_entity.key_changes,
                "human_focus": profile_entity.human_focus,
                "ai_focus": profile_entity.ai_focus,
                "future_capabilities": profile_entity.future_capabilities
            }

        # Fetch evidence sources
        evidence = RAGService.retrieve_evidence(db, role.name, top_k=3)
        
        return {
            "id": role.id,
            "name": role.name,
            "department": role.department,
            "description": role.description,
            "current_responsibilities": role.current_responsibilities,
            "processes": processes_data,
            "analysis": analysis_data,
            "future_profile_details": profile_details,
            "evidence": evidence
        }


class RoleComparisonService:
    """Service for comparing roles"""
    
    @staticmethod
    def compare_roles(db: Session, role_1_id: int, role_2_id: int) -> Dict:
        """Compare two roles by AI impact metrics"""
        role_1 = RoleRepository.get_by_id(db, role_1_id)
        role_2 = RoleRepository.get_by_id(db, role_2_id)
        
        if not role_1 or not role_2:
            return None
        
        # Get or create analyses
        analysis_1 = RoleAnalysisRepository.get_by_role(db, role_1_id)
        if not analysis_1:
            RoleAnalysisService.analyze_role(db, role_1_id)
            analysis_1 = RoleAnalysisRepository.get_by_role(db, role_1_id)
        
        analysis_2 = RoleAnalysisRepository.get_by_role(db, role_2_id)
        if not analysis_2:
            RoleAnalysisService.analyze_role(db, role_2_id)
            analysis_2 = RoleAnalysisRepository.get_by_role(db, role_2_id)
        
        # Calculate differences
        ai_exposure_diff = analysis_1.average_ai_exposure - analysis_2.average_ai_exposure
        automation_diff = analysis_1.average_automation_potential - analysis_2.average_automation_potential
        augmentation_diff = analysis_1.average_augmentation_potential - analysis_2.average_augmentation_potential
        
        # Determine which role is more affected
        if ai_exposure_diff >= 0:
            more_affected = role_1.name
            less_affected = role_2.name
        else:
            more_affected = role_2.name
            less_affected = role_1.name
        
        return {
            "role_1": {
                "id": role_1.id,
                "name": role_1.name,
                "department": role_1.department,
                "ai_exposure": round(analysis_1.average_ai_exposure, 3),
                "automation_potential": round(analysis_1.average_automation_potential, 3),
                "augmentation_potential": round(analysis_1.average_augmentation_potential, 3),
                "affected_activities": analysis_1.activities_likely_automated + analysis_1.activities_likely_augmented
            },
            "role_2": {
                "id": role_2.id,
                "name": role_2.name,
                "department": role_2.department,
                "ai_exposure": round(analysis_2.average_ai_exposure, 3),
                "automation_potential": round(analysis_2.average_automation_potential, 3),
                "augmentation_potential": round(analysis_2.average_augmentation_potential, 3),
                "affected_activities": analysis_2.activities_likely_automated + analysis_2.activities_likely_augmented
            },
            "comparison": {
                "ai_exposure_difference": round(abs(ai_exposure_diff), 3),
                "automation_difference": round(abs(automation_diff), 3),
                "augmentation_difference": round(abs(augmentation_diff), 3),
                "more_affected_role": more_affected,
                "less_affected_role": less_affected,
                "key_difference": f"{more_affected} faces {abs(ai_exposure_diff)*100:.1f}% more AI exposure than {less_affected} due to routine standardized activities."
            }
        }


class AnalyticsService:
    """Service for providing analytics and insights"""
    
    @staticmethod
    def get_top_ai_impact_roles(db: Session, limit: int = 5) -> List[Dict]:
        """Get top roles with highest AI impact"""
        results = AnalyticsRepository.get_top_ai_impact_roles(db, limit)
        
        response = []
        for rank, (role_id, role_name, avg_exposure, activity_count) in enumerate(results, 1):
            response.append({
                "rank": rank,
                "role": {
                    "id": role_id,
                    "name": role_name
                },
                "ai_impact_score": round(float(avg_exposure), 3),
                "affected_activities": int(activity_count),
                "reasoning": f"{role_name} has {float(avg_exposure)*100:.1f}% average AI exposure across {int(activity_count)} activities"
            })
        
        return response
    
    @staticmethod
    def get_dashboard_stats(db: Session) -> Dict:
        """Get comprehensive dashboard statistics"""
        stats = AnalyticsRepository.get_dashboard_stats(db)
        top_roles = AnalyticsService.get_top_ai_impact_roles(db, limit=5)
        
        future_skills_raw = db.query(Skill).filter(Skill.is_future_skill == True).all()
        future_skills = [skill.name for skill in future_skills_raw]
        
        return {
            "summary": stats,
            "top_ai_impacted_roles": top_roles,
            "future_skills": future_skills,
            "dashboard_timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_role_skills_comparison(db: Session, role_id: int) -> Dict:
        """Get current vs future skills for a role"""
        role = RoleRepository.get_by_id(db, role_id)
        if not role:
            return None
        
        analysis = RoleAnalysisRepository.get_by_role(db, role_id)
        if not analysis:
            RoleAnalysisService.analyze_role(db, role_id)
            analysis = RoleAnalysisRepository.get_by_role(db, role_id)
        
        current_skills = db.query(Skill).join(
            RoleSkill, RoleSkill.skill_id == Skill.id
        ).filter(RoleSkill.role_id == role_id).all()
        
        future_skills_list = json.loads(analysis.future_skills) if analysis.future_skills else []
        
        return {
            "role_id": role_id,
            "role_name": role.name,
            "current_skills": [{"id": s.id, "name": s.name, "category": s.category} for s in current_skills],
            "future_skills": future_skills_list,
            "new_skills_required": [s for s in future_skills_list if s not in [cs.name for cs in current_skills]]
        }


class RoleCreationService:
    """
    Dynamic Role Creation & Analysis Engine (Surprise Test: e.g. Supply Chain Analyst).
    Does NOT require modifying source code. Persists completely to database.
    """
    
    @staticmethod
    def create_role_with_analysis(
        db: Session,
        industry_id: int,
        role_name: str,
        role_description: str,
        processes_data: List[Dict],
        department: Optional[str] = "Supply Chain & Logistics",
        current_responsibilities: Optional[str] = None,
        skills_data: Optional[List[str]] = None
    ) -> Dict:
        """
        Dynamically save role, processes, activities, skills, calculate AI impact,
        retrieve RAG evidence, generate future profiles, and persist to database.
        """
        # 1. Check if role already exists
        existing_role = db.query(Role).filter(Role.name == role_name).first()
        if existing_role:
            return RoleAnalysisService.get_role_detail(db, existing_role.id)

        # 2. Save Role
        role = Role(
            industry_id=industry_id or 1,
            name=role_name,
            department=department or "Operations & Supply Chain",
            description=role_description,
            current_responsibilities=current_responsibilities or "Inventory tracking, vendor compliance review, logistics data analysis."
        )
        db.add(role)
        db.commit()
        db.refresh(role)

        # 3. Save Processes, Activities, and calculate AI Impact
        all_created_activities = []
        for p_data in processes_data:
            proc = Process(
                role_id=role.id,
                name=p_data["name"],
                department=p_data.get("department", role.department),
                description=p_data.get("description", "")
            )
            db.add(proc)
            db.commit()
            db.refresh(proc)

            # Relational join table
            rp = RoleProcess(role_id=role.id, process_id=proc.id, involvement_level="Primary")
            db.add(rp)

            for a_data in p_data.get("activities", []):
                # Extract inputs (accepts 0-1 or 0-100)
                scores = AIScoringEngine.calculate_activity_scores(
                    repetition=a_data.get("repetitiveness", 0.7),
                    data_availability=a_data.get("data_availability", 0.8),
                    rule_based=a_data.get("rule_based_nature", 0.7),
                    complexity=a_data.get("language_cognitive_complexity", a_data.get("complexity", 0.4)),
                    human_judgement=a_data.get("human_judgment_requirement", a_data.get("human_judgement", 0.4)),
                    regulatory_sensitivity=a_data.get("regulatory_sensitivity", 0.3),
                    human_interaction=a_data.get("human_interaction_requirement", a_data.get("human_interaction", 0.3))
                )

                act = Activity(
                    process_id=proc.id,
                    name=a_data["name"],
                    description=a_data.get("description", ""),
                    repetitiveness=scores["repetition_score"] / 100.0,
                    data_availability=scores["data_availability_score"] / 100.0,
                    rule_based_nature=scores["rule_based_nature"] / 100.0,
                    language_cognitive_complexity=scores["complexity_score"] / 100.0,
                    human_judgment_requirement=scores["human_judgement_score"] / 100.0,
                    regulatory_sensitivity=scores["regulatory_sensitivity_score"] / 100.0,
                    human_interaction_requirement=scores["human_interaction_score"] / 100.0,
                    ai_exposure_score=scores["ai_exposure_score"] / 100.0,
                    automation_potential=scores["automation_score"] / 100.0,
                    augmentation_potential=scores["augmentation_score"] / 100.0
                )
                db.add(act)
                db.commit()
                db.refresh(act)
                all_created_activities.append(act)

                # Relational join table
                ra = RoleActivity(role_id=role.id, activity_id=act.id, responsibility_level="Primary")
                db.add(ra)

                # Save ActivityAIImpact
                impact = ActivityAIImpact(
                    activity_id=act.id,
                    automation_score=scores["automation_score"],
                    augmentation_score=scores["augmentation_score"],
                    human_judgement_score=scores["human_judgement_score"],
                    repetition_score=scores["repetition_score"],
                    data_availability_score=scores["data_availability_score"],
                    complexity_score=scores["complexity_score"],
                    regulatory_sensitivity_score=scores["regulatory_sensitivity_score"],
                    human_interaction_score=scores["human_interaction_score"],
                    ai_exposure_score=scores["ai_exposure_score"],
                    impact_category=scores["impact_category"],
                    reasoning=scores["reasoning"]
                )
                db.add(impact)

        # 4. Save Skills & Relationships
        input_skills = skills_data or ["Supply Chain Analytics", "SQL", "Excel", "Vendor Management", "Logistics Planning"]
        for sk_name in input_skills:
            sk = db.query(Skill).filter(Skill.name == sk_name).first()
            if not sk:
                sk = Skill(name=sk_name, category="Domain", is_future_skill=False)
                db.add(sk)
                db.commit()
                db.refresh(sk)
            
            rs = RoleSkill(role_id=role.id, skill_id=sk.id, proficiency_level="Advanced")
            db.add(rs)

        # 5. Retrieve Evidence via RAG
        evidence = RAGService.retrieve_evidence(db, role_name, top_k=3)

        # 6. Generate Future Responsibilities
        fut_resps = [
            {"responsibility": f"Audit AI-generated {role_name} forecasting and inventory optimization scripts", "reason": "Ensure machine projections account for unexpected global supply disruptions."},
            {"responsibility": f"Manage automated vendor compliance and logistics monitoring bots", "reason": "Supervise automated tracking algorithms to maintain supply chain resilience."},
            {"responsibility": f"Oversee ethical supplier sustainability and ESG compliance metrics", "reason": "Human oversight required for ethical sourcing decisions."}
        ]
        for fr in fut_resps:
            db_fr = FutureResponsibility(
                role_id=role.id,
                responsibility=fr["responsibility"],
                reason=fr["reason"],
                related_activity_id=all_created_activities[0].id if all_created_activities else None
            )
            db.add(db_fr)

        # 7. Generate Future Skills
        fut_skills_list = [
            {"name": "AI Workflow Automation", "category": "Technical", "status": "Emerging", "reason": "Required to build automated logistics and supply chain tracking bots."},
            {"name": "AI Model Oversight", "category": "Analytics", "status": "Increasing", "reason": "Crucial to verify AI inventory prediction outputs."},
            {"name": "Negotiation", "category": "Soft", "status": "Enduring Human Capability", "reason": "Human relationship management is essential in supplier deal-making."}
        ]

        for fs_info in fut_skills_list:
            sk = db.query(Skill).filter(Skill.name == fs_info["name"]).first()
            if not sk:
                sk = Skill(name=fs_info["name"], category=fs_info["category"], is_future_skill=True)
                db.add(sk)
                db.commit()
                db.refresh(sk)
            
            db_fs = FutureSkill(role_id=role.id, skill_id=sk.id, skill_status=fs_info["status"], reason=fs_info["reason"])
            db.add(db_fs)

        # 8. Save Future Role Profile
        profile = RoleFutureProfile(
            role_id=role.id,
            future_role_title=f"AI-Augmented {role_name} & Logistics Strategist",
            future_role_summary=f"The {role_name} role transitions into an AI-augmented strategic position. Routine tracking and reporting are automated, allowing the specialist to focus on resilience, vendor negotiations, and exception management.",
            key_changes="Routine inventory reporting automated; focus moves to supply chain risk mitigation.",
            human_focus="Supplier relationship management, ethical sourcing, crisis management.",
            ai_focus="Continuous demand forecasting, real-time shipment tracking, automated reorder triggers.",
            future_capabilities="Autonomous logistics orchestration, predictive risk modeling."
        )
        db.add(profile)
        db.commit()

        # 9. Perform and Store Role Analysis
        analysis_result = RoleAnalysisService.analyze_role(db, role.id)
        
        return RoleAnalysisService.get_role_detail(db, role.id)
