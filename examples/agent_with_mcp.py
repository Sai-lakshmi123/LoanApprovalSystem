#!/usr/bin/env python3
"""
Example: Using MCP Tools in LangChain Agents

This demonstrates how to create LangChain agents that use MCP tools
to analyze applicants and make decisions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from mcp.clients.mcp_client import SyncMCPClient
import json


def create_credit_analyzer_agent():
    """
    Create a credit analyzer agent that uses MCP tools.

    This agent analyzes an applicant's credit history and determines
    if they meet credit requirements.
    """
    client = SyncMCPClient()
    model = ChatAnthropic(model="claude-opus-4-1-20250805")

    def analyze_credit(applicant_id: str) -> dict:
        """Analyze applicant credit using MCP and LLM."""

        # Step 1: Get applicant profile from MCP
        print(f"\n📊 Credit Analyzer - Analyzing {applicant_id}")
        profile = client.get_applicant_profile(applicant_id)

        if profile.get('status') != 'success':
            return {"status": "error", "message": profile.get('message')}

        # Step 2: Get credit history from MCP
        credit = client.get_credit_history_summary(applicant_id)

        # Step 3: Get credit rules from MCP resources
        rules = client.get_credit_scoring_rules()

        # Step 4: Prepare context for LLM
        context = f"""
Applicant ID: {applicant_id}
Name: {profile['data']['name']}
Age: {profile['data']['age']}
Annual Income: ${profile['data']['annual_income']:,.2f}

Credit Profile:
- Credit Score: {credit['analysis']['credit_score']}
- Score Category: {credit['analysis']['score_category']}
- Delinquencies: {credit['analysis']['delinquencies']}
- Payment Trend: {credit['analysis']['payment_trend']}
- Credit Utilization: {credit['analysis']['credit_utilization_ratio']}%
- Open Accounts: {credit['analysis']['accounts_open']}
- Total Debt: ${credit['analysis']['total_debt']:,.2f}

Scoring Rules:
- Minimum Credit Score: {rules['minimum_credit_score']}
- Recommended Minimum: {rules['recommended_minimum']}
- Excellent Score Range: 750+
- Good Score Range: 700-749
- Fair Score Range: 650-699
"""

        # Step 5: Use LLM to generate analysis
        response = model.invoke([
            HumanMessage(content=f"""
Analyze the following applicant's credit profile and provide a recommendation.

{context}

Consider:
1. Does their credit score meet the minimum requirement?
2. What is the delinquency status?
3. How is their payment trend?
4. Is their credit utilization acceptable?
5. Should we approve, reject, or request more information?

Provide a structured analysis with:
- Credit Assessment (Poor/Fair/Good/Excellent)
- Risk Level (Low/Medium/High)
- Recommendation (APPROVE/REJECT/REVIEW)
- Key Concerns (if any)
- Reasoning
""")
        ])

        return {
            "status": "success",
            "applicant_id": applicant_id,
            "credit_score": credit['analysis']['credit_score'],
            "analysis": response.content
        }

    return analyze_credit


def create_employment_risk_agent():
    """
    Create an employment risk analyzer agent.

    This agent assesses employment stability and risk.
    """
    client = SyncMCPClient()
    model = ChatAnthropic(model="claude-opus-4-1-20250805")

    def analyze_employment(applicant_id: str) -> dict:
        """Analyze employment risk using MCP and LLM."""

        print(f"\n💼 Employment Analyzer - Analyzing {applicant_id}")

        # Get data from MCP
        profile = client.get_applicant_profile(applicant_id)
        income_stability = client.get_income_stability_score(applicant_id)
        employment_risk = client.get_employment_risk(applicant_id)
        factors = client.get_employment_stability_factors()

        if profile.get('status') != 'success':
            return {"status": "error", "message": profile.get('message')}

        data = profile['data']

        context = f"""
Applicant ID: {applicant_id}
Name: {data['name']}
Age: {data['age']}

