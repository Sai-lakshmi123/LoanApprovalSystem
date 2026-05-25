"""
FastMCP Server: Application DB
Simulates fetching applicant profile data and providing analysis tools
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
app = FastMCP("Application DB", version="1.0.0")

# ============================================================================
# SIMULATED DATABASE
# ============================================================================

APPLICANTS_DB = {
    "APP001": {
        "id": "APP001",
        "name": "John Smith",
        "age": 35,
        "email": "john.smith@email.com",
        "phone": "555-0101",
        "income": 85000,
        "annual_income": 85000,
        "employment_type": "full_time",
        "employer": "Tech Corp",
        "job_title": "Senior Software Engineer",
        "years_at_current_job": 4,
        "credit_score": 750,
        "credit_history": {
            "accounts": 5,
            "total_accounts": 8,
            "delinquencies": 0,
            "delinquent_accounts": 0,
            "inquiries_last_6_months": 1,
            "average_account_age": 8.5,
            "total_debt": 15000,
            "credit_utilization": 0.35,
            "payment_history": [
                {"month": -1, "status": "on_time"},
                {"month": -2, "status": "on_time"},
                {"month": -3, "status": "on_time"},
            ]
        },
        "monthly_expenses": 3200,
        "existing_loans": 1,
        "application_date": "2024-05-20"
    },
    "APP002": {
        "id": "APP002",
        "name": "Sarah Johnson",
        "age": 28,
        "email": "sarah.j@email.com",
        "phone": "555-0102",
        "income": 55000,
        "annual_income": 55000,
        "employment_type": "full_time",
        "employer": "Marketing Plus",
        "job_title": "Marketing Manager",
        "years_at_current_job": 2,
        "credit_score": 680,
        "credit_history": {
            "accounts": 3,
            "total_accounts": 5,
            "delinquencies": 1,
            "delinquent_accounts": 1,
            "inquiries_last_6_months": 3,
            "average_account_age": 4.2,
            "total_debt": 8500,
            "credit_utilization": 0.55,
            "payment_history": [
                {"month": -1, "status": "on_time"},
                {"month": -2, "status": "30_days_late"},
                {"month": -3, "status": "on_time"},
            ]
        },
        "monthly_expenses": 2800,
        "existing_loans": 0,
        "application_date": "2024-05-20"
    },
    "APP003": {
        "id": "APP003",
        "name": "Michael Chen",
        "age": 45,
        "email": "m.chen@email.com",
        "phone": "555-0103",
        "income": 120000,
        "annual_income": 120000,
        "employment_type": "self_employed",
        "employer": "Chen Consulting LLC",
        "job_title": "Owner",
        "years_at_current_job": 8,
        "credit_score": 720,
        "credit_history": {
            "accounts": 7,
            "total_accounts": 10,
            "delinquencies": 0,
            "delinquent_accounts": 0,
            "inquiries_last_6_months": 2,
            "average_account_age": 12.3,
            "total_debt": 35000,
            "credit_utilization": 0.45,
            "payment_history": [
                {"month": -1, "status": "on_time"},
                {"month": -2, "status": "on_time"},
                {"month": -3, "status": "on_time"},
            ]
        },
        "monthly_expenses": 5000,
        "existing_loans": 2,
        "application_date": "2024-05-20"
    },
    "APP004": {
        "id": "APP004",
        "name": "Emma Wilson",
        "age": 32,
        "email": "emma.w@email.com",
        "phone": "555-0104",
        "income": 72000,
        "annual_income": 72000,
        "employment_type": "part_time",
        "employer": "Retail Store",
        "job_title": "Sales Associate",
        "years_at_current_job": 1,
        "credit_score": 620,
        "credit_history": {
            "accounts": 2,
            "total_accounts": 4,
            "delinquencies": 2,
            "delinquent_accounts": 2,
            "inquiries_last_6_months": 5,
            "average_account_age": 2.1,
            "total_debt": 12000,
            "credit_utilization": 0.80,
            "payment_history": [
                {"month": -1, "status": "60_days_late"},
                {"month": -2, "status": "30_days_late"},
                {"month": -3, "status": "on_time"},
            ]
        },
        "monthly_expenses": 3500,
        "existing_loans": 0,
        "application_date": "2024-05-20"
    }
}

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def calculate_income_stability_score(applicant: dict) -> dict:
    """
    Calculate income stability score based on employment type and duration.
    Score: 0-100 (higher is more stable)
    """
    employment_type = applicant.get("employment_type", "unknown")
    years_at_job = applicant.get("years_at_current_job", 0)
    age = applicant.get("age", 0)

    # Base score by employment type
    base_scores = {
        "full_time": 75,
        "self_employed": 50,
        "part_time": 40,
        "contract": 45,
        "unknown": 30
    }

    base_score = base_scores.get(employment_type, 30)

    # Adjust based on tenure
    if years_at_job >= 5:
        base_score += 15
    elif years_at_job >= 3:
        base_score += 10
    elif years_at_job >= 1:
        base_score += 5
    else:
        base_score -= 10

    # Adjust based on age (more stable if 25-55)
    if 25 <= age <= 55:
        base_score += 5
    elif age < 25 or age > 65:
        base_score -= 10

    # Cap at 100
    score = min(max(base_score, 0), 100)

    return {
        "score": score,
        "employment_type": employment_type,
        "years_at_job": years_at_job,
        "age": age,
        "stability_category": (
            "Very High" if score >= 85 else
            "High" if score >= 70 else
            "Medium" if score >= 50 else
            "Low"
        )
    }


def calculate_employment_risk(applicant: dict) -> dict:
    """
    Calculate employment risk based on industry, job tenure, and employment type.
    Risk Score: 0-100 (higher = higher risk)
    """
    employment_type = applicant.get("employment_type", "unknown")
    years_at_job = applicant.get("years_at_current_job", 0)

    # Risk by employment type
    risk_scores = {
        "full_time": 20,
        "self_employed": 40,
        "contract": 50,
        "part_time": 60,
        "unknown": 80
    }

    risk_score = risk_scores.get(employment_type, 80)

    # Adjust based on tenure
    if years_at_job < 1:
        risk_score += 25
    elif years_at_job < 2:
        risk_score += 15
    elif years_at_job < 3:
        risk_score += 10
    elif years_at_job >= 5:
        risk_score -= 15

    # Cap between 0-100
    risk_score = min(max(risk_score, 0), 100)

    return {
        "risk_score": risk_score,
        "risk_level": (
            "Very High" if risk_score >= 75 else
            "High" if risk_score >= 60 else
            "Medium" if risk_score >= 40 else
            "Low"
        ),
        "employment_type": employment_type,
        "tenure_risk": (
            "Recent Change" if years_at_job < 1 else
            "New Job" if years_at_job < 2 else
            "Stable"
        ),
        "recommendations": []
    }


def calculate_credit_history_summary(applicant: dict) -> dict:
    """
    Generate credit history summary and analysis.
    """
    credit_data = applicant.get("credit_history", {})
    credit_score = applicant.get("credit_score", 0)

    # Credit score category
    score_category = (
        "Excellent" if credit_score >= 750 else
        "Good" if credit_score >= 700 else
        "Fair" if credit_score >= 650 else
        "Poor"
    )

    # Delinquency analysis
    delinquencies = credit_data.get("delinquencies", 0)
    delinquency_status = (
        "No delinquencies" if delinquencies == 0 else
        f"{delinquencies} delinquency(ies) on record"
    )

    # Payment history trend
    payment_history = credit_data.get("payment_history", [])
    late_payments = sum(1 for p in payment_history if "late" in p.get("status", ""))
    payment_trend = (
        "Improving" if late_payments == 0 else
        "Deteriorating" if late_payments >= 2 else
        "Mixed"
    )

    # Credit utilization analysis
    credit_util = credit_data.get("credit_utilization", 0)
    utilization_status = (
        "Excellent" if credit_util < 0.30 else
        "Good" if credit_util < 0.50 else
        "Fair" if credit_util < 0.70 else
        "High"
    )

    return {
        "credit_score": credit_score,
        "score_category": score_category,
        "delinquencies": delinquencies,
        "delinquency_status": delinquency_status,
        "accounts_open": credit_data.get("accounts", 0),
        "total_accounts": credit_data.get("total_accounts", 0),
        "average_account_age": credit_data.get("average_account_age", 0),
        "total_debt": credit_data.get("total_debt", 0),
        "credit_utilization_ratio": round(credit_util * 100, 1),
        "utilization_status": utilization_status,
        "payment_trend": payment_trend,
        "inquiries_last_6_months": credit_data.get("inquiries_last_6_months", 0),
        "summary": f"Credit score of {credit_score} ({score_category}). {delinquency_status}. Payment history is {payment_trend}. Credit utilization is {utilization_status}."
    }


def check_application_completeness(applicant: dict) -> dict:
    """
    Check completeness of application and flag missing information.
    """
    required_fields = [
        "id", "name", "age", "email", "phone",
        "annual_income", "employment_type", "years_at_current_job",
        "credit_score", "credit_history"
    ]

    missing_fields = []
    incomplete_sections = []

    for field in required_fields:
        if field not in applicant or applicant[field] is None:
            missing_fields.append(field)

    # Check for incomplete credit history
    credit_history = applicant.get("credit_history", {})
    required_credit_fields = [
        "accounts", "delinquencies", "credit_utilization",
        "payment_history"
    ]
    for field in required_credit_fields:
        if field not in credit_history:
            incomplete_sections.append(f"credit_history.{field}")

    completeness_percentage = max(
        0,
        100 - ((len(missing_fields) + len(incomplete_sections)) /
               (len(required_fields) + len(required_credit_fields)) * 100)
    )

    return {
        "is_complete": len(missing_fields) == 0 and len(incomplete_sections) == 0,
        "completeness_percentage": round(completeness_percentage, 1),
        "missing_fields": missing_fields,
        "incomplete_sections": incomplete_sections,
        "flags": [
            "⚠️ Missing required field" if missing_fields else None,
            "⚠️ Incomplete sections" if incomplete_sections else None,
        ],
        "flags": list(filter(None, [
            "MISSING_FIELDS" if missing_fields else None,
            "INCOMPLETE_SECTIONS" if incomplete_sections else None,
            "COMPLETE" if len(missing_fields) == 0 and len(incomplete_sections) == 0 else None,
        ]))
    }


# ============================================================================
# MCP TOOLS
# ============================================================================

@app.tool()
def get_applicant_profile(applicant_id: str) -> dict:
    """
    Fetch applicant profile data including demographics, income, employment, and credit info.

    Args:
        applicant_id: The unique identifier for the applicant (e.g., 'APP001')

    Returns:
        Applicant profile data or error message
    """
    if applicant_id not in APPLICANTS_DB:
        return {
            "status": "error",
            "message": f"Applicant {applicant_id} not found",
            "available_applicants": list(APPLICANTS_DB.keys())
        }

    applicant = APPLICANTS_DB[applicant_id]
    logger.info(f"Retrieved profile for applicant: {applicant_id}")

    return {
        "status": "success",
        "data": applicant
    }


@app.tool()
def get_income_stability_score(applicant_id: str) -> dict:
    """
    Calculate income stability score based on employment type and duration.
    Considers: employment type (full-time, self-employed, part-time),
    years at current job, and age.

    Args:
        applicant_id: The unique identifier for the applicant

    Returns:
        Income stability analysis with score (0-100)
    """
    if applicant_id not in APPLICANTS_DB:
        return {"status": "error", "message": f"Applicant {applicant_id} not found"}

    applicant = APPLICANTS_DB[applicant_id]
    stability = calculate_income_stability_score(applicant)
    logger.info(f"Calculated income stability score for {applicant_id}: {stability['score']}")

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "analysis": stability
    }


@app.tool()
def get_employment_risk(applicant_id: str) -> dict:
    """
    Calculate employment risk score based on employment type and job tenure.
    Assesses the risk level of income loss or job change.

    Args:
        applicant_id: The unique identifier for the applicant

    Returns:
        Employment risk analysis with risk score (0-100, higher = more risky)
    """
    if applicant_id not in APPLICANTS_DB:
        return {"status": "error", "message": f"Applicant {applicant_id} not found"}

    applicant = APPLICANTS_DB[applicant_id]
    risk = calculate_employment_risk(applicant)
    logger.info(f"Calculated employment risk for {applicant_id}: {risk['risk_score']}")

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "analysis": risk
    }


@app.tool()
def get_credit_history_summary(applicant_id: str) -> dict:
    """
    Get comprehensive credit history summary including credit score,
    delinquencies, payment history trend, and credit utilization.

    Args:
        applicant_id: The unique identifier for the applicant

    Returns:
        Credit history analysis and summary
    """
    if applicant_id not in APPLICANTS_DB:
        return {"status": "error", "message": f"Applicant {applicant_id} not found"}

    applicant = APPLICANTS_DB[applicant_id]
    credit_summary = calculate_credit_history_summary(applicant)
    logger.info(f"Generated credit history summary for {applicant_id}")

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "analysis": credit_summary
    }


@app.tool()
def check_application_completeness_tool(applicant_id: str) -> dict:
    """
    Check if application has all required fields and flag missing information.
    Returns completeness percentage and flags for missing or incomplete sections.

    Args:
        applicant_id: The unique identifier for the applicant

    Returns:
        Completeness check with flags and missing fields
    """
    if applicant_id not in APPLICANTS_DB:
        return {"status": "error", "message": f"Applicant {applicant_id} not found"}

    applicant = APPLICANTS_DB[applicant_id]
    completeness = check_application_completeness(applicant)
    logger.info(f"Checked application completeness for {applicant_id}: {completeness['completeness_percentage']}%")

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "analysis": completeness
    }


@app.tool()
def get_complete_applicant_analysis(applicant_id: str) -> dict:
    """
    Get complete applicant analysis including all metrics:
    - Income stability score
    - Employment risk assessment
    - Credit history summary
    - Application completeness

    Args:
        applicant_id: The unique identifier for the applicant

    Returns:
        Comprehensive analysis report
    """
    if applicant_id not in APPLICANTS_DB:
        return {"status": "error", "message": f"Applicant {applicant_id} not found"}

    applicant = APPLICANTS_DB[applicant_id]

    return {
        "status": "success",
        "applicant_id": applicant_id,
        "name": applicant.get("name"),
        "analysis": {
            "income_stability": calculate_income_stability_score(applicant),
            "employment_risk": calculate_employment_risk(applicant),
            "credit_history": calculate_credit_history_summary(applicant),
            "application_completeness": check_application_completeness(applicant)
        },
        "timestamp": datetime.now().isoformat()
    }


@app.tool()
def list_all_applicants() -> dict:
    """
    List all available applicants in the system.

    Returns:
        List of applicant IDs and names
    """
    applicants = [
        {
            "id": app_id,
            "name": data.get("name"),
            "age": data.get("age"),
            "credit_score": data.get("credit_score")
        }
        for app_id, data in APPLICANTS_DB.items()
    ]
    logger.info(f"Listed {len(applicants)} applicants")

    return {
        "status": "success",
        "count": len(applicants),
        "applicants": applicants
    }


# ============================================================================
# MCP RESOURCES
# ============================================================================

@app.resource("applicant://credit/scoring_rules")
def credit_scoring_rules() -> dict:
    """
    Credit scoring rules and thresholds used for applicant evaluation.
    """
    return {
        "version": "1.0",
        "description": "Credit scoring rules for loan applications",
        "score_categories": {
            "excellent": {"range": "750+", "description": "Excellent credit profile"},
            "good": {"range": "700-749", "description": "Good credit profile"},
            "fair": {"range": "650-699", "description": "Fair credit profile"},
            "poor": {"range": "below 650", "description": "Poor credit profile"}
        },
        "utilization_thresholds": {
            "excellent": "< 30%",
            "good": "30-50%",
            "fair": "50-70%",
            "high": "> 70%"
        },
        "delinquency_impact": {
            "no_delinquencies": 0,
            "recent_30_days": -50,
            "recent_60_days": -75,
            "recent_90_days": -100,
            "old_delinquency": -25
        },
        "minimum_credit_score": 620,
        "recommended_minimum": 650
    }


@app.resource("applicant://employment/stability_factors")
def employment_stability_factors() -> dict:
    """
    Employment stability factors and risk assessment criteria.
    """
    return {
        "version": "1.0",
        "description": "Employment stability assessment factors",
        "employment_types": {
            "full_time": {
                "base_stability_score": 75,
                "risk_level": "Low",
                "description": "Full-time permanent employment"
            },
            "self_employed": {
                "base_stability_score": 50,
                "risk_level": "Medium-High",
                "description": "Self-employed or business owner"
            },
            "contract": {
                "base_stability_score": 45,
                "risk_level": "High",
                "description": "Contract or temporary work"
            },
            "part_time": {
                "base_stability_score": 40,
                "risk_level": "Very High",
                "description": "Part-time employment"
            }
        },
        "tenure_adjustments": {
            "less_than_1_year": -10,
            "1_to_2_years": 5,
            "2_to_3_years": 10,
            "3_to_5_years": 15,
            "more_than_5_years": 25
        },
        "minimum_acceptable_stability": 50
    }


@app.resource("applicant://compliance/regulatory_requirements")
def regulatory_requirements() -> dict:
    """
    Compliance and regulatory requirements for loan approvals.
    """
    return {
        "version": "1.0",
        "description": "Regulatory compliance requirements",
        "minimum_requirements": {
            "minimum_age": 18,
            "minimum_income": 25000,
            "minimum_credit_score": 620,
            "maximum_debt_to_income": 0.43
        },
        "preferred_thresholds": {
            "recommended_age": 21,
            "recommended_income": 40000,
            "recommended_credit_score": 650,
            "maximum_dti": 0.36
        },
        "documentation_required": [
            "Proof of income (pay stubs or tax returns)",
            "Employment verification",
            "Credit report authorization",
            "ID verification",
            "Address verification"
        ],
        "fair_lending_checks": [
            "No age discrimination",
            "No gender discrimination",
            "No race/ethnicity discrimination",
            "No disability discrimination",
            "Consistent underwriting standards"
        ]
    }


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting Application DB MCP Server...")
    logger.info(f"Available applicants: {list(APPLICANTS_DB.keys())}")

    # Run the FastMCP server
    import uvicorn
    uvicorn.run(
        "mcp.server:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
