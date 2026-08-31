# Enterprise Data Dictionary

## Database Overview
- **Database Engine**: SQLite (`backend/role_ai.db`)
- **ORM Framework**: SQLAlchemy 2.0
- **Validation**: Pydantic v2

---

## Data Tables & Schemas

### 1. `industries`
Stores industry classifications.
- `id` (INTEGER, PK): Primary Key.
- `name` (VARCHAR(255), UNIQUE, NOT NULL): Industry name ("Banking & Financial Services").
- `description` (TEXT): Overview of industry scope.
- `created_at` (DATETIME): Timestamp.

### 2. `roles`
Stores representative enterprise roles.
- `id` (INTEGER, PK): Primary Key.
- `industry_id` (INTEGER, FK -> `industries.id`): Industry reference.
- `name` (VARCHAR(255), UNIQUE, NOT NULL): Role name (e.g. "Data Analyst").
- `department` (VARCHAR(255)): Department name.
- `description` (TEXT): Role overview.
- `current_responsibilities` (TEXT): Baseline responsibilities summary.
- `created_at`, `updated_at` (DATETIME): Timestamps.

### 3. `processes`
Stores enterprise processes.
- `id` (INTEGER, PK): Primary Key.
- `role_id` (INTEGER, FK -> `roles.id`, NULLABLE): Role reference.
- `name` (VARCHAR(255), NOT NULL): Process name (e.g., "Data Management").
- `department` (VARCHAR(255)): Department.
- `description` (TEXT): Process description.
- `created_at` (DATETIME): Timestamp.

### 4. `activities`
Stores specific granular activities.
- `id` (INTEGER, PK): Primary Key.
- `process_id` (INTEGER, FK -> `processes.id`): Process reference.
- `name` (VARCHAR(255), NOT NULL): Activity title (e.g. "SQL Data Extraction").
- `description` (TEXT): Activity details.
- `repetitiveness` (FLOAT): 0.0–1.0 score.
- `data_availability` (FLOAT): 0.0–1.0 score.
- `rule_based_nature` (FLOAT): 0.0–1.0 score.
- `language_cognitive_complexity` (FLOAT): 0.0–1.0 score.
- `human_judgment_requirement` (FLOAT): 0.0–1.0 score.
- `regulatory_sensitivity` (FLOAT): 0.0–1.0 score.
- `human_interaction_requirement` (FLOAT): 0.0–1.0 score.
- `ai_exposure_score` (FLOAT): Calculated 0.0–1.0 score.
- `automation_potential` (FLOAT): Calculated 0.0–1.0 score.
- `augmentation_potential` (FLOAT): Calculated 0.0–1.0 score.

### 5. `skills`
Reusable skills catalog.
- `id` (INTEGER, PK): Primary Key.
- `name` (VARCHAR(255), UNIQUE, NOT NULL): Skill name (e.g., "SQL", "AI Prompt Engineering").
- `category` (VARCHAR(100)): Category (`Technical`, `Analytics`, `Domain`, `Soft`, `Management`).
- `is_future_skill` (BOOLEAN): True if emerging/future skill.

### 6. `role_processes`
Role-Process relationship join table.
- `id` (INTEGER, PK): Primary Key.
- `role_id` (INTEGER, FK -> `roles.id`): Role reference.
- `process_id` (INTEGER, FK -> `processes.id`): Process reference.
- `involvement_level` (VARCHAR(50)): `Primary`, `Secondary`, `Supporting`.

### 7. `role_activities`
Role-Activity relationship join table.
- `id` (INTEGER, PK): Primary Key.
- `role_id` (INTEGER, FK -> `roles.id`): Role reference.
- `activity_id` (INTEGER, FK -> `activities.id`): Activity reference.
- `responsibility_level` (VARCHAR(50)): `Primary`, `Supporting`, `Review`.

### 8. `role_skills`
Role-Skill relationship join table.
- `id` (INTEGER, PK): Primary Key.
- `role_id` (INTEGER, FK -> `roles.id`): Role reference.
- `skill_id` (INTEGER, FK -> `skills.id`): Skill reference.
- `proficiency_level` (VARCHAR(50)): `Basic`, `Intermediate`, `Advanced`, `Expert`.

### 9. `activity_skills`
Activity-Skill relationship join table.
- `id` (INTEGER, PK): Primary Key.
- `activity_id` (INTEGER, FK -> `activities.id`): Activity reference.
- `skill_id` (INTEGER, FK -> `skills.id`): Skill reference.
- `importance` (VARCHAR(50)): `Low`, `Medium`, `High`.

### 10. `activity_ai_impact`
Detailed 0–100 scale activity AI impact assessment.
- `id` (INTEGER, PK): Primary Key.
- `activity_id` (INTEGER, FK -> `activities.id`, UNIQUE): Activity reference.
- `automation_score` (FLOAT): 0–100.
- `augmentation_score` (FLOAT): 0–100.
- `human_judgement_score` (FLOAT): 0–100.
- `ai_exposure_score` (FLOAT): 0–100.
- `impact_category` (VARCHAR(50)): `Mostly Automated`, `AI Augmented`, `Human Led`.
- `reasoning` (TEXT): Generated explainable reasoning string.

### 11. `future_responsibilities`
Role future responsibilities.
- `id` (INTEGER, PK): Primary Key.
- `role_id` (INTEGER, FK -> `roles.id`): Role reference.
- `responsibility` (TEXT): Future task description.
- `reason` (TEXT): Justification.
- `related_activity_id` (INTEGER, FK -> `activities.id`): Related activity link.

### 12. `future_skills`
Role future skills requirements.
- `id` (INTEGER, PK): Primary Key.
- `role_id` (INTEGER, FK -> `roles.id`): Role reference.
- `skill_id` (INTEGER, FK -> `skills.id`): Skill reference.
- `skill_status` (VARCHAR(50)): `Emerging`, `Increasing`, `AI-Augmented`, `Changing`, `Declining`, `Enduring Human Capability`.
- `reason` (TEXT): Justification.

### 13. `role_future_profiles`
Transformed future role profile.
- `id` (INTEGER, PK): Primary Key.
- `role_id` (INTEGER, FK -> `roles.id`, UNIQUE): Role reference.
- `future_role_title` (VARCHAR(255)): Future role title.
- `future_role_summary` (TEXT): Overview summary.
- `key_changes` (TEXT): Key operational shifts.
- `human_focus` (TEXT): Human focus areas.
- `ai_focus` (TEXT): AI focus areas.
- `future_capabilities` (TEXT): Future capabilities required.

### 14. `research_sources`
Verified research evidence base.
- `id` (INTEGER, PK): Primary Key.
- `source_id` (VARCHAR(100), UNIQUE): Source code (e.g. `WEF_FOJ_2023`).
- `title` (VARCHAR(500)): Report title.
- `publisher` (VARCHAR(255)): Publisher (e.g., "McKinsey Global Institute").
- `url` (VARCHAR(1000)): Public Web URL.
- `publication_date` (VARCHAR(50)): Date.
- `summary` (TEXT): Report summary.
- `relevance_score` (FLOAT): 0.0–1.0 relevance.
