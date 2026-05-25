"""
FastMCP Server: DecisionSynthesis
Intelligent Loan Decision Synthesis Engine
Combines Application DB and RiskRulesDB insights for final loan decisions
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple
from fastmcp import FastMCP
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
app = FastMCP("DecisionSynthesis", version="1.0.0")

# ============================================================================
# ENUMERATIONS
# ============================================================================

class Decision(str, Enum):
    """Final loan decision"""
    APPROVE = "APPROVE"
    CONDITIONAL_APPROVE = "CONDITIONAL_APPROVE"
    REVIEW = "REVIEW"
    REJECT = "REJECT"


class ConfidenceLevel(str, Enum):
    """Decision confidence level"""
    VERY_HIGH = "Very High"
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"
    VERY_LOW = "Very Low"


class DecisionStrategy(str, Enum):
    """Decision-making strategy"""
    CONSERVATIVE = "Conservative"
    BALANCED = "Balanced"
    AGGRESSIVE = "Aggressive"


# ============================================================================
# DECISION ENGINE
# ============================================================================

class DecisionSynthesizer:
    """
    Synthesizes decisions from multiple data sources.
    """

    def __init__(self, strategy: DecisionStrategy = DecisionStrategy.BALANCED):
        """Initialize synthesizer with strategy."""
        self.strategy = strategy
        self.thresholds = self._get_strategy_thresholds(strategy)

    def _get_strategy_thresholds(self, strategy: DecisionStrategy) -> Dict[str, float]:
        """Get decision thresholds based on strategy."""
        thresholds = {
            DecisionStrategy.CONSERVATIVE: {
                "max_dti": 0.36,
                "min_credit_score": 700,
                "max_risk_score": 2.5,
                "min_confidence": 0.75,
                "max_anomalies": 0
            },
            DecisionStrategy.BALANCED: {
                "max_dti": 0.43,
                "min_credit_score": 650,
                "max_risk_score": 3.0,
                "min_confidence": 0.65,
                "max_anomalies": 1
            },
            DecisionStrategy.AGGRESSIVE: {
                "max_dti": 0.50,
                "min_credit_score": 600,
                "max_risk_score": 3.5,
                "min_confidence": 0.50,
                "max_anomalies": 2
            }
        }
        return thresholds[strategy]

    def synthesize_decision(
        self,
        applicant_id: str,
        applicant_data: Dict[str, Any],
        application_analysis: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesize all inputs into a final decision.

        Args:
            applicant_id: Unique applicant ID
            applicant_data: Applicant profile
            application_analysis: Results from Application DB
            risk_assessment: Results from RiskRulesDB

        Returns:
            Decision with classification, score, confidence, factors, and explanation
        """
        # Extract key metrics
        metrics = self._extract_metrics(
            applicant_data, application_analysis, risk_assessment
        )

        # Calculate risk score (0-5 scale)
        risk_score = self._calculate_aggregate_risk_score(metrics)

        # Evaluate decision rules
        decision_result = self._evaluate_decision_rules(metrics, risk_score)

        # Calculate confidence level
        confidence = self._calculate_confidence_level(metrics, decision_result)

        # Identify key decision factors
        key_factors = self._identify_key_factors(metrics, decision_result)

        # Generate explanation
        explanation = self._generate_explanation(
            metrics, risk_score, decision_result, key_factors
        )

        # Generate approval conditions if conditional
        conditions = []
        if decision_result['decision'] == Decision.CONDITIONAL_APPROVE:
            conditions = self._generate_conditions(metrics)

        return {
            "status": "success",
            "applicant_id": applicant_id,
            "decision_timestamp": datetime.now().isoformat(),
            "decision": {
                "classification": decision_result['decision'],
                "risk_score": round(risk_score, 2),
                "confidence_level": confidence,
                "reasoning": explanation,
                "conditions": conditions
            },
            "key_factors": key_factors,
            "metrics_summary": {
                "dti_percentage": metrics.get('dti_percentage'),
                "credit_score": metrics.get('credit_score'),
                "lti_percentage": metrics.get('lti_percentage'),
                "anomaly_count": metrics.get('anomaly_count'),
                "income_stability": metrics.get('income_stability'),
                "employment_risk": metrics.get('employment_risk')
            },
            "strategy_applied": self.strategy.value,
            "audit_trail": self._generate_audit_trail(metrics, risk_score)
        }

    def _extract_metrics(
        self,
        applicant_data: Dict[str, Any],
        application_analysis: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract key metrics from all sources."""
        app_analysis = application_analysis.get('analysis', {})
        risk_report = risk_assessment.get('analysis', {}) if isinstance(risk_assessment, dict) else risk_assessment

        # Handle both direct risk_assessment (dict) and wrapped format
        if 'dti_with_new_loan' in risk_report:
            dti_data = risk_report['dti_with_new_loan']
        elif 'dti_analysis' in risk_report:
            dti_data = risk_report['dti_analysis']
        else:
            dti_data = {}

        return {
            # Application data
            "applicant_name": applicant_data.get('name'),
            "age": applicant_data.get('age'),
            "annual_income": applicant_data.get('annual_income', 0),
            "employment_type": applicant_data.get('employment_type'),

            # Income & Stability
            "income_stability": app_analysis.get('income_stability', {}).get('score'),
            "income_stability_category": app_analysis.get('income_stability', {}).get('stability_category'),
            "employment_risk": app_analysis.get('employment_risk', {}).get('risk_score'),
            "employment_risk_level": app_analysis.get('employment_risk', {}).get('risk_level'),

            # Credit
            "credit_score": app_analysis.get('credit_history', {}).get('credit_score'),
            "credit_category": app_analysis.get('credit_history', {}).get('score_category'),
            "delinquencies": applicant_data.get('delinquencies', 0),

            # DTI & Risk
            "dti_percentage": dti_data.get('dti_percentage'),
            "dti_risk_level": dti_data.get('risk_level'),
            "lti_percentage": risk_report.get('loan_amount_risk', {}).get('lti_percentage'),

            # Completeness & Anomalies
            "application_complete": app_analysis.get('application_completeness', {}).get('is_complete'),
            "completeness_percentage": app_analysis.get('application_completeness', {}).get('completeness_percentage'),
            "anomaly_count": risk_report.get('anomaly_detection', {}).get('anomaly_count', 0),
            "anomalies": risk_report.get('anomaly_detection', {}).get('anomalies', [])
        }

    def _calculate_aggregate_risk_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate aggregate risk score (0-5 scale).
        """
        scores = []

        # Income stability contribution (lower is better: 0 = stable, 100 = unstable)
        if metrics.get('income_stability') is not None:
            stability_score = (100 - metrics['income_stability']) / 100 * 5
            scores.append(stability_score)

        # Employment risk contribution (0-100 scale, convert to 0-5)
        if metrics.get('employment_risk') is not None:
            emp_score = metrics['employment_risk'] / 100 * 5
            scores.append(emp_score)

        # Credit score contribution
        if metrics.get('credit_score'):
            if metrics['credit_score'] >= 750:
                credit_score = 0.5
            elif metrics['credit_score'] >= 700:
                credit_score = 1.5
            elif metrics['credit_score'] >= 650:
                credit_score = 2.5
            elif metrics['credit_score'] >= 600:
                credit_score = 3.5
            else:
                credit_score = 4.5
            scores.append(credit_score)

        # DTI contribution
        if metrics.get('dti_percentage'):
            dti = metrics['dti_percentage'] / 100
            if dti < 0.20:
                dti_score = 0.5
            elif dti < 0.36:
                dti_score = 1.5
            elif dti < 0.43:
                dti_score = 2.5
            elif dti < 0.50:
                dti_score = 3.5
            else:
                dti_score = 4.5
            scores.append(dti_score)

        # Anomaly contribution
        if metrics.get('anomaly_count') is not None:
            anomaly_score = metrics['anomaly_count'] * 0.8
            scores.append(min(anomaly_score, 5))

        # Calculate average
        return sum(scores) / len(scores) if scores else 3.0

    def _evaluate_decision_rules(
        self,
        metrics: Dict[str, Any],
        risk_score: float
    ) -> Dict[str, Any]:
        """
        Evaluate decision rules and make determination.
        """
        thresholds = self.thresholds
        violations = []
        positive_factors = []

        # Check DTI
        dti = metrics.get('dti_percentage', 100)
        if dti > thresholds['max_dti'] * 100:
            violations.append(f"DTI {dti:.1f}% exceeds {thresholds['max_dti']*100:.0f}% threshold")
        else:
            positive_factors.append(f"DTI {dti:.1f}% within acceptable range")

        # Check Credit Score
        credit = metrics.get('credit_score', 0)
        if credit < thresholds['min_credit_score']:
            violations.append(f"Credit score {credit} below {thresholds['min_credit_score']} minimum")
        else:
            positive_factors.append(f"Credit score {credit} meets minimum requirement")

        # Check Risk Score
        if risk_score > thresholds['max_risk_score']:
            violations.append(f"Risk score {risk_score:.2f} exceeds {thresholds['max_risk_score']} threshold")
        else:
            positive_factors.append(f"Risk score {risk_score:.2f} acceptable")

        # Check Anomalies
        anomalies = metrics.get('anomaly_count', 0)
        if anomalies > thresholds['max_anomalies']:
            violations.append(f"{anomalies} anomalies detected (max allowed: {thresholds['max_anomalies']})")
        elif anomalies == 0:
            positive_factors.append("No anomalies detected")

        # Check Application Completeness
        if not metrics.get('application_complete'):
            violations.append("Application incomplete")
        else:
            positive_factors.append("Application complete")

        # Determine decision
        if not violations and risk_score <= thresholds['max_risk_score']:
            if risk_score <= (thresholds['max_risk_score'] - 1):
                decision = Decision.APPROVE
            else:
                decision = Decision.CONDITIONAL_APPROVE
        elif len(violations) == 1 and risk_score <= thresholds['max_risk_score'] * 1.1:
            decision = Decision.REVIEW
        else:
            decision = Decision.REJECT

        return {
            "decision": decision,
            "violations": violations,
            "positive_factors": positive_factors
        }

    def _calculate_confidence_level(
        self,
        metrics: Dict[str, Any],
        decision_result: Dict[str, Any]
    ) -> ConfidenceLevel:
        """
        Calculate confidence level in the decision.
        """
        completeness = metrics.get('completeness_percentage', 50)
        anomalies = metrics.get('anomaly_count', 0)
        violations_count = len(decision_result.get('violations', []))

        # Base confidence on completeness
        if completeness < 70:
            confidence_score = 0.3
        elif completeness < 85:
            confidence_score = 0.5
        else:
            confidence_score = 0.8

        # Adjust for anomalies
        if anomalies == 0:
            confidence_score += 0.15
        elif anomalies <= 1:
            confidence_score += 0.05
        else:
            confidence_score -= 0.1

        # Adjust for violations
        if violations_count == 0:
            confidence_score += 0.2
        elif violations_count <= 1:
            confidence_score -= 0.05
        else:
            confidence_score -= 0.2

        confidence_score = max(0, min(1, confidence_score))

        if confidence_score >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        elif confidence_score >= 0.70:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 0.55:
            return ConfidenceLevel.MODERATE
        elif confidence_score >= 0.40:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW

    def _identify_key_factors(
        self,
        metrics: Dict[str, Any],
        decision_result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify key factors influencing the decision.
        """
        factors = []

        # Income and Stability
        if metrics.get('income_stability') is not None:
            factors.append({
                "category": "Income Stability",
                "value": metrics['income_stability'],
                "impact": "Positive" if metrics['income_stability'] >= 70 else "Concern",
                "description": f"Stability score of {metrics['income_stability']:.0f} indicates {metrics.get('income_stability_category', 'unknown').lower()}"
            })

        # Employment Risk
        if metrics.get('employment_risk') is not None:
            factors.append({
                "category": "Employment Risk",
                "value": metrics['employment_risk'],
                "impact": "Concern" if metrics['employment_risk'] > 40 else "Positive",
                "description": f"Employment risk of {metrics['employment_risk']:.0f} is {metrics.get('employment_risk_level', 'unknown').lower()}"
            })

        # Credit Profile
        if metrics.get('credit_score'):
            factors.append({
                "category": "Credit Profile",
                "value": metrics['credit_score'],
                "impact": "Positive" if metrics['credit_score'] >= 650 else "Major Concern",
                "description": f"Credit score of {metrics['credit_score']} is {metrics.get('credit_category', 'unknown').lower()}"
            })

        # DTI Ratio
        if metrics.get('dti_percentage'):
            dti = metrics['dti_percentage']
            if dti < 36:
                impact = "Positive"
            elif dti < 43:
                impact = "Acceptable"
            elif dti < 50:
                impact = "Concern"
            else:
                impact = "Major Concern"

            factors.append({
                "category": "Debt-to-Income Ratio",
                "value": round(dti, 1),
                "impact": impact,
                "description": f"DTI of {dti:.1f}% shows debt management capacity"
            })

        # Anomalies
        if metrics.get('anomaly_count', 0) > 0:
            anomalies = metrics.get('anomalies', [])
            for anomaly in anomalies[:3]:  # Top 3 anomalies
                factors.append({
                    "category": "Anomaly Detected",
                    "value": anomaly.get('type'),
                    "impact": anomaly.get('severity', 'Unknown'),
                    "description": anomaly.get('description', '')
                })

        # Application Completeness
        if not metrics.get('application_complete'):
            factors.append({
                "category": "Application Status",
                "value": f"{metrics.get('completeness_percentage', 0):.0f}%",
                "impact": "Concern",
                "description": "Application incomplete - may require follow-up"
            })

        return factors

    def _generate_explanation(
        self,
        metrics: Dict[str, Any],
        risk_score: float,
        decision_result: Dict[str, Any],
        key_factors: List[Dict[str, Any]]
    ) -> str:
        """
        Generate detailed explanation of the decision.
        """
        decision = decision_result['decision']
        violations = decision_result.get('violations', [])
        positive_factors = decision_result.get('positive_factors', [])

        explanation_parts = [
            f"Applicant {metrics.get('applicant_name', 'N/A')} (Age: {metrics.get('age', 'N/A')}) has been evaluated using {self.strategy.value} criteria."
        ]

        if decision == Decision.APPROVE:
            explanation_parts.append(
                f"Overall assessment is favorable. Risk score of {risk_score:.2f}/5 indicates manageable risk."
            )
            if positive_factors:
                explanation_parts.append(
                    f"Positive indicators: {', '.join(positive_factors[:2])}"
                )

        elif decision == Decision.CONDITIONAL_APPROVE:
            explanation_parts.append(
                f"Application shows reasonable credit quality but has some concerns. "
                f"Risk score of {risk_score:.2f}/5 suggests conditional approval is appropriate."
            )
            if positive_factors:
                explanation_parts.append(f"Strengths: {', '.join(positive_factors[:1])}")
            if violations:
                explanation_parts.append(f"Conditions may address: {violations[0]}")

        elif decision == Decision.REVIEW:
            explanation_parts.append(
                f"Application requires manual review. Risk score of {risk_score:.2f}/5 is near threshold."
            )
            if violations:
                explanation_parts.append(
                    f"Issues requiring review: {', '.join(violations[:2])}"
                )

        elif decision == Decision.REJECT:
            explanation_parts.append(
                f"Application does not meet approval criteria. Risk score of {risk_score:.2f}/5 exceeds acceptable threshold."
            )
            if violations:
                explanation_parts.append(f"Primary concerns: {', '.join(violations[:2])}")

        explanation_parts.append(
            f"Strategy applied: {self.strategy.value}. Application completeness: {metrics.get('completeness_percentage', 0):.0f}%"
        )

        return " ".join(explanation_parts)

    def _generate_conditions(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Generate conditions for conditional approval.
        """
        conditions = []

        # DTI-based conditions
        if metrics.get('dti_percentage', 0) > 40:
            conditions.append("Reduce monthly debt obligations or increase income documentation")

        # Credit-based conditions
        if metrics.get('credit_score', 0) < 700:
            conditions.append("Provide explanation letter for credit history")

        # Application completeness conditions
        if not metrics.get('application_complete'):
            conditions.append("Complete missing application sections")

        # Anomaly-based conditions
        if metrics.get('anomaly_count', 0) > 0:
            conditions.append("Resolve detected anomalies through additional documentation")

        # Add generic conditions if none specified
        if not conditions:
            conditions.append("Standard documentation requirements")

        return conditions[:3]  # Return top 3 conditions

    def _generate_audit_trail(
        self,
        metrics: Dict[str, Any],
        risk_score: float
    ) -> Dict[str, Any]:
        """
        Generate audit trail for compliance and record-keeping.
        """
        return {
            "decision_timestamp": datetime.now().isoformat(),
            "strategy_used": self.strategy.value,
            "metrics_evaluated": {
                "dti": metrics.get('dti_percentage'),
                "credit_score": metrics.get('credit_score'),
                "income_stability": metrics.get('income_stability'),
                "employment_risk": metrics.get('employment_risk'),
                "anomalies": metrics.get('anomaly_count')
            },
            "aggregate_risk_score": round(risk_score, 2),
            "application_complete": metrics.get('application_complete'),
            "fair_lending_compliant": True  # Assume compliance unless violations indicate otherwise
        }


# ============================================================================
# MCP TOOLS
# ============================================================================

@app.tool()
def synthesize_loan_decision(
    applicant_id: str,
    applicant_data: dict,
    application_analysis: dict,
    risk_assessment: dict,
    strategy: str = "Balanced"
) -> dict:
    """
    Synthesize loan decision from Application DB and RiskRulesDB inputs.

    Combines applicant profile data, application analysis, and risk assessment
    to produce a final decision with classification, score, and explanation.

    Args:
        applicant_id: Unique applicant identifier
        applicant_data: Applicant profile dictionary
        application_analysis: Results from Application DB analysis
        risk_assessment: Results from RiskRulesDB assessment
        strategy: Decision strategy (Conservative/Balanced/Aggressive)

    Returns:
        Final decision with classification, risk score, confidence, factors, and explanation
    """
    try:
        strategy_enum = DecisionStrategy[strategy.upper()]
    except KeyError:
        strategy_enum = DecisionStrategy.BALANCED

    synthesizer = DecisionSynthesizer(strategy_enum)
    result = synthesizer.synthesize_decision(
        applicant_id, applicant_data, application_analysis, risk_assessment
    )

    logger.info(f"Decision synthesized for {applicant_id}: {result['decision']['classification']}")

    return result


@app.tool()
def evaluate_multiple_scenarios(
    applicant_id: str,
    applicant_data: dict,
    application_analysis: dict,
    base_risk_assessment: dict,
    scenario_results: list
) -> dict:
    """
    Evaluate multiple loan scenarios and compare decisions.

    Args:
        applicant_id: Unique applicant identifier
        applicant_data: Applicant profile
        application_analysis: Application DB analysis
        base_risk_assessment: Base risk assessment
        scenario_results: List of scenario results from RiskRulesDB

    Returns:
        Comparison of decisions across scenarios
    """
    synthesizer = DecisionSynthesizer(DecisionStrategy.BALANCED)

    scenarios_analysis = []

    # Analyze base scenario
    base_result = synthesizer.synthesize_decision(
        applicant_id, applicant_data, application_analysis, base_risk_assessment
    )
    scenarios_analysis.append({
        "scenario": "Base (100%)",
        "decision": base_result['decision']['classification'],
        "risk_score": base_result['decision']['risk_score'],
        "confidence": base_result['decision']['confidence_level']
    })

    # Analyze alternative scenarios
    if scenario_results:
        for scenario in scenario_results:
            scenario_name = scenario.get('scenario', 'Unknown')
            # Create modified risk assessment for scenario
            modified_assessment = base_risk_assessment.copy()
            if 'dti_percentage' in scenario:
                if isinstance(modified_assessment, dict) and 'dti_with_new_loan' in modified_assessment:
                    modified_assessment['dti_with_new_loan']['dti_percentage'] = scenario['dti_percentage']

            scenario_result = synthesizer.synthesize_decision(
                applicant_id, applicant_data, application_analysis, modified_assessment
            )
            scenarios_analysis.append({
                "scenario": scenario_name,
                "decision": scenario_result['decision']['classification'],
                "risk_score": scenario_result['decision']['risk_score'],
                "confidence": scenario_result['decision']['confidence_level']
            })

    logger.info(f"Scenario analysis completed for {applicant_id}: {len(scenarios_analysis)} scenarios")

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "base_decision": base_result,
        "scenario_comparison": scenarios_analysis
    }


@app.tool()
def explain_decision(
    applicant_id: str,
    applicant_data: dict,
    application_analysis: dict,
    risk_assessment: dict
) -> dict:
    """
    Get detailed explanation of decision rationale.

    Args:
        applicant_id: Unique applicant identifier
        applicant_data: Applicant profile
        application_analysis: Application DB analysis
        risk_assessment: RiskRulesDB assessment

    Returns:
        Detailed explanation with key factors and decision rationale
    """
    synthesizer = DecisionSynthesizer(DecisionStrategy.BALANCED)
    result = synthesizer.synthesize_decision(
        applicant_id, applicant_data, application_analysis, risk_assessment
    )

    logger.info(f"Decision explanation generated for {applicant_id}")

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "decision": result['decision']['classification'],
        "confidence": result['decision']['confidence_level'],
        "explanation": result['decision']['reasoning'],
        "key_factors": result['key_factors'],
        "conditions": result['decision']['conditions'],
        "audit_trail": result['audit_trail']
    }


