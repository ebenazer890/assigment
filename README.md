# Role-Level AI Intelligence Platform

### MODUS Enterprise AI Build Challenge — Assignment 6

An Enterprise AI application for analysing how AI may transform roles, activities, responsibilities, and skills within the Banking and Financial Services industry.

The platform connects:

**Role → Processes → Activities → Current Skills → AI Exposure → Automated Activities → Augmented Activities → New Responsibilities → Future Skills → Future Role Profile**

The application is designed as a real enterprise application rather than a generic LLM chatbot. It combines a web interface, backend APIs, structured persistent data, AI reasoning, retrieval/research, and explainable role-level analysis.

---

## 1. Executive Summary

Organisations are adopting AI across business processes, but the impact is not the same for every job role.

Some activities may become highly automated. Others may become AI-assisted while still requiring human judgement. New responsibilities and skills may also emerge.

The purpose of this application is to help an organisation understand:

* Which roles are likely to be most affected by AI?
* Which activities may be automated?
* Which activities may be augmented by AI?
* Which activities should remain predominantly human-led?
* What new responsibilities may emerge?
* What future skills will employees need?
* Which roles may require significant reskilling?
* Why does the system reach a particular conclusion?

The application analyses these questions through connected enterprise intelligence rather than relying solely on an LLM response.

---

# 2. Business Problem

Traditional job descriptions describe what a role does today, but they do not provide a structured view of how AI may change that role.

For example, a Data Analyst may currently perform:

* Data extraction
* SQL querying
* Data cleaning
* Reporting
* Dashboard development
* Trend analysis
* Anomaly detection
* Stakeholder communication

As AI capabilities improve, some of these activities may become more automated, while others may become AI-assisted.

This creates several business questions:

> What will the Data Analyst role look like in the future?

> Which activities will change?

> What skills will become more important?

> Which responsibilities will remain human-led?

> Which other roles will experience similar changes?

This application provides a structured way to answer those questions.

---

# 3. Solution

The **Role-Level AI Intelligence Platform** analyses representative roles within Banking and Financial Services.

For each role, the platform follows this intelligence chain:

```text
Role
  ↓
Processes
  ↓
Activities
  ↓
Current Skills
  ↓
AI Exposure
  ↓
Activities Automated
  ↓
Activities Augmented
  ↓
New Responsibilities
  ↓
Future Skills
  ↓
Future Role Profile
```

The system stores these relationships in a persistent data layer and uses AI/retrieval where appropriate to enrich the analysis.

---

# 4. Selected Industry

**Industry:** Banking and Financial Services

The initial dataset contains representative roles from areas such as:

* Analytics
* Finance
* Risk
* Credit
* Fraud
* Compliance
* Procurement
* Operations
* Customer Service
* Marketing
* HR
* Treasury
* Audit
* Product Management

---

# 5. Roles

The initial dataset contains approximately 20 representative roles.

### Current roles

1. Data Analyst
2. Business Analyst
3. Financial Analyst
4. Risk Analyst
5. Credit Analyst
6. Fraud Analyst
7. Compliance Analyst
8. Procurement Analyst
9. Procurement Manager
10. Finance Manager
11. Relationship Manager
12. Loan Officer
13. Operations Manager
14. Customer Service Manager
15. Customer Service Representative
16. Marketing Analyst
17. HR Analyst
18. Treasury Analyst
19. Internal Auditor
20. Product Manager

The data model is designed so additional roles can be added without changing the application source code.

---

# 6. Primary Demonstration Role

## Data Analyst

Data Analyst is the primary demonstration role.

The application analyses activities including:

* Data extraction
* SQL querying
* Data cleaning
* Data quality validation
* Exploratory data analysis
* Dashboard creation
* Report generation
* Trend analysis
* Anomaly detection
* Forecasting
* Stakeholder reporting
* Business insight generation

Current skills include:

* SQL
* Python
* Statistics
* Excel
* Data Analysis
* Data Visualization
* Communication
* Business Acumen

The platform then analyses how AI may affect those activities and derives a future role profile.

---

# 7. Core Intelligence Model

The platform maintains relationships between roles, processes, activities and skills.

```text
Role
 │
 ├── Processes
 │     │
 │     └── Activities
 │             │
 │             ├── Required Skills
 │             └── AI Impact
 │
 ├── Current Skills
 │
 ├── Future Responsibilities
 │
 ├── Future Skills
 │
 └── Future Role Profile
```

