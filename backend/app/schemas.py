"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


# Skill schemas
class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_future_skill: bool = False


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Activity schemas
class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    repetitiveness: float = Field(0.5, ge=0, le=100)
    data_availability: float = Field(0.5, ge=0, le=100)
    rule_based_nature: float = Field(0.5, ge=0, le=100)
    language_cognitive_complexity: float = Field(0.5, ge=0, le=100)
    human_judgment_requirement: float = Field(0.5, ge=0, le=100)
    regulatory_sensitivity: float = Field(0.5, ge=0, le=100)
    human_interaction_requirement: float = Field(0.5, ge=0, le=100)


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int
    ai_exposure_score: float
    automation_potential: float
    augmentation_potential: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Detailed Activity AI Impact Schema
class ActivityAIImpactResponse(BaseModel):
    id: int
    activity_id: int
    automation_score: float
    augmentation_score: float
    human_judgement_score: float
    repetition_score: float
    data_availability_score: float
    complexity_score: float
    regulatory_sensitivity_score: float
    human_interaction_score: float
    ai_exposure_score: float
    impact_category: str
    reasoning: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# Process schemas
class ProcessBase(BaseModel):
    name: str
    description: Optional[str] = None
    department: Optional[str] = None


class ProcessCreate(ProcessBase):
    pass


class ProcessResponse(ProcessBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Role schemas
class RoleBase(BaseModel):
    name: str
    department: Optional[str] = None
    description: Optional[str] = None
    current_responsibilities: Optional[str] = None


class RoleCreate(RoleBase):
    industry_id: int = 1


class RoleResponse(RoleBase):
    id: int
    industry_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Future Responsibilities, Skills, Profile schemas
class FutureResponsibilityResponse(BaseModel):
    id: int
    role_id: int
    responsibility: str
    reason: Optional[str] = None
    related_activity_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class FutureSkillResponse(BaseModel):
    id: int
    role_id: int
    skill_id: int
    skill_name: Optional[str] = None
    skill_status: str
    reason: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class RoleFutureProfileResponse(BaseModel):
    id: int
    role_id: int
    future_role_title: str
    future_role_summary: str
    key_changes: Optional[str] = None
    human_focus: Optional[str] = None
    ai_focus: Optional[str] = None
    future_capabilities: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# AI Impact Assessment schemas
class AIImpactAssessmentBase(BaseModel):
    impact_type: str  # AUTOMATED, AUGMENTED, HUMAN_LED
    automation_likelihood: str = "low"
    augmentation_likelihood: str = "low"
    reasoning: Optional[str] = None


class AIImpactAssessmentResponse(AIImpactAssessmentBase):
    id: int
    activity_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Research Source schemas
class ResearchSourceBase(BaseModel):
    title: str
    url: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[str] = None
    source_type: Optional[str] = None
    summary: Optional[str] = None
    extracted_text: Optional[str] = None
    source_id: Optional[str] = None
    relevance_score: float = 0.85


class ResearchSourceCreate(ResearchSourceBase):
    pass


class ResearchSourceResponse(ResearchSourceBase):
    id: int
    ai_impact_id: Optional[int] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# Role Analysis schemas
class RoleAnalysisBase(BaseModel):
    average_ai_exposure: float
    average_automation_potential: float
    average_augmentation_potential: float
    activities_likely_automated: int
    activities_likely_augmented: int
    activities_human_led: int
    new_responsibilities: Optional[str] = None
    future_skills: Optional[str] = None
    future_role_profile: Optional[str] = None


class RoleAnalysisResponse(RoleAnalysisBase):
    id: int
    role_id: int
    analyzed_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Comprehensive schemas with nested relationships
class RoleDetailResponse(RoleResponse):
    processes: List[ProcessResponse] = []
    skills: List[SkillResponse] = []
    analysis: Optional[RoleAnalysisResponse] = None
    model_config = ConfigDict(from_attributes=True)


class ProcessDetailResponse(ProcessResponse):
    activities: List[ActivityResponse] = []
    model_config = ConfigDict(from_attributes=True)


# Comparison and ranking schemas
class RoleComparisonRequest(BaseModel):
    role_1_id: int
    role_2_id: int


class RoleComparisonResponse(BaseModel):
    role_1: dict
    role_2: dict
    comparison: dict
    model_config = ConfigDict(from_attributes=True)


class TopAIImpactRoleResponse(BaseModel):
    rank: int
    role: RoleResponse
    ai_impact_score: float
    reasoning: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# Question/Answer schemas
class AskIntelligenceRequest(BaseModel):
    question: str
    context_role_id: Optional[int] = None


class AskIntelligenceResponse(BaseModel):
    question: str
    answer: str
    evidence: List[ResearchSourceResponse] = []
    reasoning: Optional[str] = None
    confidence: float = 0.85