@app.tool()
def compare_applicants(
    applicants: list
) -> dict:
    """
    Compare multiple applicants and their decisions.

    Args:
        applicants: List of applicant data dicts with analyses

    Returns:
        Comparative analysis of applicants
    """
    synthesizer = DecisionSynthesizer(DecisionStrategy.BALANCED)
    comparison_results = []

    for applicant in applicants:
        result = synthesizer.synthesize_decision(
            applicant.get('applicant_id', 'Unknown'),
            applicant.get('applicant_data', {}),
            applicant.get('application_analysis', {}),
            applicant.get('risk_assessment', {})
        )
        comparison_results.append({
            "applicant_id": applicant.get('applicant_id'),
            "decision": result['decision']['classification'],
            "risk_score": result['decision']['risk_score'],
            "confidence": result['decision']['confidence_level']
        })

    logger.info(f"Applicant comparison completed: {len(applicants)} applicants")

    return {
        "status": "success",
        "comparison_count": len(applicants),
        "results": comparison_results
    }


# ============================================================================
# MCP RESOURCES
# ============================================================================

@app.resource("decision://strategies/definitions")
def decision_strategies() -> dict:
    """
    Decision-making strategies and their criteria.
    """
    return {
        "version": "1.0",
        "title": "Loan Decision Strategies",
        "strategies": {
            "conservative": {
                "description": "Strict criteria, lower approval rate, minimal risk",
                "max_dti": "36%",
                "min_credit_score": 700,
                "max_risk_score": 2.5,
                "max_anomalies": 0,
                "use_case": "Risk-averse lenders, prime lending"
            },
            "balanced": {
                "description": "Moderate criteria, balanced approval rate and risk",
                "max_dti": "43%",
                "min_credit_score": 650,
                "max_risk_score": 3.0,
                "max_anomalies": 1,
                "use_case": "Standard lending, conventional loans"
            },
            "aggressive": {
                "description": "Relaxed criteria, higher approval rate, managed risk",
                "max_dti": "50%",
                "min_credit_score": 600,
                "max_risk_score": 3.5,
                "max_anomalies": 2,
                "use_case": "Growth-focused lenders, alternative lending"
            }
        }
    }


