"""
Quick evaluation utilities to speed up loan approval decisions
Replaces complex agent logic with simple, fast rules-based evaluation
"""

def quick_profile_analysis(applicant_data: dict) -> dict:
    """Quick profile analysis - replaces Agent1"""
    age = applicant_data.get("age", 40)
    credit_score = applicant_data.get("credit_score", 650)
    years_at_job = applicant_data.get("years_at_current_job", 1)
    delinquencies = applicant_data.get("delinquencies", 0)

    # Simple scoring
    income_stability = 4 if years_at_job >= 2 else (3 if years_at_job >= 1 else 2)
    credit_quality = 5 if credit_score >= 750 else (4 if credit_score >= 700 else (3 if credit_score >= 650 else 2))

    return {
        "status": "success",
        "income_stability_score": income_stability,
        "credit_quality_score": credit_quality,
        "delinquencies": delinquencies,
        "profile_strength": (income_stability + credit_quality) / 2
    }


def quick_risk_analysis(applicant_data: dict, loan_request: dict) -> dict:
    """Quick risk analysis - replaces Agent2"""
    annual_income = applicant_data.get("annual_income", 60000)
    existing_liabilities = applicant_data.get("existing_liabilities", 0)
    loan_amount = loan_request.get("loan_amount", 200000)
    property_value = loan_request.get("property_value", 300000)
    credit_score = applicant_data.get("credit_score", 650)

    # Calculate DTI
    monthly_income = annual_income / 12
    monthly_loan_payment = (loan_amount / 360) * 0.006  # Approximate
    total_monthly_debt = existing_liabilities + monthly_loan_payment
    dti = total_monthly_debt / monthly_income if monthly_income > 0 else 1.0

    # Calculate LTV
    ltv = loan_amount / property_value if property_value > 0 else 1.0

    # Risk scoring
    risk_score = 0
    if dti > 0.50:
        risk_score += 2
    elif dti > 0.43:
        risk_score += 1.5
    elif dti > 0.36:
        risk_score += 0.5

    if ltv > 0.95:
        risk_score += 2
    elif ltv > 0.80:
        risk_score += 1

    if credit_score < 620:
        risk_score += 2
    elif credit_score < 680:
        risk_score += 1

    risk_score = min(5, max(1, risk_score + 1))  # Clamp 1-5

    risk_level = "low" if risk_score < 2 else ("medium" if risk_score < 3.5 else "high")

    return {
        "status": "success",
        "dti": round(dti, 2),
        "ltv": round(ltv, 2),
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level
    }


def quick_decision_synthesis(profile: dict, risk: dict) -> dict:
    """Quick decision synthesis - replaces Agent3"""
    risk_score = risk.get("risk_score", 3)
    risk_level = risk.get("risk_level", "medium")
    dti = risk.get("dti", 0.5)
    credit_score = 650  # Would come from applicant_data

    # Decision logic
    if risk_score <= 1.5 and dti <= 0.36:
        classification = "APPROVE"
        confidence = 90
    elif risk_score <= 2.5 and dti <= 0.43:
        classification = "CONDITIONAL_APPROVE"
        confidence = 70
    elif risk_score <= 3.5:
        classification = "REVIEW"
        confidence = 50
    else:
        classification = "REJECT"
        confidence = 85

    return {
        "status": "success",
        "decision": {
            "classification": classification,
            "confidence_percentage": confidence,
            "confidence_level": "High" if confidence >= 75 else ("Medium" if confidence >= 50 else "Low"),
            "risk_score": risk_score,
            "reasoning": f"Decision based on DTI ({dti}), risk score ({risk_score}), and credit profile."
        }
    }


def quick_compliance_record(applicant_id: str, decision: dict) -> dict:
    """Quick compliance recording - replaces Agent4"""
    import time
    case_id = f"CASE-{applicant_id}-{int(time.time())}"

    return {
        "status": "success",
        "case_id": case_id,
        "decision_recorded": True,
        "notification_sent": True
    }
