"""
FastMCP Server: RiskRulesDB
Financial Risk Evaluation Engine
Evaluates DTI, credit risk, loan amount risk, and detects anomalies
"""

import logging
from datetime import datetime
from typing import Dict, Any, List
from fastmcp import FastMCP
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
app = FastMCP("RiskRulesDB", version="1.0.0")

# ============================================================================
# ENUMERATIONS & CONSTANTS
# ============================================================================

class RiskLevel(str, Enum):
    """Risk level categories"""
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"
    EXTREME = "Extreme"


class AnomalyType(str, Enum):
    """Types of anomalies detected"""
    HIGH_DTI = "High Debt-to-Income Ratio"
    LOW_CREDIT_SCORE = "Low Credit Score"
    INCONSISTENT_INCOME = "Income Inconsistency"
    EXCESSIVE_INQUIRIES = "Excessive Credit Inquiries"
    RECENT_DELINQUENCY = "Recent Delinquency"
    HIGH_UTILIZATION = "High Credit Utilization"
    UNUSUAL_LOAN_REQUEST = "Unusual Loan Amount Request"
    SHORT_TENURE = "Short Employment Tenure"
    POOR_PAYMENT_HISTORY = "Poor Payment History"
    AGE_EMPLOYMENT_MISMATCH = "Age-Employment Mismatch"


# ============================================================================
# RISK CALCULATION FUNCTIONS
# ============================================================================

def calculate_dti_ratio(monthly_income: float, monthly_debt: float) -> Dict[str, Any]:
    """
    Calculate Debt-to-Income (DTI) ratio and assess risk.

    DTI = (Total Monthly Debt / Gross Monthly Income) * 100

    Thresholds:
    - < 36%: Acceptable
    - 36-43%: Higher Risk
    - > 43%: Very High Risk
    """
    if monthly_income <= 0:
        return {
            "dti_ratio": float('inf'),
            "dti_percentage": None,
            "risk_level": RiskLevel.EXTREME,
            "category": "Invalid Income",
            "reasoning": "Monthly income must be positive"
        }

    dti_ratio = monthly_debt / monthly_income
    dti_percentage = dti_ratio * 100

    # Determine risk level
    if dti_percentage < 20:
        risk_level = RiskLevel.VERY_LOW
        category = "Excellent"
    elif dti_percentage < 36:
        risk_level = RiskLevel.LOW
        category = "Good"
    elif dti_percentage < 43:
        risk_level = RiskLevel.MEDIUM
        category = "Acceptable"
    elif dti_percentage < 50:
        risk_level = RiskLevel.HIGH
        category = "High Risk"
    else:
        risk_level = RiskLevel.VERY_HIGH
        category = "Very High Risk"

    return {
        "dti_ratio": round(dti_ratio, 4),
        "dti_percentage": round(dti_percentage, 2),
        "risk_level": risk_level,
        "category": category,
        "acceptable_for_conventional": dti_percentage < 43,
        "acceptable_for_fha": dti_percentage < 50,
        "reasoning": f"DTI of {dti_percentage:.1f}% indicates {category.lower()} debt levels relative to income"
    }


def calculate_credit_score_risk(credit_score: int, delinquencies: int = 0, inquiries: int = 0) -> Dict[str, Any]:
    """
    Calculate credit score risk level with delinquency and inquiry adjustment.
    """
    # Base risk by credit score
    if credit_score >= 750:
        base_risk = RiskLevel.VERY_LOW
        base_risk_score = 5
    elif credit_score >= 700:
        base_risk = RiskLevel.LOW
        base_risk_score = 20
    elif credit_score >= 650:
        base_risk = RiskLevel.MEDIUM
        base_risk_score = 40
    elif credit_score >= 600:
        base_risk = RiskLevel.HIGH
        base_risk_score = 65
    else:
        base_risk = RiskLevel.VERY_HIGH
        base_risk_score = 85

    # Adjust for delinquencies
    delinquency_penalty = delinquencies * 15

    # Adjust for recent inquiries
    inquiry_penalty = min(inquiries * 3, 25)  # Cap at 25 points

    # Calculate adjusted risk score
    adjusted_risk_score = min(100, base_risk_score + delinquency_penalty + inquiry_penalty)

    # Determine final risk level
    if adjusted_risk_score < 20:
        final_risk = RiskLevel.VERY_LOW
    elif adjusted_risk_score < 35:
        final_risk = RiskLevel.LOW
    elif adjusted_risk_score < 50:
        final_risk = RiskLevel.MEDIUM
    elif adjusted_risk_score < 70:
        final_risk = RiskLevel.HIGH
    else:
        final_risk = RiskLevel.VERY_HIGH

    return {
        "credit_score": credit_score,
        "base_risk_level": base_risk,
        "base_risk_score": base_risk_score,
        "delinquencies": delinquencies,
        "delinquency_penalty": delinquency_penalty,
        "recent_inquiries": inquiries,
        "inquiry_penalty": inquiry_penalty,
        "adjusted_risk_score": adjusted_risk_score,
        "final_risk_level": final_risk,
        "category": {
            750: "Excellent",
            700: "Good",
            650: "Fair",
            600: "Poor",
            0: "Very Poor"
        }.get(next(k for k in [750, 700, 650, 600, 0] if credit_score >= k), "Unknown"),
        "reasoning": f"Credit score of {credit_score} ({base_risk}) adjusted for {delinquencies} delinquencies and {inquiries} recent inquiries"
    }