This allows the system to answer role-level questions from structured enterprise information.

---

# 8. AI Impact Analysis

AI impact is analysed at the **activity level**.

The application considers factors such as:

* Automation potential
* Repetition
* Data availability
* Rule-based characteristics
* Complexity
* Human judgement
* Regulatory sensitivity
* Human interaction

Activities can be classified as:

* **Mostly Automated**
* **AI Augmented**
* **Human Led**

The application uses a repeatable scoring methodology rather than asking an LLM to arbitrarily assign an overall role score.

---

# 9. AI Exposure

The role-level AI exposure is derived from the underlying activity-level analysis.

For example:

| Activity                    | AI Impact                 |
| --------------------------- | ------------------------- |
| Data Cleaning               | High automation potential |
| Basic SQL Generation        | High automation potential |
| Report Generation           | High automation potential |
| Exploratory Analysis        | AI augmented              |
| Anomaly Detection           | AI augmented              |
| Forecasting                 | AI augmented              |
| Stakeholder Communication   | Human-led                 |
| Business Problem Definition | Human-led                 |

The overall role assessment is derived from the underlying activities rather than simply assigning a fixed value to the role.

---

# 10. Future Role Analysis

For every analysed role, the platform identifies:

### Activities likely to be automated

Activities where AI may perform a significant portion of repetitive or structured work.

### Activities likely to be augmented

Activities where AI can assist the employee while human oversight remains important.

### Human-led activities

Activities that continue to require significant human judgement, business context, interaction, accountability, or decision-making.

### New responsibilities

Responsibilities that may emerge as AI becomes integrated into the role.

### Future skills

Skills that may become more important as the role changes.

### Future role profile

A structured description of how the role may evolve.

---

# 11. Example Future Data Analyst

A potential future Data Analyst profile may include responsibilities such as:

* Validating AI-generated analysis
* Reviewing automated data-quality results
* Designing AI-assisted analytics workflows
* Interpreting complex business questions
* Monitoring AI-assisted reporting
* Communicating insights to stakeholders

Potential future skills include:

* AI literacy
* AI-assisted analytics
* Advanced SQL
* Python
* Data engineering concepts
* Data quality management
* Critical thinking
* Business/domain knowledge

These are analytical outputs of the application and should not be interpreted as guaranteed predictions of future employment.

---

# 12. Role Comparison

The application supports comparisons between roles.

Example:

```text
Data Analyst
        VS
Procurement Analyst
```

The comparison can include:

* AI exposure
* Activities
* Automated activities
* AI-augmented activities
* Human-led activities
* Current skills
* Future skills
* New responsibilities

The system also explains the primary reasons for differences between roles.

Example question:

> Compare the future AI impact on a Data Analyst versus Procurement Analyst.

The comparison should be calculated from the underlying role/process/activity/skill intelligence rather than from a manually written answer.

---

# 13. AI Impact Ranking

The platform can calculate the roles with the highest AI impact.

Example:

> Which five roles are likely to experience the greatest change?

The ranking is dynamically calculated from the underlying activity-level AI impact scores.

It is not a hard-coded list.

If the underlying activity data changes, the ranking should also change.

---

# 14. Ask Intelligence

The application includes an AI intelligence interface for questions such as:

```text
Why is Data Analyst highly exposed to AI?

Which Data Analyst activities are likely to be automated?

Which activities will be AI augmented?

What future skills will Data Analysts need?

Which five roles have the highest AI impact?

Which roles require the greatest reskilling?

Compare Data Analyst and Procurement Analyst.

Which activities should remain human-led?

What evidence supports this conclusion?
```

The application should distinguish between:

### Deterministic queries

Questions that can be answered directly from structured database information should use application/database logic.

### AI reasoning

The LLM can be used for:

* Reasoning
* Synthesis
* Natural-language explanation
* Interpretation of retrieved evidence

The system does not send every question blindly to the LLM.

---

# 15. Evidence and Traceability

Important conclusions should be traceable to their underlying information.

The platform distinguishes between:

1. Structured application data
2. Calculated scores
3. Research evidence
4. AI-generated reasoning

Research metadata may include:

* Source title
* Publisher
* URL
* Publication date
* Source type
* Summary

