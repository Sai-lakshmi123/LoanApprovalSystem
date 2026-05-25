#!/usr/bin/env python3
"""
DecisionSynthesis Demo
Demonstrates loan decision synthesis combining Application DB and RiskRulesDB.

Run the servers first:
    python mcp/server.py (Application DB)
    python mcp/riskrulesdb/server.py (RiskRulesDB)
    python mcp/decisionsynthesis/server.py (DecisionSynthesis)

Then run this demo:
    python examples/decisionsynthesis_demo.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.clients.mcp_client import SyncMCPClient
from mcp.riskrulesdb.client import RiskRulesDBSyncClient
from mcp.decisionsynthesis.client import DecisionSynthesisSyncClient
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


def demo_basic_decision_synthesis():
    """Demo: Basic Decision Synthesis"""
    print_header("DEMO 1: BASIC LOAN DECISION SYNTHESIS")

    # Initialize all three clients
    app_db = SyncMCPClient()
    risk_db = RiskRulesDBSyncClient()
    decision_db = DecisionSynthesisSyncClient()

    print_section("Analyzing Applicant APP001")

    # Get applicant profile and analysis from Application DB
    print("\n1. Fetching applicant profile from Application DB...")
    applicant_profile = app_db.get_applicant_profile("APP001")
    if applicant_profile.get('status') == 'success':
        app_data = applicant_profile['data']
        print(f"   Name: {app_data.get('name')}")
        print(f"   Age: {app_data.get('age')}")
        print(f"   Annual Income: ${app_data.get('annual_income'):,.0f}")
        print(f"   Credit Score: {app_data.get('credit_score')}")

    print("\n2. Getting application analysis...")
    app_analysis = app_db.get_complete_applicant_analysis("APP001")
    if app_analysis.get('status') == 'success':
        analysis = app_analysis['analysis']
        print(f"   Income Stability: {analysis.get('income_stability', {}).get('score')}")
        print(f"   Employment Risk: {analysis.get('employment_risk', {}).get('risk_level')}")
        print(f"   Completeness: {analysis.get('application_completeness', {}).get('completeness_percentage'):.0f}%")

    print("\n3. Getting financial risk assessment...")
    risk_assessment = risk_db.generate_risk_report(
        "APP001",
        app_data,
        {
            "loan_amount": 300000,
            "property_value": 500000,
            "loan_term_months": 360
        }
    )
    if risk_assessment.get('status') == 'success':
        print(f"   DTI Ratio: {risk_assessment['dti_with_new_loan']['dti_percentage']:.1f}%")
        print(f"   Overall Risk Level: {risk_assessment['overall_risk_assessment']['overall_risk_level']}")
        print(f"   Anomalies Detected: {risk_assessment['anomaly_detection']['anomaly_count']}")

    print("\n4. Synthesizing final decision...")
    decision = decision_db.synthesize_loan_decision(
        "APP001",
        app_data,
        app_analysis['analysis'] if app_analysis.get('status') == 'success' else {},
        risk_assessment,
        strategy="Balanced"
    )

    if decision.get('status') == 'success':
        dec = decision['decision']
        print(f"   Classification: {dec['classification']}")
        print(f"   Risk Score: {dec['risk_score']}/5")
        print(f"   Confidence: {dec['confidence_level']}")
        print(f"   Strategy: {decision['strategy_applied']}")
        print(f"\n   Explanation:")
        print(f"   {dec['reasoning']}")

        if dec['conditions']:
            print(f"\n   Conditions:")
            for i, cond in enumerate(dec['conditions'], 1):
                print(f"   {i}. {cond}")


def demo_strategy_comparison():
    """Demo: Compare decisions across strategies"""
    print_header("DEMO 2: DECISION STRATEGY COMPARISON")

    app_db = SyncMCPClient()
    risk_db = RiskRulesDBSyncClient()
    decision_db = DecisionSynthesisSyncClient()

    print_section("Comparing Conservative vs Balanced vs Aggressive")

    # Get data
    applicant_profile = app_db.get_applicant_profile("APP002")
    app_data = applicant_profile['data']

    app_analysis = app_db.get_complete_applicant_analysis("APP002")

    risk_assessment = risk_db.generate_risk_report(
        "APP002",
        app_data,
        {
            "loan_amount": 350000,
            "property_value": 450000,
            "loan_term_months": 360
        }
    )

    # Test each strategy
    strategies = ["Conservative", "Balanced", "Aggressive"]
    results = []

    print(f"\nApplicant: {app_data.get('name')}")
    print(f"Annual Income: ${app_data.get('annual_income'):,.0f}")
    print(f"Credit Score: {app_data.get('credit_score')}")
    print(f"Requested Loan: $350,000")
    print(f"\nDecision by Strategy:")
    print(f"{'Strategy':<15} {'Decision':<20} {'Risk Score':<15} {'Confidence':<15}")
    print(f"{'-'*15} {'-'*20} {'-'*15} {'-'*15}")

    for strategy in strategies:
        decision = decision_db.synthesize_loan_decision(
            "APP002",
            app_data,
            app_analysis['analysis'] if app_analysis.get('status') == 'success' else {},
            risk_assessment,
            strategy=strategy
        )

        if decision.get('status') == 'success':
            dec = decision['decision']
            results.append({
                "strategy": strategy,
                "decision": dec['classification'],
                "risk_score": dec['risk_score'],
                "confidence": dec['confidence_level']
            })

            print(f"{strategy:<15} {dec['classification']:<20} {dec['risk_score']:<15.2f} {dec['confidence_level']:<15}")

    # Analysis
    print("\nAnalysis:")
    if len(results) >= 2:
        conservative = results[0]['decision']
        aggressive = results[2]['decision']
        if conservative == aggressive:
            print(f"✅ All strategies agree: {conservative}")
        else:
            print(f"⚠️  Strategies diverge: {conservative} (Conservative) vs {aggressive} (Aggressive)")


def demo_detailed_explanation():
    """Demo: Get detailed decision explanation"""
    print_header("DEMO 3: DETAILED DECISION EXPLANATION")

    app_db = SyncMCPClient()
    risk_db = RiskRulesDBSyncClient()
    decision_db = DecisionSynthesisSyncClient()

    print_section("Getting Detailed Explanation for APP003")

    # Get data
    applicant_profile = app_db.get_applicant_profile("APP003")
    app_data = applicant_profile['data']

    app_analysis = app_db.get_complete_applicant_analysis("APP003")

    risk_assessment = risk_db.generate_risk_report(
        "APP003",
        app_data,
        {
            "loan_amount": 250000,
            "property_value": 400000,
            "loan_term_months": 360
        }
    )

    # Get detailed explanation
    explanation = decision_db.explain_decision(
        "APP003",
        app_data,
        app_analysis['analysis'] if app_analysis.get('status') == 'success' else {},
        risk_assessment
    )

    if explanation.get('status') == 'success':
        print(f"\nApplicant: {app_data.get('name')}")
        print(f"Decision: {explanation['decision']}")
        print(f"Confidence: {explanation['confidence']}")

        print(f"\nExplanation:")
        print(f"{explanation['explanation']}")

        print(f"\nKey Factors Influencing Decision:")
        for i, factor in enumerate(explanation['key_factors'], 1):
            print(f"\n{i}. {factor.get('category')}")
            print(f"   Value: {factor.get('value')}")
            print(f"   Impact: {factor.get('impact')}")
            print(f"   Description: {factor.get('description')}")

        if explanation['conditions']:
            print(f"\nConditions (if applicable):")
            for i, cond in enumerate(explanation['conditions'], 1):
                print(f"{i}. {cond}")


def demo_applicant_comparison():
    """Demo: Compare multiple applicants"""
    print_header("DEMO 4: APPLICANT COMPARISON")

    app_db = SyncMCPClient()
    risk_db = RiskRulesDBSyncClient()
    decision_db = DecisionSynthesisSyncClient()

    print_section("Comparing 3 Applicants")

    applicants = []
    applicant_ids = ["APP001", "APP002", "APP003"]

    # Prepare data for each applicant
    for app_id in applicant_ids:
        applicant_profile = app_db.get_applicant_profile(app_id)
        app_data = applicant_profile['data']

        app_analysis = app_db.get_complete_applicant_analysis(app_id)

        risk_assessment = risk_db.generate_risk_report(
            app_id,
            app_data,
            {
                "loan_amount": 300000,
                "property_value": 500000,
                "loan_term_months": 360
            }
        )

        applicants.append({
            "applicant_id": app_id,
            "applicant_data": app_data,
            "application_analysis": app_analysis['analysis'] if app_analysis.get('status') == 'success' else {},
            "risk_assessment": risk_assessment
        })

    # Compare applicants
    comparison = decision_db.compare_applicants(applicants)

    if comparison.get('status') == 'success':
        print(f"\nComparison Results ({comparison['comparison_count']} applicants):")
        print(f"{'Applicant ID':<15} {'Name':<20} {'Decision':<20} {'Risk Score':<15} {'Confidence':<15}")
        print(f"{'-'*15} {'-'*20} {'-'*20} {'-'*15} {'-'*15}")

        for i, result in enumerate(comparison['results']):
            applicant_data = applicants[i]['applicant_data']
            print(f"{result['applicant_id']:<15} {applicant_data.get('name', 'N/A'):<20} {result['decision']:<20} {result['risk_score']:<15.2f} {result['confidence']:<15}")

        # Approve vs Reject count
        approvals = sum(1 for r in comparison['results'] if 'APPROVE' in r['decision'])
        rejects = sum(1 for r in comparison['results'] if r['decision'] == 'REJECT')
        reviews = sum(1 for r in comparison['results'] if r['decision'] == 'REVIEW')

        print(f"\nSummary:")
        print(f"  Approved: {approvals}")
        print(f"  Conditional: {len(comparison['results']) - approvals - rejects - reviews}")
        print(f"  Review: {reviews}")
        print(f"  Rejected: {rejects}")


def demo_decision_resources():
    """Demo: Access decision resources"""
    print_header("DEMO 5: DECISION RESOURCES")

    decision_db = DecisionSynthesisSyncClient()

    print_section("Decision Strategies")
    strategies = decision_db.get_decision_strategies()
    strats = strategies.get('strategies', {})

    for name, strategy in strats.items():
        print(f"\n{name.upper()}")
        print(f"  Description: {strategy.get('description')}")
        print(f"  Max DTI: {strategy.get('max_dti')}")
        print(f"  Min Credit Score: {strategy.get('min_credit_score')}")
        print(f"  Max Risk Score: {strategy.get('max_risk_score')}")
        print(f"  Max Anomalies: {strategy.get('max_anomalies')}")
        print(f"  Use Case: {strategy.get('use_case')}")

    print_section("Decision Classifications")
    classifications = decision_db.get_decision_classifications()
    classes = classifications.get('classifications', {})

    for name, classification in classes.items():
        print(f"\n{name.upper()}")
        print(f"  Description: {classification.get('description')}")
        print(f"  Action: {classification.get('action')}")

    print_section("Confidence Calibration")
    calibration = decision_db.get_confidence_calibration()
    levels = calibration.get('levels', {})

    print("\nConfidence Levels:")
    for level, description in levels.items():
        print(f"  {level.upper()}: {description}")


def main():
    """Run all demos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║           DECISIONSYNTHESIS DEMO - INTELLIGENT LOAN DECISIONS                 ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        demo_basic_decision_synthesis()
        demo_strategy_comparison()
        demo_detailed_explanation()
        demo_applicant_comparison()
        demo_decision_resources()

        print_header("DEMO COMPLETE")
        print("\n✅ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("  1. Use DecisionSynthesis in your agents")
        print("  2. Integrate all three servers for complete decision support")
        print("  3. Build a Streamlit UI for loan decisions")
        print("  4. Deploy with LangGraph for orchestration")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure all three servers are running:")
        print("  Terminal 1: python mcp/server.py")
        print("  Terminal 2: python mcp/riskrulesdb/server.py")
        print("  Terminal 3: python mcp/decisionsynthesis/server.py")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