def calculate_loan_amount_risk(
    loan_amount: float,
    annual_income: float,
    property_value: float = None,
    existing_loans: int = 0,
    credit_score: int = 0
) -> Dict[str, Any]:
    """
    Calculate loan amount risk based on multiple factors.

    Metrics:
    - Loan-to-Income (LTI) ratio
    - Loan-to-Value (LTV) ratio
    - Existing debt burden
    """
    # Loan-to-Income ratio (annual basis)
    lti_ratio = (loan_amount / annual_income) if annual_income > 0 else float('inf')
    lti_percentage = lti_ratio * 100

    # Determine LTI risk
    if lti_percentage < 3:
        lti_risk = RiskLevel.VERY_LOW
    elif lti_percentage < 5:
        lti_risk = RiskLevel.LOW
    elif lti_percentage < 8:
        lti_risk = RiskLevel.MEDIUM
    elif lti_percentage < 12:
        lti_risk = RiskLevel.HIGH
    else:
        lti_risk = RiskLevel.VERY_HIGH

    # Loan-to-Value ratio (if property value available)
    ltv_ratio = None
    ltv_percentage = None
    ltv_risk = None

    if property_value and property_value > 0:
        ltv_ratio = (loan_amount / property_value)
        ltv_percentage = ltv_ratio * 100

        if ltv_percentage <= 80:
            ltv_risk = RiskLevel.LOW
        elif ltv_percentage <= 95:
            ltv_risk = RiskLevel.MEDIUM
        else:
            ltv_risk = RiskLevel.HIGH

    # Debt burden assessment
    if existing_loans == 0:
        debt_burden = RiskLevel.VERY_LOW
        debt_burden_description = "No existing loans"
    elif existing_loans == 1:
        debt_burden = RiskLevel.LOW
        debt_burden_description = "Single existing loan"
    elif existing_loans <= 2:
        debt_burden = RiskLevel.MEDIUM
        debt_burden_description = "Multiple existing loans"
    else:
        debt_burden = RiskLevel.HIGH
        debt_burden_description = f"{existing_loans} existing loans - high debt burden"

    # Overall loan amount risk
    risk_scores = [_risk_to_score(lti_risk)]
    if ltv_risk:
        risk_scores.append(_risk_to_score(ltv_risk))
    risk_scores.append(_risk_to_score(debt_burden))

    overall_score = sum(risk_scores) / len(risk_scores)
    overall_risk = _score_to_risk(overall_score)

    return {
        "loan_amount": loan_amount,
        "annual_income": annual_income,
        "lti_ratio": round(lti_ratio, 4),
        "lti_percentage": round(lti_percentage, 2),
        "lti_risk": lti_risk,
        "ltv_ratio": round(ltv_ratio, 4) if ltv_ratio else None,
        "ltv_percentage": round(ltv_percentage, 2) if ltv_percentage else None,
        "ltv_risk": ltv_risk,
        "property_value": property_value,
        "existing_loans": existing_loans,
        "debt_burden": debt_burden,
        "debt_burden_description": debt_burden_description,
        "overall_loan_risk": overall_risk,
        "reasoning": f"Loan amount of ${loan_amount:,.0f} represents {lti_percentage:.1f}% of annual income ({lti_risk}). {debt_burden_description}."
    }


