"""
Repository layer for database access
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from app.db.models import (
    Role, Industry, Process, Activity, Skill, RoleSkill, ActivitySkill,
    AIImpactAssessment, ResearchSource, RoleAnalysis, TopAIImpactRoles
)
from app.schemas import (
    RoleCreate, ProcessCreate, ActivityCreate, SkillCreate,
    AIImpactAssessmentBase, ResearchSourceCreate
)
from typing import List, Optional


# Role Repository
class RoleRepository:
    @staticmethod
    def create(db: Session, role: RoleCreate) -> Role:
        db_role = Role(**role.dict())
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role

    @staticmethod
    def get_by_id(db: Session, role_id: int) -> Optional[Role]:
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    @staticmethod
    def get_all(db: Session, industry_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Role]:
        query = db.query(Role)
        if industry_id:
            query = query.filter(Role.industry_id == industry_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def delete(db: Session, role_id: int) -> bool:
        role = db.query(Role).filter(Role.id == role_id).first()
        if role:
            db.delete(role)
            db.commit()
            return True
        return False


# Industry Repository
class IndustryRepository:
    @staticmethod
    def create(db: Session, name: str, description: Optional[str] = None) -> Industry:
        db_industry = Industry(name=name, description=description)
        db.add(db_industry)
        db.commit()
        db.refresh(db_industry)
        return db_industry

    @staticmethod
    def get_by_id(db: Session, industry_id: int) -> Optional[Industry]:
        return db.query(Industry).filter(Industry.id == industry_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Industry]:
        return db.query(Industry).filter(Industry.name == name).first()

    @staticmethod
    def get_all(db: Session) -> List[Industry]:
        return db.query(Industry).all()


# Process Repository
class ProcessRepository:
    @staticmethod
    def create(db: Session, role_id: int, process: ProcessCreate) -> Process:
        db_process = Process(role_id=role_id, **process.dict())
        db.add(db_process)
        db.commit()
        db.refresh(db_process)
        return db_process

    @staticmethod
    def get_by_id(db: Session, process_id: int) -> Optional[Process]:
        return db.query(Process).filter(Process.id == process_id).first()

    @staticmethod
    def get_by_role_id(db: Session, role_id: int) -> List[Process]:
        return db.query(Process).filter(Process.role_id == role_id).all()


# Activity Repository
class ActivityRepository:
    @staticmethod
    def create(db: Session, process_id: int, activity: ActivityCreate) -> Activity:
        db_activity = Activity(process_id=process_id, **activity.dict())
        # Calculate scores immediately
        db_activity.ai_exposure_score = ActivityRepository.calculate_ai_exposure(db_activity)
        db_activity.automation_potential = ActivityRepository.calculate_automation_potential(db_activity)
        db_activity.augmentation_potential = ActivityRepository.calculate_augmentation_potential(db_activity)
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity

    @staticmethod
    def get_by_id(db: Session, activity_id: int) -> Optional[Activity]:
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def get_by_process_id(db: Session, process_id: int) -> List[Activity]:
        return db.query(Activity).filter(Activity.process_id == process_id).all()

    @staticmethod
    def calculate_ai_exposure(activity: Activity) -> float:
        """
        Calculate AI exposure score based on activity characteristics.
        
        AI Exposure = weighted combination of:
        - repetitiveness (30%)
        - data_availability (25%)
        - rule_based_nature (20%)
        - language_cognitive_complexity (10%)
        - inverse human_judgment_requirement (10%)
        - inverse regulatory_sensitivity (5%)
        """
        score = (
            0.30 * activity.repetitiveness +
            0.25 * activity.data_availability +
            0.20 * activity.rule_based_nature +
            0.10 * activity.language_cognitive_complexity +
            0.10 * (1 - activity.human_judgment_requirement) +
            0.05 * (1 - activity.regulatory_sensitivity)
        )
        return min(1.0, max(0.0, score))

    @staticmethod
    def calculate_automation_potential(activity: Activity) -> float:
        """Calculate automation potential (subset of AI exposure)"""
        automation = (
            0.40 * activity.repetitiveness +
            0.30 * activity.rule_based_nature +
            0.20 * activity.data_availability +
            0.10 * (1 - activity.human_judgment_requirement)
        )
        return min(1.0, max(0.0, automation))

    @staticmethod
    def calculate_augmentation_potential(activity: Activity) -> float:
        """Calculate augmentation potential (AI support for human work)"""
        augmentation = (
            0.30 * activity.language_cognitive_complexity +
            0.25 * activity.data_availability +
            0.20 * (1 - activity.rule_based_nature) +
            0.15 * activity.human_judgment_requirement +
            0.10 * activity.repetitiveness
        )
        return min(1.0, max(0.0, augmentation))

    @staticmethod
    def update(db: Session, activity_id: int, activity_data: ActivityCreate) -> Optional[Activity]:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if activity:
            for key, value in activity_data.dict().items():
                setattr(activity, key, value)
            activity.ai_exposure_score = ActivityRepository.calculate_ai_exposure(activity)
            activity.automation_potential = ActivityRepository.calculate_automation_potential(activity)
            activity.augmentation_potential = ActivityRepository.calculate_augmentation_potential(activity)
            db.commit()
            db.refresh(activity)
        return activity


# Skill Repository
class SkillRepository:
    @staticmethod
    def create(db: Session, skill: SkillCreate) -> Skill:
        db_skill = Skill(**skill.dict())
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)
        return db_skill

    @staticmethod
    def get_by_id(db: Session, skill_id: int) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.id == skill_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.name == name).first()

    @staticmethod
    def get_all(db: Session, is_future_skill: Optional[bool] = None) -> List[Skill]:
        query = db.query(Skill)
        if is_future_skill is not None:
            query = query.filter(Skill.is_future_skill == is_future_skill)
        return query.all()

    @staticmethod
    def get_or_create(db: Session, name: str, description: Optional[str] = None, category: Optional[str] = None) -> Skill:
        skill = db.query(Skill).filter(Skill.name == name).first()
        if not skill:
            skill = Skill(name=name, description=description, category=category)
            db.add(skill)
            db.commit()
            db.refresh(skill)
        return skill


# RoleSkill Repository
class RoleSkillRepository:
    @staticmethod
    def create(db: Session, role_id: int, skill_id: int, proficiency_level: str = "intermediate") -> RoleSkill:
        db_role_skill = RoleSkill(role_id=role_id, skill_id=skill_id, proficiency_level=proficiency_level)
        db.add(db_role_skill)
        db.commit()
        db.refresh(db_role_skill)
        return db_role_skill

    @staticmethod
    def get_by_role(db: Session, role_id: int) -> List[RoleSkill]:
        return db.query(RoleSkill).filter(RoleSkill.role_id == role_id).all()


# ActivitySkill Repository
class ActivitySkillRepository:
    @staticmethod
    def create(db: Session, activity_id: int, skill_id: int, importance: float = 0.5) -> ActivitySkill:
        db_activity_skill = ActivitySkill(activity_id=activity_id, skill_id=skill_id, importance=importance)
        db.add(db_activity_skill)
        db.commit()
        db.refresh(db_activity_skill)
        return db_activity_skill

    @staticmethod
    def get_by_activity(db: Session, activity_id: int) -> List[ActivitySkill]:
        return db.query(ActivitySkill).filter(ActivitySkill.activity_id == activity_id).all()


# AI Impact Assessment Repository
class AIImpactRepository:
    @staticmethod
    def create(db: Session, activity_id: int, impact_data: AIImpactAssessmentBase) -> AIImpactAssessment:
        db_impact = AIImpactAssessment(activity_id=activity_id, **impact_data.dict())
        db.add(db_impact)
        db.commit()
        db.refresh(db_impact)
        return db_impact

    @staticmethod
    def get_by_activity(db: Session, activity_id: int) -> Optional[AIImpactAssessment]:
        return db.query(AIImpactAssessment).filter(AIImpactAssessment.activity_id == activity_id).first()


# Research Source Repository
class ResearchSourceRepository:
    @staticmethod
    def create(db: Session, source: ResearchSourceCreate, ai_impact_id: Optional[int] = None) -> ResearchSource:
        db_source = ResearchSource(ai_impact_id=ai_impact_id, **source.dict())
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        return db_source

    @staticmethod
    def get_by_id(db: Session, source_id: int) -> Optional[ResearchSource]:
        return db.query(ResearchSource).filter(ResearchSource.id == source_id).first()

    @staticmethod
    def get_all(db: Session) -> List[ResearchSource]:
        return db.query(ResearchSource).all()


# Role Analysis Repository
class RoleAnalysisRepository:
    @staticmethod
    def create_or_update(db: Session, role_id: int, analysis_data: dict) -> RoleAnalysis:
        existing = db.query(RoleAnalysis).filter(RoleAnalysis.role_id == role_id).first()
        if existing:
            for key, value in analysis_data.items():
                setattr(existing, key, value)
            db.commit()
            db.refresh(existing)
            return existing
        else:
            db_analysis = RoleAnalysis(role_id=role_id, **analysis_data)
            db.add(db_analysis)
            db.commit()
            db.refresh(db_analysis)
            return db_analysis

    @staticmethod
    def get_by_role(db: Session, role_id: int) -> Optional[RoleAnalysis]:
        return db.query(RoleAnalysis).filter(RoleAnalysis.role_id == role_id).first()


# Analytics Repository
class AnalyticsRepository:
    @staticmethod
    def get_top_ai_impact_roles(db: Session, limit: int = 5) -> List[dict]:
        """Calculate and return top roles by AI impact"""
        results = db.query(
            Role.id,
            Role.name,
            func.avg(Activity.ai_exposure_score).label('avg_ai_exposure'),
            func.count(Activity.id).label('activity_count')
        ).join(
            Process, Process.role_id == Role.id
        ).join(
            Activity, Activity.process_id == Process.id
        ).group_by(
            Role.id, Role.name
        ).order_by(
            desc('avg_ai_exposure')
        ).limit(limit).all()
        
        return results

    @staticmethod
    def get_dashboard_stats(db: Session) -> dict:
        """Get overall dashboard statistics"""
        total_roles = db.query(Role).count()
        total_processes = db.query(Process).count()
        total_activities = db.query(Activity).count()
        total_skills = db.query(Skill).count()
        
        avg_ai_exposure = db.query(func.avg(Activity.ai_exposure_score)).scalar() or 0.0
        
        return {
            "total_roles": total_roles,
            "total_processes": total_processes,
            "total_activities": total_activities,
            "total_skills": total_skills,
            "average_ai_exposure": float(avg_ai_exposure)
        }
