"""
Comprehensive Pytest Test Suite for Role-Level AI Intelligence Platform
"""
import pytest
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend directory to sys.path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db.models import Base, Role, Process, Activity, Skill, RoleAnalysis, RoleFutureProfile, ActivityAIImpact
from app.db.database import get_db
from app.main import app
from app.repositories import (
    RoleRepository, IndustryRepository, ProcessRepository,
    ActivityRepository, SkillRepository, AnalyticsRepository
)
from app.scoring import AIScoringEngine
from app.services import RoleAnalysisService, RoleComparisonService, AnalyticsService, RoleCreationService
from app.schemas import RoleCreate, ProcessCreate, ActivityCreate, SkillCreate


# Test Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create fresh test database per test function"""
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_industry(db):
    """Create test industry"""
    return IndustryRepository.create(db, "Banking & Financial Services", "Test Banking")


@pytest.fixture
def test_role(db, test_industry):
    """Create test role"""
    return RoleRepository.create(db, RoleCreate(
        industry_id=test_industry.id,
        name="Data Analyst",
        description="Analyzes data"
    ))


@pytest.fixture
def test_process(db, test_role):
    """Create test process"""
    return ProcessRepository.create(db, test_role.id, ProcessCreate(
        name="Data Management",
        description="Data extraction and prep"
    ))


@pytest.fixture
def test_activity(db, test_process):
    """Create test activity"""
    return ActivityRepository.create(db, test_process.id, ActivityCreate(
        name="SQL Data Extraction",
        description="Extract data using SQL queries",
        repetitiveness=0.85,
        data_availability=0.95,
        rule_based_nature=0.80,
        language_cognitive_complexity=0.40,
        human_judgment_requirement=0.30,
        regulatory_sensitivity=0.30,
        human_interaction_requirement=0.20
    ))


# ========================
# 1. AIScoringEngine Tests
# ========================

class TestAIScoringEngine:
    """Tests for deterministic 0-100 AI Exposure Scoring Formula"""

    def test_calculate_activity_scores(self):
        scores = AIScoringEngine.calculate_activity_scores(
            repetition=0.85,
            data_availability=0.95,
            rule_based=0.80,
            complexity=0.40,
            human_judgement=0.30,
            regulatory_sensitivity=0.30,
            human_interaction=0.20
        )
        assert "automation_score" in scores
        assert "augmentation_score" in scores
        assert "ai_exposure_score" in scores
        assert "impact_category" in scores
        assert "reasoning" in scores
        
        assert scores["ai_exposure_score"] > 60.0
        assert scores["impact_category"] in ["Mostly Automated", "AI Augmented", "Human Led"]


# ========================
# 2. Repository Tests
# ========================

class TestRepositories:
    """Tests for repository CRUD operations"""

    def test_create_and_get_role(self, db, test_industry):
        role = RoleRepository.create(db, RoleCreate(
            industry_id=test_industry.id,
            name="Risk Analyst",
            description="Evaluates risks"
        ))
        assert role.id is not None
        fetched = RoleRepository.get_by_id(db, role.id)
        assert fetched.name == "Risk Analyst"

    def test_create_and_get_activity(self, db, test_process):
        activity = ActivityRepository.create(db, test_process.id, ActivityCreate(
            name="Validate Data",
            description="Data quality validation",
            repetitiveness=0.8,
            data_availability=0.9,
            rule_based_nature=0.7,
            language_cognitive_complexity=0.3,
            human_judgment_requirement=0.3,
            regulatory_sensitivity=0.5,
            human_interaction_requirement=0.2
        ))
        assert activity.id is not None
        assert activity.ai_exposure_score > 0


# ========================
# 3. Service Tests
# ========================