def detect_anomalies(
    applicant: Dict[str, Any],
    loan_request: Dict[str, Any],
    dti_analysis: Dict[str, Any],
    credit_analysis: Dict[str, Any],
    loan_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Detect anomalies and unusual patterns in application.
    """
    anomalies = []
    anomaly_scores = []

    # DTI Anomaly
    if dti_analysis['dti_percentage'] > 50:
        anomalies.append({
            "type": AnomalyType.HIGH_DTI,
            "severity": "Critical",
            "score": 100,
            "description": f"DTI ratio of {dti_analysis['dti_percentage']:.1f}% is extremely high"
        })
        anomaly_scores.append(100)
    elif dti_analysis['dti_percentage'] > 43:
        anomalies.append({
            "type": AnomalyType.HIGH_DTI,
            "severity": "High",
            "score": 80,
            "description": f"DTI ratio of {dti_analysis['dti_percentage']:.1f}% exceeds conventional limits"
        })
        anomaly_scores.append(80)

    # Credit Score Anomaly
    if applicant.get('credit_score', 0) < 620:
        anomalies.append({
            "type": AnomalyType.LOW_CREDIT_SCORE,
            "severity": "High",
            "score": 75,
            "description": f"Credit score of {applicant['credit_score']} is below acceptable threshold"
        })
        anomaly_scores.append(75)

    # Recent Delinquency
    recent_delinquencies = applicant.get('recent_delinquencies', 0)
    if recent_delinquencies > 0:
        anomalies.append({
            "type": AnomalyType.RECENT_DELINQUENCY,
            "severity": "Critical" if recent_delinquencies > 1 else "High",
            "score": 90 if recent_delinquencies > 1 else 70,
            "description": f"{recent_delinquencies} recent delinquency(ies) detected"
        })
        anomaly_scores.append(90 if recent_delinquencies > 1 else 70)

    # Excessive Inquiries
    inquiries = applicant.get('inquiries_last_6_months', 0)
    if inquiries > 5:
        anomalies.append({
            "type": AnomalyType.EXCESSIVE_INQUIRIES,
            "severity": "Medium",
            "score": 60,
            "description": f"{inquiries} credit inquiries in last 6 months (typical: 1-2)"
        })
        anomaly_scores.append(60)

    # High Credit Utilization
    utilization = applicant.get('credit_utilization', 0)
    if utilization > 0.80:
        anomalies.append({
            "type": AnomalyType.HIGH_UTILIZATION,
            "severity": "Medium",
            "score": 55,
            "description": f"Credit utilization of {utilization*100:.1f}% is high (ideal: <30%)"
        })
        anomaly_scores.append(55)

    # Loan Amount vs Income Mismatch
    if loan_analysis.get('lti_percentage', 0) > 10:
        anomalies.append({
            "type": AnomalyType.UNUSUAL_LOAN_REQUEST,
            "severity": "High",
            "score": 70,
            "description": f"Loan request of {loan_analysis['lti_percentage']:.1f}% of income is unusually high"
        })
        anomaly_scores.append(70)

    # Short Employment Tenure
    tenure = applicant.get('years_at_current_job', 0)
    if tenure < 0.5:
        anomalies.append({
            "type": AnomalyType.SHORT_TENURE,
            "severity": "Medium",
            "score": 50,
            "description": f"Employment tenure of {tenure:.1f} years is very recent"
        })
        anomaly_scores.append(50)

    # Age-Employment Mismatch
    age = applicant.get('age', 0)
    if age < 25 and tenure > 0:
        estimated_start_age = age - tenure
        if estimated_start_age < 18:
            anomalies.append({
                "type": AnomalyType.AGE_EMPLOYMENT_MISMATCH,
                "severity": "Low",
                "score": 30,
                "description": f"Employment history extends before typical working age"
            })
            anomaly_scores.append(30)

    # Overall anomaly score
    anomaly_risk_score = sum(anomaly_scores) / len(anomaly_scores) if anomaly_scores else 0
    anomaly_risk_level = _score_to_risk(anomaly_risk_score / 100 * 5)  # Scale to 0-5

    return {
        "has_anomalies": len(anomalies) > 0,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "overall_anomaly_score": round(anomaly_risk_score, 2),
        "overall_anomaly_risk_level": anomaly_risk_level,
        "severity_breakdown": {
            "critical": len([a for a in anomalies if a['severity'] == 'Critical']),
            "high": len([a for a in anomalies if a['severity'] == 'High']),
            "medium": len([a for a in anomalies if a['severity'] == 'Medium']),
            "low": len([a for a in anomalies if a['severity'] == 'Low'])
        }
    }


def generate_comprehensive_risk_report(
    applicant_id: str,
    applicant: Dict[str, Any],
    loan_request: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate comprehensive financial risk report.
    """
    # Calculate monthly income and debt
    annual_income = applicant.get('annual_income', 0)
    monthly_income = annual_income / 12
    monthly_expenses = applicant.get('monthly_expenses', 0)
    existing_monthly_debt = applicant.get('existing_monthly_debt', 0)
    total_monthly_debt = monthly_expenses + existing_monthly_debt

    # Add new loan payment to debt
    loan_amount = loan_request.get('loan_amount', 0)
    loan_term_months = loan_request.get('loan_term_months', 360)  # Assume 30 years
    estimated_monthly_payment = (loan_amount * (0.05 / 12)) / (1 - (1 + 0.05/12) ** -loan_term_months)
    total_monthly_debt_with_loan = total_monthly_debt + estimated_monthly_payment

    # Perform all analyses
    dti_analysis = calculate_dti_ratio(monthly_income, total_monthly_debt)
    dti_with_loan = calculate_dti_ratio(monthly_income, total_monthly_debt_with_loan)
    credit_analysis = calculate_credit_score_risk(
        applicant.get('credit_score', 0),
        applicant.get('delinquencies', 0),
        applicant.get('inquiries_last_6_months', 0)
    )
    loan_analysis = calculate_loan_amount_risk(
        loan_amount,
        annual_income,
        loan_request.get('property_value'),
        applicant.get('existing_loans', 0),
        applicant.get('credit_score', 0)
    )

    # Detect anomalies
    anomalies = detect_anomalies(applicant, loan_request, dti_analysis, credit_analysis, loan_analysis)

    # Calculate overall risk
    risk_components = [
        _risk_to_score(dti_with_loan['risk_level']),
        _risk_to_score(credit_analysis['final_risk_level']),
        _risk_to_score(loan_analysis['overall_loan_risk']),
        anomalies['overall_anomaly_score'] / 100 * 5
    ]
    overall_risk_score = sum(risk_components) / len(risk_components)
    overall_risk_level = _score_to_risk(overall_risk_score)

    # Generate detailed reasoning
    reasoning_points = [
        dti_analysis['reasoning'],
        f"Current DTI: {dti_analysis['dti_percentage']:.1f}%, With New Loan: {dti_with_loan['dti_percentage']:.1f}%",
        credit_analysis['reasoning'],
        loan_analysis['reasoning'],
        f"Anomalies Detected: {anomalies['anomaly_count']}"
    ]

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "analysis_timestamp": datetime.now().isoformat(),
        "dti_analysis": dti_analysis,
        "dti_with_new_loan": dti_with_loan,
        "credit_score_risk": credit_analysis,
        "loan_amount_risk": loan_analysis,
        "anomaly_detection": anomalies,
        "overall_risk_assessment": {
            "overall_risk_level": overall_risk_level,
            "overall_risk_score": round(overall_risk_score, 2),
            "approval_recommendation": _get_approval_recommendation(overall_risk_score, anomalies)
        },
        "detailed_reasoning": reasoning_points,
        "summary": f"Applicant presents {overall_risk_level} risk. DTI with new loan: {dti_with_loan['dti_percentage']:.1f}%. Credit Risk: {credit_analysis['final_risk_level']}. {anomalies['anomaly_count']} anomalies detected."
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _risk_to_score(risk_level: RiskLevel) -> float:
    """Convert risk level to numeric score (0-5)"""
    mapping = {
        RiskLevel.VERY_LOW: 1,
        RiskLevel.LOW: 2,
        RiskLevel.MEDIUM: 3,
        RiskLevel.HIGH: 4,
        RiskLevel.VERY_HIGH: 4.5,
        RiskLevel.EXTREME: 5
    }
    return mapping.get(risk_level, 3)


def _score_to_risk(score: float) -> RiskLevel:
    """Convert numeric score (0-5) to risk level"""
    if score < 1.5:
        return RiskLevel.VERY_LOW
    elif score < 2.5:
        return RiskLevel.LOW
    elif score < 3.5:
        return RiskLevel.MEDIUM
    elif score < 4.2:
        return RiskLevel.HIGH
    elif score < 4.7:
        return RiskLevel.VERY_HIGH
    else:
        return RiskLevel.EXTREME


def _get_approval_recommendation(risk_score: float, anomalies: Dict[str, Any]) -> str:
    """Get approval recommendation based on risk score and anomalies"""
    critical_anomalies = anomalies['severity_breakdown']['critical']

    if risk_score < 1.5 and critical_anomalies == 0:
        return "APPROVE - Low risk profile"
    elif risk_score < 2.5 and critical_anomalies == 0:
        return "APPROVE - Acceptable risk with conditions"
    elif risk_score < 3.5 and critical_anomalies <= 1:
        return "CONDITIONAL - Requires additional review"
    elif risk_score < 4.2:
        return "REVIEW - Higher risk, manual underwriting recommended"
    else:
        return "DECLINE - Risk profile exceeds acceptable thresholds"


# ============================================================================
# MCP TOOLS
# ============================================================================

@app.tool()
def evaluate_dti_ratio(monthly_income: float, monthly_debt: float) -> dict:
    """
    Evaluate Debt-to-Income (DTI) ratio and risk level.

    DTI = (Total Monthly Debt / Gross Monthly Income) * 100

    Args:
        monthly_income: Gross monthly income in dollars
        monthly_debt: Total monthly debt obligations in dollars

    Returns:
        DTI analysis with ratio, percentage, risk level, and reasoning
    """
    result = calculate_dti_ratio(monthly_income, monthly_debt)
    logger.info(f"DTI evaluated: {result['dti_percentage']}%")

    return {
        "status": "success",
        "analysis": result
    }


@app.tool()
def evaluate_credit_risk(
    credit_score: int,
    delinquencies: int = 0,
    inquiries_last_6_months: int = 0
) -> dict:
    """
    Evaluate credit score risk with delinquency and inquiry adjustments.

    Args:
        credit_score: Applicant's credit score (300-850)
        delinquencies: Number of delinquencies on record
        inquiries_last_6_months: Number of credit inquiries in last 6 months

    Returns:
        Credit risk analysis with adjusted risk level and reasoning
    """
    result = calculate_credit_score_risk(credit_score, delinquencies, inquiries_last_6_months)
    logger.info(f"Credit risk evaluated: {result['final_risk_level']} (score {credit_score})")

    return {
        "status": "success",
        "analysis": result
    }


@app.tool()
def evaluate_loan_amount_risk(
    loan_amount: float,
    annual_income: float,
    property_value: float = None,
    existing_loans: int = 0,
    credit_score: int = 0
) -> dict:
    """
    Evaluate loan amount risk based on LTI, LTV, and debt burden.

    Args:
        loan_amount: Requested loan amount in dollars
        annual_income: Applicant's annual income in dollars
        property_value: Property value (for LTV calculation)
        existing_loans: Number of existing loans
        credit_score: Applicant's credit score

    Returns:
        Loan amount risk analysis with LTI, LTV, and overall risk
    """
    result = calculate_loan_amount_risk(
        loan_amount, annual_income, property_value, existing_loans, credit_score
    )
    logger.info(f"Loan amount risk evaluated: {result['overall_loan_risk']} (LTI {result['lti_percentage']}%)")

    return {
        "status": "success",
        "analysis": result
    }


@app.tool()
def detect_risk_anomalies(applicant_data: dict, loan_request: dict) -> dict:
    """
    Detect anomalies and unusual patterns in application.

    Args:
        applicant_data: Dictionary with applicant information
        loan_request: Dictionary with loan request details

    Returns:
        List of detected anomalies with types, severity, and descriptions
    """
    # Quick analyses for context
    monthly_income = applicant_data.get('annual_income', 0) / 12
    monthly_debt = applicant_data.get('monthly_expenses', 0) + applicant_data.get('existing_monthly_debt', 0)
    dti_analysis = calculate_dti_ratio(monthly_income, monthly_debt)
    credit_analysis = calculate_credit_score_risk(
        applicant_data.get('credit_score', 0),
        applicant_data.get('delinquencies', 0),
        applicant_data.get('inquiries_last_6_months', 0)
    )
    loan_analysis = calculate_loan_amount_risk(
        loan_request.get('loan_amount', 0),
        applicant_data.get('annual_income', 0)
    )

    anomalies = detect_anomalies(applicant_data, loan_request, dti_analysis, credit_analysis, loan_analysis)
    logger.info(f"Anomaly detection complete: {anomalies['anomaly_count']} anomalies found")

    return {
        "status": "success",
        "analysis": anomalies
    }


@app.tool()
def generate_risk_report(applicant_id: str, applicant_data: dict, loan_request: dict) -> dict:
    """
    Generate comprehensive financial risk report.

    Combines DTI analysis, credit risk, loan amount risk, and anomaly detection.

    Args:
        applicant_id: Unique applicant identifier
        applicant_data: Applicant profile dictionary
        loan_request: Loan request details dictionary

    Returns:
        Complete risk assessment report with all metrics and recommendations
    """
    report = generate_comprehensive_risk_report(applicant_id, applicant_data, loan_request)
    logger.info(f"Risk report generated for {applicant_id}: {report['overall_risk_assessment']['overall_risk_level']}")

    return report


@app.tool()
def evaluate_with_scenario_analysis(
    applicant_id: str,
    applicant_data: dict,
    loan_request: dict,
    scenarios: list = None
) -> dict:
    """
    Evaluate applicant with scenario analysis (different loan amounts, DTI levels, etc.).

    Args:
        applicant_id: Unique applicant identifier
        applicant_data: Applicant profile dictionary
        loan_request: Loan request details dictionary
        scenarios: List of scenario definitions (optional)

    Returns:
        Risk assessment for base scenario and alternative scenarios
    """
    # Base scenario
    base_report = generate_comprehensive_risk_report(applicant_id, applicant_data, loan_request)

    # Default scenarios if not provided
    if not scenarios:
        base_loan = loan_request.get('loan_amount', 0)
        scenarios = [
            {"name": "Conservative (80% of requested)", "loan_amount": base_loan * 0.8},
            {"name": "Aggressive (120% of requested)", "loan_amount": base_loan * 1.2},
        ]

    # Run scenarios
    scenario_results = []
    for scenario in scenarios:
        scenario_request = loan_request.copy()
        scenario_request['loan_amount'] = scenario.get('loan_amount', loan_request.get('loan_amount', 0))
        scenario_report = generate_comprehensive_risk_report(applicant_id, applicant_data, scenario_request)
        scenario_results.append({
            "scenario": scenario.get('name', 'Unnamed'),
            "loan_amount": scenario_request['loan_amount'],
            "risk_level": scenario_report['overall_risk_assessment']['overall_risk_level'],
            "dti_percentage": scenario_report['dti_with_new_loan']['dti_percentage']
        })

    logger.info(f"Scenario analysis completed for {applicant_id}: {len(scenarios)} scenarios evaluated")

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "base_scenario": base_report,
        "alternative_scenarios": scenario_results
    }