The objective is to allow users to understand why the application reached a conclusion.

---

# 16. RAG / Knowledge Layer

Where applicable, the application uses retrieval to provide relevant external context to the AI layer.

The knowledge layer may contain information related to:

* AI adoption
* Workforce transformation
* Automation
* AI augmentation
* Analytics transformation
* Banking transformation
* Future skills

The retrieval pipeline should follow:

```text
Research Sources
      ↓
Document Processing
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Store
      ↓
Relevant Retrieval
      ↓
LLM Context
      ↓
Reasoned Output
```

The LLM should not be treated as the sole source of enterprise intelligence.

---

# 17. Dynamic New Role — Surprise Test

A critical feature of the application is the ability to analyse a new role without modifying source code.

Example:

```text
Supply Chain Analyst
```

The expected workflow is:

```text
New Role
   ↓
Input Validation
   ↓
Backend Processing
   ↓
Role Storage
   ↓
Process Creation
   ↓
Activity Creation
   ↓
Skill Mapping
   ↓
AI Impact Analysis
   ↓
Research / Retrieval
   ↓
AI Reasoning
   ↓
Future Responsibilities
   ↓
Future Skills
   ↓
Future Role Profile
   ↓
Persistent Storage
   ↓
Application Output
```

The new role must remain available after restarting the application.

This functionality is particularly important for technical validation.

---

# 18. Architecture

```text
┌──────────────────────────────────────┐
│              FRONTEND                │
│             Streamlit               │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          APPLICATION / API           │
│               FastAPI                │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          BUSINESS SERVICES           │
│                                      │
│ Role Analysis                        │
│ AI Impact Calculation                │
│ Comparison                           │
│ Ranking                              │
│ Dynamic Role Processing              │
└───────────────┬───────────┬──────────┘
                │           │
                ▼           ▼
       ┌──────────────┐ ┌───────────────┐
       │ PostgreSQL   │ │ RAG / Vector  │
       │              │ │ Store         │
       │ Roles        │ │               │
       │ Processes    │ │ Research      │
       │ Activities   │ │ Evidence      │
       │ Skills       │ │ Embeddings    │
       │ Analyses     │ │               │
       └──────────────┘ └───────┬───────┘
                                │
                                ▼
                       ┌────────────────┐
                       │   Local LLM    │
                       │    Ollama      │
                       └────────────────┘
```

---

# 19. Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy

### Frontend

* Streamlit

### Database

* PostgreSQL

### AI / LLM

* Ollama
* Configured open-source language model

### Embeddings / Retrieval

* Sentence Transformers
* FAISS or Chroma

### Data Processing

* Pandas

### Testing

* pytest

### Reproducibility

* Docker
* Docker Compose, where applicable

The final repository should contain the exact versions used by the application.

---

# 20. Data Model

The main entities include:

```text
Role
Process
Activity
Skill
RoleProcess
RoleActivity
RoleSkill
ActivitySkill
AIImpactAssessment
FutureResponsibility
FutureSkill
FutureRoleProfile
ResearchSource
EvidenceRelationship
```

The database uses relationships between these entities instead of treating each role as an isolated document.

---

# 21. Persistence

PostgreSQL is used as the persistent data layer.

The following information should survive application restarts:

* Roles
* Processes
* Activities
* Skills
* Role/process relationships
* Role/activity relationships
* Role/skill relationships
* AI impact assessments
* Future responsibilities
* Future skills
* Future role profiles
* Research metadata

---

# 22. Project Structure

The actual repository structure should be documented here after implementation.

Expected logical structure:

```text
role-ai-intelligence/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── ai/
│   │   ├── retrieval/
│   │   ├── db/
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── seed/
│   └── research/
│
├── scripts/
│
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   └── methodology.md
│
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── LICENSES.md
```

**Important:** the final README must be updated to match the actual repository. Do not leave assumed paths if the implementation uses different paths.

---

# 23. Installation

## Prerequisites

Install the software required by the actual implementation.

Expected prerequisites may include:

* Python 3.11+
* PostgreSQL
* Git
* Ollama

Optional:

* Docker
* Docker Compose

The final README should list the exact tested versions.

---

# 24. Clone the Repository

```bash
git clone <ACTUAL_REPOSITORY_URL>
cd <ACTUAL_PROJECT_DIRECTORY>
```

