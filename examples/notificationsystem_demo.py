#!/usr/bin/env python3
"""
NotificationSystem Demo
Demonstrates loan decision recording and notification delivery.

Run the server first:
    python mcp/notificationsystem/server.py

Then run this demo:
    python examples/notificationsystem_demo.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.notificationsystem.client import NotificationSystemSyncClient
from datetime import datetime


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_section(text: str):
    """Print formatted section."""
    print(f"\n>>> {text}")
    print("-" * 80)


def demo_record_and_notify():
    """Demo: Record compliance action and send notifications"""
    print_header("DEMO 1: RECORD AND NOTIFY")

    client = NotificationSystemSyncClient()

    print_section("Recording Approval Decision with Notifications")

    result = client.record_and_notify(
        applicant_id="APP001",
        applicant_name="John Strong",
        applicant_email="john.strong@example.com",
        decision="APPROVE",
        risk_score=1.8,
        confidence="High",
        strategy="Balanced",
        reason="Applicant meets all lending criteria with strong financial profile",
        internal_recipients=[
            {
                "name": "Jane Underwriter",
                "email": "jane.underwriter@lender.com",
                "type": "Internal Team"
            },
            {
                "name": "Compliance Officer",
                "email": "compliance@lender.com",
                "type": "Compliance Officer"
            }
        ],
        action_summary="Loan approved for $300,000 at market rate"
    )

    if result.get('status') == 'success':
        print(f"\n✅ Compliance Action Recorded")
        print(f"   Case ID: {result['case_id']}")
        print(f"   Action Taken: {result['action_taken']}")
        print(f"   Decision: {result['decision']}")
        print(f"   Timestamp: {result['timestamp']}")
        print(f"   Notifications Sent: {result['notifications_sent']}")
        print(f"\n📋 Summary:")
        summary = result['summary']
        print(f"   Applicant: {summary['applicant']}")
        print(f"   Action: {summary['action']}")
        print(f"   Decision: {summary['decision']}")
        print(f"   Risk Score: {summary['risk_score']}/5")
        print(f"   Confidence: {summary['confidence']}")
        print(f"   Reason: {summary['reason']}")
        print(f"\n📧 Notification IDs:")
        for i, notif_id in enumerate(result['notification_ids'], 1):
            print(f"   {i}. {notif_id}")

    # Store case_id for later demos
    demo_record_and_notify.last_case_id = result.get('case_id')


def demo_conditional_approval():
    """Demo: Record conditional approval"""
    print_header("DEMO 2: CONDITIONAL APPROVAL WITH CONDITIONS")

    client = NotificationSystemSyncClient()

    print_section("Recording Conditional Approval")

    result = client.record_and_notify(
        applicant_id="APP002",
        applicant_name="Jane Doe",
        applicant_email="jane.doe@example.com",
        decision="CONDITIONAL_APPROVE",
        risk_score=2.9,
        confidence="Moderate",
        strategy="Balanced",
        reason="Applicant approved pending satisfaction of specific conditions",
        internal_recipients=[
            {
                "name": "Legal Team",
                "email": "legal@lender.com",
                "type": "Legal Team"
            }
        ],
        action_summary="Loan conditionally approved for $280,000. Conditions: (1) Reduce monthly debt by $200, (2) Provide employment verification letter"
    )

    if result.get('status') == 'success':
        print(f"\n✅ Conditional Approval Recorded")
        print(f"   Case ID: {result['case_id']}")
        print(f"   Action: {result['action_taken']}")
        print(f"   Status: {result['decision']}")
        print(f"   Risk Score: {result['summary']['risk_score']}/5")
        print(f"   Notifications: {result['notifications_sent']} sent")

    demo_conditional_approval.last_case_id = result.get('case_id')


def demo_get_case_information():
    """Demo: Retrieve case information"""
    print_header("DEMO 3: RETRIEVE CASE INFORMATION")

    client = NotificationSystemSyncClient()

    # Use case from first demo
    if hasattr(demo_record_and_notify, 'last_case_id'):
        case_id = demo_record_and_notify.last_case_id
        print_section(f"Retrieving Case: {case_id}")

        result = client.get_case_information(case_id)

        if result.get('status') == 'success':
            case = result['case']
            print(f"\n📋 Case Details:")
            print(f"   Case ID: {case['case_id']}")
            print(f"   Applicant ID: {case['applicant_id']}")
            print(f"   Action Type: {case['action_type']}")
            print(f"   Decision: {case['decision']}")
            print(f"   Risk Score: {case['risk_score']}")
            print(f"   Confidence: {case['confidence_level']}")
            print(f"   Strategy: {case['strategy_applied']}")
            print(f"   Recorded At: {case['recorded_at']}")
            print(f"   Reason: {case['reason']}")

            print(f"\n📧 Notifications:")
            for i, notif in enumerate(result['notifications'], 1):
                print(f"\n   {i}. Notification ID: {notif['notification_id']}")
                print(f"      Recipient: {notif['recipient_name']} ({notif['recipient_type']})")
                print(f"      Email: {notif['recipient_email']}")
                print(f"      Status: {notif['status']}")
                print(f"      Sent At: {notif['sent_at']}")

            print(f"\n🔐 Audit Trail:")
            audit = case['audit_trail']
            print(f"   Created By: {audit['created_by']}")
            print(f"   Fair Lending Compliant: {audit['fair_lending_compliant']}")


def demo_check_notification_status():
    """Demo: Check notification delivery status"""
    print_header("DEMO 4: CHECK NOTIFICATION STATUS")

    client = NotificationSystemSyncClient()

    # Record a new action to get notification IDs
    print_section("Recording action and checking notification status")

    record_result = client.record_and_notify(
        applicant_id="APP003",
        applicant_name="Robert Smith",
        applicant_email="robert.smith@example.com",
        decision="REVIEW",
        risk_score=3.2,
        confidence="Low",
        strategy="Balanced",
        reason="Application requires manual review due to multiple factors",
        internal_recipients=[
            {
                "name": "Senior Underwriter",
                "email": "senior@lender.com",
                "type": "Internal Team"
            }
        ],
        action_summary="Application routed to senior underwriter for manual review"
    )

    if record_result.get('status') == 'success' and record_result.get('notification_ids'):
        notif_id = record_result['notification_ids'][0]

        print_section(f"Checking notification status: {notif_id}")

        status_result = client.check_notification_status(notif_id)

        if status_result.get('status') == 'success':
            print(f"\n📧 Notification Status:")
            print(f"   Notification ID: {status_result['notification_id']}")
            print(f"   Case ID: {status_result['case_id']}")
            print(f"   Recipient: {status_result['recipient']}")
            print(f"   Status: {status_result['status']}")
            print(f"   Sent At: {status_result['sent_at']}")
            print(f"   Delivery Confirmed: {status_result['delivery_confirmed']}")


def demo_resend_notification():
    """Demo: Resend failed notification"""
    print_header("DEMO 5: RESEND NOTIFICATION")

    client = NotificationSystemSyncClient()

    # Record an action and get notification ID
    record_result = client.record_and_notify(
        applicant_id="APP004",
        applicant_name="Sarah Johnson",
        applicant_email="sarah.johnson@example.com",
        decision="REJECT",
        risk_score=4.5,
        confidence="Very Low",
        strategy="Conservative",
        reason="Application does not meet lending criteria due to high risk profile",
        internal_recipients=[
            {
                "name": "Compliance Officer",
                "email": "compliance@lender.com",
                "type": "Compliance Officer"
            },
            {
                "name": "Legal Team",
                "email": "legal@lender.com",
                "type": "Legal Team"
            }
        ],
        action_summary="Loan application denied - high DTI and recent delinquency"
    )

    if record_result.get('status') == 'success':
        case_id = record_result['case_id']
        notif_id = record_result['notification_ids'][0] if record_result.get('notification_ids') else None

        if notif_id:
            print_section(f"Resending notification: {notif_id}")

            resend_result = client.resend_notification(case_id, notif_id)

            if resend_result.get('status') == 'success':
                print(f"\n✅ Notification Resent")
                print(f"   Notification ID: {resend_result['notification_id']}")
                print(f"   Case ID: {resend_result['case_id']}")
                print(f"   Resent At: {resend_result['resent_at']}")
                print(f"   Message: {resend_result['message']}")


def demo_compliance_report():
    """Demo: Generate compliance report"""
    print_header("DEMO 6: COMPLIANCE REPORT")

    client = NotificationSystemSyncClient()

    print_section("Generating Compliance Report")

    result = client.get_compliance_report()

    if result.get('status') == 'success':
        print(f"\n📊 Compliance Report")
        print(f"   Generated: {result['generated_at']}")
        print(f"   Total Cases: {result['total_cases']}")
        print(f"   Total Notifications: {result['total_notifications']}")

        if result.get('cases_by_action'):
            print(f"\n   Cases by Action Type:")
            for action_type, count in result['cases_by_action'].items():
                print(f"      {action_type}: {count}")

        if result.get('notification_status_summary'):
            print(f"\n   Notification Status Summary:")
            for status, count in result['notification_status_summary'].items():
                print(f"      {status}: {count}")

        if result.get('cases') and len(result['cases']) > 0:
            print(f"\n   Recent Cases:")
            for case in result['cases'][:3]:
                print(f"\n      Case: {case['case_id']}")
                print(f"      Applicant: {case['applicant_id']}")
                print(f"      Action: {case['action']}")
                print(f"      Decision: {case['decision']}")
                print(f"      Notifications Sent: {case['notifications_sent']}")


def demo_resources():
    """Demo: Access compliance resources"""
    print_header("DEMO 7: COMPLIANCE RESOURCES")

    client = NotificationSystemSyncClient()

    print_section("Notification Templates")
    templates = client.get_notification_templates()
    if templates:
        for template_name, template_def in templates.get('templates', {}).items():
            print(f"\n   {template_name.upper()}:")
            print(f"      Subject: {template_def.get('subject')}")
            print(f"      Priority: {template_def.get('priority')}")
            print(f"      Stakeholders: {', '.join(template_def.get('stakeholders', []))}")

    print_section("Compliance Rules")
    rules = client.get_compliance_rules()
    if rules:
        print(f"\n   Notification Timing:")
        for decision, timing in rules.get('rules', {}).get('notification_timing', {}).items():
            print(f"      {decision.upper()}: {timing}")

    print_section("Stakeholder Types")
    stakeholders = client.get_stakeholder_list()
    if stakeholders:
        print(f"\n   Defined Stakeholders:")
        for stakeholder_type, details in stakeholders.get('stakeholders', {}).items():
            print(f"\n      {stakeholder_type.upper()}:")
            print(f"         Description: {details.get('description')}")
            print(f"         Notification Type: {details.get('notification_type')}")
            print(f"         Timing: {details.get('timing')}")


def main():
    """Run all demos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║          NOTIFICATIONSYSTEM DEMO - COMPLIANCE & NOTIFICATION ENGINE            ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    try:
        demo_record_and_notify()
        demo_conditional_approval()
        demo_get_case_information()
        demo_check_notification_status()
        demo_resend_notification()
        demo_compliance_report()
        demo_resources()

        print_header("DEMO COMPLETE")
        print("\n✅ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("  1. Integrate with DecisionSynthesis for full pipeline")
        print("  2. Add email sending integration")
        print("  3. Implement database persistence for case records")
        print("  4. Build compliance dashboard in Streamlit")
        print("  5. Set up automated compliance report generation")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the NotificationSystem server is running:")
        print("  python mcp/notificationsystem/server.py")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