# ============================================================================
# MCP RESOURCES
# ============================================================================

@app.resource("risk://dti/guidelines")
def dti_guidelines() -> dict:
    """
    DTI ratio guidelines and thresholds.
    """
    return {
        "version": "1.0",
        "title": "Debt-to-Income Guidelines",
        "thresholds": {
            "excellent": {
                "range": "< 20%",
                "description": "Excellent debt management",
                "risk_level": "Very Low"
            },
            "good": {
                "range": "20-36%",
                "description": "Good debt levels, conventional loans acceptable",
                "risk_level": "Low"
            },
            "acceptable": {
                "range": "36-43%",
                "description": "Higher risk, some loan types may be restricted",
                "risk_level": "Medium"
            },
            "high_risk": {
                "range": "43-50%",
                "description": "High risk, FHA loans may not be eligible",
                "risk_level": "High"
            },
            "very_high_risk": {
                "range": "> 50%",
                "description": "Very high risk, most loans not eligible",
                "risk_level": "Very High"
            }
        },
        "conventional_loan_limit": 43,
        "fha_loan_limit": 50,
        "va_loan_limit": 60,
        "calculation": "DTI = (Total Monthly Debt / Gross Monthly Income) * 100"
    }


@app.resource("risk://credit/assessment_criteria")
def credit_assessment_criteria() -> dict:
    """
    Credit score assessment criteria and risk levels.
    """
    return {
        "version": "1.0",
        "title": "Credit Score Risk Assessment",
        "score_ranges": {
            "excellent": {
                "range": "750-850",
                "description": "Excellent credit profile",
                "risk_level": "Very Low",
                "default_probability": "0-1%"
            },
            "good": {
                "range": "700-749",
                "description": "Good credit profile",
                "risk_level": "Low",
                "default_probability": "1-2%"
            },
            "fair": {
                "range": "650-699",
                "description": "Fair credit profile, some risk",
                "risk_level": "Medium",
                "default_probability": "2-5%"
            },
            "poor": {
                "range": "600-649",
                "description": "Poor credit profile, higher risk",
                "risk_level": "High",
                "default_probability": "5-10%"
            },
            "very_poor": {
                "range": "< 600",
                "description": "Very poor credit profile, very high risk",
                "risk_level": "Very High",
                "default_probability": "> 10%"
            }
        },
        "adjustment_factors": {
            "delinquency": -15,
            "recent_inquiry": -3,
            "high_utilization": -10,
            "long_history": 5
        },
        "minimum_for_conventional": 620,
        "recommended_minimum": 650
    }


