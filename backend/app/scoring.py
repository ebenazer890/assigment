"""
Deterministic and Explainable AI Impact Scoring Engine
"""
from typing import Dict, List, Tuple

class AIScoringEngine:
    """
    Repeatable scoring methodology for activity and role level AI impact.
    Outputs scores on a 0 - 100 scale.
    """

    @staticmethod
    def calculate_activity_scores(
        repetition: float,
        data_availability: float,
        rule_based: float,
        complexity: float,
        human_judgement: float,
        regulatory_sensitivity: float,
        human_interaction: float
    ) -> Dict[str, float]:
        """
        Calculate scores on 0-100 scale based on inputs.
        Accepts inputs either as 0-1 or 0-100.
        """
        # Normalize inputs to 0-100 scale
        r = repetition * 100 if repetition <= 1.0 else repetition
        d = data_availability * 100 if data_availability <= 1.0 else data_availability
        rb = rule_based * 100 if rule_based <= 1.0 else rule_based
        c = complexity * 100 if complexity <= 1.0 else complexity
        j = human_judgement * 100 if human_judgement <= 1.0 else human_judgement
        reg = regulatory_sensitivity * 100 if regulatory_sensitivity <= 1.0 else regulatory_sensitivity
        hi = human_interaction * 100 if human_interaction <= 1.0 else human_interaction

        # Automation Score (0-100)
        automation_score = (
            0.35 * r +
            0.30 * rb +
            0.25 * d +
            0.10 * max(0.0, 100.0 - j)
        )

        # Augmentation Score (0-100)
        augmentation_score = (
            0.30 * c +
            0.25 * d +
            0.20 * j +
            0.15 * rb +
            0.10 * r
        )

        # Overall AI Exposure Score (0-100)
        ai_exposure_score = (
            0.30 * r +
            0.25 * d +
            0.20 * rb +
            0.10 * c +
            0.10 * max(0.0, 100.0 - j) +
            0.05 * max(0.0, 100.0 - reg)
        )

        # Clamp all scores strictly within 0-100
        automation_score = min(100.0, max(0.0, automation_score))
        augmentation_score = min(100.0, max(0.0, augmentation_score))
        ai_exposure_score = min(100.0, max(0.0, ai_exposure_score))

        # Classification
        if automation_score >= 65.0 and j < 60.0:
            category = "Mostly Automated"
        elif ai_exposure_score >= 45.0 or augmentation_score >= 50.0:
            category = "AI Augmented"
        else:
            category = "Human Led"

        # Generate Explainable Reasoning
        reasoning = AIScoringEngine._generate_explainability(
            category, automation_score, augmentation_score, ai_exposure_score,
            r, d, rb, c, j, reg, hi
        )

        return {
            "repetition_score": round(r, 1),
            "data_availability_score": round(d, 1),
            "rule_based_nature": round(rb, 1),
            "complexity_score": round(c, 1),
            "human_judgement_score": round(j, 1),
            "regulatory_sensitivity_score": round(reg, 1),
            "human_interaction_score": round(hi, 1),
            "automation_score": round(automation_score, 1),
            "augmentation_score": round(augmentation_score, 1),
            "ai_exposure_score": round(ai_exposure_score, 1),
            "impact_category": category,
            "reasoning": reasoning
        }

    @staticmethod
    def _generate_explainability(
        category: str, auto: float, aug: float, exp: float,
        r: float, d: float, rb: float, c: float, j: float, reg: float, hi: float
    ) -> str:
        drivers = []
        if r >= 70:
            drivers.append(f"high repetition ({r:.0f}/100)")
        if d >= 70:
            drivers.append(f"structured data availability ({d:.0f}/100)")
        if rb >= 70:
            drivers.append(f"rule-based workflow ({rb:.0f}/100)")
        if j >= 70:
            drivers.append(f"critical human judgment requirement ({j:.0f}/100)")
        if reg >= 70:
            drivers.append(f"high regulatory sensitivity ({reg:.0f}/100)")
        if hi >= 70:
            drivers.append(f"intensive stakeholder interaction ({hi:.0f}/100)")

        drivers_str = ", ".join(drivers) if drivers else "balanced activity characteristics"

        if category == "Mostly Automated":
            return f"Activity is mostly automated due to {drivers_str}. Routine execution and standardized inputs allow AI algorithms to execute tasks with minimal human intervention."
        elif category == "AI Augmented":
            return f"Activity is AI-augmented due to {drivers_str}. AI copilots synthesize data and draft analyses while human experts validate outputs and retain final decision accountability."
        else:
            return f"Activity remains human-led due to {drivers_str}. Complex reasoning, ethical accountability, and stakeholder nuances require deep human oversight."
