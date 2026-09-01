# AI Exposure & Scoring Methodology Documentation

## Overview

The **Role-Level AI Intelligence Platform** uses a deterministic, repeatable, and explainable scoring methodology to quantify AI impact on organizational roles in Banking & Financial Services.

Rather than relying on black-box LLM prompts to guess impact percentages, the platform evaluates granular activity characteristics against a mathematical formula to compute scores on a **0–100 scale**.

---

## 🧮 AI Exposure Formula

For each activity, 7 normalized input dimensions are evaluated:

1. **`repetition_score` ($R$)**: Degree of routine, standardized repetition (0–100).
2. **`data_availability_score` ($D$)**: Availability of structured digital data (0–100).
3. **`rule_based_nature` ($RB$)**: Extent to which tasks follow fixed rules/code (0–100).
4. **`complexity_score` ($C$)**: Cognitive and linguistic complexity (0–100).
5. **`human_judgement_score` ($J$)**: Requirement for high-stakes human discretion (0–100).
6. **`regulatory_sensitivity_score` ($REG$)**: Regulatory compliance/audit sensitivity (0–100).
7. **`human_interaction_score` ($INT$)**: Requirement for interpersonal empathy/negotiation (0–100).

---

### Formula Equations

$$
\text{Automation Score} = 0.35 \times R + 0.30 \times RB + 0.25 \times D + 0.10 \times (100 - J)
$$

$$
\text{Augmentation Score} = 0.30 \times C + 0.25 \times D + 0.20 \times J + 0.15 \times RB + 0.10 \times R
$$

$$
\text{AI Exposure Score} = 0.30 \times R + 0.25 \times D + 0.20 \times RB + 0.10 \times C + 0.10 \times (100 - J) + 0.05 \times (100 - REG)
$$

All scores are clamped within $[0.0, 100.0]$.

---

## 🏷 Classification Categories

Each activity is assigned an impact category based on score boundaries:

- **`Mostly Automated`**: $\text{Automation Score} \ge 65.0$ AND $\text{Human Judgment} < 60.0$.
  - *Example*: Routine data extraction, SQL script execution, invoice matching, balance reporting.
- **`AI Augmented`**: $\text{AI Exposure Score} \ge 45.0$ OR $\text{Augmentation Score} \ge 50.0$.
  - *Example*: Exploratory data analysis, financial statement spreading, risk stress testing, ad campaign analytics.
- **`Human Led`**: Activities where human discretion, empathy, or regulatory accountability dominates.
  - *Example*: Stakeholder presentations, client negotiations, complex fraud investigations, executive leadership.

---

## 📊 Role-Level Score Aggregation

The role-level **Overall AI Exposure Score** is calculated as the arithmetic mean of its underlying activities:

$$
\text{Role AI Exposure} = \frac{1}{N} \sum_{i=1}^{N} \text{Activity AI Exposure}_i
$$

Where $N$ is the number of activities performed by the role.

---

## 🔍 Qualitative Explainability Engine

For every activity and role, the system dynamically generates qualitative explainability statements identifying the exact factors driving the score:

- *Automated Example*: *"Activity is mostly automated due to high repetition (85/100) and structured data availability (95/100). Routine execution allows AI scripts to execute tasks with minimal human intervention."*
- *Augmented Example*: *"Activity is AI-augmented due to cognitive complexity (75/100) and structured data availability (85/100). AI copilots draft analyses while human experts validate outputs."*
- *Human Led Example*: *"Activity remains human-led due to intensive stakeholder interaction (90/100) and critical human judgment requirement (90/100)."*