@app.resource("risk://loan/risk_assessment")
def loan_risk_assessment_criteria() -> dict:
    """
    Loan amount risk assessment criteria.
    """
    return {
        "version": "1.0",
        "title": "Loan Amount Risk Assessment",
        "lti_guidelines": {
            "excellent": "< 3% of annual income",
            "good": "3-5% of annual income",
            "acceptable": "5-8% of annual income",
            "high_risk": "8-12% of annual income",
            "very_high_risk": "> 12% of annual income"
        },
        "ltv_guidelines": {
            "excellent": "< 60%",
            "good": "60-80%",
            "acceptable": "80-95%",
            "high_risk": "> 95%"
        },
        "debt_burden": {
            "low": "0 existing loans",
            "medium": "1 existing loan",
            "high": "2+ existing loans"
        }
    }


@app.resource("risk://anomalies/detection_rules")
def anomaly_detection_rules() -> dict:
    """
    Rules and criteria for anomaly detection.
    """
    return {
        "version": "1.0",
        "title": "Anomaly Detection Rules",
        "anomaly_types": {
            "high_dti": {
                "trigger": "DTI > 50%",
                "severity": "Critical",
                "description": "Debt-to-income ratio critically high"
            },
            "low_credit": {
                "trigger": "Credit Score < 620",
                "severity": "High",
                "description": "Credit score below acceptable threshold"
            },
            "recent_delinquency": {
                "trigger": "Delinquency within last 6 months",
                "severity": "Critical",
                "description": "Recent payment delinquency detected"
            },
            "excessive_inquiries": {
                "trigger": "> 5 inquiries in 6 months",
                "severity": "Medium",
                "description": "Unusually high number of credit inquiries"
            },
            "high_utilization": {
                "trigger": "Credit utilization > 80%",
                "severity": "Medium",
                "description": "High credit card balances relative to limits"
            },
            "unusual_loan": {
                "trigger": "LTI > 10%",
                "severity": "High",
                "description": "Loan amount unusually high relative to income"
            },
            "short_tenure": {
                "trigger": "Employment < 6 months",
                "severity": "Medium",
                "description": "Very recent employment"
            }
        }
    }


@app.resource("risk://regulatory/compliance")
def regulatory_compliance_rules() -> dict:
    """
    Regulatory compliance requirements and guidelines.
    """
    return {
        "version": "1.0",
        "title": "Regulatory Compliance Rules",
        "fair_lending_requirements": [
            "No discrimination based on protected characteristics",
            "Consistent underwriting standards",
            "Documented reasons for adverse decisions",
            "Monitoring for disparate impact"
        ],
        "qualified_mortgage": {
            "max_debt_ratio": 43,
            "min_credit_score": 620,
            "loan_term": "30 years or less"
        },
        "required_disclosures": [
            "Loan Estimate (within 3 days of application)",
            "Truth in Lending Disclosure",
            "Adverse action notices if declined"
        ]
    }


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting RiskRulesDB MCP Server...")
    logger.info("Available tools: 6 risk evaluation tools")
    logger.info("Available resources: 5 reference resources")

    import uvicorn
    uvicorn.run(
        "mcp.riskrulesdb.server:app",
        host="0.0.0.0",
        port=3001,
        reload=True,
        log_level="info"
    )
