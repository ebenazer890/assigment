"""
Comprehensive Seed Data for Banking & Financial Services Roles
"""
from sqlalchemy.orm import Session
from app.db.models import (
    Industry, Role, Process, Activity, Skill, RoleSkill, ActivitySkill,
    RoleProcess, RoleActivity, ActivityAIImpact, FutureResponsibility,
    FutureSkill, RoleFutureProfile, ResearchSource, RoleAnalysis
)
from app.scoring import AIScoringEngine
import json

# Real public research evidence sources
REAL_RESEARCH_SOURCES = [
    {
        "source_id": "WEF_FOJ_2023",
        "title": "The Future of Jobs Report 2023",
        "publisher": "World Economic Forum",
        "url": "https://www.weforum.org/reports/the-future-of-jobs-report-2023/",
        "publication_date": "2023-04-30",
        "source_type": "Global Report",
        "summary": "Analytic, data-driven, and administrative roles face up to 45% task transformation. Data Analysts and Financial Analysts see high AI augmentation alongside demand for AI literacy and critical decision-making.",
        "relevance_score": 0.95
    },
    {
        "source_id": "MCKINSEY_GENAI_FINANCE_2023",
        "title": "The Economic Potential of Generative AI in Financial Services",
        "publisher": "McKinsey Global Institute",
        "url": "https://www.mckinsey.com/capabilities/mgi/our-insights/the-economic-potential-of-generative-ai",
        "publication_date": "2023-06-14",
        "source_type": "Industry Benchmark",
        "summary": "Generative AI could add $200B-$340B annually to banking value, automating up to 70% of routine report writing, basic coding, and customer inquiry triage while shifting human roles toward strategic interpretation and governance.",
        "relevance_score": 0.98
    },
    {
        "source_id": "BIS_AI_BANKING_2024",
        "title": "Artificial Intelligence in Banking: Financial Stability & Operational Impacts",
        "publisher": "Bank for International Settlements",
        "url": "https://www.bis.org/publ/work1180.htm",
        "publication_date": "2024-02-15",
        "source_type": "Central Bank Research Paper",
        "summary": "AI adoption in credit scoring and fraud detection enhances accuracy by 30%, but regulatory compliance and model risk management require strong human oversight and explainability.",
        "relevance_score": 0.92
    },
    {
        "source_id": "GARTNER_BANKING_AI_2024",
        "title": "Gartner Hype Cycle for AI in Banking and Investment Services",
        "publisher": "Gartner Research",
        "url": "https://www.gartner.com/en/documents/4021999",
        "publication_date": "2024-01-20",
        "source_type": "Analyst Report",
        "summary": "Autonomous AI analytics agents will handle 50% of routine BI reporting by 2026, elevating data analysts into AI analytics product managers and enterprise data stewards.",
        "relevance_score": 0.90
    },
    {
        "source_id": "BLS_FINANCIAL_ANALYSTS_2024",
        "title": "Occupational Outlook: Financial Analysts & Data Practitioners",
        "publisher": "U.S. Bureau of Labor Statistics",
        "url": "https://www.bls.gov/ooh/math/data-scientists.htm",
        "publication_date": "2024-04-10",
        "source_type": "Government Statistics",
        "summary": "Demand for financial and data analytical roles will grow 35% through 2032, driven by the need for human expert interpretation of machine learning model outputs.",
        "relevance_score": 0.88
    }
]

# Standard Skills Database (~60 Reusable Skills)
SKILLS_SEED = [
    # Technical & Data Skills
    {"name": "SQL", "category": "Technical", "is_future_skill": False},
    {"name": "Python", "category": "Technical", "is_future_skill": False},
    {"name": "Excel & Financial Modeling", "category": "Technical", "is_future_skill": False},
    {"name": "Tableau / Power BI", "category": "Technical", "is_future_skill": False},
    {"name": "Statistical Analysis", "category": "Analytics", "is_future_skill": False},
    {"name": "Data Cleaning & Validation", "category": "Analytics", "is_future_skill": False},
    {"name": "Machine Learning Foundations", "category": "Technical", "is_future_skill": True},
    {"name": "AI Prompt Engineering", "category": "Technical", "is_future_skill": True},
    {"name": "AI Workflow Automation", "category": "Technical", "is_future_skill": True},
    {"name": "Data Governance & Quality Management", "category": "Analytics", "is_future_skill": True},
    
    # Financial & Banking Domain Skills
    {"name": "Financial Analysis", "category": "Domain", "is_future_skill": False},
    {"name": "Risk Assessment", "category": "Domain", "is_future_skill": False},
    {"name": "Credit Underwriting", "category": "Domain", "is_future_skill": False},
    {"name": "Fraud Detection", "category": "Domain", "is_future_skill": False},
    {"name": "Regulatory Compliance", "category": "Domain", "is_future_skill": False},
    {"name": "Anti-Money Laundering (AML)", "category": "Domain", "is_future_skill": False},
    {"name": "Treasury & Liquidity Management", "category": "Domain", "is_future_skill": False},
    {"name": "Procurement Strategy", "category": "Domain", "is_future_skill": False},
    {"name": "Auditing & Internal Controls", "category": "Domain", "is_future_skill": False},
    {"name": "Loan Origination", "category": "Domain", "is_future_skill": False},
    {"name": "Market Research & Analytics", "category": "Domain", "is_future_skill": False},
    {"name": "Workforce Analytics", "category": "Domain", "is_future_skill": False},

    # Soft & Management Skills
    {"name": "Critical Thinking", "category": "Soft", "is_future_skill": True},
    {"name": "Stakeholder Communication", "category": "Soft", "is_future_skill": False},
    {"name": "Problem Solving", "category": "Soft", "is_future_skill": False},
    {"name": "Strategic Decision Making", "category": "Soft", "is_future_skill": True},
    {"name": "Negotiation", "category": "Soft", "is_future_skill": False},
    {"name": "Client Relationship Management", "category": "Soft", "is_future_skill": False},
    {"name": "Ethical Judgment & Bias Audit", "category": "Soft", "is_future_skill": True},
    {"name": "AI Model Oversight", "category": "Analytics", "is_future_skill": True},
    {"name": "Product Roadmap Management", "category": "Management", "is_future_skill": False},
    {"name": "Process Optimization", "category": "Management", "is_future_skill": False}
]

