#!/usr/bin/env python3
"""
LangGraph Orchestration Engine Usage Examples
Demonstrates various ways to use the orchestration engine for loan decision workflows.

Run all 4 MCP servers first:
    python mcp/server.py
    python mcp/riskrulesdb/server.py
    python mcp/decisionsynthesis/server.py
    python mcp/notificationsystem/server.py

Then run this example:
    python examples/orchestration_example.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.orchestration_engine import LoanDecisionOrchestrator
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


def example1_strong_applicant():
    """Example 1: Process strong applicant (auto-approve path)."""
    print_header("EXAMPLE 1: STRONG APPLICANT - AUTO-APPROVE PATH")

    orchestrator = LoanDecisionOrchestrator()
    workflow = orchestrator.create_workflow()

    print_section("Processing Strong Financial Profile")

    # Strong applicant data
    test_case = {
        "applicant_id": "STRONG001",
        "applicant_data": {
            "name": "John Strong",
            "age": 45,
            "email": "john.strong@example.com",
            "phone": "+1-555-0100",
            "annual_income": 200000,
            "monthly_expenses": 5000,
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
    }

    # Initialize state
    initial_state = {
        "applicant_id": test_case["applicant_id"],
        "applicant_data": test_case["applicant_data"],
        "loan_request": test_case["loan_request"],
        "profile_analysis": {},
        "profile_status": "",
        "profile_error": "",
        "risk_analysis": {},
        "risk_status": "",
        "risk_error": "",
        "routing_decision": "",
        "risk_score": 0.0,
        "risk_level": "",
        "decision_data": {},
        "decision_status": "",
        "decision_error": "",
        "action_result": {},
        "action_status": "",
        "action_error": "",
        "case_id": "",
        "final_decision": {},
        "workflow_status": "",
        "execution_path": [],
        "timestamp": ""
    }

    try:
        # Run workflow
        final_state = workflow.invoke(initial_state)

        # Display results
        print(f"\n✅ Workflow Complete")
        final = final_state["final_decision"]

        print(f"\n📊 Results:")
        print(f"   Risk Score: {final_state['risk_score']}/5")
        print(f"   Risk Level: {final_state['risk_level']}")
        print(f"   Routing: {final_state['routing_decision'].upper()}")
        print(f"   Case ID: {final_state['case_id']}")

        # Extract decision
        decision = final_state["decision_data"].get("decision", {})
        print(f"\n📋 Decision:")
        print(f"   Classification: {decision.get('classification', 'N/A')}")
        print(f"   Confidence: {decision.get('confidence_percentage', 0)}%")

        # Show next steps
        print(f"\n📍 Next Steps:")
        for step in final["next_steps"]:
            print(f"   {step}")

        # Show execution path
        print(f"\n🔄 Execution Path:")
        print(f"   {final['execution_path']}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def example2_high_risk_applicant():
    """Example 2: Process high-risk applicant (escalate path)."""
    print_header("EXAMPLE 2: HIGH-RISK APPLICANT - ESCALATE PATH")

    orchestrator = LoanDecisionOrchestrator()
    workflow = orchestrator.create_workflow()

    print_section("Processing High-Risk Profile")

    # High risk applicant
    test_case = {
        "applicant_id": "HIGHRISK001",
        "applicant_data": {
            "name": "Bob Risky",
            "age": 35,
            "email": "bob.risky@example.com",
            "phone": "+1-555-0200",
            "annual_income": 60000,
            "monthly_expenses": 3000,
            "existing_monthly_debt": 2500,
            "credit_score": 580,
            "delinquencies": 2,
            "inquiries_last_6_months": 5,
            "credit_utilization": 0.85,
            "years_at_current_job": 1,
            "existing_loans": 3
        },
        "loan_request": {
            "loan_amount": 300000,
            "property_value": 320000,
            "loan_term_months": 360
        }
    }

    initial_state = {
        "applicant_id": test_case["applicant_id"],
        "applicant_data": test_case["applicant_data"],
        "loan_request": test_case["loan_request"],
        "profile_analysis": {},
        "profile_status": "",
        "profile_error": "",
        "risk_analysis": {},
        "risk_status": "",
        "risk_error": "",
        "routing_decision": "",
        "risk_score": 0.0,
        "risk_level": "",
        "decision_data": {},
        "decision_status": "",
        "decision_error": "",
        "action_result": {},
        "action_status": "",
        "action_error": "",
        "case_id": "",
        "final_decision": {},
        "workflow_status": "",
        "execution_path": [],
        "timestamp": ""
    }

    try:
        final_state = workflow.invoke(initial_state)

        final = final_state["final_decision"]

        print(f"\n✅ Workflow Complete")

        print(f"\n📊 Results:")
        print(f"   Risk Score: {final_state['risk_score']}/5")
        print(f"   Risk Level: {final_state['risk_level']}")
        print(f"   Routing: {final_state['routing_decision'].upper()}")
        print(f"   Case ID: {final_state['case_id']}")

        decision = final_state["decision_data"].get("decision", {})
        print(f"\n📋 Decision:")
        print(f"   Classification: {decision.get('classification', 'N/A')}")
        print(f"   Confidence: {decision.get('confidence_percentage', 0)}%")

        print(f"\n📍 Next Steps:")
        for step in final["next_steps"]:
            print(f"   {step}")

        print(f"\n🔄 Execution Path:")
        print(f"   {final['execution_path']}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def example3_batch_processing():
    """Example 3: Process multiple applicants in batch."""
    print_header("EXAMPLE 3: BATCH PROCESSING - MULTIPLE APPLICANTS")

    orchestrator = LoanDecisionOrchestrator()
    workflow = orchestrator.create_workflow()

    print_section("Processing Multiple Applicants")

    # Multiple test cases
    test_cases = [
        {
            "applicant_id": "BATCH001",
            "name": "Alice Good",
            "profile_type": "Excellent",
            "applicant_data": {
                "name": "Alice Good",
                "annual_income": 180000,
                "credit_score": 790,
                "delinquencies": 0,
                "years_at_current_job": 12,
                "existing_monthly_debt": 800,
                "inquiries_last_6_months": 0,
                "credit_utilization": 0.15,
                "existing_loans": 1
            }
        },
        {
            "applicant_id": "BATCH002",
            "name": "Charlie Fair",
            "profile_type": "Moderate",
            "applicant_data": {
                "name": "Charlie Fair",
                "annual_income": 95000,
                "credit_score": 700,
                "delinquencies": 0,
                "years_at_current_job": 4,
                "existing_monthly_debt": 1200,
                "inquiries_last_6_months": 2,
                "credit_utilization": 0.50,
                "existing_loans": 2
            }
        },
        {
            "applicant_id": "BATCH003",
            "name": "Diana Poor",
            "profile_type": "Weak",
            "applicant_data": {
                "name": "Diana Poor",
                "annual_income": 55000,
                "credit_score": 620,
                "delinquencies": 1,
                "years_at_current_job": 2,
                "existing_monthly_debt": 1800,
                "inquiries_last_6_months": 4,
                "credit_utilization": 0.80,
                "existing_loans": 3
            }
        }
    ]

    results = {}

    for test_case in test_cases:
        applicant_id = test_case["applicant_id"]
        profile_type = test_case["profile_type"]

        print(f"\n📋 Processing {applicant_id} ({profile_type})...")

        # Add required fields for orchestration
        applicant_data = test_case["applicant_data"]
        applicant_data.update({
            "age": 40,
            "email": f"{applicant_id}@example.com",
            "phone": "+1-555-0000",
            "monthly_expenses": applicant_data.get("existing_monthly_debt", 0) * 2,
        })

        loan_request = {
            "loan_amount": 250000,
            "property_value": 400000,
            "loan_term_months": 360
        }

        initial_state = {
            "applicant_id": applicant_id,
            "applicant_data": applicant_data,
            "loan_request": loan_request,
            "profile_analysis": {},
            "profile_status": "",
            "profile_error": "",
            "risk_analysis": {},
            "risk_status": "",
            "risk_error": "",
            "routing_decision": "",
            "risk_score": 0.0,
            "risk_level": "",
            "decision_data": {},
            "decision_status": "",
            "decision_error": "",
            "action_result": {},
            "action_status": "",
            "action_error": "",
            "case_id": "",
            "final_decision": {},
            "workflow_status": "",
            "execution_path": [],
            "timestamp": ""
        }

        try:
            final_state = workflow.invoke(initial_state)
            results[applicant_id] = final_state

            risk_score = final_state["risk_score"]
            routing = final_state["routing_decision"]
            case_id = final_state["case_id"]
            decision = final_state["decision_data"].get("decision", {}).get("classification", "N/A")

            print(f"   ✅ Risk: {risk_score:.1f}/5 | Route: {routing.upper()} | Decision: {decision} | Case: {case_id}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[applicant_id] = None

    # Summary
    print_section("Summary")
    print(f"\nTotal Processed: {len(test_cases)}")
    successful = sum(1 for r in results.values() if r is not None and r.get("workflow_status") == "success")
    print(f"Successful: {successful}")

    # Decision breakdown
    print(f"\nDecision Breakdown:")
    for applicant_id, result in results.items():
        if result:
            decision = result["decision_data"].get("decision", {}).get("classification", "N/A")
            risk_score = result["risk_score"]
            print(f"   {applicant_id}: {decision} (Risk: {risk_score:.1f}/5)")


def example4_workflow_analysis():
    """Example 4: Analyze workflow execution and state transitions."""
    print_header("EXAMPLE 4: WORKFLOW ANALYSIS & STATE TRANSITIONS")

    orchestrator = LoanDecisionOrchestrator()
    workflow = orchestrator.create_workflow()

    print_section("Analyzing Workflow State Transitions")

    test_case = {
        "applicant_id": "ANALYSIS001",
        "applicant_data": {
            "name": "Test User",
            "age": 40,
            "email": "test@example.com",
            "phone": "+1-555-0000",
            "annual_income": 120000,
            "monthly_expenses": 3000,
            "existing_monthly_debt": 1200,
            "credit_score": 740,
            "delinquencies": 0,
            "inquiries_last_6_months": 1,
            "credit_utilization": 0.35,
            "years_at_current_job": 6,
            "existing_loans": 1
        },
        "loan_request": {
            "loan_amount": 280000,
            "property_value": 450000,
            "loan_term_months": 360
        }
    }

    initial_state = {
        "applicant_id": test_case["applicant_id"],
        "applicant_data": test_case["applicant_data"],
        "loan_request": test_case["loan_request"],
        "profile_analysis": {},
        "profile_status": "",
        "profile_error": "",
        "risk_analysis": {},
        "risk_status": "",
        "risk_error": "",
        "routing_decision": "",
        "risk_score": 0.0,
        "risk_level": "",
        "decision_data": {},
        "decision_status": "",
        "decision_error": "",
        "action_result": {},
        "action_status": "",
        "action_error": "",
        "case_id": "",
        "final_decision": {},
        "workflow_status": "",
        "execution_path": [],
        "timestamp": ""
    }

    try:
        final_state = workflow.invoke(initial_state)

        print(f"\n📊 Workflow State Analysis:")

        # Node execution status
        print(f"\nNode Execution Status:")
        print(f"   Agent1 (Profile): {final_state['profile_status']}")
        print(f"   Agent2 (Risk): {final_state['risk_status']}")
        print(f"   Routing Decision: {final_state['routing_decision']}")
        print(f"   Agent3 (Decision): {final_state['decision_status']}")
        print(f"   Agent4 (Compliance): {final_state['action_status']}")

        # State values
        print(f"\nKey State Values:")
        print(f"   Risk Score: {final_state['risk_score']}/5")
        print(f"   Risk Level: {final_state['risk_level']}")
        print(f"   Routing: {final_state['routing_decision']}")
        print(f"   Case ID: {final_state['case_id']}")

        # Execution path
        print(f"\nExecution Path:")
        print(f"   {' → '.join(final_state['execution_path'])}")

        # Decision information
        decision = final_state["decision_data"].get("decision", {})
        print(f"\nDecision Information:")
        print(f"   Classification: {decision.get('classification', 'N/A')}")
        print(f"   Risk Score: {decision.get('risk_score', 'N/A')}")
        print(f"   Confidence: {decision.get('confidence_percentage', 'N/A')}%")

        # Compliance information
        compliance = final_state["action_result"].get("compliance_certification", {})
        print(f"\nCompliance Certification:")
        print(f"   Fair Lending: {compliance.get('fair_lending_compliant', 'N/A')}")
        print(f"   Documentation: {compliance.get('documentation_complete', 'N/A')}")
        print(f"   Regulatory: {compliance.get('regulatory_requirements_met', 'N/A')}")

        # Summary
        print(f"\nFinal Summary:")
        print(f"   Workflow Status: {final_state['workflow_status'].upper()}")
        print(f"   Timestamp: {final_state['timestamp']}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run all examples."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║              LANGGRAPH ORCHESTRATION ENGINE USAGE EXAMPLES                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        example1_strong_applicant()
        example2_high_risk_applicant()
        example3_batch_processing()
        example4_workflow_analysis()

        print_header("EXAMPLES COMPLETE")
        print("\n✅ All examples completed successfully!")
        print("\nKey Takeaways:")
        print("  1. Orchestration routes automatically based on risk score")
        print("  2. Complete state is maintained through all nodes")
        print("  3. Execution path tracks which nodes were executed")
        print("  4. Can process single or batch applications")
        print("  5. Ready to integrate with Streamlit UI or FastAPI")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure all MCP servers are running:")
        print("  1. python mcp/server.py")
        print("  2. python mcp/riskrulesdb/server.py")
        print("  3. python mcp/decisionsynthesis/server.py")
        print("  4. python mcp/notificationsystem/server.py")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
