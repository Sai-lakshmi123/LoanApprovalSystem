#!/usr/bin/env python3
"""
Loan Approval System - Test Script with 3 Scenarios

Tests the complete loan approval workflow with:
1. SCENARIO 1: Strong applicant -> Expected: APPROVE
2. SCENARIO 2: Weak applicant -> Expected: REJECT
3. SCENARIO 3: Moderate applicant -> Expected: REVIEW

Usage:
    python tests/test_loan_scenarios.py

Requirements:
    - All 6 services running (5 MCP servers + FastAPI)
    - Python 3.8+
    - requests library

Run with:
    python tests/test_loan_scenarios.py --verbose
    python tests/test_loan_scenarios.py --save-results
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# ==================== Configuration ====================

API_BASE_URL = "http://localhost:8000"
EVALUATE_LOAN_ENDPOINT = f"{API_BASE_URL}/evaluate-loan"
HEALTH_CHECK_ENDPOINT = f"{API_BASE_URL}/health"

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


class TestResult(Enum):
    """Test result status"""
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    ERROR = "ERROR"


@dataclass
class TestScenario:
    """Test scenario definition"""
    name: str
    description: str
    applicant_id: str
    test_data: Dict[str, Any]
    expected_decision: str  # APPROVE, REJECT, or REVIEW
    expected_confidence_min: int
    expected_confidence_max: int
    expected_risk_level: str  # low, medium, high
    key_metrics: Dict[str, Any]  # Expected values for key metrics


# ==================== Test Data ====================

def create_strong_applicant_data() -> Dict[str, Any]:
    """
    Scenario 1: STRONG APPLICANT
    Expected Decision: APPROVE

    Profile:
    - Excellent credit (780)
    - Stable employment (10 years)
    - High income ($200,000/year)
    - Low debt obligations
    - No delinquencies
    - Low credit utilization (20%)

    Metrics:
    - DTI: ~0.27 (Excellent)
    - LTV: ~0.50 (Low risk)
    - Debt-to-Income: Very good
    """
    return {
        "applicant_id": "SCENARIO1_STRONG",
        "age": 45,
        "annual_income": 200000,
        "employment_type": "employed",
        "credit_score": 780,
        "loan_amount": 300000,
        "tenure_months": 360,
        "existing_liabilities": 1000,  # Low monthly debt
        "location": "CA",
        "monthly_expenses": 4000,
        "delinquencies": 0,
        "inquiries_last_6_months": 0,
        "credit_utilization": 0.20,
        "years_at_current_job": 10,
        "existing_loans": 1,
        "property_value": 600000,
        "email": "strong.applicant@example.com",
        "phone": "+1-555-0100"
    }


def create_weak_applicant_data() -> Dict[str, Any]:
    """
    Scenario 2: WEAK APPLICANT
    Expected Decision: REJECT

    Profile:
    - Poor credit (580)
    - Recent job change (1 month)
    - Low income ($50,000/year)
    - High debt obligations ($2,500/month)
    - Recent delinquencies (2)
    - High credit utilization (85%)
    - Multiple recent inquiries (6 in 6 months)

    Metrics:
    - DTI: ~0.65 (Way too high - auto escalate)
    - LTV: ~0.94 (High risk)
    - Multiple risk factors
    """
    return {
        "applicant_id": "SCENARIO2_WEAK",
        "age": 35,
        "annual_income": 50000,
        "employment_type": "employed",
        "credit_score": 580,
        "loan_amount": 300000,  # Very high relative to income
        "tenure_months": 360,
        "existing_liabilities": 2500,  # Very high monthly debt
        "location": "TX",
        "monthly_expenses": 2500,
        "delinquencies": 2,  # Recent delinquencies
        "inquiries_last_6_months": 6,  # Multiple inquiries (shopping)
        "credit_utilization": 0.85,  # Very high utilization
        "years_at_current_job": 0,  # ~1 month (very recent - less than 1 year)
        "existing_loans": 3,
        "property_value": 320000,
        "email": "weak.applicant@example.com",
        "phone": "+1-555-0200"
    }


def create_moderate_applicant_data() -> Dict[str, Any]:
    """
    Scenario 3: MODERATE APPLICANT
    Expected Decision: REVIEW

    Profile:
    - Fair credit (720)
    - Stable employment (5 years)
    - Moderate income ($120,000/year)
    - Moderate debt obligations
    - No recent delinquencies (but had 1 in past)
    - Moderate credit utilization (45%)
    - Some recent inquiries (2 in 6 months)

    Metrics:
    - DTI: ~0.39 (Borderline acceptable)
    - LTV: ~0.70 (Moderate risk)
    - Needs manual review due to moderate risk profile
    """
    return {
        "applicant_id": "SCENARIO3_MODERATE",
        "age": 40,
        "annual_income": 120000,
        "employment_type": "employed",
        "credit_score": 720,
        "loan_amount": 280000,
        "tenure_months": 360,
        "existing_liabilities": 1500,
        "location": "NY",
        "monthly_expenses": 3000,
        "delinquencies": 0,  # No recent delinquencies
        "inquiries_last_6_months": 2,
        "credit_utilization": 0.45,
        "years_at_current_job": 5,
        "existing_loans": 2,
        "property_value": 450000,
        "email": "moderate.applicant@example.com",
        "phone": "+1-555-0300"
    }


# ==================== Test Scenarios ====================

SCENARIOS = [
    TestScenario(
        name="Scenario 1: Strong Applicant",
        description="Excellent credit, stable employment, high income, low debt -> APPROVE",
        applicant_id="SCENARIO1_STRONG",
        test_data=create_strong_applicant_data(),
        expected_decision="APPROVE",
        expected_confidence_min=85,
        expected_confidence_max=95,
        expected_risk_level="Low",
        key_metrics={
            "credit_score": 780,
            "dti_max": 0.36,
            "delinquencies": 0,
            "employment_years": 10
        }
    ),
    TestScenario(
        name="Scenario 2: Weak Applicant",
        description="Poor credit, recent job, low income, high debt, delinquencies -> REJECT",
        applicant_id="SCENARIO2_WEAK",
        test_data=create_weak_applicant_data(),
        expected_decision="REJECT",
        expected_confidence_min=75,
        expected_confidence_max=95,
        expected_risk_level="High",
        key_metrics={
            "credit_score": 580,
            "dti_min": 0.50,  # Should exceed threshold
            "delinquencies": 2,
            "employment_years": 0.08
        }
    ),
    TestScenario(
        name="Scenario 3: Moderate Applicant",
        description="Fair credit, stable employment, moderate income -> REVIEW",
        applicant_id="SCENARIO3_MODERATE",
        test_data=create_moderate_applicant_data(),
        expected_decision="REVIEW",
        expected_confidence_min=40,
        expected_confidence_max=75,
        expected_risk_level="Medium",
        key_metrics={
            "credit_score": 720,
            "dti_range": (0.36, 0.43),
            "delinquencies": 0,
            "employment_years": 5
        }
    ),
]


# ==================== Helper Functions ====================

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


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def print_json(data: Dict[str, Any], indent: int = 2):
    """Pretty print JSON"""
    print(json.dumps(data, indent=indent, default=str))


def check_api_health() -> bool:
    """Check if API is running"""
    try:
        response = requests.get(HEALTH_CHECK_ENDPOINT, timeout=5)
        return response.status_code == 200
    except:
        return False


def submit_loan_application(test_data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Submit a loan application to the API

    Returns:
        Tuple of (success: bool, response_data: dict or None, error_message: str or None)
    """
    try:
        response = requests.post(
            EVALUATE_LOAN_ENDPOINT,
            json=test_data,
            timeout=300
        )

        if response.status_code == 200:
            return True, response.json(), None
        else:
            return False, None, f"Status {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return False, None, "Request timeout (300s)"
    except requests.exceptions.ConnectionError:
        return False, None, f"Cannot connect to API at {EVALUATE_LOAN_ENDPOINT}"
    except Exception as e:
        return False, None, f"Error: {str(e)}"