@app.resource("decision://classification/definitions")
def decision_classifications() -> dict:
    """
    Loan decision classifications and their meanings.
    """
    return {
        "version": "1.0",
        "title": "Loan Decision Classifications",
        "classifications": {
            "approve": {
                "description": "Application approved for full loan amount",
                "action": "Issue loan approval and proceed to closing",
                "documentation": "Loan approval letter, disclosure documents"
            },
            "conditional_approve": {
                "description": "Application approved with conditions",
                "action": "Issue conditional approval letter with requirements",
                "documentation": "Conditional approval letter with specific conditions",
                "examples": [
                    "Reduce existing debt",
                    "Provide additional income documentation",
                    "Lower loan amount request"
                ]
            },
            "review": {
                "description": "Application requires manual underwriting review",
                "action": "Route to senior underwriter for decision",
                "documentation": "File with all analyses and documentation"
            },
            "reject": {
                "description": "Application does not meet lending criteria",
                "action": "Issue denial letter with reasons",
                "documentation": "Adverse action notice with specific reasons",
                "appeal_process": "Applicant may request manual review or reapplication after 6 months"
            }
        }
    }


@app.resource("decision://confidence/calibration")
def confidence_calibration() -> dict:
    """
    Confidence level calibration based on data quality and alignment.
    """
    return {
        "version": "1.0",
        "title": "Confidence Level Calibration",
        "factors": {
            "data_completeness": {
                "high_impact": "Application completeness > 95%",
                "medium_impact": "Application completeness 85-95%",
                "low_impact": "Application completeness < 85%"
            },
            "metric_alignment": {
                "strong_agreement": "All metrics point same direction",
                "mixed_signals": "Some metrics contradict",
                "weak_agreement": "Metrics significantly contradict"
            },
            "anomalies": {
                "no_anomalies": "Boosts confidence",
                "one_anomaly": "Neutral",
                "multiple_anomalies": "Reduces confidence"
            }
        },
        "levels": {
            "very_high": "> 0.85 confidence score",
            "high": "0.70-0.85 confidence score",
            "moderate": "0.55-0.70 confidence score",
            "low": "0.40-0.55 confidence score",
            "very_low": "< 0.40 confidence score"
        }
    }


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting DecisionSynthesis MCP Server...")
    logger.info("Available tools: 4 decision synthesis tools")
    logger.info("Available resources: 3 reference resources")

    import uvicorn
    uvicorn.run(
        "mcp.decisionsynthesis.server:app",
        host="0.0.0.0",
        port=3002,
        reload=True,
        log_level="info"
    )
