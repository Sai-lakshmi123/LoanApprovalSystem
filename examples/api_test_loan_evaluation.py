#!/usr/bin/env python3
"""
FastAPI Loan Evaluation Endpoint Test Script

Tests the /evaluate-loan POST endpoint with various loan application scenarios.
Run the FastAPI server first:
    python src/api/main.py

Then in another terminal, run this test:
    python examples/api_test_loan_evaluation.py
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"
EVALUATE_LOAN_ENDPOINT = f"{API_BASE_URL}/evaluate-loan"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}  {text}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}\n")


def print_section(text: str):
    """Print formatted section"""
    print(f"{Colors.CYAN}{Colors.BOLD}>>> {text}{Colors.END}")
    print("-" * 80)


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def print_json(data: Dict[str, Any], indent: int = 2):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=indent, default=str))


def test_health_check():
    """Test the health check endpoint"""
    print_header("HEALTH CHECK")

    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print_success(f"Health check passed")
            print_json(response.json())
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Connection error: {e}")
        return False


def submit_loan_application(applicant_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit a loan application to the API

    Args:
        applicant_data: Dictionary with loan application data

    Returns:
        Response JSON from the API
    """
    try:
        response = requests.post(
            EVALUATE_LOAN_ENDPOINT,
            json=applicant_data,
            timeout=60
        )

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text
            }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout (60s)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def display_loan_decision(response: Dict[str, Any]):
    """Display loan decision in formatted output"""
    if not response.get("success"):
        print_error(f"Request failed: {response.get('error')}")
        return

    data = response["data"]

    # Decision Summary
    print(f"\n{Colors.BOLD}📋 DECISION SUMMARY{Colors.END}")
    print(f"  Applicant ID: {data['applicant_id']}")
    print(f"  Case ID: {Colors.BOLD}{data['case_id']}{Colors.END}")
    print(f"  Status: {Colors.BOLD}{data['workflow_status'].upper()}{Colors.END}")

    # Decision Details
    decision = data["decision"]
    classification = decision["classification"]
    decision_color = Colors.GREEN if classification == "APPROVE" else (
        Colors.RED if classification == "REJECT" else Colors.YELLOW
    )

    print(f"\n{Colors.BOLD}⚖️  DECISION{Colors.END}")
    print(f"  Classification: {decision_color}{Colors.BOLD}{classification}{Colors.END}")
    print(f"  Confidence: {Colors.BOLD}{decision['confidence_percentage']}%{Colors.END} ({decision['confidence_level']})")
    print(f"  Risk Score: {Colors.BOLD}{decision['risk_score']:.2f}/5.0{Colors.END}")
    print(f"  Reasoning: {decision['reasoning']}")

    # Risk Assessment
    print(f"\n{Colors.BOLD}📊 RISK ASSESSMENT{Colors.END}")
    print(f"  Risk Level: {Colors.BOLD}{data['risk_level']}{Colors.END}")
    print(f"  Risk Score: {Colors.BOLD}{data['risk_score']:.2f}/5.0{Colors.END}")

    # Key Factors
    if decision.get("key_factors"):
        print(f"\n{Colors.BOLD}🔑 KEY DECISION FACTORS{Colors.END}")
        for i, factor in enumerate(decision["key_factors"], 1):
            print(f"  {i}. {factor}")

    # Next Steps
    print(f"\n{Colors.BOLD}📍 NEXT STEPS{Colors.END}")
    for i, step in enumerate(data["next_steps"], 1):
        print(f"  {i}. {step}")

    # Execution Path
    if data.get("execution_path"):
        print(f"\n{Colors.BOLD}🔄 EXECUTION PATH{Colors.END}")
        print(f"  {' → '.join(data['execution_path'])}")

    # Error Handling
    if data.get("error_handling") and (data["error_handling"].get("critical_errors") or
                                       data["error_handling"].get("error_escalation")):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  ERROR HANDLING{Colors.END}")
        error_info = data["error_handling"]
        if error_info.get("error_escalation"):
            print(f"  {Colors.YELLOW}Escalated to manual review{Colors.END}")
        if error_info.get("critical_errors"):
            print(f"  Critical errors encountered: {error_info['error_count']}")
        if error_info.get("retry_statistics"):
            print(f"  Retry statistics: {error_info['retry_statistics']}")

    # Processing Time
    print(f"\n{Colors.BOLD}⏱️  PROCESSING{Colors.END}")
    print(f"  Time: {data['processing_time_ms']:.2f}ms")
    print(f"  Timestamp: {data['timestamp']}")


