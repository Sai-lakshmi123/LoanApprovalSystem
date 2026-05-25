#!/usr/bin/env python3
"""
Agent2 Usage Examples
Demonstrates various ways to use the Financial Risk Analysis Agent

Run the RiskRulesDB server first:
    python mcp/riskrulesdb/server.py

Then run this example:
    python examples/agent2_usage_example.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent
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


def example1_single_risk_analysis():
    """Example 1: Analyze financial risk for single applicant"""
    print_header("EXAMPLE 1: FINANCIAL RISK ANALYSIS")

    agent = FinancialRiskAnalysisAgent()

    print_section("Analyzing Financial Risk for APP001")

    result = agent.analyze_financial_risk(
        applicant_id="APP001",
        applicant_data={
            "name": "John Strong",
            "age": 45,
            "annual_income": 150000,
            "monthly_expenses": 4000,
            "existing_monthly_debt": 1000,
            "credit_score": 760,
            "delinquencies": 0,
            "inquiries_last_6_months": 1,
            "credit_utilization": 0.30,
            "years_at_current_job": 8,
            "existing_loans": 1
        },
        loan_request={
            "loan_amount": 300000,
            "property_value": 500000,
            "loan_term_months": 360
        }
    )

    if result["status"] == "success":
        analysis = result["analysis"]

        print("\n✅ Analysis Complete")

        # DTI Analysis
        dti_info = analysis.get("dti_analysis", {})
        print(f"\n📊 Debt-to-Income (DTI) Analysis:")
        print(f"   Current DTI: {dti_info.get('current_dti_percentage', 'N/A'):.1f}%")
        print(f"   With New Loan: {dti_info.get('dti_with_new_loan_percentage', 'N/A'):.1f}%")
        print(f"   Risk Level: {dti_info.get('dti_risk_level', 'N/A')}")

        # Credit Risk
        credit_info = analysis.get("credit_risk", {})
        print(f"\n📊 Credit Risk Assessment:")
        print(f"   Credit Score: {credit_info.get('credit_score', 'N/A')}")
        print(f"   Base Risk: {credit_info.get('base_risk_level', 'N/A')}")
        print(f"   Adjusted Risk: {credit_info.get('adjusted_risk_level', 'N/A')}")
        print(f"   Delinquencies: {credit_info.get('delinquencies', 'N/A')}")

        # Loan Amount Risk
        loan_info = analysis.get("loan_amount_risk", {})
        print(f"\n📊 Loan Amount Risk:")
        print(f"   Loan Amount: ${loan_info.get('loan_amount', 'N/A'):,.0f}")
        print(f"   LTI: {loan_info.get('lti_percentage', 'N/A'):.2f}%")
        print(f"   LTV: {loan_info.get('ltv_percentage', 'N/A'):.2f}%")
        print(f"   Overall Risk: {loan_info.get('overall_loan_risk', 'N/A')}")

        # Anomalies
        anomaly_info = analysis.get("anomaly_detection", {})
        print(f"\n📊 Anomaly Detection:")
        print(f"   Count: {anomaly_info.get('anomaly_count', 0)}")
        print(f"   Has Critical: {anomaly_info.get('has_critical_anomalies', False)}")
        if anomaly_info.get('anomalies'):
            for anomaly in anomaly_info['anomalies'][:3]:
                print(f"   • {anomaly.get('type')} ({anomaly.get('severity')})")

        # Overall Assessment
        overall = analysis.get("aggregate_risk_assessment", {})
        print(f"\n📊 Aggregate Risk Assessment:")
        print(f"   Risk Score: {overall.get('overall_risk_score', 'N/A')}/5")
        print(f"   Risk Level: {overall.get('overall_risk_level', 'N/A')}")
        print(f"   Recommendation: {overall.get('recommendation', 'N/A')}")

        print(f"\n📋 Summary:")
        print(f"   {analysis.get('financial_summary', 'N/A')}")


def example2_batch_risk_analysis():
    """Example 2: Analyze multiple applicants"""
    print_header("EXAMPLE 2: BATCH RISK ANALYSIS")

    agent = FinancialRiskAnalysisAgent()

    test_cases = [
        {
            "applicant_id": "APP001",
            "applicant_data": {
                "annual_income": 150000,
                "monthly_expenses": 4000,
                "existing_monthly_debt": 1000,
                "credit_score": 760,
                "delinquencies": 0,
                "inquiries_last_6_months": 1,
                "credit_utilization": 0.30,
                "years_at_current_job": 8,
                "existing_loans": 1
            },
            "loan_request": {
                "loan_amount": 300000,
                "property_value": 500000,
                "loan_term_months": 360
            }
        },
        {
            "applicant_id": "APP002",
            "applicant_data": {
                "annual_income": 80000,
                "monthly_expenses": 2500,
                "existing_monthly_debt": 500,
                "credit_score": 700,
                "delinquencies": 0,
                "inquiries_last_6_months": 1,
                "credit_utilization": 0.45,
                "years_at_current_job": 3,
                "existing_loans": 1
            },
            "loan_request": {
                "loan_amount": 250000,
                "property_value": 400000,
                "loan_term_months": 360
            }
        }
    ]

    print_section("Analyzing Multiple Applicants")

    results = {}
    for test_case in test_cases:
        applicant_id = test_case["applicant_id"]
        print(f"\nAnalyzing {applicant_id}...")

        result = agent.analyze_financial_risk(
            applicant_id,
            test_case["applicant_data"],
            test_case["loan_request"]
        )
        results[applicant_id] = result

        if result["status"] == "success":
            analysis = result["analysis"]
            dti = analysis.get("dti_analysis", {}).get("dti_with_new_loan_percentage")
            risk_score = analysis.get("aggregate_risk_assessment", {}).get("overall_risk_score")
            recommendation = analysis.get("aggregate_risk_assessment", {}).get("recommendation")

            print(f"  ✅ DTI: {dti:.1f}%, Risk: {risk_score:.1f}/5, Rec: {recommendation}")

    # Summary
    print_section("Summary")
    print(f"Total Analyzed: {len(test_cases)}")
    print(f"Successful: {sum(1 for r in results.values() if r['status'] == 'success')}")


def example3_risk_comparison():
    """Example 3: Compare risk profiles"""
    print_header("EXAMPLE 3: RISK PROFILE COMPARISON")

    agent = FinancialRiskAnalysisAgent()

    test_cases = [
        {
            "id": "Strong Profile",
            "applicant_id": "STRONG",
            "applicant_data": {
                "annual_income": 200000,
                "existing_monthly_debt": 1000,
                "credit_score": 780,
                "delinquencies": 0,
                "inquiries_last_6_months": 0,
                "credit_utilization": 0.20,
                "years_at_current_job": 10,
                "existing_loans": 1
            },
            "loan_request": {
                "loan_amount": 300000,
                "property_value": 600000,
                "loan_term_months": 360
            }
        },
        {
            "id": "Weak Profile",
            "applicant_id": "WEAK",
            "applicant_data": {
                "annual_income": 60000,
                "existing_monthly_debt": 1500,
                "credit_score": 620,
                "delinquencies": 1,
                "inquiries_last_6_months": 3,
                "credit_utilization": 0.80,
                "years_at_current_job": 1,
                "existing_loans": 2
            },
            "loan_request": {
                "loan_amount": 200000,
                "property_value": 250000,
                "loan_term_months": 360
            }
        }
    ]

    print_section("Comparing Risk Profiles")

    analyses = {}
    for test_case in test_cases:
        result = agent.analyze_financial_risk(
            test_case["applicant_id"],
            test_case["applicant_data"],
            test_case["loan_request"]
        )

        if result["status"] == "success":
            analyses[test_case["id"]] = result["analysis"]

    # Comparison
    if len(analyses) == 2:
        profile_names = list(analyses.keys())
        strong = analyses[profile_names[0]]
        weak = analyses[profile_names[1]]

        print(f"\nComparison: {profile_names[0]} vs {profile_names[1]}")
        print(f"\n{'Metric':<30} {profile_names[0]:<20} {profile_names[1]:<20}")
        print("-" * 70)

        # DTI
        dti1 = strong["dti_analysis"]["dti_with_new_loan_percentage"]
        dti2 = weak["dti_analysis"]["dti_with_new_loan_percentage"]
        print(f"{'DTI':<30} {dti1:<20.1f}% {dti2:<20.1f}%")

        # Credit
        credit1 = strong["credit_risk"]["credit_score"]
        credit2 = weak["credit_risk"]["credit_score"]
        print(f"{'Credit Score':<30} {credit1:<20} {credit2:<20}")

        # LTI
        lti1 = strong["loan_amount_risk"]["lti_percentage"]
        lti2 = weak["loan_amount_risk"]["lti_percentage"]
        print(f"{'LTI':<30} {lti1:<20.2f}% {lti2:<20.2f}%")

        # Risk Score
        risk1 = strong["aggregate_risk_assessment"]["overall_risk_score"]
        risk2 = weak["aggregate_risk_assessment"]["overall_risk_score"]
        print(f"{'Overall Risk Score':<30} {risk1:<20.1f}/5 {risk2:<20.1f}/5")

        # Recommendation
        rec1 = strong["aggregate_risk_assessment"]["recommendation"]
        rec2 = weak["aggregate_risk_assessment"]["recommendation"]
        print(f"{'Recommendation':<30} {rec1:<20} {rec2:<20}")


def example4_key_findings():
    """Example 4: Extract key findings and conditions"""
    print_header("EXAMPLE 4: KEY FINDINGS AND CONDITIONS")

    agent = FinancialRiskAnalysisAgent()

    print_section("Extracting Key Findings")

    result = agent.analyze_financial_risk(
        "APP001",
        {
            "annual_income": 150000,
            "monthly_expenses": 4000,
            "existing_monthly_debt": 1000,
            "credit_score": 760,
            "delinquencies": 0,
            "inquiries_last_6_months": 1,
            "credit_utilization": 0.30,
            "years_at_current_job": 8,
            "existing_loans": 1
        },
        {
            "loan_amount": 300000,
            "property_value": 500000,
            "loan_term_months": 360
        }
    )

    if result["status"] == "success":
        analysis = result["analysis"]

        print("\nKey Findings:")
        for finding in analysis.get("key_findings", []):
            print(f"  • {finding}")

        print("\nMitigating Factors:")
        for factor in analysis.get("aggregate_risk_assessment", {}).get("mitigating_factors", []):
            print(f"  ✅ {factor}")

        print("\nPrimary Risk Factors:")
        factors = analysis.get("aggregate_risk_assessment", {}).get("primary_risk_factors", [])
        if factors:
            for factor in factors:
                print(f"  ❌ {factor}")
        else:
            print("  None identified")

        print("\nRecommended Conditions:")
        conditions = analysis.get("recommended_conditions", [])
        if conditions:
            for condition in conditions:
                print(f"  • {condition}")
        else:
            print("  No conditions required")

        print("\nNext Steps:")
        for step in analysis.get("next_steps", []):
            print(f"  → {step}")


def example5_json_export():
    """Example 5: Export analysis as JSON"""
    print_header("EXAMPLE 5: JSON EXPORT")

    agent = FinancialRiskAnalysisAgent()

    print_section("Exporting Risk Analysis as JSON")

    result = agent.analyze_financial_risk(
        "APP001",
        {
            "annual_income": 150000,
            "existing_monthly_debt": 1000,
            "credit_score": 760,
            "delinquencies": 0,
            "inquiries_last_6_months": 1,
            "credit_utilization": 0.30,
            "years_at_current_job": 8,
            "existing_loans": 1
        },
        {
            "loan_amount": 300000,
            "property_value": 500000,
            "loan_term_months": 360
        }
    )

    if result["status"] == "success":
        analysis = result["analysis"]
        json_output = json.dumps(analysis, indent=2)

        print("\nJSON Structure (first 500 chars):")
        print(json_output[:500] + "...\n")

        print("To save to file:")
        print("  with open('risk_analysis.json', 'w') as f:")
        print("      json.dump(analysis, f, indent=2)")


def main():
    """Run all examples."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║              AGENT2 USAGE EXAMPLES - FINANCIAL RISK ANALYSIS                   ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        example1_single_risk_analysis()
        example2_batch_risk_analysis()
        example3_risk_comparison()
        example4_key_findings()
        example5_json_export()

        print_header("EXAMPLES COMPLETE")
        print("\n✅ All examples completed successfully!")
        print("\nNext Steps:")
        print("  1. Review the risk analysis output format")
        print("  2. Integrate Agent2 with Agent1 results")
        print("  3. Create Agent3 (Decision Synthesis Agent)")
        print("  4. Build multi-agent orchestration")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. RiskRulesDB server is running: python mcp/riskrulesdb/server.py")
        print("  2. ANTHROPIC_API_KEY is set")
        print("  3. All dependencies are installed")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
