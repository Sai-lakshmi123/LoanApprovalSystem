#!/usr/bin/env python3
"""
Agent1 Usage Examples
Demonstrates various ways to use the Application Profile Agent

Run the Application DB server first:
    python mcp/server.py

Then run this example:
    python examples/agent1_usage_example.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.application_profile_agent import ApplicationProfileAgent
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


def example1_single_applicant():
    """Example 1: Analyze a single applicant"""
    print_header("EXAMPLE 1: ANALYZE SINGLE APPLICANT")

    agent = ApplicationProfileAgent()

    print_section("Analyzing Applicant APP001")

    result = agent.analyze_applicant("APP001")

    if result["status"] == "success":
        analysis = result["analysis"]

        print("\n✅ Analysis Complete")
        print(f"\nApplicant: {analysis.get('applicant_name', 'N/A')}")
        print(f"Timestamp: {analysis.get('analysis_timestamp', 'N/A')}")

        # Income Stability
        income_info = analysis.get("income_stability", {})
        print(f"\n📊 Income Stability:")
        print(f"   Score: {income_info.get('score', 'N/A')}/100")
        print(f"   Category: {income_info.get('stability_category', 'N/A')}")
        print(f"   Analysis: {income_info.get('analysis', 'N/A')[:100]}...")

        # Employment Risk
        emp_info = analysis.get("employment_risk", {})
        print(f"\n📊 Employment Risk:")
        print(f"   Risk Score: {emp_info.get('risk_score', 'N/A')}/100")
        print(f"   Risk Level: {emp_info.get('risk_level', 'N/A')}")
        print(f"   Employment Type: {emp_info.get('employment_type', 'N/A')}")
        print(f"   Tenure: {emp_info.get('tenure_years', 'N/A')} years")

        # Credit History
        credit_info = analysis.get("credit_history", {})
        print(f"\n📊 Credit History:")
        print(f"   Credit Score: {credit_info.get('credit_score', 'N/A')}")
        print(f"   Category: {credit_info.get('score_category', 'N/A')}")
        print(f"   Delinquencies: {credit_info.get('delinquencies', 'N/A')}")
        print(f"   Utilization: {credit_info.get('credit_utilization', 'N/A')}%")

        # Completeness
        comp_info = analysis.get("application_completeness", {})
        print(f"\n📊 Application Completeness:")
        print(f"   Completion: {comp_info.get('completeness_percentage', 'N/A')}%")
        print(f"   Complete: {'Yes' if comp_info.get('is_complete') else 'No'}")
        if comp_info.get('missing_items'):
            print(f"   Missing Items: {', '.join(comp_info['missing_items'])}")

        # Overall Assessment
        print(f"\n📋 Overall Assessment:")
        print(f"   {analysis.get('overall_assessment', 'N/A')}")

        # Key Strengths
        if analysis.get('key_strengths'):
            print(f"\n✅ Key Strengths:")
            for strength in analysis['key_strengths']:
                print(f"   • {strength}")

        # Key Concerns
        if analysis.get('key_concerns'):
            print(f"\n⚠️  Key Concerns:")
            for concern in analysis['key_concerns']:
                print(f"   • {concern}")

        # Recommendations
        if analysis.get('recommended_next_steps'):
            print(f"\n🎯 Recommended Next Steps:")
            for step in analysis['recommended_next_steps']:
                print(f"   • {step}")


def example2_batch_analysis():
    """Example 2: Analyze multiple applicants"""
    print_header("EXAMPLE 2: BATCH ANALYSIS")

    agent = ApplicationProfileAgent()

    applicants = ["APP001", "APP002", "APP003"]
    results = {}

    print_section("Analyzing Multiple Applicants")

    for applicant_id in applicants:
        print(f"\nAnalyzing {applicant_id}...")
        result = agent.analyze_applicant(applicant_id)
        results[applicant_id] = result

        if result["status"] == "success":
            analysis = result["analysis"]
            income = analysis.get("income_stability", {}).get("score", "N/A")
            employment = analysis.get("employment_risk", {}).get("risk_level", "N/A")
            credit = analysis.get("credit_history", {}).get("credit_score", "N/A")

            print(f"  ✅ {applicant_id}: Income={income}, Employment={employment}, Credit={credit}")
        else:
            print(f"  ❌ {applicant_id}: Error - {result.get('message', 'Unknown error')}")

    # Summary
    print_section("Summary")
    print(f"Total Analyzed: {len(applicants)}")
    print(f"Successful: {sum(1 for r in results.values() if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results.values() if r['status'] != 'success')}")


def example3_extract_metrics():
    """Example 3: Extract specific metrics"""
    print_header("EXAMPLE 3: EXTRACT SPECIFIC METRICS")

    agent = ApplicationProfileAgent()

    print_section("Extracting Individual Metrics")

    result = agent.analyze_applicant("APP001")

    if result["status"] == "success":
        analysis = result["analysis"]

        # Extract specific values
        income_score = analysis["income_stability"]["score"]
        employment_risk = analysis["employment_risk"]["risk_score"]
        credit_score = analysis["credit_history"]["credit_score"]
        completeness = analysis["application_completeness"]["completeness_percentage"]

        print(f"\nExtracted Metrics:")
        print(f"  Income Stability Score: {income_score}")
        print(f"  Employment Risk Score: {employment_risk}")
        print(f"  Credit Score: {credit_score}")
        print(f"  Completeness Percentage: {completeness}")

        # Determine overall risk
        avg_risk = (income_score + employment_risk) / 2
        if avg_risk < 40:
            risk_level = "LOW"
        elif avg_risk < 60:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        print(f"\n  Calculated Overall Risk Level: {risk_level}")


def example4_comparison():
    """Example 4: Compare applicants"""
    print_header("EXAMPLE 4: APPLICANT COMPARISON")

    agent = ApplicationProfileAgent()

    applicants_to_compare = ["APP001", "APP002"]
    analyses = {}

    print_section("Comparing Applicants")

    for applicant_id in applicants_to_compare:
        result = agent.analyze_applicant(applicant_id)
        if result["status"] == "success":
            analyses[applicant_id] = result["analysis"]

    if len(analyses) == 2:
        app1_id, app2_id = applicants_to_compare
        app1 = analyses[app1_id]
        app2 = analyses[app2_id]

        print(f"\nComparison: {app1_id} vs {app2_id}")
        print(f"\n{'Metric':<30} {app1_id:<15} {app2_id:<15}")
        print("-" * 60)

        # Income Stability
        income1 = app1["income_stability"]["score"]
        income2 = app2["income_stability"]["score"]
        print(f"{'Income Stability':<30} {income1:<15} {income2:<15}")

        # Employment Risk
        emp1 = app1["employment_risk"]["risk_score"]
        emp2 = app2["employment_risk"]["risk_score"]
        print(f"{'Employment Risk':<30} {emp1:<15} {emp2:<15}")

        # Credit Score
        credit1 = app1["credit_history"]["credit_score"]
        credit2 = app2["credit_history"]["credit_score"]
        print(f"{'Credit Score':<30} {credit1:<15} {credit2:<15}")

        # Completeness
        comp1 = app1["application_completeness"]["completeness_percentage"]
        comp2 = app2["application_completeness"]["completeness_percentage"]
        print(f"{'Completeness %':<30} {comp1:<15} {comp2:<15}")

        # Analysis
        print(f"\n📊 Analysis:")
        if income1 > income2:
            print(f"  {app1_id} has better income stability")
        else:
            print(f"  {app2_id} has better income stability")

        if emp1 < emp2:
            print(f"  {app1_id} has lower employment risk")
        else:
            print(f"  {app2_id} has lower employment risk")

        if credit1 > credit2:
            print(f"  {app1_id} has better credit profile")
        else:
            print(f"  {app2_id} has better credit profile")


def example5_json_export():
    """Example 5: Export results as JSON"""
    print_header("EXAMPLE 5: JSON EXPORT")

    agent = ApplicationProfileAgent()

    print_section("Exporting Analysis as JSON")

    result = agent.analyze_applicant("APP001")

    if result["status"] == "success":
        analysis = result["analysis"]

        # Convert to JSON string
        json_output = json.dumps(analysis, indent=2)

        print("\nJSON Output:")
        print(json_output[:500] + "...\n")

        # Show how to save
        print("To save to file:")
        print("  with open('analysis.json', 'w') as f:")
        print("      json.dump(analysis, f, indent=2)")


def example6_integration():
    """Example 6: Integration with downstream processing"""
    print_header("EXAMPLE 6: INTEGRATION EXAMPLE")

    agent = ApplicationProfileAgent()

    print_section("Preparing Data for Downstream Agents")

    result = agent.analyze_applicant("APP001")

    if result["status"] == "success":
        analysis = result["analysis"]

        # Prepare data structure for Agent2
        agent2_input = {
            "applicant_id": analysis["applicant_id"],
            "applicant_name": analysis["applicant_name"],
            "applicant_analysis": {
                "income_stability": analysis["income_stability"],
                "employment_risk": analysis["employment_risk"],
                "credit_history": analysis["credit_history"],
                "application_completeness": analysis["application_completeness"]
            }
        }

        print("\nData prepared for Agent2 (Risk Rules Agent):")
        print(json.dumps(agent2_input, indent=2)[:300] + "...\n")

        print("This structure is ready to be passed to:")
        print("  risk_agent = RiskRulesAgent()")
        print("  risk_result = risk_agent.evaluate_risk(agent2_input)")


def main():
    """Run all examples."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║                   AGENT1 USAGE EXAMPLES - CLAUDE SONNET 4.6                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        example1_single_applicant()
        example2_batch_analysis()
        example3_extract_metrics()
        example4_comparison()
        example5_json_export()
        example6_integration()

        print_header("EXAMPLES COMPLETE")
        print("\n✅ All examples completed successfully!")
        print("\nNext Steps:")
        print("  1. Review the structured output format")
        print("  2. Integrate Agent1 with your system")
        print("  3. Create Agent2 (Risk Rules Agent)")
        print("  4. Build multi-agent orchestration")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Application DB server is running: python mcp/server.py")
        print("  2. ANTHROPIC_API_KEY is set")
        print("  3. All dependencies are installed: pip install anthropic httpx")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