Replace the placeholders with the actual repository information before submission.

---

# 25. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 26. Install Dependencies

```bash
pip install -r requirements.txt
```

The exact dependency file and command should match the final repository.

---

# 27. Environment Configuration

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database>
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=<configured-model>
VECTOR_STORE_PATH=./data/vector_store
```

Do not commit secrets to the repository.

The final `.env.example` should contain all required configuration variables without real credentials.

---

# 28. Database Setup

Start PostgreSQL.

Create the application database.

Example:

```sql
CREATE DATABASE role_ai;
```

Then run the actual database initialization command implemented by the project.

For example:

```bash
python scripts/init_db.py
```

**The command above must only remain in the final README if that file actually exists and the command has been tested.**

---

# 29. Load the Dataset

Run the project's actual seed-data command.

Example:

```bash
python scripts/seed_data.py
```

This should load:

* Roles
* Processes
* Activities
* Skills
* Relationships
* AI impact data
* Future skills
* Future responsibilities
* Research metadata

The final README should document the actual seed command implemented in the repository.

---

# 30. Configure the LLM

If the project uses Ollama locally:

Start Ollama and verify it is available.

Pull the configured model:

```bash
ollama pull <ACTUAL_MODEL_NAME>
```

Verify:

```bash
ollama list
```

The final README must contain the actual model name used by the application.

---

# 31. Start the Backend

Run the actual FastAPI entry point.

Example:

```bash
uvicorn backend.app.main:app --reload
```

If the project's actual entry point differs, use the actual command.

FastAPI documentation should be available at:

```text
http://localhost:8000/docs
```

if the application uses the default port.

---

# 32. Start the Frontend

Open a second terminal.

Activate the virtual environment.

Run the actual Streamlit entry point.

Example:

```bash
streamlit run frontend/app.py
```

The terminal will display the application URL.

---

# 33. Running the Complete Application

The final application may require the following services:

### PostgreSQL

Persistent database.

### Ollama

Local language model service, if used.

### FastAPI

Backend and API layer.

Example:

```bash
uvicorn backend.app.main:app --reload
```

### Streamlit

Frontend.

Example:

```bash
streamlit run frontend/app.py
```

The final README should document the exact startup sequence after testing it end-to-end.

---

# 34. Quick Start

After the initial installation:

### Terminal 1

Start the backend:

```bash
<ACTUAL_BACKEND_COMMAND>
```

### Terminal 2

Start the frontend:

```bash
<ACTUAL_FRONTEND_COMMAND>
```

Make sure PostgreSQL and the required AI service are available.

Then open the URL displayed by the frontend.

---

# 35. Testing

Run the complete test suite:

```bash
pytest
```

For detailed output:

```bash
pytest -v
```

Tests should cover:

* Role creation
* Role retrieval
* Process relationships
* Activity relationships
* Skill relationships
* AI exposure calculation
* Role analysis
* Role comparison
* AI impact ranking
* New-role creation
* API endpoints
* Persistence

---

# 36. End-to-End Test

The most important end-to-end workflow is:

```text
Create New Role
      ↓
Save Role
      ↓
Create Relationships
      ↓
Analyse Activities
      ↓
Calculate AI Impact
      ↓
Retrieve Evidence
      ↓
Generate Future Analysis
      ↓
Persist Result
      ↓