Employment:
- Type: {data['employment_type'].replace('_', ' ').title()}
- Employer: {data['employer']}
- Job Title: {data['job_title']}
- Years at Current Job: {data['years_at_current_job']}
- Annual Income: ${data['annual_income']:,.2f}

Analysis:
- Income Stability Score: {income_stability['analysis']['score']}/100 ({income_stability['analysis']['stability_category']})
- Employment Risk Score: {employment_risk['analysis']['risk_score']}/100 ({employment_risk['analysis']['risk_level']})
- Tenure Risk: {employment_risk['analysis']['tenure_risk']}

Stability Factors:
- Minimum Acceptable Stability: {factors['minimum_acceptable_stability']}
- {data['employment_type'].replace('_', ' ').title()} Base Stability: {factors['employment_types'][data['employment_type']]['base_stability_score']}
"""

        # Use LLM to analyze
        response = model.invoke([
            HumanMessage(content=f"""
Analyze the following applicant's employment situation and stability.

{context}

Consider:
1. Is the employment type stable?
2. How long have they been at their current job?
3. What is the income level adequate?
4. Is there risk of job loss?
5. Is the income growth potential positive?

Provide:
- Employment Stability Assessment
- Risk Factors
- Stability Confidence Level
- Recommendation for approval
""")
        ])

        return {
            "status": "success",
            "applicant_id": applicant_id,
            "stability_score": income_stability['analysis']['score'],
            "risk_score": employment_risk['analysis']['risk_score'],
            "analysis": response.content
        }

    return analyze_employment


def create_completeness_checker_agent():
    """
    Create an application completeness checker agent.
    """
    client = SyncMCPClient()

    def check_completeness(applicant_id: str) -> dict:
        """Check application completeness."""

        print(f"\n✅ Completeness Checker - Analyzing {applicant_id}")

        completeness = client.check_application_completeness(applicant_id)

        if completeness.get('status') != 'success':
            return {"status": "error", "message": completeness.get('message')}

        analysis = completeness['analysis']

        return {
            "status": "success",
            "applicant_id": applicant_id,
            "is_complete": analysis['is_complete'],
            "completeness_percentage": analysis['completeness_percentage'],
            "missing_fields": analysis['missing_fields'],
            "incomplete_sections": analysis['incomplete_sections'],
            "flags": analysis['flags']
        }

    return check_completeness


def create_comprehensive_loan_agent():
    """
    Create a comprehensive loan assessment agent that uses all MCP tools.
    """
    client = SyncMCPClient()
    model = ChatAnthropic(model="claude-opus-4-1-20250805")

    def assess_loan_application(applicant_id: str) -> dict:
        """Perform comprehensive loan assessment."""

        print(f"\n🏦 Loan Assessment Agent - Analyzing {applicant_id}")
        print("   Fetching all applicant data from MCP...")

        # Get complete analysis from MCP
        complete_analysis = client.get_complete_analysis(applicant_id)

        if complete_analysis.get('status') != 'success':
            return {"status": "error", "message": complete_analysis.get('message')}

        analysis = complete_analysis['analysis']
        profile = client.get_applicant_profile(applicant_id)['data']

        # Get regulatory requirements
        requirements = client.get_regulatory_requirements()
        min_req = requirements['minimum_requirements']

        # Prepare comprehensive context
        context = f"""
APPLICANT PROFILE
=================
ID: {applicant_id}
Name: {profile['name']}
Age: {profile['age']}
Contact: {profile['email']} | {profile['phone']}

FINANCIAL PROFILE
=================
Annual Income: ${profile['annual_income']:,.2f}
Monthly Expenses: ${profile['monthly_expenses']:,.2f}
Debt-to-Income Ratio: {(profile['monthly_expenses'] * 12 / profile['annual_income']):.1%}
Existing Loans: {profile['existing_loans']}

INCOME STABILITY
================
Score: {analysis['income_stability']['score']}/100
Category: {analysis['income_stability']['stability_category']}
Employment Type: {profile['employment_type'].replace('_', ' ').title()}
Years at Job: {profile['years_at_current_job']}

