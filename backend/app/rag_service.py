"""
Simple and Reliable RAG (Retrieval-Augmented Generation) Pipeline
"""
import math
import re
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.db.models import ResearchSource, Role, Activity, RoleAnalysis, ActivityAIImpact


class RAGService:
    """
    RAG engine for retrieving relevant research evidence and structured intelligence context.
    Uses TF-IDF vector similarity over evidence summaries and activity details.
    """

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple tokenizer for string matching"""
        return re.findall(r'\w+', text.lower())

    @staticmethod
    def retrieve_evidence(db: Session, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve top_k research sources relevant to the user query.
        """
        sources = db.query(ResearchSource).all()
        if not sources:
            return []

        query_tokens = set(RAGService._tokenize(query))
        if not query_tokens:
            return [RAGService._format_source(s) for s in sources[:top_k]]

        scored_sources = []
        for source in sources:
            source_text = f"{source.title} {source.summary or ''} {source.publisher or ''}"
            source_tokens = RAGService._tokenize(source_text)
            
            # Simple TF-IDF / keyword overlap score
            match_count = sum(1 for t in query_tokens if t in source_tokens)
            score = match_count / (math.log(len(source_tokens) + 1) + 1.0)
            
            # Boost score based on source relevance score
            final_score = score + (source.relevance_score * 0.5 if match_count > 0 else 0.1)
            scored_sources.append((final_score, source))

        # Sort by relevance score descending
        scored_sources.sort(key=lambda x: x[0], reverse=True)
        
        return [RAGService._format_source(s[1]) for s in scored_sources[:top_k]]

    @staticmethod
    def _format_source(source: ResearchSource) -> Dict:
        return {
            "id": source.id,
            "source_id": source.source_id or f"SRC-{source.id}",
            "title": source.title,
            "publisher": source.publisher or "Industry Research",
            "url": source.url,
            "publication_date": source.publication_date,
            "source_type": source.source_type or "Report",
            "summary": source.summary,
            "relevance_score": round(source.relevance_score, 2),
            "created_at": source.created_at.isoformat() if source.created_at else None
        }

    @staticmethod
    def get_role_context(db: Session, role_name: str) -> Optional[Dict]:
        """Retrieve structured context for a role to inject into LLM prompts"""
        role = db.query(Role).filter(Role.name.ilike(f"%{role_name}%")).first()
        if not role:
            return None

        analysis = db.query(RoleAnalysis).filter(RoleAnalysis.role_id == role.id).first()
        
        # Get activity impacts
        activities_data = []
        for proc in role.processes:
            for act in proc.activities:
                impact = db.query(ActivityAIImpact).filter(ActivityAIImpact.activity_id == act.id).first()
                activities_data.append({
                    "activity_name": act.name,
                    "process": proc.name,
                    "ai_exposure": round(act.ai_exposure_score * 100, 1),
                    "impact_category": impact.impact_category if impact else "AI Augmented",
                    "reasoning": impact.reasoning if impact else ""
                })

        return {
            "role_id": role.id,
            "role_name": role.name,
            "department": role.department,
            "description": role.description,
            "average_ai_exposure": round(analysis.average_ai_exposure * 100, 1) if analysis else 0.0,
            "activities": activities_data
        }