Retrieve Result
```

Example test role:

**Supply Chain Analyst**

After creating the role:

1. Restart the backend.
2. Restart the frontend.
3. Open the application.
4. Confirm the role still exists.
5. Confirm its analysis still exists.

---

# 37. Application Features

## Executive Dashboard

Displays high-level intelligence such as:

* Total roles
* Total processes
* Total activities
* Average AI exposure
* Highest-impact roles
* Important future skills

---

## Role Explorer

Allows the user to browse available roles.

---

## Role Analysis

Provides detailed analysis for an individual role.

---

## Role Comparison

Allows two roles to be compared.

Example:

```text
Data Analyst
VS
Procurement Analyst
```

---

## AI Impact Ranking

Displays the roles with the highest calculated AI impact.

---

## Add New Role

Allows a user to add a new role dynamically.

---

## Ask Intelligence

Allows users to ask natural-language questions about the role intelligence.

---

## Evidence / Research

Displays supporting research and source metadata where implemented.

---

# 38. Demo Scenario 1 — Executive Dashboard

Open the dashboard.

Show:

* Number of roles
* Number of processes
* Number of activities
* Average AI exposure
* Highest-impact roles
* Future skills

Explain that the results are calculated from the underlying application data.

---

# 39. Demo Scenario 2 — Data Analyst

Select:

**Data Analyst**

Demonstrate:

1. Role overview
2. Processes
3. Activities
4. Current skills
5. AI exposure
6. Automated activities
7. Augmented activities
8. Human-led activities
9. New responsibilities
10. Future skills
11. Future role profile
12. Evidence
13. Explanation

The key point is to demonstrate the chain:

```text
Role
→ Process
→ Activity
→ Skill
→ AI Impact
→ Future Change
```

---

# 40. Demo Scenario 3 — Role Comparison

Select:

**Data Analyst**

and:

**Procurement Analyst**

Show:

* AI exposure
* Activity-level differences
* Automation
* Augmentation
* Human-led activities
* Current skills
* Future skills
* New responsibilities

Then explain why the system calculates different levels of AI impact.

---

# 41. Demo Scenario 4 — Surprise Test

Create:

**Supply Chain Analyst**

Demonstrate the complete workflow:

```text
New Role
→ Backend Processing
→ Activity Analysis
→ AI Impact
→ Research / Retrieval
→ Future Responsibilities
→ Future Skills
→ Future Role Profile
→ Storage
→ Output
```

Do not modify the source code while performing this test.

---

# 42. Explainability

The system should not display an unexplained score such as:

```text
AI Exposure = 72%
```

Instead, it should show the contributing activities and factors.

For example:

```text
Data Cleaning
→ High automation potential

SQL Querying
→ High automation potential

Report Generation
→ High automation potential

Trend Analysis
→ Medium AI impact

Stakeholder Communication
→ Low automation potential
```

The role-level assessment is derived from these underlying activity-level results.

---

# 43. Research Sources

Research sources should be stored with metadata such as:

* Title
* Publisher
* URL
* Publication date
* Source type
* Summary

The application should not invent research sources.

Research should support conclusions about areas such as:

* AI transformation
* Automation
* AI augmentation
* Analytics
* Banking
* Workforce transformation
* Future skills

---

# 44. Data and Knowledge Layer

The application uses structured data for enterprise intelligence.

Example entities:

```text
Role
Process
Activity
Skill
AI Impact
Future Responsibility
Future Skill
Future Role Profile
Research Source
```

This allows relationships to be queried rather than storing every answer as a static paragraph.

---

# 45. Persistence

The application uses persistent storage for enterprise information.

Data should survive application restarts.

The database should contain:

* Roles
* Processes
* Activities
* Skills
* Relationships
* AI assessments
* Future analysis
* Research metadata

---

# 46. Error Handling

The application should gracefully handle:

* Invalid role input
* Missing database
* Database connection failure
* Missing activity information
* Missing skills
* LLM unavailable
* Ollama unavailable
* Vector store unavailable
* Empty retrieval results
* Invalid AI output

Where possible, deterministic application functionality should remain available when the AI service is unavailable.

---

# 47. Design Principles

### 1. Structured intelligence

The application uses structured role/process/activity/skill relationships.

### 2. Explainability

Important conclusions should be explainable using underlying data and evidence.

### 3. Dynamic processing

New roles should be processable without source-code changes.

### 4. Persistent storage

Enterprise intelligence should persist beyond a single application session.

### 5. Modular architecture

Frontend, backend, AI, retrieval, business logic and data layers should remain separated.

### 6. AI as an intelligence layer

The LLM should enhance reasoning and synthesis rather than contain the entire application logic.

---

# 48. What This Application Is Not

This project is not intended to be:

* A generic chatbot
* A static HTML page
* A manually populated spreadsheet
* A notebook containing manually executed prompts
* A collection of hard-coded role reports
* A simple wrapper around a hosted LLM
* A single giant prompt containing all project intelligence

The objective is to demonstrate a working enterprise AI application with meaningful backend intelligence and dynamic processing.

---

# 49. Scalability Considerations

The architecture is designed around structured data and reusable processing rather than manually generated outputs.

If the number of roles, activities or processes increases:

```text
More Data
   ↓
Same Data Model
   ↓
Same Processing Pipeline
   ↓
Same AI Analysis
   ↓
