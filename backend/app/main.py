"""
FastAPI application with role intelligence endpoints
"""
from typing import List, Optional, Dict
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.db.database import get_db, init_db
from app.repositories import (
    RoleRepository, ProcessRepository, ActivityRepository,
    IndustryRepository, SkillRepository, ResearchSourceRepository
)
from app.services import (
    RoleAnalysisService, RoleComparisonService,
    AnalyticsService, RoleCreationService
)
from app.ai_service import AIService
from app.schemas import (
    RoleResponse, ProcessCreate, ActivityCreate,
    RoleComparisonRequest, AskIntelligenceRequest, AskIntelligenceResponse
)

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup & shutdown"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
    yield


# Initialize FastAPI
app = FastAPI(
    title="Role-Level AI Intelligence Platform",
    description="Analyze AI impact on organizational roles in Banking and Financial Services",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================
# HEALTH & INFO ENDPOINTS
# ========================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "role-ai-intelligence"}


@app.get("/info")
async def get_info():
    """Get application info"""
    return {
        "name": os.getenv("APP_NAME", "Role-Level AI Intelligence Platform"),
        "version": "1.0.0",
        "industry": "Banking & Financial Services",
        "environment": os.getenv("APP_ENVIRONMENT", "development")
    }


# ========================
# ROLE ENDPOINTS
# ========================

@app.get("/roles", response_model=list[RoleResponse])
async def list_roles(
    industry_id: int = Query(None),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    """List all roles with optional filtering by industry"""
    roles = RoleRepository.get_all(db, industry_id=industry_id, skip=skip, limit=limit)
    return roles


@app.get("/roles/{role_id}")
async def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get detailed role information including processes, activities, analysis, and research evidence"""
    role_detail = RoleAnalysisService.get_role_detail(db, role_id)
    if not role_detail:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_detail


@app.post("/roles")
async def create_role(
    role_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new role dynamically"""
    try:
        if "processes" in role_data and isinstance(role_data["processes"], list):
            result = RoleCreationService.create_role_with_analysis(
                db=db,
                industry_id=role_data.get("industry_id", 1),
                role_name=role_data["role_name"] if "role_name" in role_data else role_data["name"],
                role_description=role_data.get("description", role_data.get("role_description", "")),
                processes_data=role_data["processes"],
                department=role_data.get("department"),
                current_responsibilities=role_data.get("current_responsibilities"),
                skills_data=role_data.get("skills")
            )
            return result
        else:
            from app.schemas import RoleCreate
            role = RoleRepository.create(db, RoleCreate(**role_data))
            return {"id": role.id, "name": role.name, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/roles/{role_id}/analysis")
@app.post("/roles/{role_id}/analyze")
async def analyze_role(role_id: int, db: Session = Depends(get_db)):
    """Perform AI impact analysis on a role"""
    analysis = RoleAnalysisService.analyze_role(db, role_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Role not found or no activities defined")
    return analysis


@app.get("/roles/{role_id}/activities")
async def get_role_activities(role_id: int, db: Session = Depends(get_db)):
    """Get all activities for a role across all processes"""
    role = RoleRepository.get_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    processes = ProcessRepository.get_by_role_id(db, role_id)
    activities = []
    for process in processes:
        process_activities = ActivityRepository.get_by_process_id(db, process.id)
        for activity in process_activities:
            activities.append({
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "process": process.name,
                "ai_exposure_score": round(activity.ai_exposure_score * 100, 1),
                "automation_potential": round(activity.automation_potential * 100, 1),
                "augmentation_potential": round(activity.augmentation_potential * 100, 1)
            })
    
    return {"role_id": role_id, "role_name": role.name, "activities": activities}


@app.get("/roles/{role_id}/skills")
async def get_role_skills(role_id: int, db: Session = Depends(get_db)):
    """Get current and future skills for a role"""
    skills_comparison = AnalyticsService.get_role_skills_comparison(db, role_id)
    if not skills_comparison:
        raise HTTPException(status_code=404, detail="Role not found or not analyzed")
    return skills_comparison


# ========================
# COMPARISON ENDPOINTS
# ========================

@app.post("/roles/compare")
@app.get("/roles/compare")
async def compare_roles(
    role_1_id: int = Query(None),
    role_2_id: int = Query(None),
    comparison: Optional[RoleComparisonRequest] = None,
    db: Session = Depends(get_db)
):
    """Compare two roles by AI impact metrics"""
    r1 = role_1_id or (comparison.role_1_id if comparison else None)
    r2 = role_2_id or (comparison.role_2_id if comparison else None)
    
    if not r1 or not r2:
        raise HTTPException(status_code=400, detail="Must provide role_1_id and role_2_id")
    
    result = RoleComparisonService.compare_roles(db, r1, r2)
    if not result:
        raise HTTPException(status_code=404, detail="One or both roles not found")
    return result


# ========================
# ANALYTICS ENDPOINTS
# ========================

@app.get("/analytics/top-ai-impact")
async def get_top_ai_impact(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get top roles with highest AI impact"""
    top_roles = AnalyticsService.get_top_ai_impact_roles(db, limit=limit)
    return {"top_roles": top_roles}


@app.get("/analytics/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get comprehensive dashboard statistics"""
    stats = AnalyticsService.get_dashboard_stats(db)
    return stats


# ========================
# INTELLIGENCE ENDPOINTS
# ========================

@app.post("/ask")
async def ask_intelligence(
    request: AskIntelligenceRequest,
    db: Session = Depends(get_db)
) -> AskIntelligenceResponse:
    """
    Ask intelligent questions about roles and AI impact with RAG evidence synthesis.
    """
    try:
        res = AIService.answer_question(db, request.question, request.context_role_id)
        return AskIntelligenceResponse(**res)
    except Exception as e:
        return AskIntelligenceResponse(
            question=request.question,
            answer=f"Could not process question: {str(e)}",
            confidence=0.0
        )


# ========================
# RESEARCH ENDPOINTS
# ========================

@app.get("/research/sources")
async def get_research_sources(db: Session = Depends(get_db)):
    """Get all research sources"""
    sources = ResearchSourceRepository.get_all(db)
    return {
        "total_sources": len(sources),
        "sources": [
            {
                "id": s.id,
                "source_id": s.source_id,
                "title": s.title,
                "publisher": s.publisher,
                "url": s.url,
                "publication_date": s.publication_date,
                "source_type": s.source_type,
                "summary": s.summary,
                "relevance_score": s.relevance_score
            }
            for s in sources
        ]
    }


# ========================
# SURPRISE TEST ENDPOINT
# ========================

@app.post("/roles/new-role/create-and-analyze")
async def create_and_analyze_role(
    role_data: dict,
    db: Session = Depends(get_db)
):
    """
    Dynamic Add New Role endpoint (Surprise Test).
    Accepts role_name, description, processes, activities, skills.
    Calculates AI impact, retrieves evidence, generates future profile, and persists to DB.
    """
    try:
        role_name = role_data.get("role_name") or role_data.get("name")
        role_description = role_data.get("role_description") or role_data.get("description", "")
        processes = role_data.get("processes", [])

        if not role_name or not role_description:
            raise HTTPException(status_code=400, detail="Missing required field: role_name or role_description")

        result = RoleCreationService.create_role_with_analysis(
            db=db,
            industry_id=role_data.get("industry_id", 1),
            role_name=role_name,
            role_description=role_description,
            processes_data=processes,
            department=role_data.get("department"),
            current_responsibilities=role_data.get("current_responsibilities"),
            skills_data=role_data.get("skills")
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========================
# SEED DATA ENDPOINT
# ========================

@app.post("/seed-data/initialize")
async def initialize_seed_data(db: Session = Depends(get_db)):
    """Initialize database with complete synthetic banking dataset"""
    import sys
    from pathlib import Path
    backend_dir = Path(__file__).parent.parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    from scripts.seed_data import seed_banking_roles
    try:
        result = seed_banking_roles(db)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========================
# ERROR HANDLERS
# ========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": exc.detail, "status_code": exc.status_code}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("APP_DEBUG", "False").lower() == "true"
    )