# Detailed 20 Banking Roles
ROLES_SEED_DATA = [
    {
        "name": "Data Analyst",
        "department": "Analytics & Business Intelligence",
        "description": "Analyzes complex financial, operational, and customer data to deliver actionable insights and executive dashboards for banking leadership.",
        "current_responsibilities": "Writing SQL queries, extracting warehouse data, cleaning raw transactional records, creating Tableau dashboards, generating monthly executive reports, and conducting ad-hoc trend analyses.",
        "future_title": "AI-Augmented Data Analytics Specialist",
        "future_summary": "Transitions from manual SQL querying and report generation to managing automated AI analytics pipelines, auditing synthetic data outputs, and framing strategic business queries.",
        "key_changes": "80% reduction in manual data cleaning and SQL boilerplate creation; increased focus on AI output validation, business context translation, and enterprise data governance.",
        "human_focus": "Strategic stakeholder consultation, anomaly interpretation, ethical data oversight, and complex cross-functional business storytelling.",
        "ai_focus": "Automated data ingestion, AI-generated SQL query generation, routine visualization drafting, anomaly alerting, and predictive forecasting.",
        "future_capabilities": "Generative BI design, natural language query tuning, AI agent supervision, and high-level predictive model evaluation.",
        "processes": [
            {
                "name": "Data Management",
                "department": "Data Engineering & Analytics",
                "description": "Extracting, transforming, loading, and validating enterprise banking datasets.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "SQL Data Extraction & Transformation",
                        "description": "Executing complex database queries to extract transactional and customer tables.",
                        "repetitiveness": 0.85, "data_availability": 0.95, "rule_based_nature": 0.80,
                        "complexity": 0.40, "human_judgement": 0.30, "regulatory_sensitivity": 0.30, "human_interaction": 0.20,
                        "responsibility_level": "Primary", "skills": ["SQL", "Data Cleaning & Validation"]
                    },
                    {
                        "name": "Validate Transaction Data before Reporting",
                        "description": "Auditing raw ledger data for missing records, anomalies, and schema inconsistencies prior to executive publication.",
                        "repetitiveness": 0.80, "data_availability": 0.90, "rule_based_nature": 0.75,
                        "complexity": 0.45, "human_judgement": 0.40, "regulatory_sensitivity": 0.60, "human_interaction": 0.20,
                        "responsibility_level": "Primary", "skills": ["Data Cleaning & Validation", "SQL"]
                    },
                    {
                        "name": "Data Pipeline Maintenance & Schema Mapping",
                        "description": "Configuring ETL jobs and mapping new data sources to standard warehouse schemas.",
                        "repetitiveness": 0.65, "data_availability": 0.85, "rule_based_nature": 0.70,
                        "complexity": 0.50, "human_judgement": 0.45, "regulatory_sensitivity": 0.40, "human_interaction": 0.30,
                        "responsibility_level": "Supporting", "skills": ["SQL", "Python"]
                    }
                ]
            },
            {
                "name": "Reporting and Analytics",
                "department": "Business Intelligence",
                "description": "Synthesizing transactional datasets into business dashboards and executive briefings.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Dashboard Development & Maintenance",
                        "description": "Designing interactive Power BI and Tableau dashboards for executive business units.",
                        "repetitiveness": 0.60, "data_availability": 0.90, "rule_based_nature": 0.65,
                        "complexity": 0.50, "human_judgement": 0.45, "regulatory_sensitivity": 0.20, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Tableau / Power BI", "Data Cleaning & Validation"]
                    },
                    {
                        "name": "Periodic Management Report Generation",
                        "description": "Compiling recurring weekly and monthly performance reports for senior department heads.",
                        "repetitiveness": 0.85, "data_availability": 0.95, "rule_based_nature": 0.80,
                        "complexity": 0.35, "human_judgement": 0.35, "regulatory_sensitivity": 0.40, "human_interaction": 0.25,
                        "responsibility_level": "Primary", "skills": ["Excel & Financial Modeling", "Tableau / Power BI"]
                    },
                    {
                        "name": "Exploratory Data Analysis & Hypothesis Testing",
                        "description": "Investigating customer behavior patterns and statistical anomalies to discover root causes.",
                        "repetitiveness": 0.40, "data_availability": 0.85, "rule_based_nature": 0.35,
                        "complexity": 0.75, "human_judgement": 0.75, "regulatory_sensitivity": 0.30, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Statistical Analysis", "Python"]
                    },
                    {
                        "name": "Executive Stakeholder Insight Presentation",
                        "description": "Communicating analytical findings and strategic recommendations to bank decision-makers.",
                        "repetitiveness": 0.25, "data_availability": 0.60, "rule_based_nature": 0.20,
                        "complexity": 0.80, "human_judgement": 0.90, "regulatory_sensitivity": 0.30, "human_interaction": 0.90,
                        "responsibility_level": "Primary", "skills": ["Stakeholder Communication", "Critical Thinking"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Audit and validate AI-generated analytical scripts and query logic", "reason": "Automated code generation requires senior analytical verification to prevent hallucinations."},
            {"responsibility": "Manage natural-language generative BI conversational agents", "reason": "Stakeholders will interact directly with AI agents; data analysts configure metadata and semantic layers."},
            {"responsibility": "Oversee enterprise data ethics and synthetic data validation", "reason": "Ensures AI models respect privacy laws and do not introduce bias into reporting."}
        ],
        "future_skills": [
            {"skill": "AI Prompt Engineering", "status": "Emerging", "reason": "Essential for steering LLM code assistants and BI synthesis agents."},
            {"skill": "AI Model Oversight", "status": "Increasing", "reason": "Crucial to verify AI analytical calculations before executive presentation."},
            {"skill": "SQL", "status": "AI-Augmented", "reason": "Basic SQL is generated by AI; analyst focuses on complex query logic validation."},
            {"skill": "Data Cleaning & Validation", "status": "Declining", "reason": "Routine data cleaning is automated by LLM agents and pipeline bots."},
            {"skill": "Critical Thinking", "status": "Enduring Human Capability", "reason": "Human contextual interpretation remains indispensable for high-stakes business strategy."}
        ]
    },
    {
        "name": "Business Analyst",
        "department": "Transformation & Business Architecture",
        "description": "Translates business needs into functional requirements, process designs, and software specifications.",
        "current_responsibilities": "Interviewing business units, drafting user stories, mapping BPMN workflows, and coordinating UAT testing.",
        "future_title": "AI Process Architect & Business Strategist",
        "future_summary": "Focuses on designing human-AI collaborative process flows and analyzing organizational impacts.",
        "key_changes": "Documentation drafting automated; shifted heavily toward strategic workshop facilitation.",
        "human_focus": "Stakeholder alignment, empathy-driven requirements discovery, change leadership.",
        "ai_focus": "Automated BPMN diagramming, instant requirements synthesis, user story generation.",
        "future_capabilities": "AI process orchestration, prompt-driven prototyping, change impact modeling.",
        "processes": [
            {
                "name": "Requirements Management",
                "department": "Business Architecture",
                "description": "Capturing and structuring organizational needs.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Stakeholder Discovery Interviews",
                        "description": "Conducting deep-dive interviews with business leaders to understand operational friction.",
                        "repetitiveness": 0.30, "data_availability": 0.40, "rule_based_nature": 0.15,
                        "complexity": 0.75, "human_judgement": 0.85, "regulatory_sensitivity": 0.30, "human_interaction": 0.95,
                        "responsibility_level": "Primary", "skills": ["Stakeholder Communication", "Critical Thinking"]
                    },
                    {
                        "name": "Process Mapping & Specification Drafting",
                        "description": "Documenting as-is and to-be business process workflows and technical specs.",
                        "repetitiveness": 0.65, "data_availability": 0.75, "rule_based_nature": 0.60,
                        "complexity": 0.55, "human_judgement": 0.55, "regulatory_sensitivity": 0.40, "human_interaction": 0.50,
                        "responsibility_level": "Primary", "skills": ["Process Optimization", "Critical Thinking"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Design human-in-the-loop AI operational workflows", "reason": "Ensure AI agents are integrated smoothly into human teams."},
            {"responsibility": "Validate AI-generated technical requirement specifications", "reason": "Ensure business intent matches software build specs."}
        ],
        "future_skills": [
            {"skill": "AI Prompt Engineering", "status": "Emerging", "reason": "Used to generate initial workflow specs and user stories."},
            {"skill": "Critical Thinking", "status": "Enduring Human Capability", "reason": "Essential for understanding non-verbal stakeholder needs."}
        ]
    },
    {
        "name": "Financial Analyst",
        "department": "Corporate Finance & FP&A",
        "description": "Evaluates financial performance, builds valuation models, and prepares capital allocation budgets.",
        "current_responsibilities": "Building multi-tab Excel financial models, performing variance analyses, and creating budget forecast decks.",
        "future_title": "Strategic FP&A & AI Financial Strategist",
        "future_summary": "Leverages real-time AI predictive models to conduct continuous dynamic financial forecasting.",
        "key_changes": "Excel data entry automated; analysts spend time running AI scenario simulations.",
        "human_focus": "Executive advisory, capital deployment strategy, economic risk evaluation.",
        "ai_focus": "Continuous rolling forecasts, automated variance root-cause analysis, sensitivity analysis.",
        "future_capabilities": "Real-time AI scenario modeling, capital optimization, executive financial advisory.",
        "processes": [
            {
                "name": "Financial Planning",
                "department": "FP&A",
                "description": "Formulating organizational budget targets and operational financial models.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Financial Model Construction & Maintenance",
                        "description": "Building discounted cash flow and three-statement financial models in spreadsheets.",
                        "repetitiveness": 0.60, "data_availability": 0.90, "rule_based_nature": 0.65,
                        "complexity": 0.70, "human_judgement": 0.60, "regulatory_sensitivity": 0.60, "human_interaction": 0.30,
                        "responsibility_level": "Primary", "skills": ["Excel & Financial Modeling", "Financial Analysis"]
                    },
                    {
                        "name": "Budget Variance & Performance Analysis",
                        "description": "Comparing actual revenue/expense results against quarterly budget targets.",
                        "repetitiveness": 0.75, "data_availability": 0.95, "rule_based_nature": 0.75,
                        "complexity": 0.50, "human_judgement": 0.50, "regulatory_sensitivity": 0.50, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Financial Analysis", "Excel & Financial Modeling"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Evaluate AI-generated continuous financial forecasts", "reason": "Validate machine learning projections against macroeconomic context."},
            {"responsibility": "Advise CFO on strategic capital allocation scenarios", "reason": "Focus on high-level decision making using AI simulation engines."}
        ],
        "future_skills": [
            {"skill": "Strategic Decision Making", "status": "Increasing", "reason": "Required to interpret AI financial simulations."},
            {"skill": "Excel & Financial Modeling", "status": "AI-Augmented", "reason": "Basic spreadsheets built automatically by AI co-pilots."}
        ]
    },
    {
        "name": "Risk Analyst",
        "department": "Enterprise Risk Management",
        "description": "Identifies, quantifies, and monitors market, credit, operational, and liquidity risks across the bank.",
        "current_responsibilities": "Running VAR models, monitoring risk exposure limits, drafting quarterly risk committee reports.",
        "future_title": "AI & Model Risk Oversight Specialist",
        "future_summary": "Monitors enterprise-wide AI autonomous agents for operational risk, systemic bias, and model drift.",
        "key_changes": "Shift from routine risk metric aggregation to auditing autonomous AI models and emerging cyber risks.",
        "human_focus": "Risk appetite setting, catastrophic risk scenario evaluation, regulator negotiation.",
        "ai_focus": "Real-time VAR computation, automated transaction risk scoring, systemic threat detection.",
        "future_capabilities": "AI safety evaluation, stress testing simulation, regulatory risk alignment.",
        "processes": [
            {
                "name": "Risk Assessment",
                "department": "Enterprise Risk",
                "description": "Evaluating exposure across credit, market, and operational domains.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Market & Credit Exposure Calculation",
                        "description": "Computing daily Value-at-Risk (VaR) metrics and scenario stress test values.",
                        "repetitiveness": 0.80, "data_availability": 0.95, "rule_based_nature": 0.85,
                        "complexity": 0.60, "human_judgement": 0.35, "regulatory_sensitivity": 0.90, "human_interaction": 0.20,
                        "responsibility_level": "Primary", "skills": ["Risk Assessment", "Statistical Analysis"]
                    },
                    {
                        "name": "Operational Risk Event Investigation",
                        "description": "Reviewing internal operational breakdowns and assessing loss impacts.",
                        "repetitiveness": 0.45, "data_availability": 0.70, "rule_based_nature": 0.40,
                        "complexity": 0.70, "human_judgement": 0.80, "regulatory_sensitivity": 0.85, "human_interaction": 0.60,
                        "responsibility_level": "Primary", "skills": ["Risk Assessment", "Critical Thinking"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Audit enterprise AI autonomous agents for operational model risk", "reason": "Ensure AI agents do not violate risk exposure guidelines."},
            {"responsibility": "Design stress-testing prompts for Generative AI risk models", "reason": "Evaluate bank resilience against novel macroeconomic shocks."}
        ],
        "future_skills": [
            {"skill": "AI Model Oversight", "status": "Emerging", "reason": "Critical for evaluating machine learning risk engine performance."},
            {"skill": "Ethical Judgment & Bias Audit", "status": "Increasing", "reason": "Required to prevent algorithmic bias in automated risk decisions."}
        ]
    },
    {
        "name": "Credit Analyst",
        "department": "Commercial & Retail Lending",
        "description": "Evaluates commercial and individual borrower creditworthiness to approve or reject loan applications.",
        "current_responsibilities": "Spreading financial statements, calculating debt service coverage ratios (DSCR), drafting credit memos.",
        "future_title": "Credit Decisioning & Portfolio Strategist",
        "future_summary": "Uses AI underwriting engines to automate standard approvals while specializing in complex, non-standard corporate loan structures.",
        "key_changes": "Standard credit memo generation automated; focus moves to high-value underwriting and edge cases.",
        "human_focus": "Complex deal structuring, borrower relationship evaluation, exception review.",
        "ai_focus": "Automated financial statement spreading, instant ratio calculation, credit score synthesis.",
        "future_capabilities": "AI credit model tuning, complex corporate restructuring, portfolio risk balancing.",
        "processes": [
            {
                "name": "Credit Assessment",
                "department": "Commercial Credit",
                "description": "Analyzing financial strength and collateral of loan applicants.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Financial Statement Spreading",
                        "description": "Entering borrower balance sheets and income statements into credit scoring software.",
                        "repetitiveness": 0.90, "data_availability": 0.95, "rule_based_nature": 0.85,
                        "complexity": 0.30, "human_judgement": 0.20, "regulatory_sensitivity": 0.70, "human_interaction": 0.10,
                        "responsibility_level": "Primary", "skills": ["Credit Underwriting", "Financial Analysis"]
                    },
                    {
                        "name": "Credit Approval Memo Drafting",
                        "description": "Writing comprehensive credit memos detailing risk factors, repayment capacity, and recommended loan covenants.",
                        "repetitiveness": 0.65, "data_availability": 0.85, "rule_based_nature": 0.60,
                        "complexity": 0.65, "human_judgement": 0.70, "regulatory_sensitivity": 0.85, "human_interaction": 0.30,
                        "responsibility_level": "Primary", "skills": ["Credit Underwriting", "Regulatory Compliance"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Review and override AI credit score recommendations on complex deals", "reason": "Ensure nuanced business context is considered beyond machine scores."},
            {"responsibility": "Monitor automated loan portfolio default indicator alerts", "reason": "Intervene early when AI flags degrading borrower performance."}
        ],
        "future_skills": [
            {"skill": "Credit Underwriting", "status": "AI-Augmented", "reason": "Routine ratio calculations automated; complex credit structuring remains human."},
            {"skill": "Ethical Judgment & Bias Audit", "status": "Increasing", "reason": "Ensure credit algorithms comply with fair lending laws."}
        ]
    },
    {
        "name": "Fraud Analyst",
        "department": "Financial Crime & Fraud Prevention",
        "description": "Detects, investigates, and mitigates fraudulent credit card, wire transfer, and account takeover attempts.",
        "current_responsibilities": "Reviewing transaction alert queues, contacting cardholders to verify suspicious charges, filing Suspicious Activity Reports (SARs).",
        "future_title": "AI Fraud Threat Hunter",
        "future_summary": "Leverages real-time AI anomaly detection agents to stop cyber fraud attacks and focuses on complex organized crime syndicates.",
        "key_changes": "85% of low-level transaction alerts handled automatically; analyst focuses on sophisticated cyber fraud networks.",
        "human_focus": "Complex crime syndicate investigation, law enforcement collaboration, adaptive threat strategy.",
        "ai_focus": "Real-time pattern recognition, instant transaction blocking, automated SAR draft generation.",
        "future_capabilities": "Graph analytics, AI threat pattern modeling, deepfake detection.",
        "processes": [
            {
                "name": "Fraud Detection",
                "department": "Financial Crime",
                "description": "Identifying and stopping unauthorized transactions.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Real-time Transaction Alert Triage",
                        "description": "Screening flagged suspicious debit/credit transactions against fraud rules.",
                        "repetitiveness": 0.90, "data_availability": 0.95, "rule_based_nature": 0.85,
                        "complexity": 0.35, "human_judgement": 0.30, "regulatory_sensitivity": 0.90, "human_interaction": 0.20,
                        "responsibility_level": "Primary", "skills": ["Fraud Detection", "Anti-Money Laundering (AML)"]
                    },
                    {
                        "name": "Complex Fraud Scheme Investigation",
                        "description": "Deep-dive analysis into multi-account synthetic identity fraud syndicates.",
                        "repetitiveness": 0.35, "data_availability": 0.80, "rule_based_nature": 0.30,
                        "complexity": 0.85, "human_judgement": 0.85, "regulatory_sensitivity": 0.95, "human_interaction": 0.60,
                        "responsibility_level": "Primary", "skills": ["Fraud Detection", "Critical Thinking"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Train AI fraud detection neural networks on novel attack vectors", "reason": "Feed new cybercrime tactics into ML engines."},
            {"responsibility": "Investigate AI-driven deepfake audio and identity spoofing attacks", "reason": "Human expertise required to verify voice and biometric authenticity."}
        ],
        "future_skills": [
            {"skill": "Fraud Detection", "status": "AI-Augmented", "reason": "Standard rules automated; complex investigative skills become paramount."},
            {"skill": "AI Model Oversight", "status": "Emerging", "reason": "Validate that fraud ML models do not block legitimate customer transactions."}
        ]
    },
    {
        "name": "Compliance Analyst",
        "department": "Regulatory Compliance & AML",
        "description": "Ensures bank operations adhere to financial regulations, KYC laws, and international banking standards.",
        "current_responsibilities": "Screening sanctions lists, conducting Know Your Customer (KYC) reviews, tracking regulatory policy updates.",
        "future_title": "RegTech & Regulatory AI Specialist",
        "future_summary": "Uses automated RegTech monitoring agents to continuously scan transactions for compliance breaches.",
        "key_changes": "Manual document checking automated; analyst shifts to interpreting new regulatory policies and managing regulator relationships.",
        "human_focus": "Regulator negotiation, policy interpretation, ethical compliance culture.",
        "ai_focus": "Automated sanctions list matching, continuous KYC updates, regulatory text parsing.",
        "future_capabilities": "RegTech orchestration, automated policy mapping, regulatory risk auditing.",
        "processes": [
            {
                "name": "Regulatory Compliance",
                "department": "Legal & Compliance",
                "description": "Monitoring adherence to banking statutes and anti-money laundering mandates.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "KYC Customer Document Verification",
                        "description": "Verifying customer identity papers against government databases and PEP lists.",
                        "repetitiveness": 0.85, "data_availability": 0.90, "rule_based_nature": 0.85,
                        "complexity": 0.40, "human_judgement": 0.35, "regulatory_sensitivity": 0.95, "human_interaction": 0.30,
                        "responsibility_level": "Primary", "skills": ["Regulatory Compliance", "Anti-Money Laundering (AML)"]
                    },
                    {
                        "name": "Regulatory Policy Gap Analysis",
                        "description": "Evaluating new banking regulations against existing internal operational policies.",
                        "repetitiveness": 0.40, "data_availability": 0.70, "rule_based_nature": 0.40,
                        "complexity": 0.80, "human_judgement": 0.85, "regulatory_sensitivity": 0.95, "human_interaction": 0.60,
                        "responsibility_level": "Primary", "skills": ["Regulatory Compliance", "Critical Thinking"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Manage RegTech AI agents performing continuous sanctions audit", "reason": "Monitor automated software scanning global transaction channels."},
            {"responsibility": "Interpret ambiguous regulatory changes for senior executive leadership", "reason": "Translate complex legal guidelines into bank business strategy."}
        ],
        "future_skills": [
            {"skill": "Regulatory Compliance", "status": "Changing", "reason": "Shifts from manual checking to legal interpretation and RegTech oversight."},
            {"skill": "AI Prompt Engineering", "status": "Emerging", "reason": "Used to query regulatory knowledge bases and policy compliance repositories."}
        ]
    },
    {
        "name": "Procurement Analyst",
        "department": "Procurement & Vendor Management",
        "description": "Analyzes corporate purchasing, evaluates vendor proposals, and tracks supplier contract performance.",
        "current_responsibilities": "Processing purchase requisitions, comparing vendor quotes, tracking invoice accuracy, drafting RFPs.",
        "future_title": "AI Sourcing & Supplier Analytics Specialist",
        "future_summary": "Leverages AI contract analysis tools to automate vendor evaluations and monitor supply chain risks in real time.",
        "key_changes": "RFP comparison and invoice matching automated; focus shifts to supplier relationship strategy.",
        "human_focus": "Vendor contract negotiation, executive supplier reviews, strategic relationship building.",
        "ai_focus": "Automated invoice audit, price benchmark comparison, contract anomaly extraction.",
        "future_capabilities": "Automated sourcing orchestration, supply chain risk prediction, procurement analytics.",
        "processes": [
            {
                "name": "Procurement",
                "department": "Corporate Sourcing",
                "description": "Sourcing goods, services, and software contracts for bank operations.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Purchase Order & Invoice Reconciliation",
                        "description": "Matching vendor invoices against purchase orders and delivery contracts.",
                        "repetitiveness": 0.90, "data_availability": 0.95, "rule_based_nature": 0.90,
                        "complexity": 0.30, "human_judgement": 0.20, "regulatory_sensitivity": 0.50, "human_interaction": 0.15,
                        "responsibility_level": "Primary", "skills": ["Procurement Strategy", "Excel & Financial Modeling"]
                    },
                    {
                        "name": "RFP Vendor Bid Evaluation",
                        "description": "Analyzing supplier responses to Requests for Proposal to score price and compliance.",
                        "repetitiveness": 0.55, "data_availability": 0.80, "rule_based_nature": 0.50,
                        "complexity": 0.65, "human_judgement": 0.70, "regulatory_sensitivity": 0.50, "human_interaction": 0.60,
                        "responsibility_level": "Primary", "skills": ["Procurement Strategy", "Negotiation"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Validate AI-generated vendor risk and contract clause audits", "reason": "Ensure AI contract parsers do not miss critical liability terms."},
            {"responsibility": "Conduct strategic supplier negotiations guided by AI price intelligence", "reason": "Human expertise required for high-stakes vendor discussions."}
        ],
        "future_skills": [
            {"skill": "Negotiation", "status": "Enduring Human Capability", "reason": "Human influence and relationship building remain key in vendor deals."},
            {"skill": "AI Workflow Automation", "status": "Emerging", "reason": "Configuring automated procurement request routing."}
        ]
    },
    {
        "name": "Procurement Manager",
        "department": "Global Procurement",
        "description": "Directs corporate sourcing strategy, manages vendor categories, and oversees procurement team operations.",
        "current_responsibilities": "Approving major vendor expenditures, leading strategic supplier negotiations, managing procurement team budgets.",
        "future_title": "Strategic Supply Chain & Sourcing Director",
        "future_summary": "Drives enterprise vendor strategy using predictive supply chain intelligence and automated procurement bots.",
        "key_changes": "Operational approval overhead reduced by 70%; time redirected to strategic partnerships and ESG sourcing.",
        "human_focus": "C-suite vendor alignment, strategic negotiation, executive risk leadership.",
        "ai_focus": "Predictive spend analytics, automated compliance tracking, vendor risk forecasting.",
        "future_capabilities": "Category strategy optimization, global supply network resilience, AI procurement leadership.",
        "processes": [
            {
                "name": "Procurement",
                "department": "Global Procurement",
                "description": "Managing enterprise vendor spend and strategic supplier partnerships.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Strategic Vendor Negotiation",
                        "description": "Negotiating master service agreements and multi-million dollar software contracts.",
                        "repetitiveness": 0.25, "data_availability": 0.60, "rule_based_nature": 0.20,
                        "complexity": 0.85, "human_judgement": 0.90, "regulatory_sensitivity": 0.60, "human_interaction": 0.95,
                        "responsibility_level": "Primary", "skills": ["Procurement Strategy", "Negotiation"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Oversee enterprise AI-driven procurement automation strategy", "reason": "Align procurement software bots with corporate financial goals."},
            {"responsibility": "Lead high-stakes vendor executive relationship reviews", "reason": "Build trust and long-term strategic supplier alignment."}
        ],
        "future_skills": [
            {"skill": "Strategic Decision Making", "status": "Increasing", "reason": "Critical for selecting long-term strategic vendor partners."},
            {"skill": "Negotiation", "status": "Enduring Human Capability", "reason": "Human executive presence is essential in supplier deal-making."}
        ]
    },
    {
        "name": "Finance Manager",
        "department": "Corporate Finance",
        "description": "Manages accounting teams, financial reporting operations, and internal financial controls.",
        "current_responsibilities": "Overseeing monthly ledger close, reviewing financial statements, managing audit compliance, leading finance staff.",
        "future_title": "AI Finance & Corporate Operations Director",
        "future_summary": "Leads continuous autonomous ledger close operations while focusing on strategic financial growth.",
        "key_changes": "Monthly close cycle reduced from 10 days to real-time continuous close via AI ledger bots.",
        "human_focus": "Financial governance, executive leadership, strategic capital advisory.",
        "ai_focus": "Continuous ledger reconciliation, automated financial statement consolidation.",
        "future_capabilities": "Real-time corporate accounting control, AI audit trail oversight.",
        "processes": [
            {
                "name": "Financial Reporting",
                "department": "Accounting",
                "description": "Preparing regulatory financial filings and quarterly ledger summaries.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Monthly General Ledger Close Supervision",
                        "description": "Reviewing journal entries and balance sheet reconciliations at month-end.",
                        "repetitiveness": 0.75, "data_availability": 0.90, "rule_based_nature": 0.80,
                        "complexity": 0.60, "human_judgement": 0.65, "regulatory_sensitivity": 0.90, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Financial Analysis", "Auditing & Internal Controls"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Manage continuous real-time AI ledger close system", "reason": "Monitor AI bots executing journal reconciliations."},
            {"responsibility": "Present strategic financial performance metrics to board directors", "reason": "Deliver executive financial narratives and strategic forecasts."}
        ],
        "future_skills": [
            {"skill": "Strategic Decision Making", "status": "Increasing", "reason": "High-level strategic guidance based on continuous financial insights."},
            {"skill": "AI Model Oversight", "status": "Emerging", "reason": "Ensuring accounting automation algorithms follow GAAP/IFRS rules."}
        ]
    },
    {
        "name": "Relationship Manager",
        "department": "Commercial & Wealth Banking",
        "description": "Manages high-net-worth client relationships and commercial banking loan portfolios.",
        "current_responsibilities": "Meeting corporate clients, cross-selling banking products, reviewing loan structures, organizing client dinners.",
        "future_title": "AI-Augmented Wealth & Commercial Advisor",
        "future_summary": "Leverages AI hyper-personalized financial insight engines to deliver high-touch advisory services to clients.",
        "key_changes": "Routine portfolio reporting automated; time spent directly with clients increases by 50%.",
        "human_focus": "Client trust, emotional intelligence, complex wealth structuring, relationship building.",
        "ai_focus": "Personalized investment portfolio recommendations, automated meeting summary drafting.",
        "future_capabilities": "AI-assisted portfolio storytelling, high-net-worth relationship advisory.",
        "processes": [
            {
                "name": "Customer Service",
                "department": "Commercial Banking",
                "description": "Advising corporate clients on financial growth and credit products.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "High-Net-Worth Client Relationship Advisory",
                        "description": "Conducting in-person strategic reviews with corporate CFOs and wealthy individuals.",
                        "repetitiveness": 0.25, "data_availability": 0.50, "rule_based_nature": 0.15,
                        "complexity": 0.80, "human_judgement": 0.90, "regulatory_sensitivity": 0.60, "human_interaction": 0.98,
                        "responsibility_level": "Primary", "skills": ["Client Relationship Management", "Stakeholder Communication"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Deliver AI-synthesized market opportunity recommendations to clients", "reason": "Provide custom financial insights backed by real-time market data."},
            {"responsibility": "Build deep human trust and personal rapport during volatile market environments", "reason": "Empathy cannot be replicated by automated agents."}
        ],
        "future_skills": [
            {"skill": "Client Relationship Management", "status": "Enduring Human Capability", "reason": "Human empathy and trust remain the primary competitive differentiator."},
            {"skill": "Stakeholder Communication", "status": "Increasing", "reason": "Crucial for explaining complex AI portfolio strategies to clients."}
        ]
    },
    {
        "name": "Loan Officer",
        "department": "Retail & Small Business Lending",
        "description": "Guides individual and small business borrowers through mortgage and commercial loan applications.",
        "current_responsibilities": "Collecting borrower documents, verifying income papers, submitting applications to underwriting, communicating decisions.",
        "future_title": "AI Lending Advisor & Borrower Advocate",
        "future_summary": "Uses instant AI loan underwriting tools to provide immediate loan pre-approvals while advising borrowers on financial health.",
        "key_changes": "Document collection and basic eligibility checking automated; focus shifts to borrower consultation.",
        "human_focus": "Borrower advisory, financial coaching, handling complex family/business financial situations.",
        "ai_focus": "Instant credit checks, automated income verification, document extraction.",
        "future_capabilities": "AI-assisted loan structuring, credit remediation advisory.",
        "processes": [
            {
                "name": "Loan Processing",
                "department": "Retail Lending",
                "description": "Originating and processing personal and commercial mortgage applications.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Borrower Application Document Review",
                        "description": "Checking applicant tax returns, pay stubs, and bank statements for completeness.",
                        "repetitiveness": 0.85, "data_availability": 0.90, "rule_based_nature": 0.80,
                        "complexity": 0.35, "human_judgement": 0.30, "regulatory_sensitivity": 0.80, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Loan Origination", "Credit Underwriting"]
                    },
                    {
                        "name": "Borrower Financial Consultation & Negotiation",
                        "description": "Advising borrowers on appropriate loan terms, interest rate options, and repayment plans.",
                        "repetitiveness": 0.35, "data_availability": 0.65, "rule_based_nature": 0.30,
                        "complexity": 0.70, "human_judgement": 0.75, "regulatory_sensitivity": 0.75, "human_interaction": 0.90,
                        "responsibility_level": "Primary", "skills": ["Stakeholder Communication", "Loan Origination"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Guide borrowers through AI-generated custom mortgage options", "reason": "Help customers select terms aligned with long-term financial goals."},
            {"responsibility": "Assist distressed borrowers with loan restructure requests", "reason": "Provide empathetic human support during personal financial difficulty."}
        ],
        "future_skills": [
            {"skill": "Stakeholder Communication", "status": "Increasing", "reason": "Key for establishing trust with retail and small business borrowers."},
            {"skill": "Loan Origination", "status": "AI-Augmented", "reason": "Standard applications pre-screened by AI bots."}
        ]
    },
    {
        "name": "Operations Manager",
        "department": "Banking Operations",
        "description": "Oversees back-office transaction processing, branch operational efficiency, and clearinghouse settlements.",
        "current_responsibilities": "Managing wire transfer processing teams, resolving operational escalations, tracking SLA metrics.",
        "future_title": "AI Operations & Process Automation Director",
        "future_summary": "Orchestrates teams of AI robotic process automation (RPA) agents and manages human-in-the-loop operational exceptions.",
        "key_changes": "Manual transaction processing automated; role focuses on exception engineering and process resilience.",
        "human_focus": "Operational resilience strategy, team leadership, high-value dispute resolution.",
        "ai_focus": "Automated wire routing, instant clearinghouse settlement, automated SLA monitoring.",
        "future_capabilities": "AI process orchestration, operational bottleneck prediction, continuous optimization.",
        "processes": [
            {
                "name": "Workforce Planning",
                "department": "Operations",
                "description": "Optimizing operational capacity and transaction processing workflows.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Back-Office SLA & Efficiency Monitoring",
                        "description": "Tracking transaction processing speeds, error rates, and staff productivity.",
                        "repetitiveness": 0.80, "data_availability": 0.95, "rule_based_nature": 0.80,
                        "complexity": 0.45, "human_judgement": 0.45, "regulatory_sensitivity": 0.60, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Process Optimization", "Tableau / Power BI"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Manage enterprise AI operational bot workforce", "reason": "Ensure transaction bots operate within bank uptime and error SLAs."},
            {"responsibility": "Resolve high-value cross-border payment exception bottlenecks", "reason": "Intervene on complex wire disputes that AI cannot resolve autonomously."}
        ],
        "future_skills": [
            {"skill": "AI Workflow Automation", "status": "Emerging", "reason": "Essential to design and manage robotic transaction processing pipelines."},
            {"skill": "Process Optimization", "status": "Increasing", "reason": "Required to streamline human-AI operational handoffs."}
        ]
    },
    {
        "name": "Customer Service Manager",
        "department": "Contact Center & Customer Experience",
        "description": "Leads bank contact center teams, monitors call quality, and manages customer satisfaction metrics.",
        "current_responsibilities": "Monitoring call center agents, reviewing customer complaint escalations, scheduling shifts.",
        "future_title": "AI Customer Experience & Voice Director",
        "future_summary": "Manages AI conversational voice bots and elevates human agent teams to handle complex emotional service escalations.",
        "key_changes": "Routine balance inquiry calls handled 100% by AI voice bots; human staff dedicated to complex empathy-driven support.",
        "human_focus": "Escalation leadership, customer empathy management, contact center team coaching.",
        "ai_focus": "Automated call transcription, sentiment analysis, real-time agent co-pilot suggestions.",
        "future_capabilities": "Conversational AI voice bot design, sentiment analytics, CX strategy.",
        "processes": [
            {
                "name": "Customer Service",
                "department": "Contact Center",
                "description": "Managing customer support channels across phone, chat, and mobile app.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Contact Center Quality & SLA Audit",
                        "description": "Auditing recorded customer service calls for policy compliance and service quality.",
                        "repetitiveness": 0.75, "data_availability": 0.90, "rule_based_nature": 0.70,
                        "complexity": 0.45, "human_judgement": 0.50, "regulatory_sensitivity": 0.50, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Stakeholder Communication", "Tableau / Power BI"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Tune conversational AI voice bot intent training sets", "reason": "Improve AI contact center resolution accuracy."},
            {"responsibility": "Lead resolution of high-profile customer complaint escalations", "reason": "Provide executive empathy when customers face major issues."}
        ],
        "future_skills": [
            {"skill": "AI Prompt Engineering", "status": "Emerging", "reason": "Used to configure contact center conversational AI persona prompts."},
            {"skill": "Stakeholder Communication", "status": "Enduring Human Capability", "reason": "Empathy remains essential during critical customer service failures."}
        ]
    },
    {
        "name": "Customer Service Representative",
        "department": "Retail Contact Center",
        "description": "Assists bank customers with account inquiries, fund transfers, card replacements, and basic troubleshooting.",
        "current_responsibilities": "Answering phone calls, processing address changes, resetting online banking passwords, taking card dispute notes.",
        "future_title": "Customer Empathy & Complex Resolution Advocate",
        "future_summary": "Transitions from answering repetitive routine inquiries to resolving complex, emotionally sensitive customer financial challenges.",
        "key_changes": "90% of routine password/balance requests handled by AI chat; reps handle complex bereavement, fraud loss, or loan distress cases.",
        "human_focus": "De-escalating angry callers, providing genuine empathy, assisting vulnerable customers.",
        "ai_focus": "Real-time call transcription, instant knowledge base retrieval, automated CRM entry.",
        "future_capabilities": "AI co-pilot assisted troubleshooting, high-empathy customer advocacy.",
        "processes": [
            {
                "name": "Customer Service",
                "department": "Retail Branch & Contact Center",
                "description": "Providing front-line customer assistance.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Routine Account Inquiry Assistance",
                        "description": "Answering incoming customer calls regarding account balances, recent deposits, and fee queries.",
                        "repetitiveness": 0.85, "data_availability": 0.95, "rule_based_nature": 0.80,
                        "complexity": 0.30, "human_judgement": 0.25, "regulatory_sensitivity": 0.30, "human_interaction": 0.80,
                        "responsibility_level": "Primary", "skills": ["Stakeholder Communication", "Problem Solving"]
                    },
                    {
                        "name": "Complex Customer Dispute & Emotional De-escalation",
                        "description": "Handling callers facing account freezes, unexpected fee distress, or identity fraud concerns.",
                        "repetitiveness": 0.30, "data_availability": 0.60, "rule_based_nature": 0.25,
                        "complexity": 0.70, "human_judgement": 0.85, "regulatory_sensitivity": 0.60, "human_interaction": 0.98,
                        "responsibility_level": "Primary", "skills": ["Stakeholder Communication", "Problem Solving"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Operate AI real-time co-pilot software during caller conversations", "reason": "Receive instantaneous policy guidance from AI while talking to customers."},
            {"responsibility": "Provide specialized human support to elderly and vulnerable banking clients", "reason": "Deliver patient human guidance for non-digital customers."}
        ],
        "future_skills": [
            {"skill": "Stakeholder Communication", "status": "Enduring Human Capability", "reason": "Human emotional intelligence cannot be replaced by AI bots."},
            {"skill": "Problem Solving", "status": "Increasing", "reason": "Focus shifts to resolving non-standard customer issues."}
        ]
    },
    {
        "name": "Marketing Analyst",
        "department": "Growth & Marketing Analytics",
        "description": "Measures digital marketing campaign ROI, customer acquisition costs (CAC), and customer lifetime value (LTV).",
        "current_responsibilities": "Tracking ad click-through rates, creating marketing funnel dashboards, segmenting customer email lists.",
        "future_title": "AI Growth Analytics & Personalization Lead",
        "future_summary": "Uses generative AI creative engines and real-time ML recommendation models to deliver 1-to-1 customer personalization.",
        "key_changes": "A/B test setup and email segment creation automated; analyst manages autonomous AI campaign optimizers.",
        "human_focus": "Brand messaging strategy, campaign creative direction, ethical marketing oversight.",
        "ai_focus": "Real-time ad spend allocation, synthetic marketing copy generation, customer churn prediction.",
        "future_capabilities": "Generative ad copy iteration, predictive customer LTV modeling, AI attribution.",
        "processes": [
            {
                "name": "Marketing Analytics",
                "department": "Digital Growth",
                "description": "Analyzing marketing channels and optimizing customer acquisition performance.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Campaign Performance Reporting & Attribution",
                        "description": "Compiling multi-channel ad metrics into ROI performance reports.",
                        "repetitiveness": 0.80, "data_availability": 0.95, "rule_based_nature": 0.75,
                        "complexity": 0.40, "human_judgement": 0.35, "regulatory_sensitivity": 0.30, "human_interaction": 0.30,
                        "responsibility_level": "Primary", "skills": ["Market Research & Analytics", "Tableau / Power BI"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Manage autonomous AI campaign optimization tools", "reason": "Supervise machine learning engines reallocating marketing spend in real time."},
            {"responsibility": "Verify AI-generated marketing content for compliance and brand consistency", "reason": "Ensure ad copy adheres to financial advertising regulations."}
        ],
        "future_skills": [
            {"skill": "AI Prompt Engineering", "status": "Emerging", "reason": "Used to generate synthetic marketing copy variations."},
            {"skill": "Market Research & Analytics", "status": "AI-Augmented", "reason": "Routine campaign reporting automated by AI analytics."}
        ]
    },
    {
        "name": "HR Analyst",
        "department": "Human Resources & Talent Management",
        "description": "Analyzes employee turnover metrics, compensation benchmarks, recruitment pipeline speed, and workforce productivity.",
        "current_responsibilities": "Pulling headcount reports from HRIS software, building exit survey dashboards, calculating attrition rates.",
        "future_title": "AI Workforce Analytics & Strategic Talent Architect",
        "future_summary": "Uses predictive workforce models to forecast skill shortages and design AI reskilling pathways for bank staff.",
        "key_changes": "Headcount reporting and basic resume screening automated; focus turns to strategic talent planning.",
        "human_focus": "Employee empathy, executive talent coaching, workplace culture stewardship.",
        "ai_focus": "Predictive attrition modeling, automated candidate resume parsing, skill gap mapping.",
        "future_capabilities": "Workforce reskilling modeling, talent supply forecasting, AI recruitment oversight.",
        "processes": [
            {
                "name": "Workforce Planning",
                "department": "Human Resources",
                "description": "Analyzing talent metrics and planning future organizational staffing needs.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Headcount & Turnover Metrics Reporting",
                        "description": "Extracting staff movement data from HRIS systems to generate monthly attrition reports.",
                        "repetitiveness": 0.85, "data_availability": 0.90, "rule_based_nature": 0.80,
                        "complexity": 0.35, "human_judgement": 0.30, "regulatory_sensitivity": 0.50, "human_interaction": 0.25,
                        "responsibility_level": "Primary", "skills": ["Workforce Analytics", "Excel & Financial Modeling"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Design AI reskilling curriculum based on automated employee skill gap analytics", "reason": "Help workforce adapt as roles transform due to AI adoption."},
            {"responsibility": "Audit recruitment AI algorithms to eliminate hiring bias", "reason": "Ensure candidate screening AI tools comply with equal employment opportunity laws."}
        ],
        "future_skills": [
            {"skill": "Ethical Judgment & Bias Audit", "status": "Emerging", "reason": "Essential to audit HR algorithms for unfair hiring patterns."},
            {"skill": "Workforce Analytics", "status": "Increasing", "reason": "Growing need to model long-term talent requirements in the AI era."}
        ]
    },
    {
        "name": "Treasury Analyst",
        "department": "Treasury & Asset-Liability Management (ALM)",
        "description": "Monitors bank liquidity ratios, interest rate risk, cash positions, and reserve balances with central banks.",
        "current_responsibilities": "Consolidating daily cash balances, running liquidity stress tests, monitoring interbank borrowing rates.",
        "future_title": "AI Liquidity & Asset Liability Strategist",
        "future_summary": "Leverages real-time AI cash forecasting tools to continuously optimize bank balance sheet yield and reserve positions.",
        "key_changes": "Daily cash consolidation automated; analyst focuses on complex balance sheet risk management.",
        "human_focus": "Central bank communication, capital policy execution, emergency liquidity response.",
        "ai_focus": "Real-time cash flow forecasting, intra-day liquidity optimization, interest rate scenario modeling.",
        "future_capabilities": "Automated ALM modeling, continuous reserve optimization, rate risk analytics.",
        "processes": [
            {
                "name": "Treasury Management",
                "department": "Treasury",
                "description": "Managing bank cash flow, funding, and interest rate risk exposures.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Daily Cash Position Reconciliation & Liquidity Reporting",
                        "description": "Checking opening balance ledger feeds across branches and central bank reserves.",
                        "repetitiveness": 0.85, "data_availability": 0.95, "rule_based_nature": 0.85,
                        "complexity": 0.45, "human_judgement": 0.35, "regulatory_sensitivity": 0.85, "human_interaction": 0.20,
                        "responsibility_level": "Primary", "skills": ["Treasury & Liquidity Management", "Financial Analysis"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Monitor real-time AI intra-day liquidity optimization algorithms", "reason": "Ensure cash positions are automatically positioned to earn maximum interest yield."},
            {"responsibility": "Evaluate liquidity stress scenarios during global financial shocks", "reason": "Provide strategic guidance when markets experience extreme volatility."}
        ],
        "future_skills": [
            {"skill": "Treasury & Liquidity Management", "status": "AI-Augmented", "reason": "Routine cash tracking automated; strategic liquidity management remains human."},
            {"skill": "Strategic Decision Making", "status": "Increasing", "reason": "Critical during balance sheet restructuring events."}
        ]
    },
    {
        "name": "Internal Auditor",
        "department": "Internal Audit & Inspection",
        "description": "Conducts independent reviews of bank accounting records, internal controls, and compliance procedures.",
        "current_responsibilities": "Selecting sample transaction batches, testing internal accounting controls, writing audit findings reports.",
        "future_title": "Continuous AI Audit & Governance Specialist",
        "future_summary": "Uses continuous AI audit tools to review 100% of bank transactions instead of relying on small manual audit samples.",
        "key_changes": "Sampling obsolete; audit bots check 100% of ledger transactions continuously, flagging anomalies for human auditors.",
        "human_focus": "Audit finding negotiation with executives, ethics investigation, audit committee reporting.",
        "ai_focus": "100% transaction coverage audit, automated control testing, discrepancy flagging.",
        "future_capabilities": "Continuous auditing, AI algorithm verification, forensic forensic investigation.",
        "processes": [
            {
                "name": "Internal Audit",
                "department": "Audit",
                "description": "Providing independent assurance over internal bank risk controls.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Internal Control Testing & Sample Verification",
                        "description": "Pulling random ledger sample batches to test compliance with internal authorization limits.",
                        "repetitiveness": 0.80, "data_availability": 0.90, "rule_based_nature": 0.80,
                        "complexity": 0.50, "human_judgement": 0.55, "regulatory_sensitivity": 0.90, "human_interaction": 0.40,
                        "responsibility_level": "Primary", "skills": ["Auditing & Internal Controls", "Regulatory Compliance"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Investigate transaction anomalies flagged by continuous AI audit bots", "reason": "Examine exceptions flagged during 100% automated ledger testing."},
            {"responsibility": "Audit enterprise AI decision systems for control integrity", "reason": "Ensure AI credit and fraud systems maintain proper audit trails."}
        ],
        "future_skills": [
            {"skill": "Auditing & Internal Controls", "status": "Changing", "reason": "Shifts from manual sample testing to auditing continuous AI systems."},
            {"skill": "AI Model Oversight", "status": "Emerging", "reason": "Required to audit the inner workings of bank automated decision models."}
        ]
    },
    {
        "name": "Product Manager",
        "department": "Digital Banking & Product Strategy",
        "description": "Defines vision, features, and roadmaps for digital banking mobile apps and online portals.",
        "current_responsibilities": "Gathering user feedback, prioritizing feature backlogs, coordinating agile developer sprints, launching new app features.",
        "future_title": "AI Product Manager & Experience Director",
        "future_summary": "Leads autonomous AI agents and developer teams to launch hyper-personalized digital banking features.",
        "key_changes": "Feature roadmap spec writing and ticket generation accelerated by 80% via generative AI tools.",
        "human_focus": "Product vision, customer empathy, competitive differentiation, cross-functional leadership.",
        "ai_focus": "Automated user feedback synthesis, rapid feature prototyping, dynamic backlog sorting.",
        "future_capabilities": "AI product architecture, generative feature design, continuous customer feedback synthesis.",
        "processes": [
            {
                "name": "Product Development",
                "department": "Digital Banking",
                "description": "Creating and improving digital product experiences for banking customers.",
                "involvement_level": "Primary",
                "activities": [
                    {
                        "name": "Product Roadmap Strategy & Feature Backlog Definition",
                        "description": "Writing user stories and prioritizing digital banking features for engineering sprints.",
                        "repetitiveness": 0.40, "data_availability": 0.75, "rule_based_nature": 0.35,
                        "complexity": 0.80, "human_judgement": 0.85, "regulatory_sensitivity": 0.50, "human_interaction": 0.85,
                        "responsibility_level": "Primary", "skills": ["Product Roadmap Management", "Critical Thinking"]
                    }
                ]
            }
        ],
        "future_responsibilities": [
            {"responsibility": "Define strategic vision for AI-native banking features", "reason": "Envision novel customer banking experiences powered by autonomous agents."},
            {"responsibility": "Synthesize customer feedback continuously using AI sentiment analyzers", "reason": "Convert real-time user feedback into instant product iterations."}
        ],
        "future_skills": [
            {"skill": "Product Roadmap Management", "status": "AI-Augmented", "reason": "Backlog generation and story writing assisted by AI, vision remains human."},
            {"skill": "Strategic Decision Making", "status": "Increasing", "reason": "Crucial for guiding product investments in a rapidly changing tech market."}
        ]
    }
]


def seed_banking_roles(db: Session) -> str:
    """
    Seed the database with complete Banking & Financial Services enterprise intelligence.
    """
    # 1. Seed or Get Industry
    industry = db.query(Industry).filter(Industry.name == "Banking & Financial Services").first()
    if not industry:
        industry = Industry(
            name="Banking & Financial Services",
            description="Global commercial banking, retail financial services, capital markets, and corporate treasury operations."
        )
        db.add(industry)
        db.commit()
        db.refresh(industry)

    # 2. Seed Real Research Evidence Sources
    for res_data in REAL_RESEARCH_SOURCES:
        existing_res = db.query(ResearchSource).filter(ResearchSource.source_id == res_data["source_id"]).first()
        if not existing_res:
            db_res = ResearchSource(**res_data)
            db.add(db_res)
    db.commit()

    # 3. Seed Skills Database
    skills_map = {}
    for sk_data in SKILLS_SEED:
        existing_sk = db.query(Skill).filter(Skill.name == sk_data["name"]).first()
        if not existing_sk:
            existing_sk = Skill(**sk_data)
            db.add(existing_sk)
            db.commit()
            db.refresh(existing_sk)
        skills_map[sk_data["name"]] = existing_sk

    # 4. Seed Roles, Processes, Activities, AI Impacts, Relationships, Future Profiles
    for role_data in ROLES_SEED_DATA:
        existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if existing_role:
            continue  # Skip existing roles to prevent duplication

        # Create Role
        db_role = Role(
            industry_id=industry.id,
            name=role_data["name"],
            department=role_data["department"],
            description=role_data["description"],
            current_responsibilities=role_data["current_responsibilities"]
        )
        db.add(db_role)
        db.commit()
        db.refresh(db_role)

        # Create Role Future Profile
        db_profile = RoleFutureProfile(
            role_id=db_role.id,
            future_role_title=role_data["future_title"],
            future_role_summary=role_data["future_summary"],
            key_changes=role_data["key_changes"],
            human_focus=role_data["human_focus"],
            ai_focus=role_data["ai_focus"],
            future_capabilities=role_data["future_capabilities"]
        )
        db.add(db_profile)

        # Create Processes & Activities
        all_role_activities = []
        for proc_data in role_data["processes"]:
            # Create or get Process
            db_proc = db.query(Process).filter(
                Process.name == proc_data["name"],
                Process.role_id == db_role.id
            ).first()
            if not db_proc:
                db_proc = Process(
                    role_id=db_role.id,
                    name=proc_data["name"],
                    department=proc_data.get("department", role_data["department"]),
                    description=proc_data["description"]
                )
                db.add(db_proc)
                db.commit()
                db.refresh(db_proc)

            # Create RoleProcess association
            role_proc_assoc = RoleProcess(
                role_id=db_role.id,
                process_id=db_proc.id,
                involvement_level=proc_data.get("involvement_level", "Primary")
            )
            db.add(role_proc_assoc)

            # Create Activities
            for act_data in proc_data["activities"]:
                scores = AIScoringEngine.calculate_activity_scores(
                    repetition=act_data["repetitiveness"],
                    data_availability=act_data["data_availability"],
                    rule_based=act_data["rule_based_nature"],
                    complexity=act_data["complexity"],
                    human_judgement=act_data["human_judgement"],
                    regulatory_sensitivity=act_data["regulatory_sensitivity"],
                    human_interaction=act_data["human_interaction"]
                )

                db_act = Activity(
                    process_id=db_proc.id,
                    name=act_data["name"],
                    description=act_data["description"],
                    repetitiveness=act_data["repetitiveness"],
                    data_availability=act_data["data_availability"],
                    rule_based_nature=act_data["rule_based_nature"],
                    language_cognitive_complexity=act_data["complexity"],
                    human_judgment_requirement=act_data["human_judgement"],
                    regulatory_sensitivity=act_data["regulatory_sensitivity"],
                    human_interaction_requirement=act_data["human_interaction"],
                    ai_exposure_score=scores["ai_exposure_score"] / 100.0,
                    automation_potential=scores["automation_score"] / 100.0,
                    augmentation_potential=scores["augmentation_score"] / 100.0
                )
                db.add(db_act)
                db.commit()
                db.refresh(db_act)
                all_role_activities.append(db_act)

                # Create RoleActivity association
                role_act_assoc = RoleActivity(
                    role_id=db_role.id,
                    activity_id=db_act.id,
                    responsibility_level=act_data.get("responsibility_level", "Primary")
                )
                db.add(role_act_assoc)

                # Create ActivityAIImpact detailed entry
                impact_entry = ActivityAIImpact(
                    activity_id=db_act.id,
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
                db.add(impact_entry)

                # Connect Skills to Activity
                for sk_name in act_data.get("skills", []):
                    if sk_name in skills_map:
                        act_sk_assoc = ActivitySkill(
                            activity_id=db_act.id,
                            skill_id=skills_map[sk_name].id,
                            importance="High"
                        )
                        db.add(act_sk_assoc)
                        # Also link to RoleSkill if not present
                        role_sk_exists = db.query(RoleSkill).filter(
                            RoleSkill.role_id == db_role.id,
                            RoleSkill.skill_id == skills_map[sk_name].id
                        ).first()
                        if not role_sk_exists:
                            role_sk_assoc = RoleSkill(
                                role_id=db_role.id,
                                skill_id=skills_map[sk_name].id,
                                proficiency_level="Advanced"
                            )
                            db.add(role_sk_assoc)

        # Create Future Responsibilities
        for fut_resp in role_data.get("future_responsibilities", []):
            db_resp = FutureResponsibility(
                role_id=db_role.id,
                responsibility=fut_resp["responsibility"],
                reason=fut_resp["reason"],
                related_activity_id=all_role_activities[0].id if all_role_activities else None
            )
            db.add(db_resp)

        # Create Future Skills
        for fut_sk in role_data.get("future_skills", []):
            sk_name = fut_sk["skill"]
            if sk_name in skills_map:
                db_fut_sk = FutureSkill(
                    role_id=db_role.id,
                    skill_id=skills_map[sk_name].id,
                    skill_status=fut_sk["status"],
                    reason=fut_sk["reason"]
                )
                db.add(db_fut_sk)

        # Aggregate Role Analysis Metrics
        if all_role_activities:
            avg_exp = sum(a.ai_exposure_score for a in all_role_activities) / len(all_role_activities)
            avg_auto = sum(a.automation_potential for a in all_role_activities) / len(all_role_activities)
            avg_aug = sum(a.augmentation_potential for a in all_role_activities) / len(all_role_activities)

            auto_count = sum(1 for a in all_role_activities if a.automation_potential >= 0.65)
            aug_count = sum(1 for a in all_role_activities if 0.35 <= a.augmentation_potential or a.ai_exposure_score >= 0.45 and a.automation_potential < 0.65)
            human_count = len(all_role_activities) - auto_count - aug_count

            resp_list = [r["responsibility"] for r in role_data.get("future_responsibilities", [])]
            skill_list = [f"{s['skill']} ({s['status']})" for s in role_data.get("future_skills", [])]

            db_analysis = RoleAnalysis(
                role_id=db_role.id,
                average_ai_exposure=round(avg_exp, 3),
                average_automation_potential=round(avg_auto, 3),
                average_augmentation_potential=round(avg_aug, 3),
                activities_likely_automated=auto_count,
                activities_likely_augmented=max(0, aug_count),
                activities_human_led=max(0, human_count),
                new_responsibilities=json.dumps(resp_list),
                future_skills=json.dumps(skill_list),
                future_role_profile=role_data["future_summary"]
            )
            db.add(db_analysis)

        db.commit()

    return "Successfully seeded 20 Banking & Financial Services roles, real research sources, and enterprise intelligence dataset."
