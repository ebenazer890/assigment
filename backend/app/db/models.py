"""
Database models for Role-Level AI Intelligence Platform
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Industry(Base):
    """Industry model"""
    __tablename__ = "industries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roles = relationship("Role", back_populates="industry")


class Role(Base):
    """Role model"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    industry_id = Column(Integer, ForeignKey("industries.id"), nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    department = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    current_responsibilities = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    industry = relationship("Industry", back_populates="roles")
    processes = relationship("Process", back_populates="role", cascade="all, delete-orphan")
    role_processes = relationship("RoleProcess", back_populates="role", cascade="all, delete-orphan")
    role_activities = relationship("RoleActivity", back_populates="role", cascade="all, delete-orphan")
    skills = relationship("RoleSkill", back_populates="role", cascade="all, delete-orphan")
    analysis = relationship("RoleAnalysis", back_populates="role", cascade="all, delete-orphan", uselist=False)
    future_responsibilities = relationship("FutureResponsibility", back_populates="role", cascade="all, delete-orphan")
    future_skills = relationship("FutureSkill", back_populates="role", cascade="all, delete-orphan")
    future_profile = relationship("RoleFutureProfile", back_populates="role", cascade="all, delete-orphan", uselist=False)


class Process(Base):
    """Process model"""
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    name = Column(String(255), nullable=False)
    department = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="processes")
    role_processes = relationship("RoleProcess", back_populates="process", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="process", cascade="all, delete-orphan")


class RoleProcess(Base):
    """Association table connecting Roles and Processes with involvement level"""
    __tablename__ = "role_processes"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)
    involvement_level = Column(String(50), default="Primary")  # Primary, Secondary, Supporting
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="role_processes")
    process = relationship("Process", back_populates="role_processes")