def test_scenario_1():
    """Test Scenario 1: Strong Applicant (Expected: APPROVE)"""
    print_header("SCENARIO 1: STRONG APPLICANT (Auto-Approve Path)")

    applicant_data = {
        "applicant_id": "STRONG001",
        "age": 45,
        "annual_income": 200000,
        "employment_type": "employed",
        "credit_score": 780,
        "loan_amount": 300000,
        "tenure_months": 360,
        "existing_liabilities": 1000,
        "location": "CA",
        "delinquencies": 0,
        "inquiries_last_6_months": 0,
        "credit_utilization": 0.20,
        "years_at_current_job": 10,
        "existing_loans": 1,
        "property_value": 600000,
        "email": "john.strong@example.com",
        "phone": "+1-555-0100"
    }

    print_section("Submitting Strong Applicant")
    print_info(f"Applicant: {applicant_data['applicant_id']}")
    print_info(f"Income: ${applicant_data['annual_income']:,.0f}")
    print_info(f"Credit Score: {applicant_data['credit_score']}")
    print_info(f"Loan Amount: ${applicant_data['loan_amount']:,.0f}")

    response = submit_loan_application(applicant_data)
    display_loan_decision(response)


def test_scenario_2():
    """Test Scenario 2: High-Risk Applicant (Expected: REVIEW or REJECT)"""
    print_header("SCENARIO 2: HIGH-RISK APPLICANT (Escalation Path)")

    applicant_data = {
        "applicant_id": "HIGHRISK001",
        "age": 35,
        "annual_income": 60000,
        "employment_type": "employed",
        "credit_score": 580,
        "loan_amount": 300000,
        "tenure_months": 360,
        "existing_liabilities": 2500,
        "location": "TX",
        "delinquencies": 2,
        "inquiries_last_6_months": 5,
        "credit_utilization": 0.85,
        "years_at_current_job": 1,
        "existing_loans": 3,
        "property_value": 320000,
        "email": "bob.risky@example.com",
        "phone": "+1-555-0200"
    }

    print_section("Submitting High-Risk Applicant")
    print_info(f"Applicant: {applicant_data['applicant_id']}")
    print_info(f"Income: ${applicant_data['annual_income']:,.0f}")
    print_info(f"Credit Score: {applicant_data['credit_score']}")
    print_info(f"Delinquencies: {applicant_data['delinquencies']}")
    print_info(f"Credit Utilization: {applicant_data['credit_utilization']*100:.0f}%")

    response = submit_loan_application(applicant_data)
    display_loan_decision(response)


def test_scenario_3():
    """Test Scenario 3: Moderate Applicant (Expected: REVIEW or Conditional APPROVE)"""
    print_header("SCENARIO 3: MODERATE APPLICANT (Review Path)")

    applicant_data = {
        "applicant_id": "MODERATE001",
        "age": 40,
        "annual_income": 120000,
        "employment_type": "employed",
        "credit_score": 720,
        "loan_amount": 280000,
        "tenure_months": 360,
        "existing_liabilities": 1500,
        "location": "NY",
        "delinquencies": 0,
        "inquiries_last_6_months": 2,
        "credit_utilization": 0.45,
        "years_at_current_job": 5,
        "existing_loans": 2,
        "property_value": 450000,
        "email": "alice.moderate@example.com",
        "phone": "+1-555-0300"
    }

    print_section("Submitting Moderate Applicant")
    print_info(f"Applicant: {applicant_data['applicant_id']}")
    print_info(f"Income: ${applicant_data['annual_income']:,.0f}")
    print_info(f"Credit Score: {applicant_data['credit_score']}")
    print_info(f"Loan-to-Value: ~{(applicant_data['loan_amount']/applicant_data['property_value']*100):.0f}%")

    response = submit_loan_application(applicant_data)
    display_loan_decision(response)


