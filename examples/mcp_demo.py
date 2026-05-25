#!/usr/bin/env python3
"""
MCP Application DB Demo
Demonstrates how to use the MCP server to fetch and analyze applicant data.

Run the MCP server first:
    python mcp/server.py

Then run this demo:
    python examples/mcp_demo.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.clients.mcp_client import SyncMCPClient
import json
from datetime import datetime


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_section(text: str):
    """Print a formatted section header."""
    print(f"\n>>> {text}")
    print("-" * 80)


def demo_list_applicants():
    """Demo: List all available applicants."""
    print_header("DEMO 1: LIST ALL APPLICANTS")

    client = SyncMCPClient()
    result = client.list_all_applicants()

    if result.get('status') == 'success':
        print(f"\nTotal Applicants: {result['count']}\n")
        for app in result['applicants']:
            print(f"  ID: {app['id']:<8} | Name: {app['name']:<20} | Age: {app['age']:<3} | Credit: {app['credit_score']}")
    else:
        print(f"Error: {result.get('message')}")


def demo_get_profile(applicant_id: str):
    """Demo: Get applicant profile."""
    print_header(f"DEMO 2: GET APPLICANT PROFILE ({applicant_id})")

    client = SyncMCPClient()
    result = client.get_applicant_profile(applicant_id)

    if result.get('status') == 'success':
        data = result['data']
        print(f"\nName: {data['name']}")
        print(f"Age: {data['age']}")
        print(f"Email: {data['email']}")
        print(f"Phone: {data['phone']}")
        print(f"\nIncome Information:")
        print(f"  Annual Income: ${data['annual_income']:,.2f}")
        print(f"  Monthly Expenses: ${data['monthly_expenses']:,.2f}")
        print(f"\nEmployment Information:")
        print(f"  Type: {data['employment_type'].replace('_', ' ').title()}")
        print(f"  Employer: {data['employer']}")
        print(f"  Job Title: {data['job_title']}")
        print(f"  Years at Job: {data['years_at_current_job']}")
        print(f"\nCredit Information:")
        print(f"  Credit Score: {data['credit_score']}")
        print(f"  Existing Loans: {data['existing_loans']}")
    else:
        print(f"Error: {result.get('message')}")


def demo_income_stability(applicant_id: str):
    """Demo: Get income stability score."""
    print_header(f"DEMO 3: INCOME STABILITY SCORE ({applicant_id})")

    client = SyncMCPClient()
    result = client.get_income_stability_score(applicant_id)

    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"\nIncome Stability Analysis:")
        print(f"  Score: {analysis['score']}/100")
        print(f"  Category: {analysis['stability_category']}")
        print(f"  Employment Type: {analysis['employment_type'].replace('_', ' ').title()}")
        print(f"  Years at Job: {analysis['years_at_job']}")
        print(f"  Age: {analysis['age']}")

        # Color-coded visual
        bar_length = int(analysis['score'] / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"\n  Stability: [{bar}] {analysis['score']}%")
    else:
        print(f"Error: {result.get('message')}")


def demo_employment_risk(applicant_id: str):
    """Demo: Get employment risk."""
    print_header(f"DEMO 4: EMPLOYMENT RISK ASSESSMENT ({applicant_id})")

    client = SyncMCPClient()
    result = client.get_employment_risk(applicant_id)

    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"\nEmployment Risk Analysis:")
        print(f"  Risk Score: {analysis['risk_score']}/100 (higher = more risky)")
        print(f"  Risk Level: {analysis['risk_level']}")
        print(f"  Employment Type: {analysis['employment_type'].replace('_', ' ').title()}")
        print(f"  Tenure Risk: {analysis['tenure_risk']}")

        # Risk visualization
        risk_bar = "▓" * int(analysis['risk_score'] / 5) + "░" * (20 - int(analysis['risk_score'] / 5))
        print(f"\n  Risk: [{risk_bar}] {analysis['risk_score']}%")

        # Risk level color
        if analysis['risk_level'] == 'Low':
            emoji = "✅"
        elif analysis['risk_level'] == 'Medium':
            emoji = "⚠️"
        else:
            emoji = "🚨"
        print(f"\n  {emoji} {analysis['risk_level']} Risk")
    else:
        print(f"Error: {result.get('message')}")


def demo_credit_history(applicant_id: str):
    """Demo: Get credit history summary."""
    print_header(f"DEMO 5: CREDIT HISTORY SUMMARY ({applicant_id})")

    client = SyncMCPClient()
    result = client.get_credit_history_summary(applicant_id)

    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"\nCredit Analysis:")
        print(f"  Credit Score: {analysis['credit_score']}")
        print(f"  Score Category: {analysis['score_category']}")
        print(f"\nDelinquencies:")
        print(f"  Status: {analysis['delinquency_status']}")
        print(f"  Payment Trend: {analysis['payment_trend']}")
        print(f"\nAccounts:")
        print(f"  Open Accounts: {analysis['accounts_open']}")
        print(f"  Total Accounts: {analysis['total_accounts']}")
        print(f"  Average Age: {analysis['average_account_age']} years")
        print(f"\nCredit Utilization:")
        print(f"  Ratio: {analysis['credit_utilization_ratio']}%")
        print(f"  Status: {analysis['utilization_status']}")
        print(f"  Total Debt: ${analysis['total_debt']:,.2f}")
        print(f"\nRecent Inquiries: {analysis['inquiries_last_6_months']}")
        print(f"\nSummary: {analysis['summary']}")
    else:
        print(f"Error: {result.get('message')}")


def demo_application_completeness(applicant_id: str):
    """Demo: Check application completeness."""
    print_header(f"DEMO 6: APPLICATION COMPLETENESS CHECK ({applicant_id})")

    client = SyncMCPClient()
    result = client.check_application_completeness(applicant_id)

    if result.get('status') == 'success':
        analysis = result['analysis']
        print(f"\nApplication Completeness:")
        print(f"  Status: {'✅ COMPLETE' if analysis['is_complete'] else '❌ INCOMPLETE'}")
        print(f"  Completeness: {analysis['completeness_percentage']}%")

        # Completeness bar
        bar_len = int(analysis['completeness_percentage'] / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  Progress: [{bar}]")

        if analysis['missing_fields']:
            print(f"\n⚠️  Missing Fields:")
            for field in analysis['missing_fields']:
                print(f"    - {field}")

        if analysis['incomplete_sections']:
            print(f"\n⚠️  Incomplete Sections:")
            for section in analysis['incomplete_sections']:
                print(f"    - {section}")

        if analysis['flags']:
            print(f"\nFlags: {', '.join(analysis['flags'])}")
    else:
        print(f"Error: {result.get('message')}")


def demo_complete_analysis(applicant_id: str):
    """Demo: Get complete applicant analysis."""
    print_header(f"DEMO 7: COMPLETE APPLICANT ANALYSIS ({applicant_id})")

    client = SyncMCPClient()
    result = client.get_complete_analysis(applicant_id)

    if result.get('status') == 'success':
        data = result
        analysis = data['analysis']

        print(f"\nApplicant: {data['name']}")
        print(f"ID: {data['applicant_id']}")
        print(f"Timestamp: {data['timestamp']}")

        # Income Stability
        print_section("Income Stability Score")
        print(f"  Score: {analysis['income_stability']['score']}/100")
        print(f"  Category: {analysis['income_stability']['stability_category']}")

        # Employment Risk
        print_section("Employment Risk")
        print(f"  Risk Score: {analysis['employment_risk']['risk_score']}/100")
        print(f"  Risk Level: {analysis['employment_risk']['risk_level']}")

        # Credit History
        print_section("Credit History")
        credit = analysis['credit_history']
        print(f"  Score: {credit['credit_score']} ({credit['score_category']})")
        print(f"  Utilization: {credit['credit_utilization_ratio']}% ({credit['utilization_status']})")
        print(f"  Status: {credit['delinquency_status']}")
        print(f"  Trend: {credit['payment_trend']}")

        # Application Completeness
        print_section("Application Completeness")
        complete = analysis['application_completeness']
        print(f"  Complete: {'✅ Yes' if complete['is_complete'] else '❌ No'}")
        print(f"  Completeness: {complete['completeness_percentage']}%")
        print(f"  Flags: {', '.join(complete['flags'])}")

        # Overall Assessment
        print_section("Overall Assessment")
        score = analysis['income_stability']['score']
        risk = analysis['employment_risk']['risk_score']
        credit_score = credit['credit_score']

        print(f"\n  Income Stability: {'Strong ✅' if score >= 70 else 'Moderate ⚠️' if score >= 50 else 'Weak ❌'}")
        print(f"  Employment Risk: {'Low ✅' if risk <= 30 else 'Medium ⚠️' if risk <= 60 else 'High ❌'}")
        print(f"  Credit Profile: {'Strong ✅' if credit_score >= 700 else 'Fair ⚠️' if credit_score >= 650 else 'Poor ❌'}")

    else:
        print(f"Error: {result.get('message')}")


def demo_resources():
    """Demo: Access MCP resources."""
    print_header("DEMO 8: ACCESS MCP RESOURCES")

    client = SyncMCPClient()

    # Credit Scoring Rules
    print_section("Credit Scoring Rules")
    rules = client.get_credit_scoring_rules()
    print(f"  Min Credit Score: {rules['minimum_credit_score']}")
    print(f"  Recommended Min: {rules['recommended_minimum']}")
    print(f"  Score Categories:")
    for category, info in rules['score_categories'].items():
        print(f"    - {category.title()}: {info['range']} ({info['description']})")

    # Employment Stability Factors
    print_section("Employment Stability Factors")
    factors = client.get_employment_stability_factors()
    print(f"  Min Stability Score: {factors['minimum_acceptable_stability']}")
    print(f"  Employment Types:")
    for emp_type, info in factors['employment_types'].items():
        print(f"    - {emp_type.replace('_', ' ').title()}: {info['risk_level']}")

    # Regulatory Requirements
    print_section("Regulatory Requirements")
    reqs = client.get_regulatory_requirements()
    min_req = reqs['minimum_requirements']
    print(f"  Minimum Requirements:")
    print(f"    - Age: {min_req['minimum_age']}")
    print(f"    - Income: ${min_req['minimum_income']:,.2f}")
    print(f"    - Credit Score: {min_req['minimum_credit_score']}")
    print(f"    - Max Debt-to-Income: {min_req['maximum_debt_to_income']}")


def demo_comparison():
    """Demo: Compare multiple applicants."""
    print_header("DEMO 9: COMPARE MULTIPLE APPLICANTS")

    client = SyncMCPClient()

    applicants = ["APP001", "APP002", "APP003", "APP004"]
    analyses = []

    print("\nFetching data for all applicants...")
    for app_id in applicants:
        result = client.get_complete_analysis(app_id)
        if result.get('status') == 'success':
            analyses.append(result)

    # Create comparison table
    print("\n" + "=" * 120)
    print(f"{'ID':<6} {'Name':<15} {'Income Stab':<12} {'Emp Risk':<12} {'Credit':<8} {'Complete':<10} {'Status':<15}")
    print("=" * 120)

    for analysis in analyses:
        income_stab = analysis['analysis']['income_stability']['score']
        emp_risk = analysis['analysis']['employment_risk']['risk_score']
        credit_score = analysis['analysis']['credit_history']['credit_score']
        complete = analysis['analysis']['application_completeness']['completeness_percentage']

        # Determine overall status
        if income_stab >= 70 and emp_risk <= 30 and credit_score >= 700 and complete == 100:
            status = "✅ Strong Candidate"
        elif income_stab >= 50 and emp_risk <= 60 and credit_score >= 650:
            status = "⚠️  Fair Candidate"
        else:
            status = "❌ High Risk"

        print(f"{analysis['applicant_id']:<6} {analysis['name']:<15} {income_stab:<12} {emp_risk:<12} {credit_score:<8} {complete:<10}% {status:<15}")

    print("=" * 120)


def main():
    """Run all demos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║           MCP APPLICATION DB DEMO - COMPLETE APPLICANT ANALYSIS                ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        # Run demos
        demo_list_applicants()
        demo_get_profile("APP001")
        demo_income_stability("APP001")
        demo_employment_risk("APP001")
        demo_credit_history("APP001")
        demo_application_completeness("APP001")
        demo_complete_analysis("APP001")
        demo_resources()
        demo_comparison()

        print_header("DEMO COMPLETE")
        print("\n✅ All demos completed successfully!")
        print("\nNext steps:")
        print("  1. Use these tools in your agents: from mcp.clients.mcp_client import SyncMCPClient")
        print("  2. Integrate with LangChain agents for intelligent decision making")
        print("  3. Use in FastAPI endpoints for loan processing")
        print("  4. Extend with custom analysis tools")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the MCP server is running:")
        print("  python mcp/server.py")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
