#!/usr/bin/env python3
"""
Agent4 Usage Examples
Demonstrates various ways to use the Compliance & Action Orchestrator Agent

Run the NotificationSystem server first:
    python mcp/notificationsystem/server.py

Then run this example:
    python examples/agent4_usage_example.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.compliance_action_agent import ComplianceActionAgent
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


def example1_single_action_orchestration():
    """Example 1: Orchestrate single decision action"""
    print_header("EXAMPLE 1: SINGLE DECISION ACTION ORCHESTRATION")

    agent = ComplianceActionAgent()

    print_section("Orchestrating Action for APPROVE Decision")

    result = agent.orchestrate_action(
        applicant_id="APP001",
        applicant_data={
            "name": "John Strong",
            "age": 45,
            "email": "john.strong@example.com",
            "phone": "+1-555-0100",
            "annual_income": 150000,
            "monthly_expenses": 4000,
            "existing_monthly_debt": 1000,
            "credit_score": 760,
            "delinquencies": 0,
            "years_at_current_job": 8,
            "existing_loans": 1
        },
        decision_data={
            "applicant_id": "APP001",
            "analysis_timestamp": "2026-05-25T10:30:00",
            "decision": {
                "classification": "APPROVE",
                "risk_score": 1.8,
                "confidence_level": "Very High",
                "confidence_percentage": 92,
                "reasoning": "Strong financial profile with excellent credit, very low employment risk, and manageable DTI.",
                "conditions": []
            },
            "key_factors": [
                {
                    "category": "Income Stability",
                    "impact": "Positive",
                    "description": "8 years at current job with $150k annual income",
                    "score": 85
                },
                {
                    "category": "Credit Profile",
                    "impact": "Positive",
                    "description": "Excellent credit score of 760",
                    "score": 95
                }
            ],
            "risk_summary": {
                "strengths": [
                    "Strong income stability",
                    "Excellent credit score",
                    "Very low employment risk"
                ],
                "concerns": [],
                "mitigating_factors": [],
                "critical_factors": []
            },
            "compliance_notes": {
                "fair_lending_compliant": True,
                "documentation_complete": True,
                "audit_trail_created": True
            }
        }
    )

    if result["status"] == "success":
        action = result["result"]

        print("\n✅ Action Orchestration Complete")

        # Case Information
        case_info = action.get("case_management", {})
        print(f"\n📋 Case Management:")
        print(f"   Case ID: {action.get('case_id', 'N/A')}")
        print(f"   Status: {case_info.get('status', 'N/A')}")
        print(f"   Next Action: {case_info.get('next_action', 'N/A')}")
        print(f"   Assigned To: {case_info.get('assigned_to', 'N/A')}")
        print(f"   Deadline: {case_info.get('deadline', 'N/A')}")
        print(f"   Priority: {case_info.get('priority', 'N/A')}")

        # Notifications
        notif_info = action.get("notifications", {})
        print(f"\n📧 Notifications:")
        print(f"   Total Sent: {notif_info.get('total_notifications', 0)}")
        print(f"   Sent To: {', '.join(notif_info.get('sent_to', []))}")
        print(f"   Template: {notif_info.get('notification_template', 'N/A')}")

        # Compliance
        compliance = action.get("compliance_certification", {})
        print(f"\n✅ Compliance Certification:")
        print(f"   Fair Lending: {compliance.get('fair_lending_compliant', False)}")
        print(f"   Documentation: {compliance.get('documentation_complete', False)}")
        print(f"   Regulatory: {compliance.get('regulatory_requirements_met', False)}")
        print(f"   Audit Trail: {compliance.get('audit_trail_created', False)}")

        # Summary
        print(f"\n📋 Action Summary:")
        print(f"   {action.get('action_summary', 'N/A')}")

        # Next Steps
        print(f"\n📍 Next Steps:")
        for step in action.get('next_steps', []):
            print(f"   → {step}")


def example2_batch_action_orchestration():
    """Example 2: Orchestrate actions for multiple decisions"""
    print_header("EXAMPLE 2: BATCH ACTION ORCHESTRATION")

    agent = ComplianceActionAgent()

    test_cases = [
        {
            "applicant_id": "APP001",
            "applicant_data": {
                "name": "John Strong",
                "email": "john.strong@example.com",
                "annual_income": 150000,
                "credit_score": 760,
                "delinquencies": 0,
                "years_at_current_job": 8
            },
            "decision_data": {
                "decision": {
                    "classification": "APPROVE",
                    "risk_score": 1.8,
                    "confidence_percentage": 92
                },
                "compliance_notes": {
                    "fair_lending_compliant": True,
                    "documentation_complete": True
                }
            }
        },
        {
            "applicant_id": "APP002",
            "applicant_data": {
                "name": "Jane Moderate",
                "email": "jane.moderate@example.com",
                "annual_income": 80000,
                "credit_score": 700,
                "delinquencies": 0,
                "years_at_current_job": 3
            },
            "decision_data": {
                "decision": {
                    "classification": "CONDITIONAL_APPROVE",
                    "risk_score": 2.2,
                    "confidence_percentage": 78,
                    "conditions": [
                        "Provide recent pay stubs (30 days)",
                        "Reduce credit utilization below 50%"
                    ]
                },
                "compliance_notes": {
                    "fair_lending_compliant": True,
                    "documentation_complete": True
                }
            }
        },
        {
            "applicant_id": "APP003",
            "applicant_data": {
                "name": "Bob Review",
                "email": "bob.review@example.com",
                "annual_income": 60000,
                "credit_score": 650,
                "delinquencies": 1,
                "years_at_current_job": 1
            },
            "decision_data": {
                "decision": {
                    "classification": "REVIEW",
                    "risk_score": 3.1,
                    "confidence_percentage": 65
                },
                "compliance_notes": {
                    "fair_lending_compliant": True,
                    "documentation_complete": True
                }
            }
        }
    ]

    print_section("Orchestrating Multiple Applications")

    results = {}
    for test_case in test_cases:
        applicant_id = test_case["applicant_id"]
        print(f"\nOrchestrating {applicant_id}...")

        result = agent.orchestrate_action(
            applicant_id,
            test_case["applicant_data"],
            test_case["decision_data"]
        )
        results[applicant_id] = result

        if result["status"] == "success":
            action = result["result"]
            case_id = action.get("case_id")
            status = action.get("case_management", {}).get("status")
            notifications = action.get("notifications", {}).get("total_notifications", 0)
            compliance = action.get("compliance_certification", {}).get("fair_lending_compliant")

            print(f"  ✅ Case ID: {case_id}, Status: {status}, Notifications: {notifications}, Compliant: {compliance}")

    # Summary
    print_section("Summary")
    print(f"Total Orchestrated: {len(test_cases)}")
    print(f"Successful: {sum(1 for r in results.values() if r['status'] == 'success')}")


def example3_notification_status_tracking():
    """Example 3: Track notification delivery status"""
    print_header("EXAMPLE 3: NOTIFICATION STATUS TRACKING")

    agent = ComplianceActionAgent()

    print_section("Orchestrating and Tracking Notifications")

    # First orchestrate an action
    result = agent.orchestrate_action(
        "APP001",
        {
            "name": "John Strong",
            "email": "john.strong@example.com",
            "annual_income": 150000,
            "credit_score": 760
        },
        {
            "decision": {
                "classification": "APPROVE",
                "risk_score": 1.8,
                "confidence_percentage": 92
            },
            "compliance_notes": {
                "fair_lending_compliant": True,
                "documentation_complete": True
            }
        }
    )

    if result["status"] == "success":
        case_id = result["result"]["case_id"]
        print(f"\n✅ Action Orchestrated - Case ID: {case_id}")

        # Check notification status
        print_section("Checking Notification Delivery Status")

        try:
            status_result = agent.notification_system.check_notification_status(case_id)

            if status_result.get("status") == "success":
                delivery_status = status_result.get("delivery_status", [])

                print(f"\n📧 Notification Delivery Status ({len(delivery_status)} total):")
                for delivery in delivery_status:
                    stakeholder = delivery.get("stakeholder", "Unknown")
                    status = delivery.get("status", "unknown")
                    timestamp = delivery.get("timestamp", "N/A")
                    print(f"   {stakeholder}: {status.upper()} ({timestamp})")

                # Count by status
                sent = sum(1 for d in delivery_status if d.get("status") == "sent")
                pending = sum(1 for d in delivery_status if d.get("status") == "pending")
                failed = sum(1 for d in delivery_status if d.get("status") == "failed")

                print(f"\n📊 Status Summary:")
                print(f"   Sent: {sent}")
                print(f"   Pending: {pending}")
                print(f"   Failed: {failed}")

                # Attempt resend for failed
                if failed > 0:
                    print(f"\n🔄 Resending Failed Notifications:")
                    for delivery in delivery_status:
                        if delivery.get("status") == "failed":
                            stakeholder = delivery.get("stakeholder")
                            print(f"   Resending to {stakeholder}...")
                            resend = agent.notification_system.resend_notification(
                                case_id,
                                stakeholder
                            )
                            if resend.get("status") == "success":
                                print(f"   ✅ Resend successful")
                            else:
                                print(f"   ❌ Resend failed")

        except Exception as e:
            print(f"Error checking notification status: {e}")


def example4_compliance_report_generation():
    """Example 4: Generate compliance report"""
    print_header("EXAMPLE 4: COMPLIANCE REPORT GENERATION")

    agent = ComplianceActionAgent()

    print_section("Orchestrating and Generating Compliance Report")

    # Orchestrate action
    result = agent.orchestrate_action(
        "APP001",
        {
            "name": "John Strong",
            "email": "john.strong@example.com",
            "annual_income": 150000,
            "credit_score": 760
        },
        {
            "decision": {
                "classification": "APPROVE",
                "risk_score": 1.8,
                "confidence_percentage": 92
            },
            "compliance_notes": {
                "fair_lending_compliant": True,
                "documentation_complete": True
            }
        }
    )

    if result["status"] == "success":
        case_id = result["result"]["case_id"]
        print(f"\n✅ Action Orchestrated - Case ID: {case_id}")

        # Get compliance report
        print_section("Generating Compliance Report")

        try:
            report_result = agent.notification_system.get_compliance_report(case_id)

            if report_result.get("status") == "success":
                report = report_result.get("report", {})

                print(f"\n📋 Compliance Report:")
                print(f"\nDecision Summary:")
                print(f"   {report.get('decision_summary', 'N/A')}")

                print(f"\nKey Compliance Factors:")
                for factor in report.get('key_compliance_factors', []):
                    print(f"   • {factor}")

                print(f"\nRegulatory Notes:")
                print(f"   {report.get('regulatory_notes', 'N/A')}")

                print(f"\nRecommendations:")
                for rec in report.get('recommendations', []):
                    print(f"   → {rec}")

        except Exception as e:
            print(f"Error generating compliance report: {e}")


def example5_case_information_retrieval():
    """Example 5: Retrieve and track case information"""
    print_header("EXAMPLE 5: CASE INFORMATION RETRIEVAL")

    agent = ComplianceActionAgent()

    print_section("Orchestrating and Retrieving Case Information")

    # Orchestrate action
    result = agent.orchestrate_action(
        "APP001",
        {
            "name": "John Strong",
            "email": "john.strong@example.com",
            "annual_income": 150000,
            "credit_score": 760
        },
        {
            "decision": {
                "classification": "APPROVE",
                "risk_score": 1.8,
                "confidence_percentage": 92
            },
            "compliance_notes": {
                "fair_lending_compliant": True,
                "documentation_complete": True
            }
        }
    )

    if result["status"] == "success":
        case_id = result["result"]["case_id"]
        print(f"\n✅ Action Orchestrated - Case ID: {case_id}")

        # Retrieve case information
        print_section("Retrieving Complete Case Information")

        try:
            case_info_result = agent.notification_system.get_case_information(case_id)

            if case_info_result.get("status") == "success":
                case = case_info_result.get("case", {})

                print(f"\n📋 Case Information:")
                print(f"   Case ID: {case.get('case_id', 'N/A')}")
                print(f"   Applicant ID: {case.get('applicant_id', 'N/A')}")
                print(f"   Status: {case.get('status', 'N/A')}")
                print(f"   Created: {case.get('created_at', 'N/A')}")
                print(f"   Updated: {case.get('updated_at', 'N/A')}")

                print(f"\n📍 Case Timeline:")
                for event in case.get('timeline', [])[:5]:
                    timestamp = event.get('timestamp', 'N/A')
                    action_type = event.get('action', 'unknown')
                    details = event.get('details', 'N/A')
                    print(f"   {timestamp} - {action_type}: {details}")

                print(f"\n🎯 Current Assignment:")
                assignment = case.get('assignment', {})
                print(f"   Assigned To: {assignment.get('assigned_to', 'Unassigned')}")
                print(f"   Deadline: {assignment.get('deadline', 'N/A')}")
                print(f"   Priority: {assignment.get('priority', 'N/A')}")

                print(f"\n✅ Compliance Status:")
                compliance = case.get('compliance', {})
                print(f"   Fair Lending: {compliance.get('fair_lending_compliant', 'Unknown')}")
                print(f"   Documentation: {compliance.get('documentation_complete', 'Unknown')}")
                print(f"   Regulatory: {compliance.get('regulatory_met', 'Unknown')}")

        except Exception as e:
            print(f"Error retrieving case information: {e}")


def main():
    """Run all examples."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║    AGENT4 USAGE EXAMPLES - COMPLIANCE & ACTION ORCHESTRATOR                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        example1_single_action_orchestration()
        example2_batch_action_orchestration()
        example3_notification_status_tracking()
        example4_compliance_report_generation()
        example5_case_information_retrieval()

        print_header("EXAMPLES COMPLETE")
        print("\n✅ All examples completed successfully!")
        print("\nNext Steps:")
        print("  1. Review the action orchestration output format")
        print("  2. Integrate Agent4 with full 4-agent pipeline")
        print("  3. Build LangGraph orchestration")
        print("  4. Create Streamlit UI frontend")
        print("  5. Test complete multi-agent pipeline")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. NotificationSystem server is running: python mcp/notificationsystem/server.py")
        print("  2. ANTHROPIC_API_KEY is set")
        print("  3. All dependencies are installed")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
