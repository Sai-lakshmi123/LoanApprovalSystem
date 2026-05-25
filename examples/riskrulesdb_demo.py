#!/usr/bin/env python3
"""
RiskRulesDB Demo
Demonstrates financial risk evaluation with DTI analysis, credit risk,
loan amount risk, and anomaly detection.

Run the server first:
    python mcp/riskrulesdb/server.py

Then run this demo:
    python examples/riskrulesdb_demo.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.riskrulesdb.client import RiskRulesDBSyncClient
import json


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_section(text: str):
    """Print formatted section."""
    print(f"\n>>> {text}")
    print("-" * 80)


def demo_dti_analysis():
    """Demo: DTI Analysis"""
    print_header("DEMO 1: DEBT-TO-INCOME RATIO ANALYSIS")

    client = RiskRulesDBSyncClient()

    # Test cases with different DTI levels
    test_cases = [
        {"monthly_income": 5000, "monthly_debt": 800, "label": "Excellent DTI"},
        {"monthly_income": 5000, "monthly_debt": 1500, "label": "Good DTI"},
        {"monthly_income": 5000, "monthly_debt": 2150, "label": "Acceptable DTI"},
        {"monthly_income": 5000, "monthly_debt": 2500, "label": "High DTI"},
        {"monthly_income": 5000, "monthly_debt": 2700, "label": "Very High DTI"},
    ]

    for test in test_cases:
        result = client.evaluate_dti_ratio(
            test["monthly_income"],
            test["monthly_debt"]
        )

        if result.get('status') == 'success':
            analysis = result['analysis']
            print_section(test['label'])
            print(f"  Monthly Income: ${test['monthly_income']:,.2f}")
            print(f"  Monthly Debt: ${test['monthly_debt']:,.2f}")
            print(f"  DTI Ratio: {analysis['dti_ratio']:.4f}")
            print(f"  DTI Percentage: {analysis['dti_percentage']:.2f}%")
            print(f"  Risk Level: {analysis['risk_level']}")
            print(f"  Category: {analysis['category']}")
            print(f"  Conventional Eligible: {analysis['acceptable_for_conventional']}")
            print(f"  FHA Eligible: {analysis['acceptable_for_fha']}")
            print(f"  Reasoning: {analysis['reasoning']}")


def demo_credit_risk_analysis():
    """Demo: Credit Risk Analysis"""
    print_header("DEMO 2: CREDIT RISK ANALYSIS")

    client = RiskRulesDBSyncClient()

    # Test cases with different credit profiles
    test_cases = [
        {
            "credit_score": 800,
            "delinquencies": 0,
            "inquiries": 0,
            "label": "Excellent Credit"
        },
        {
            "credit_score": 720,
            "delinquencies": 0,
            "inquiries": 1,
            "label": "Good Credit"
        },
        {
            "credit_score": 670,
            "delinquencies": 0,
            "inquiries": 2,
            "label": "Fair Credit"
        },
        {
            "credit_score": 620,
            "delinquencies": 1,
            "inquiries": 3,
            "label": "Poor Credit with Issues"
        },
        {
            "credit_score": 550,
            "delinquencies": 2,
            "inquiries": 5,
            "label": "Very Poor Credit"
        },
    ]

    for test in test_cases:
        result = client.evaluate_credit_risk(
            test["credit_score"],
            test["delinquencies"],
            test["inquiries"]
        )

        if result.get('status') == 'success':
            analysis = result['analysis']
            print_section(test['label'])
            print(f"  Credit Score: {analysis['credit_score']}")
            print(f"  Category: {analysis['category']}")
            print(f"  Base Risk: {analysis['base_risk_level']}")
            print(f"  Delinquencies: {analysis['delinquencies']} (Penalty: {analysis['delinquency_penalty']})")
            print(f"  Recent Inquiries: {analysis['recent_inquiries']} (Penalty: {analysis['inquiry_penalty']})")
            print(f"  Adjusted Risk Score: {analysis['adjusted_risk_score']}/100")
            print(f"  Final Risk Level: {analysis['final_risk_level']}")
            print(f"  Reasoning: {analysis['reasoning']}")


def demo_loan_amount_risk():
    """Demo: Loan Amount Risk Analysis"""
    print_header("DEMO 3: LOAN AMOUNT RISK ANALYSIS")

    client = RiskRulesDBSyncClient()

    print_section("Conservative Loan Request")
    result = client.evaluate_loan_amount_risk(
        loan_amount=200000,
        annual_income=100000,
        property_value=400000,
        existing_loans=0,
        credit_score=750
    )
    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"  Loan Amount: ${analysis['loan_amount']:,.0f}")
        print(f"  Annual Income: ${analysis['annual_income']:,.0f}")
        print(f"  LTI Ratio: {analysis['lti_ratio']:.4f} ({analysis['lti_percentage']:.2f}%)")
        print(f"  LTI Risk: {analysis['lti_risk']}")
        print(f"  LTV Ratio: {analysis['ltv_ratio']:.4f} ({analysis['ltv_percentage']:.2f}%)")
        print(f"  LTV Risk: {analysis['ltv_risk']}")
        print(f"  Existing Loans: {analysis['existing_loans']}")
        print(f"  Overall Loan Risk: {analysis['overall_loan_risk']}")

    print_section("Aggressive Loan Request")
    result = client.evaluate_loan_amount_risk(
        loan_amount=400000,
        annual_income=100000,
        property_value=400000,
        existing_loans=2,
        credit_score=650
    )
    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"  Loan Amount: ${analysis['loan_amount']:,.0f}")
        print(f"  Annual Income: ${analysis['annual_income']:,.0f}")
        print(f"  LTI Ratio: {analysis['lti_ratio']:.4f} ({analysis['lti_percentage']:.2f}%)")
        print(f"  LTI Risk: {analysis['lti_risk']}")
        print(f"  LTV Ratio: {analysis['ltv_ratio']:.4f} ({analysis['ltv_percentage']:.2f}%)")
        print(f"  LTV Risk: {analysis['ltv_risk']}")
        print(f"  Existing Loans: {analysis['existing_loans']}")
        print(f"  Debt Burden: {analysis['debt_burden']}")
        print(f"  Overall Loan Risk: {analysis['overall_loan_risk']}")


def demo_anomaly_detection():
    """Demo: Anomaly Detection"""
    print_header("DEMO 4: ANOMALY DETECTION")

    client = RiskRulesDBSyncClient()

    print_section("Applicant with Clean Profile")
    applicant = {
        "credit_score": 750,
        "delinquencies": 0,
        "recent_delinquencies": 0,
        "inquiries_last_6_months": 0,
        "credit_utilization": 0.25,
        "years_at_current_job": 5,
        "age": 40
    }
    loan_request = {
        "loan_amount": 200000,
        "property_value": 400000
    }

    result = client.detect_risk_anomalies(applicant, loan_request)
    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"  Has Anomalies: {analysis['has_anomalies']}")
        print(f"  Anomaly Count: {analysis['anomaly_count']}")
        print(f"  Overall Anomaly Score: {analysis['overall_anomaly_score']}/100")
        print(f"  Risk Level: {analysis['overall_anomaly_risk_level']}")

    print_section("Applicant with Risk Flags")
    applicant_risky = {
        "credit_score": 600,
        "delinquencies": 1,
        "recent_delinquencies": 1,
        "inquiries_last_6_months": 6,
        "credit_utilization": 0.90,
        "years_at_current_job": 0.3,
        "age": 28
    }
    loan_request_large = {
        "loan_amount": 500000,
        "property_value": 400000
    }

    result = client.detect_risk_anomalies(applicant_risky, loan_request_large)
    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"  Has Anomalies: {analysis['has_anomalies']}")
        print(f"  Anomaly Count: {analysis['anomaly_count']}")
        print(f"  Overall Anomaly Score: {analysis['overall_anomaly_score']}/100")
        print(f"  Risk Level: {analysis['overall_anomaly_risk_level']}")
        print(f"\n  Detected Anomalies:")
        for anomaly in analysis['anomalies']:
            print(f"    • {anomaly['type']} ({anomaly['severity']})")
            print(f"      {anomaly['description']}")


def demo_comprehensive_risk_report():
    """Demo: Comprehensive Risk Report"""
    print_header("DEMO 5: COMPREHENSIVE RISK REPORT")

    client = RiskRulesDBSyncClient()

    print_section("Strong Applicant Profile")
    applicant = {
        "name": "John Strong",
        "age": 45,
        "annual_income": 150000,
        "monthly_expenses": 4000,
        "existing_monthly_debt": 1000,
        "credit_score": 760,
        "delinquencies": 0,
        "recent_delinquencies": 0,
        "inquiries_last_6_months": 1,
        "credit_utilization": 0.30,
        "years_at_current_job": 8,
        "existing_loans": 1
    }
    loan_request = {
        "loan_amount": 300000,
        "loan_term_months": 360,
        "property_value": 500000
    }

    result = client.generate_risk_report("APP_STRONG", applicant, loan_request)
    if result.get('status') == 'success':
        report = result
        print(f"  Status: {report['status']}")
        print(f"  Applicant ID: {report['applicant_id']}")
        print(f"\n  DTI Analysis:")
        print(f"    Current DTI: {report['dti_analysis']['dti_percentage']:.2f}%")
        print(f"    With New Loan: {report['dti_with_new_loan']['dti_percentage']:.2f}%")
        print(f"\n  Credit Risk: {report['credit_score_risk']['final_risk_level']}")
        print(f"  Loan Amount Risk: {report['loan_amount_risk']['overall_loan_risk']}")
        print(f"\n  Anomalies Detected: {report['anomaly_detection']['anomaly_count']}")
        print(f"  Overall Risk Level: {report['overall_risk_assessment']['overall_risk_level']}")
        print(f"  Overall Risk Score: {report['overall_risk_assessment']['overall_risk_score']}/5")
        print(f"\n  Recommendation: {report['overall_risk_assessment']['approval_recommendation']}")
        print(f"\n  Summary: {report['summary']}")


def demo_scenario_analysis():
    """Demo: Scenario Analysis"""
    print_header("DEMO 6: SCENARIO ANALYSIS")

    client = RiskRulesDBSyncClient()

    applicant = {
        "name": "Jane Doe",
        "age": 35,
        "annual_income": 80000,
        "monthly_expenses": 2500,
        "existing_monthly_debt": 500,
        "credit_score": 700,
        "delinquencies": 0,
        "inquiries_last_6_months": 1,
        "credit_utilization": 0.45,
        "years_at_current_job": 3,
        "existing_loans": 1
    }

    base_loan_request = {
        "loan_amount": 250000,
        "loan_term_months": 360,
        "property_value": 400000
    }

    scenarios = [
        {"name": "Conservative (80%)", "loan_amount": 200000},
        {"name": "Requested (100%)", "loan_amount": 250000},
        {"name": "Aggressive (120%)", "loan_amount": 300000},
    ]

    result = client.evaluate_with_scenario_analysis(
        "APP_SCENARIOS",
        applicant,
        base_loan_request,
        scenarios
    )

    if result.get('status') == 'success':
        print(f"  Applicant: APP_SCENARIOS")
        print(f"  Annual Income: ${applicant['annual_income']:,.0f}")
        print(f"  Credit Score: {applicant['credit_score']}")
        print(f"\n  Scenario Comparison:")
        print(f"  {'Scenario':<25} {'Loan Amount':<20} {'DTI':<12} {'Risk Level':<15}")
        print(f"  {'-'*25} {'-'*20} {'-'*12} {'-'*15}")

        for scenario in result['alternative_scenarios']:
            print(f"  {scenario['scenario']:<25} ${scenario['loan_amount']:>15,.0f}  {scenario['dti_percentage']:>10.2f}%  {scenario['risk_level']:<15}")


def demo_resources():
    """Demo: Access Reference Resources"""
    print_header("DEMO 7: REFERENCE RESOURCES")

    client = RiskRulesDBSyncClient()

    print_section("DTI Guidelines")
    guidelines = client.get_dti_guidelines()
    print(f"  Excellent: {guidelines['thresholds']['excellent']['range']}")
    print(f"  Good: {guidelines['thresholds']['good']['range']}")
    print(f"  Acceptable: {guidelines['thresholds']['acceptable']['range']}")
    print(f"  High Risk: {guidelines['thresholds']['high_risk']['range']}")
    print(f"  Very High Risk: {guidelines['thresholds']['very_high_risk']['range']}")

    print_section("Credit Assessment Criteria")
    criteria = client.get_credit_assessment_criteria()
    print(f"  Excellent (750-850): {criteria['score_ranges']['excellent']['default_probability']} default probability")
    print(f"  Good (700-749): {criteria['score_ranges']['good']['default_probability']} default probability")
    print(f"  Fair (650-699): {criteria['score_ranges']['fair']['default_probability']} default probability")
    print(f"  Poor (600-649): {criteria['score_ranges']['poor']['default_probability']} default probability")

    print_section("Loan Risk Criteria")
    loan_criteria = client.get_loan_risk_criteria()
    print(f"  LTI Excellent: {loan_criteria['lti_guidelines']['excellent']}")
    print(f"  LTI Good: {loan_criteria['lti_guidelines']['good']}")
    print(f"  LTI Acceptable: {loan_criteria['lti_guidelines']['acceptable']}")
    print(f"  LTI High Risk: {loan_criteria['lti_guidelines']['high_risk']}")

    print_section("Anomaly Detection Rules")
    rules = client.get_anomaly_rules()
    print(f"  High DTI: Trigger {rules['anomaly_types']['high_dti']['trigger']} ({rules['anomaly_types']['high_dti']['severity']})")
    print(f"  Low Credit: Trigger {rules['anomaly_types']['low_credit']['trigger']} ({rules['anomaly_types']['low_credit']['severity']})")
    print(f"  Recent Delinquency: Trigger {rules['anomaly_types']['recent_delinquency']['trigger']} ({rules['anomaly_types']['recent_delinquency']['severity']})")


def main():
    """Run all demos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║            RISKRULESDB DEMO - FINANCIAL RISK EVALUATION ENGINE                ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        demo_dti_analysis()
        demo_credit_risk_analysis()
        demo_loan_amount_risk()
        demo_anomaly_detection()
        demo_comprehensive_risk_report()
        demo_scenario_analysis()
        demo_resources()

        print_header("DEMO COMPLETE")
        print("\n✅ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("  1. Use RiskRulesDB in your agents: from mcp.riskrulesdb.client import RiskRulesDBSyncClient")
        print("  2. Integrate with FastAPI for loan approval decisions")
        print("  3. Use with LangGraph for intelligent risk-based routing")
        print("  4. Combine with Application DB for complete applicant analysis")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the RiskRulesDB server is running:")
        print("  python mcp/riskrulesdb/server.py")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