EMPLOYMENT RISK
===============
Risk Score: {analysis['employment_risk']['risk_score']}/100
Risk Level: {analysis['employment_risk']['risk_level']}
Tenure Risk: {analysis['employment_risk']['tenure_risk']}

CREDIT PROFILE
==============
Credit Score: {analysis['credit_history']['credit_score']}
Score Category: {analysis['credit_history']['score_category']}
Delinquencies: {analysis['credit_history']['delinquencies']}
Payment Trend: {analysis['credit_history']['payment_trend']}
Credit Utilization: {analysis['credit_history']['credit_utilization_ratio']}%
Total Debt: ${analysis['credit_history']['total_debt']:,.2f}
Inquiries (6mo): {analysis['credit_history']['inquiries_last_6_months']}

APPLICATION STATUS
==================
Complete: {analysis['application_completeness']['is_complete']}
Completeness: {analysis['application_completeness']['completeness_percentage']}%
Missing Fields: {', '.join(analysis['application_completeness']['missing_fields']) if analysis['application_completeness']['missing_fields'] else 'None'}

REGULATORY REQUIREMENTS
=======================
Minimum Age: {min_req['minimum_age']} (Applicant: {profile['age']})
Minimum Credit Score: {min_req['minimum_credit_score']} (Applicant: {analysis['credit_history']['credit_score']})
Minimum Income: ${min_req['minimum_income']:,.2f} (Applicant: ${profile['annual_income']:,.2f})
Maximum Debt-to-Income: {min_req['maximum_debt_to_income']:.0%}
"""

        # Use LLM for comprehensive assessment
        response = model.invoke([
            HumanMessage(content=f"""
You are a loan underwriter. Perform a comprehensive assessment of this loan application.

{context}

Based on all the data provided, provide:

1. REGULATORY COMPLIANCE
   - Does the applicant meet all minimum requirements?
   - Are there any compliance concerns?

2. FINANCIAL STRENGTH
   - Income adequacy (relative to debt)
   - Expense management
   - Overall financial health

3. CREDIT ASSESSMENT
   - Credit score evaluation
   - Payment history analysis
   - Credit risk level

4. EMPLOYMENT STABILITY
   - Job security assessment
   - Income stability
   - Employment risk factors

5. OVERALL RECOMMENDATION
   - APPROVE / CONDITIONAL APPROVE / REJECT
   - Loan amount recommendation
   - Terms recommendation (if approved)
   - Conditions required (if conditional)

6. KEY RISK FACTORS
   - List any concerns or red flags
   - Mitigation strategies (if applicable)

Provide a structured, professional assessment suitable for a loan decision.
""")
        ])

        return {
            "status": "success",
            "applicant_id": applicant_id,
            "name": complete_analysis['name'],
            "assessment": response.content
        }

    return assess_loan_application


def main():
    """Run agent examples."""
    print("\n" + "=" * 80)
    print("  MCP INTEGRATION WITH LANGCHAIN AGENTS")
    print("=" * 80)

    # Test applicants
    test_applicants = ["APP001", "APP002", "APP003"]

    # Create agents
    print("\n🤖 Creating agents...\n")
    credit_analyzer = create_credit_analyzer_agent()
    employment_analyzer = create_employment_risk_agent()
    completeness_checker = create_completeness_checker_agent()
    loan_assessor = create_comprehensive_loan_agent()

    # Run comprehensive assessment for first applicant
    applicant_id = "APP001"
    print("\n" + "=" * 80)
    print(f"  COMPREHENSIVE LOAN ASSESSMENT FOR {applicant_id}")
    print("=" * 80)

    result = loan_assessor(applicant_id)
    if result['status'] == 'success':
        print(f"\n✅ Assessment for {result['name']}:\n")
        print(result['assessment'])
    else:
        print(f"❌ Error: {result['message']}")

    print("\n" + "=" * 80)
    print("  ASSESSMENT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