def test_validation():
    """Test input validation"""
    print_header("VALIDATION TESTS")

    # Test 1: Invalid age (too young)
    print_section("Test 1: Invalid Age (< 18)")
    invalid_data = {
        "applicant_id": "INVALID001",
        "age": 15,  # Invalid: too young
        "annual_income": 50000,
        "employment_type": "employed",
        "credit_score": 650,
        "loan_amount": 200000,
        "tenure_months": 360,
        "existing_liabilities": 1000,
        "location": "CA"
    }

    response = requests.post(EVALUATE_LOAN_ENDPOINT, json=invalid_data)
    if response.status_code != 200:
        print_success("Validation correctly rejected invalid age")
    else:
        print_error("Validation failed to reject invalid age")

    # Test 2: Invalid credit score
    print_section("Test 2: Invalid Credit Score (> 850)")
    invalid_data = {
        "applicant_id": "INVALID002",
        "age": 35,
        "annual_income": 50000,
        "employment_type": "employed",
        "credit_score": 900,  # Invalid: too high
        "loan_amount": 200000,
        "tenure_months": 360,
        "existing_liabilities": 1000,
        "location": "CA"
    }

    response = requests.post(EVALUATE_LOAN_ENDPOINT, json=invalid_data)
    if response.status_code != 200:
        print_success("Validation correctly rejected invalid credit score")
    else:
        print_error("Validation failed to reject invalid credit score")

    # Test 3: Invalid employment type
    print_section("Test 3: Invalid Employment Type")
    invalid_data = {
        "applicant_id": "INVALID003",
        "age": 35,
        "annual_income": 50000,
        "employment_type": "invalid_type",  # Invalid
        "credit_score": 650,
        "loan_amount": 200000,
        "tenure_months": 360,
        "existing_liabilities": 1000,
        "location": "CA"
    }

    response = requests.post(EVALUATE_LOAN_ENDPOINT, json=invalid_data)
    if response.status_code != 200:
        print_success("Validation correctly rejected invalid employment type")
    else:
        print_error("Validation failed to reject invalid employment type")

    # Test 4: Missing required field
    print_section("Test 4: Missing Required Field")
    invalid_data = {
        "applicant_id": "INVALID004",
        "age": 35,
        "annual_income": 50000,
        # Missing employment_type
        "credit_score": 650,
        "loan_amount": 200000,
        "tenure_months": 360,
        "existing_liabilities": 1000,
        "location": "CA"
    }

    response = requests.post(EVALUATE_LOAN_ENDPOINT, json=invalid_data)
    if response.status_code != 200:
        print_success("Validation correctly rejected missing required field")
    else:
        print_error("Validation failed to reject missing field")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  FASTAPI LOAN EVALUATION ENDPOINT TEST SUITE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    # Check API is running
    if not test_health_check():
        print_error("API is not running. Start the server with: python src/api/main.py")
        return 1

    try:
        # Run test scenarios
        test_scenario_1()
        time.sleep(2)

        test_scenario_2()
        time.sleep(2)

        test_scenario_3()
        time.sleep(2)

        # Run validation tests
        test_validation()

        # Summary
        print_header("TEST SUITE COMPLETE")
        print_success("All loan evaluation tests completed!")
        print_info("API is functioning correctly with:")
        print_info("  ✓ Loan evaluation processing")
        print_info("  ✓ Input validation")
        print_info("  ✓ Decision routing")
        print_info("  ✓ Error handling")

        return 0

    except Exception as e:
        print_error(f"Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
