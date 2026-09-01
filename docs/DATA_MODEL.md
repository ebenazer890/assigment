# Data Model Documentation

## Entity Relationship (ER) Diagram

```mermaid
erDiagram
    INDUSTRY ||--|{ ROLE : contains
    ROLE ||--|{ ROLE_PROCESS : has
    PROCESS ||--|{ ROLE_PROCESS : mapped_to
    ROLE ||--|{ PROCESS : defines
    PROCESS ||--|{ ACTIVITY : contains
    ROLE ||--|{ ROLE_ACTIVITY : performs
    ACTIVITY ||--|{ ROLE_ACTIVITY : assigned_to
    
    ROLE ||--|{ ROLE_SKILL : requires
    SKILL ||--|{ ROLE_SKILL : assigned_to
    ACTIVITY ||--|{ ACTIVITY_SKILL : utilizes
    SKILL ||--|{ ACTIVITY_SKILL : required_for
    
    ACTIVITY ||--|| ACTIVITY_AI_IMPACT : scored_by
    ROLE ||--|| ROLE_FUTURE_PROFILE : transforms_into
    ROLE ||--|{ FUTURE_RESPONSIBILITY : gains
    ROLE ||--|{ FUTURE_SKILL : demands
    SKILL ||--|{ FUTURE_SKILL : maps_to
    ROLE ||--|| ROLE_ANALYSIS : evaluated_by
    ACTIVITY_AI_IMPACT ||--o{ RESEARCH_SOURCE : supported_by

    ROLE {
        int id PK
        int industry_id FK
        string name
        string department
        text description
        text current_responsibilities
    }

    PROCESS {
        int id PK
        int role_id FK
        string name
        string department
        text description
    }

    ACTIVITY {
        int id PK
        int process_id FK
        string name
        text description
        float repetitiveness
        float data_availability
        float rule_based_nature
        float language_cognitive_complexity
        float human_judgment_requirement
        float regulatory_sensitivity
        float human_interaction_requirement
        float ai_exposure_score
        float automation_potential
        float augmentation_potential
    }

    SKILL {
        int id PK
        string name
        string category
        boolean is_future_skill
    }

    ROLE_PROCESS {
        int id PK
        int role_id FK
        int process_id FK
        string involvement_level
    }

    ROLE_ACTIVITY {
        int id PK
        int role_id FK
        int activity_id FK
        string responsibility_level
    }

    ROLE_SKILL {
        int id PK
        int role_id FK
        int skill_id FK
        string proficiency_level
    }

    ACTIVITY_SKILL {
        int id PK
        int activity_id FK
        int skill_id FK
        string importance
    }

    ACTIVITY_AI_IMPACT {
        int id PK
        int activity_id FK
        float automation_score
        float augmentation_score
        float human_judgement_score
        float ai_exposure_score
        string impact_category
        text reasoning
    }

    FUTURE_RESPONSIBILITY {
        int id PK
        int role_id FK
        text responsibility
        text reason
        int related_activity_id FK
    }

    FUTURE_SKILL {
        int id PK
        int role_id FK
        int skill_id FK
        string skill_status
        text reason
    }

    ROLE_FUTURE_PROFILE {
        int id PK
        int role_id FK
        string future_role_title
        text future_role_summary
        text key_changes
        text human_focus
        text ai_focus
        text future_capabilities
    }

    RESEARCH_SOURCE {
        int id PK
        string source_id
        string title
        string publisher
        string url
        string publication_date
        text summary
        float relevance_score
    }

    ROLE_ANALYSIS {
        int id PK
        int role_id FK
        float average_ai_exposure
        float average_automation_potential
        float average_augmentation_potential
        int activities_likely_automated
        int activities_likely_augmented
        int activities_human_led
        text new_responsibilities
        text future_skills
        text future_role_profile
    }
```

---

## Table Descriptions

1. **`roles`**: Stores the 20+ banking roles, their descriptions, department, and baseline responsibilities.
2. **`processes`**: Stores banking processes (e.g., Data Management, Risk Assessment, Credit Underwriting).
3. **`activities`**: Stores specific granular activities with input characteristics and normalized scores.
4. **`skills`**: Reusable skills catalog (~60 skills across Technical, Domain, Analytics, and Soft categories).
5. **`role_processes`**: Association mapping connecting roles to processes with `involvement_level` (`Primary`, `Secondary`, `Supporting`).
6. **`role_activities`**: Association mapping connecting roles to activities with `responsibility_level` (`Primary`, `Supporting`, `Review`).
7. **`role_skills`**: Association mapping connecting roles to skills with `proficiency_level` (`Basic`, `Intermediate`, `Advanced`, `Expert`).
8. **`activity_skills`**: Association mapping connecting activities to skills with `importance` (`Low`, `Medium`, `High`).
9. **`activity_ai_impact`**: Detailed 0–100 scale activity AI impact assessment with qualitative reasoning.
10. **`future_responsibilities`**: New tasks emerging for each role due to AI adoption.
11. **`future_skills`**: Skill requirements for the future role with explicit status (`Emerging`, `Increasing`, `AI-Augmented`, `Changing`, `Declining`, `Enduring Human Capability`).
12. **`role_future_profiles`**: Transformed future role profile title, summary, human vs AI focus, and capabilities.
13. **`research_sources`**: Verified public research papers and industry benchmarks (WEF, McKinsey, BIS, Gartner, BLS).
14. **`role_analyses`**: Aggregated role-level AI exposure metrics and summary statistics.