class Activity(Base):
    """Activity model"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Scoring components (0-1 normalized for internal backward compatibility if needed, or 0-100)
    repetitiveness = Column(Float, default=0.5)
    data_availability = Column(Float, default=0.5)
    rule_based_nature = Column(Float, default=0.5)
    language_cognitive_complexity = Column(Float, default=0.5)
    human_judgment_requirement = Column(Float, default=0.5)
    regulatory_sensitivity = Column(Float, default=0.5)
    human_interaction_requirement = Column(Float, default=0.5)
    
    # Calculated scores (0-1 normalized)
    ai_exposure_score = Column(Float, default=0.0)
    automation_potential = Column(Float, default=0.0)
    augmentation_potential = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    process = relationship("Process", back_populates="activities")
    role_activities = relationship("RoleActivity", back_populates="activity", cascade="all, delete-orphan")
    skills = relationship("ActivitySkill", back_populates="activity", cascade="all, delete-orphan")
    ai_impact = relationship("AIImpactAssessment", back_populates="activity", uselist=False, cascade="all, delete-orphan")
    detailed_impact = relationship("ActivityAIImpact", back_populates="activity", uselist=False, cascade="all, delete-orphan")


class RoleActivity(Base):
    """Association table connecting Roles and Activities with responsibility level"""
    __tablename__ = "role_activities"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    responsibility_level = Column(String(50), default="Primary")  # Primary, Supporting, Review
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="role_activities")
    activity = relationship("Activity", back_populates="role_activities")


class Skill(Base):
    """Skill model"""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # Technical, Soft, Domain, Analytics, Compliance
    is_future_skill = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    role_skills = relationship("RoleSkill", back_populates="skill", cascade="all, delete-orphan")
    activity_skills = relationship("ActivitySkill", back_populates="skill", cascade="all, delete-orphan")
    future_skills = relationship("FutureSkill", back_populates="skill", cascade="all, delete-orphan")


class RoleSkill(Base):
    """Association between Role and current Skill"""
    __tablename__ = "role_skills"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency_level = Column(String(50), default="Intermediate")  # Basic, Intermediate, Advanced, Expert
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="skills")
    skill = relationship("Skill", back_populates="role_skills")


class ActivitySkill(Base):
    """Association between Activity and required Skill"""
    __tablename__ = "activity_skills"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    importance = Column(String(50), default="Medium")  # Low, Medium, High
    created_at = Column(DateTime, default=datetime.utcnow)

    activity = relationship("Activity", back_populates="skills")
    skill = relationship("Skill", back_populates="activity_skills")


class ActivityAIImpact(Base):
    """Detailed activity-level AI impact assessment with 0-100 scores"""
    __tablename__ = "activity_ai_impact"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False, unique=True)
    
    automation_score = Column(Float, default=0.0)  # 0-100
    augmentation_score = Column(Float, default=0.0)  # 0-100
    human_judgement_score = Column(Float, default=0.0)  # 0-100
    repetition_score = Column(Float, default=0.0)  # 0-100
    data_availability_score = Column(Float, default=0.0)  # 0-100
    complexity_score = Column(Float, default=0.0)  # 0-100
    regulatory_sensitivity_score = Column(Float, default=0.0)  # 0-100
    human_interaction_score = Column(Float, default=0.0)  # 0-100
    ai_exposure_score = Column(Float, default=0.0)  # 0-100
    
    impact_category = Column(String(50), nullable=False)  # Mostly Automated, AI Augmented, Human Led
    reasoning = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activity = relationship("Activity", back_populates="detailed_impact")


class AIImpactAssessment(Base):
    """Legacy/High-level AI Impact assessment for an activity"""
    __tablename__ = "ai_impact_assessments"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False, unique=True)
    
    impact_type = Column(String(50), nullable=False)  # AUTOMATED, AUGMENTED, HUMAN_LED
    automation_likelihood = Column(String(50), default="low")  # low, medium, high
    augmentation_likelihood = Column(String(50), default="low")  # low, medium, high
    reasoning = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activity = relationship("Activity", back_populates="ai_impact")
    sources = relationship("ResearchSource", back_populates="ai_impact", cascade="all, delete-orphan")


class FutureResponsibility(Base):
    """Future responsibilities for a role"""
    __tablename__ = "future_responsibilities"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    responsibility = Column(Text, nullable=False)
    reason = Column(Text, nullable=True)
    related_activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="future_responsibilities")
    related_activity = relationship("Activity")


class FutureSkill(Base):
    """Future skills requirements for a role"""
    __tablename__ = "future_skills"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    skill_status = Column(String(50), nullable=False)  # Emerging, Increasing, AI-Augmented, Changing, Declining, Enduring Human Capability
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="future_skills")
    skill = relationship("Skill", back_populates="future_skills")


class RoleFutureProfile(Base):
    """Comprehensive future role profile"""
    __tablename__ = "role_future_profiles"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, unique=True)
    future_role_title = Column(String(255), nullable=False)
    future_role_summary = Column(Text, nullable=False)
    key_changes = Column(Text, nullable=True)
    human_focus = Column(Text, nullable=True)
    ai_focus = Column(Text, nullable=True)
    future_capabilities = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="future_profile")


class ResearchSource(Base):
    """Research source for evidence"""
    __tablename__ = "research_sources"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(100), nullable=True, unique=True)
    ai_impact_id = Column(Integer, ForeignKey("ai_impact_assessments.id"), nullable=True)
    
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=True)
    publisher = Column(String(255), nullable=True)
    publication_date = Column(String(50), nullable=True)
    source_type = Column(String(100), nullable=True)  # research, article, report, benchmark
    summary = Column(Text, nullable=True)
    extracted_text = Column(Text, nullable=True)
    source_metadata = Column(Text, nullable=True)
    relevance_score = Column(Float, default=0.85)  # 0-1
    
    created_at = Column(DateTime, default=datetime.utcnow)

    ai_impact = relationship("AIImpactAssessment", back_populates="sources")


class RoleAnalysis(Base):
    """Complete analysis result for a role"""
    __tablename__ = "role_analyses"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, unique=True)
    
    # Average metrics
    average_ai_exposure = Column(Float, default=0.0)
    average_automation_potential = Column(Float, default=0.0)
    average_augmentation_potential = Column(Float, default=0.0)
    
    # Impact summary
    activities_likely_automated = Column(Integer, default=0)
    activities_likely_augmented = Column(Integer, default=0)
    activities_human_led = Column(Integer, default=0)
    
    # Analysis results (JSON or text representations for backwards compatibility)
    new_responsibilities = Column(Text, nullable=True)  # JSON-formatted list
    future_skills = Column(Text, nullable=True)  # JSON-formatted list
    future_role_profile = Column(Text, nullable=True)
    
    # Metadata
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    analysis_version = Column(Integer, default=1)

    role = relationship("Role", back_populates="analysis")


class RoleComparison(Base):
    """Cached role comparison results"""
    __tablename__ = "role_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    role_1_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role_2_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    comparison_result = Column(Text, nullable=True)  # JSON
    comparison_date = Column(DateTime, default=datetime.utcnow)


class TopAIImpactRoles(Base):
    """Cached top roles by AI impact"""
    __tablename__ = "top_ai_impact_roles"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    rank = Column(Integer, nullable=False)
    ai_impact_score = Column(Float, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)