class TestServices:
    """Tests for RoleAnalysis, Comparison, and Analytics Services"""

    def test_role_analysis_service(self, db, test_role, test_activity):
        analysis = RoleAnalysisService.analyze_role(db, test_role.id)
        assert analysis is not None
        assert "role" in analysis
        assert "analysis" in analysis
        assert "activities_summary" in analysis

    def test_role_comparison_service(self, db, test_industry):
        # Role 1
        r1 = RoleRepository.create(db, RoleCreate(industry_id=test_industry.id, name="Data Analyst", description=""))
        p1 = ProcessRepository.create(db, r1.id, ProcessCreate(name="P1"))
        ActivityRepository.create(db, p1.id, ActivityCreate(
            name="A1", description="", repetitiveness=0.9, data_availability=0.9, rule_based_nature=0.9,
            language_cognitive_complexity=0.2, human_judgment_requirement=0.2, regulatory_sensitivity=0.2, human_interaction_requirement=0.1
        ))

        # Role 2
        r2 = RoleRepository.create(db, RoleCreate(industry_id=test_industry.id, name="Relationship Manager", description=""))
        p2 = ProcessRepository.create(db, r2.id, ProcessCreate(name="P2"))
        ActivityRepository.create(db, p2.id, ActivityCreate(
            name="A2", description="", repetitiveness=0.2, data_availability=0.5, rule_based_nature=0.1,
            language_cognitive_complexity=0.8, human_judgment_requirement=0.9, regulatory_sensitivity=0.4, human_interaction_requirement=0.95
        ))

        comp = RoleComparisonService.compare_roles(db, r1.id, r2.id)
        assert comp is not None
        assert comp["comparison"]["more_affected_role"] == "Data Analyst"


# ========================
# 4. Surprise Test (Dynamic Role Creation & Persistence)
# ========================

class TestSurpriseTestWorkflow:
    """CRITICAL SURPRISE TEST: Dynamic Add New Role & Persistence Test"""

    def test_create_and_persist_supply_chain_analyst(self, db, test_industry):
        # 1. Create Supply Chain Analyst dynamically
        processes_payload = [
            {
                "name": "Logistics & Inventory Management",
                "description": "Managing inventory flows and freight routing.",
                "activities": [
                    {
                        "name": "Automated Stock Level & Reorder Reconciliation",
                        "description": "Reconciling daily stock against reorder limits.",
                        "repetitiveness": 0.85,
                        "data_availability": 0.90,
                        "rule_based_nature": 0.85,
                        "language_cognitive_complexity": 0.35,
                        "human_judgment_requirement": 0.30,
                        "regulatory_sensitivity": 0.30,
                        "human_interaction_requirement": 0.20
                    }
                ]
            }
        ]

        result = RoleCreationService.create_role_with_analysis(
            db=db,
            industry_id=test_industry.id,
            role_name="Supply Chain Analyst",
            role_description="Analyzes supply chain operations.",
            processes_data=processes_payload,
            department="Supply Chain & Logistics"
        )

        assert result is not None
        assert result["name"] == "Supply Chain Analyst"
        assert len(result["processes"]) >= 1

        # 2. Persistence Verification: Query fresh from database
        persisted_role = db.query(Role).filter(Role.name == "Supply Chain Analyst").first()
        assert persisted_role is not None
        assert persisted_role.department == "Supply Chain & Logistics"

        persisted_analysis = db.query(RoleAnalysis).filter(RoleAnalysis.role_id == persisted_role.id).first()
        assert persisted_analysis is not None
        assert persisted_analysis.average_ai_exposure > 0


# ========================
# 5. API Endpoint Tests
# ========================

@pytest.fixture
def client(db):
    """Create test FastAPI client overriding database dependency"""
    def override_get_db():
        return db
    
    app.dependency_overrides[get_db] = override_get_db
    from fastapi.testclient import TestClient
    return TestClient(app)


class TestAPIEndpoints:
    """Tests for FastAPI endpoints"""

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_list_roles(self, client, test_role):
        response = client.get("/roles")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_role(self, client, test_role):
        response = client.get(f"/roles/{test_role.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Data Analyst"

    def test_ask_intelligence(self, client, test_role):
        response = client.post("/ask", json={"question": "Why is Data Analyst highly exposed to AI?"})
        assert response.status_code == 200
        res = response.json()
        assert "answer" in res
        assert "evidence" in res

    def test_create_new_role_endpoint(self, client):
        response = client.post(
            "/roles/new-role/create-and-analyze",
            json={
                "role_name": "Procurement Analyst",
                "role_description": "Manages procurement contracts.",
                "processes": [
                    {
                        "name": "Vendor Sourcing",
                        "description": "Evaluating suppliers.",
                        "activities": [
                            {
                                "name": "Invoice Reconciliation",
                                "description": "Matching invoices to POs.",
                                "repetitiveness": 0.90,
                                "data_availability": 0.95,
                                "rule_based_nature": 0.90,
                                "complexity": 0.30,
                                "human_judgement": 0.20,
                                "regulatory_sensitivity": 0.50,
                                "human_interaction": 0.15
                            }
                        ]
                    }
                ]
            }
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Procurement Analyst"