def verify_decision_output(response: Dict[str, Any], expected_decision: str) -> Tuple[bool, str]:
    """
    Verify the decision output matches expected structure and values

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not response:
        return False, "No response data"

    required_fields = [
        "success",
        "applicant_id",
        "decision",
        "risk_score",
        "case_id",
        "processing_time_ms"
    ]

    # Check required fields
    for field in required_fields:
        if field not in response:
            return False, f"Missing required field: {field}"

    # Check decision object
    decision = response.get("decision", {})
    decision_fields = [
        "classification",
        "confidence_percentage",
        "confidence_level",
        "reasoning"
    ]

    for field in decision_fields:
        if field not in decision:
            return False, f"Missing decision field: {field}"

    # Check decision classification
    classification = decision.get("classification", "")
    if classification not in ["APPROVE", "REJECT", "REVIEW", "CONDITIONAL_APPROVE"]:
        return False, f"Invalid classification: {classification}"

    # Verify expected decision (with some flexibility for CONDITIONAL_APPROVE -> APPROVE)
    if expected_decision == "APPROVE" and classification not in ["APPROVE", "CONDITIONAL_APPROVE"]:
        return False, f"Expected APPROVE but got {classification}"
    elif expected_decision in ["REJECT", "REVIEW"] and classification != expected_decision:
        return False, f"Expected {expected_decision} but got {classification}"

    return True, "Output structure valid"


def check_decision_alignment(actual_decision: str, expected_decision: str) -> Tuple[bool, str]:
    """
    Check if actual decision matches expected decision

    Returns:
        Tuple of (matches: bool, message: str)
    """
    # APPROVE and CONDITIONAL_APPROVE are both approval decisions
    if expected_decision == "APPROVE":
        if actual_decision in ["APPROVE", "CONDITIONAL_APPROVE"]:
            return True, f"✓ Decision matches (expected {expected_decision}, got {actual_decision})"
        else:
            return False, f"✗ Decision mismatch (expected {expected_decision}, got {actual_decision})"

    elif actual_decision == expected_decision:
        return True, f"✓ Decision matches ({actual_decision})"
    else:
        return False, f"✗ Decision mismatch (expected {expected_decision}, got {actual_decision})"


def check_confidence_range(
    confidence: int,
    expected_min: int,
    expected_max: int
) -> Tuple[bool, str]:
    """
    Check if confidence is within expected range

    Returns:
        Tuple of (in_range: bool, message: str)
    """
    if expected_min <= confidence <= expected_max:
        return True, f"✓ Confidence {confidence}% is within range [{expected_min}%, {expected_max}%]"
    else:
        return False, f"✗ Confidence {confidence}% is outside range [{expected_min}%, {expected_max}%]"


def analyze_decision_factors(response: Dict[str, Any], scenario_name: str) -> str:
    """Analyze decision factors in the response"""
    decision = response.get("decision", {})
    factors = decision.get("key_factors", [])
    reasoning = decision.get("reasoning", "")

    analysis = f"\n📊 Decision Factors for {scenario_name}:\n"
    analysis += f"   Reasoning: {reasoning}\n"

    if factors:
        analysis += "   Key Factors:\n"
        for i, factor in enumerate(factors, 1):
            analysis += f"      {i}. {factor}\n"

    return analysis


# ==================== Test Execution ====================

def run_single_test(scenario: TestScenario) -> Tuple[TestResult, Dict[str, Any]]:
    """
    Run a single test scenario

    Returns:
        Tuple of (result: TestResult, details: dict)
    """
    details = {
        "scenario_name": scenario.name,
        "applicant_id": scenario.applicant_id,
        "test_result": None,
        "decision": None,
        "confidence": None,
        "risk_level": None,
        "issues": [],
        "warnings": [],
        "passed_checks": [],
        "failed_checks": [],
        "raw_response": None
    }

    print_section(scenario.name)
    print_info(scenario.description)
    print(f"\nTest Data Summary:")
    print(f"  Applicant ID: {scenario.test_data['applicant_id']}")
    print(f"  Age: {scenario.test_data['age']}")
    print(f"  Income: ${scenario.test_data['annual_income']:,.0f}")
    print(f"  Credit Score: {scenario.test_data['credit_score']}")
    print(f"  Loan Amount: ${scenario.test_data['loan_amount']:,.0f}")
    print(f"  Employment Type: {scenario.test_data['employment_type']}")
    print(f"  Years at Job: {scenario.test_data['years_at_current_job']}")
    print(f"  DTI Components:")
    print(f"    - Monthly Income: ${scenario.test_data['annual_income']/12:,.0f}")
    print(f"    - Monthly Debt: ${scenario.test_data['existing_liabilities']:,.0f}")
    print(f"    - Monthly Expenses: ${scenario.test_data['monthly_expenses']:,.0f}")

    # Submit application
    print(f"\n📤 Submitting application...")
    start_time = time.time()
    success, response, error = submit_loan_application(scenario.test_data)
    elapsed_time = time.time() - start_time

    if not success:
        print_error(f"API Error: {error}")
        details["issues"].append(f"API Error: {error}")
        return TestResult.ERROR, details

    # Store raw response
    details["raw_response"] = response

    # Extract decision info
    decision = response.get("decision", {})
    classification = decision.get("classification", "UNKNOWN")
    confidence = decision.get("confidence_percentage", 0)
    risk_score = response.get("risk_score", 0)
    risk_level = response.get("risk_level", "UNKNOWN")
    case_id = response.get("case_id", "N/A")

    details["decision"] = classification
    details["confidence"] = confidence
    details["risk_level"] = risk_level

    print(f"\n✅ Response received in {elapsed_time:.2f}s")
    print(f"\nDecision Details:")
    print(f"  Classification: {Colors.BOLD}{classification}{Colors.END}")
    print(f"  Confidence: {confidence}%")
    print(f"  Risk Score: {risk_score:.2f}/5.0")
    print(f"  Risk Level: {risk_level}")
    print(f"  Case ID: {case_id}")

    # ===== Validation Checks =====

    # Check 1: Output structure validity
    print(f"\n🔍 Validation Checks:")
    is_valid, msg = verify_decision_output(response, scenario.expected_decision)
    if is_valid:
        print_success(msg)
        details["passed_checks"].append("Output structure valid")
    else:
        print_error(msg)
        details["failed_checks"].append(msg)

    # Check 2: Decision alignment
    decision_match, msg = check_decision_alignment(classification, scenario.expected_decision)
    print(msg)
    if decision_match:
        details["passed_checks"].append("Decision matches expected")
    else:
        details["failed_checks"].append(f"Decision mismatch: expected {scenario.expected_decision}")

    # Check 3: Confidence range
    conf_match, msg = check_confidence_range(
        confidence,
        scenario.expected_confidence_min,
        scenario.expected_confidence_max
    )
    print(msg)
    if conf_match:
        details["passed_checks"].append("Confidence in expected range")
    else:
        details["failed_checks"].append(f"Confidence {confidence}% outside range")

    # Check 4: Risk level alignment
    if risk_level.lower() == scenario.expected_risk_level.lower():
        print_success(f"✓ Risk level matches ({risk_level})")
        details["passed_checks"].append("Risk level matches expected")
    else:
        print_warning(f"⚠️  Risk level mismatch (expected {scenario.expected_risk_level}, got {risk_level})")
        details["warnings"].append(f"Risk level mismatch")

    # Additional analysis
    analysis_text = analyze_decision_factors(response, scenario.name)
    print(analysis_text)

    # Determine overall result
    if len(details["failed_checks"]) == 0:
        result = TestResult.PASS
        print_success(f"\n✅ {scenario.name} PASSED")
    elif len(details["failed_checks"]) == 1 and "Decision mismatch" not in details["failed_checks"][0]:
        result = TestResult.PARTIAL
        print_warning(f"\n⚠️  {scenario.name} PARTIAL PASS")
    else:
        result = TestResult.FAIL
        print_error(f"\n❌ {scenario.name} FAILED")

    details["test_result"] = result
    return result, details


def run_all_tests(verbose: bool = False, save_results: bool = False) -> Dict[str, Any]:
    """
    Run all test scenarios

    Returns:
        Dictionary with test summary and results
    """
    print_header("LOAN APPROVAL SYSTEM - COMPREHENSIVE TEST SUITE")

    # Check API connection
    print_section("Pre-Test Verification")
    print_info("Checking API connectivity...")

    if not check_api_health():
        print_error("Cannot connect to API")
        print_info("Ensure FastAPI server is running: python src/api/main.py")
        sys.exit(1)

    print_success("API is healthy and running")

    # Run all tests
    print_header("Running Test Scenarios")

    results = {
        "test_suite": "Loan Approval System",
        "timestamp": datetime.now().isoformat(),
        "total_scenarios": len(SCENARIOS),
        "results": [],
        "summary": {
            "passed": 0,
            "failed": 0,
            "partial": 0,
            "error": 0
        }
    }

    for scenario in SCENARIOS:
        result, details = run_single_test(scenario)
        results["results"].append({
            "scenario": scenario.name,
            "expected_decision": scenario.expected_decision,
            "actual_decision": details["decision"],
            "result": result.value,
            "details": details
        })

        # Update summary
        if result == TestResult.PASS:
            results["summary"]["passed"] += 1
        elif result == TestResult.FAIL:
            results["summary"]["failed"] += 1
        elif result == TestResult.PARTIAL:
            results["summary"]["partial"] += 1
        elif result == TestResult.ERROR:
            results["summary"]["error"] += 1

        # Add spacing between tests
        time.sleep(1)

    # Print summary
    print_header("TEST SUMMARY")

    print(f"Total Scenarios: {results['total_scenarios']}")
    print(f"{Colors.GREEN}✅ Passed: {results['summary']['passed']}{Colors.END}")
    if results['summary']['partial'] > 0:
        print(f"{Colors.YELLOW}⚠️  Partial: {results['summary']['partial']}{Colors.END}")
    if results['summary']['failed'] > 0:
        print(f"{Colors.RED}❌ Failed: {results['summary']['failed']}{Colors.END}")
    if results['summary']['error'] > 0:
        print(f"{Colors.RED}❌ Error: {results['summary']['error']}{Colors.END}")

    # Print scenario details
    print_section("Scenario Results")
    for result in results["results"]:
        status = result["result"]
        icon = "✅" if status == "PASS" else ("⚠️" if status == "PARTIAL" else "❌")
        print(f"{icon} {result['scenario']}")
        print(f"   Expected: {result['expected_decision']}")
        print(f"   Actual: {result['actual_decision']}")
        print(f"   Status: {status}")

    # Save results if requested
    if save_results:
        results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print_success(f"\nResults saved to {results_file}")

    return results


# ==================== Main Entry Point ====================

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Loan Approval System - Comprehensive Test Suite"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose output"
    )
    parser.add_argument(
        "--save-results",
        action="store_true",
        help="Save test results to JSON file"
    )

    args = parser.parse_args()

    try:
        results = run_all_tests(
            verbose=args.verbose,
            save_results=args.save_results
        )

        # Exit with appropriate code
        if results["summary"]["failed"] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print_error("\n\nTest suite interrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