Same Application
```

The application should be designed so that increasing the dataset does not require rewriting role-specific application logic.

---

# 50. Limitations

The AI exposure analysis is an analytical model and should not be interpreted as a guaranteed prediction of job elimination.

Actual AI impact can depend on:

* Organisation
* Technology maturity
* Business model
* Data availability
* Regulation
* Human oversight
* Implementation quality
* Workforce strategy

The application therefore provides decision-support intelligence rather than certainty about future employment.

---

# 51. Future Improvements

Possible future improvements include:

* Expand from 20 to 50+ roles
* Support multiple industries
* Continuous research updates
* More detailed skill-gap analysis
* Reskilling recommendations
* Scenario modelling
* Historical AI-impact tracking
* More advanced knowledge graphs
* Enterprise authentication
* Cloud deployment
* Role-specific transformation plans
* Workforce planning integration

---

# 52. Third-Party Libraries and Models

See:

`LICENSES.md`

for the complete list of third-party dependencies, models, licences and usage information.

The final repository should include:

* Library name
* Version
* Purpose
* Licence
* Model licence where applicable
* Source/reference

---

# 53. AI-Assisted Development Disclosure

AI coding and development tools were used during development.

The final submission should clearly identify:

* Which AI tools were used
* What they were used for
* Which architectural decisions were made by the candidate
* Which components were reviewed and validated by the candidate

The candidate must be able to explain the application's major architectural and implementation decisions during technical validation.

---

# 54. Challenge Alignment

This application implements:

**MODUS Enterprise AI Build Challenge — Assignment 6: Role-Level AI Intelligence**

The implementation addresses the required role-level intelligence chain:

```text
Role
↓
Processes
↓
Activities
↓
Current Skills
↓
AI Exposure
↓
Activities Automated
↓
Activities Augmented
↓
New Responsibilities
↓
Future Skills
↓
Future Role Profile
```

The application also supports:

* Role comparison
* AI-impact ranking
* Explainability
* Dynamic new-role processing
* Persistent storage
* AI reasoning
* Research/retrieval where implemented

---

# 55. Final Submission Checklist

Before submitting, verify:

### Application

* [ ] Frontend works
* [ ] Backend works
* [ ] Database works
* [ ] AI service works
* [ ] Role analysis works
* [ ] Role comparison works
* [ ] AI-impact ranking works
* [ ] Ask Intelligence works
* [ ] New Role works
* [ ] New role persists after restart

### Data

* [ ] Approximately 20 representative roles
* [ ] Processes populated
* [ ] Activities populated
* [ ] Current skills populated
* [ ] Role/process relationships populated
* [ ] Role/activity relationships populated
* [ ] Role/skill relationships populated
* [ ] AI impact information populated
* [ ] Future skills populated
* [ ] Future responsibilities populated

### Documentation

* [ ] README
* [ ] Setup instructions
* [ ] Architecture diagram
* [ ] Data model
* [ ] AI scoring methodology
* [ ] Research sources
* [ ] Model/library inventory
* [ ] Licences
* [ ] Sample/synthetic data
* [ ] Testing instructions
* [ ] Demo instructions

### Demonstration

* [ ] Executive dashboard
* [ ] Data Analyst analysis
* [ ] Role comparison
* [ ] Top AI-impact roles
* [ ] New-role Surprise Test
* [ ] Evidence/reasoning demonstration

---

# 56. Final Demo

Recommended demonstration sequence:

```text
1. Business Problem
       ↓
2. Architecture
       ↓
3. Executive Dashboard
       ↓
4. Data Analyst Analysis
       ↓
5. Explain AI Exposure
       ↓
6. Compare Two Roles
       ↓
7. Show AI Impact Ranking
       ↓
8. Add New Role
       ↓
9. Demonstrate Dynamic Processing
       ↓
10. Explain Technical Decisions
```

Recommended duration:

**10–15 minutes**

The demonstration should focus on showing that the application is a working enterprise AI system rather than simply a collection of generated AI responses.

---

# 57. Contact / Repository

Repository:

`<ACTUAL_GITHUB_REPOSITORY_URL>`

Project:

**Role-Level AI Intelligence Platform**

Challenge:

**MODUS Enterprise AI Build Challenge — Assignment 6**

Industry:

**Banking and Financial Services**

Primary demonstration:

**Data Analyst**
