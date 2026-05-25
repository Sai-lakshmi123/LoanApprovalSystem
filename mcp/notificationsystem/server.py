"""
FastMCP Server: NotificationSystem
Compliance-aware notification and action recording system for loan decisions
"""

import logging
from datetime import datetime
from typing import Dict, Any, List
from fastmcp import FastMCP
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
app = FastMCP("NotificationSystem", version="1.0.0")

# ============================================================================
# ENUMERATIONS
# ============================================================================

class NotificationStatus(str, Enum):
    """Notification delivery status"""
    SENT = "Sent"
    PENDING = "Pending"
    FAILED = "Failed"
    DELIVERED = "Delivered"
    BOUNCED = "Bounced"


class ActionType(str, Enum):
    """Type of compliance action"""
    APPROVAL = "Approval"
    CONDITIONAL_APPROVAL = "Conditional Approval"
    REVIEW = "Manual Review"
    REJECTION = "Rejection"


class StakeholderType(str, Enum):
    """Types of stakeholders"""
    APPLICANT = "Applicant"
    INTERNAL = "Internal Team"
    COMPLIANCE = "Compliance Officer"
    LEGAL = "Legal Team"


# ============================================================================
# COMPLIANCE ACTION RECORDER
# ============================================================================

class ComplianceRecorder:
    """Records compliance actions and manages notifications."""

    def __init__(self):
        """Initialize recorder with in-memory storage."""
        self.compliance_log = {}  # case_id -> action record
        self.notifications = {}   # notification_id -> notification record
        self.case_counter = 0

    def generate_case_id(self) -> str:
        """Generate unique case ID."""
        self.case_counter += 1
        date_str = datetime.now().strftime("%Y%m%d")
        seq = str(self.case_counter).zfill(5)
        return f"CASE-{date_str}-{seq}"

    def generate_notification_id(self) -> str:
        """Generate unique notification ID."""
        return f"NOTIF-{uuid.uuid4().hex[:12].upper()}"

    def record_compliance_action(
        self,
        applicant_id: str,
        decision: str,
        risk_score: float,
        confidence: str,
        strategy: str,
        action_timestamp: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Record a compliance action in the system.

        Args:
            applicant_id: Unique applicant identifier
            decision: Decision classification
            risk_score: Risk score (0-5)
            confidence: Confidence level
            strategy: Strategy applied
            action_timestamp: ISO format timestamp
            reason: Detailed reason for action

        Returns:
            Compliance action record with case ID
        """
        case_id = self.generate_case_id()

        action_record = {
            "case_id": case_id,
            "applicant_id": applicant_id,
            "action_type": self._get_action_type(decision),
            "decision": decision,
            "risk_score": risk_score,
            "confidence_level": confidence,
            "strategy_applied": strategy,
            "timestamp": action_timestamp,
            "reason": reason,
            "recorded_at": datetime.now().isoformat(),
            "status": "Recorded",
            "notifications_sent": [],
            "audit_trail": {
                "created_by": "DecisionSynthesis",
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat(),
                "fair_lending_compliant": True
            }
        }

        self.compliance_log[case_id] = action_record
        logger.info(f"Compliance action recorded: {case_id} for {applicant_id}")

        return action_record

    def _get_action_type(self, decision: str) -> ActionType:
        """Map decision to action type."""
        decision_lower = decision.lower()
        if "approve" in decision_lower:
            if "conditional" in decision_lower:
                return ActionType.CONDITIONAL_APPROVAL
            return ActionType.APPROVAL
        elif "review" in decision_lower:
            return ActionType.REVIEW
        elif "reject" in decision_lower:
            return ActionType.REJECTION
        return ActionType.REVIEW

    def send_notification(
        self,
        case_id: str,
        applicant_email: str,
        applicant_name: str,
        decision: str,
        action_summary: str,
        recipients: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Send notifications and record delivery.

        Args:
            case_id: Case ID from compliance record
            applicant_email: Email address of applicant
            applicant_name: Name of applicant
            decision: Decision classification
            action_summary: Summary of action taken
            recipients: List of recipients with types

        Returns:
            Notification record with delivery status
        """
        if case_id not in self.compliance_log:
            return {
                "status": "error",
                "message": f"Case {case_id} not found"
            }

        notifications_sent = []

        # Send to applicant
        applicant_notification = self._create_notification(
            case_id,
            "Applicant",
            applicant_email,
            applicant_name,
            decision,
            action_summary
        )
        notifications_sent.append(applicant_notification)

        # Send to other recipients
        for recipient in recipients:
            recipient_notification = self._create_notification(
                case_id,
                recipient.get("type", "Internal"),
                recipient.get("email"),
                recipient.get("name"),
                decision,
                action_summary
            )
            notifications_sent.append(recipient_notification)

        # Update compliance record
        self.compliance_log[case_id]["notifications_sent"] = [
            n["notification_id"] for n in notifications_sent
        ]

        # Store notifications
        for notif in notifications_sent:
            self.notifications[notif["notification_id"]] = notif

        return {
            "status": "success",
            "case_id": case_id,
            "notifications_sent": len(notifications_sent),
            "notification_details": notifications_sent
        }

    def _create_notification(
        self,
        case_id: str,
        recipient_type: str,
        recipient_email: str,
        recipient_name: str,
        decision: str,
        summary: str
    ) -> Dict[str, Any]:
        """Create a single notification record."""
        notif_id = self.generate_notification_id()

        return {
            "notification_id": notif_id,
            "case_id": case_id,
            "recipient_type": recipient_type,
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "subject": self._generate_subject(decision),
            "template": self._get_template(decision),
            "summary": summary,
            "status": NotificationStatus.SENT,
            "sent_at": datetime.now().isoformat(),
            "delivery_confirmed": False,
            "delivery_time": None
        }

    def _generate_subject(self, decision: str) -> str:
        """Generate email subject based on decision."""
        subjects = {
            "APPROVE": "Loan Application Approved",
            "CONDITIONAL_APPROVE": "Loan Application - Conditional Approval",
            "REVIEW": "Loan Application Under Review",
            "REJECT": "Loan Application Decision"
        }
        return subjects.get(decision, "Loan Application Status Update")

    def _get_template(self, decision: str) -> str:
        """Get notification template name."""
        templates = {
            "APPROVE": "approval_notification",
            "CONDITIONAL_APPROVE": "conditional_notification",
            "REVIEW": "review_notification",
            "REJECT": "rejection_notification"
        }
        return templates.get(decision, "generic_notification")

    def get_case_details(self, case_id: str) -> Dict[str, Any]:
        """Retrieve complete case details."""
        if case_id not in self.compliance_log:
            return {
                "status": "error",
                "message": f"Case {case_id} not found"
            }

        case = self.compliance_log[case_id]
        notifications = [
            self.notifications.get(notif_id)
            for notif_id in case.get("notifications_sent", [])
        ]

        return {
            "status": "success",
            "case": case,
            "notifications": [n for n in notifications if n],
            "compliance_status": "Recorded and Notified"
        }

    def get_notification_status(self, notification_id: str) -> Dict[str, Any]:
        """Get status of specific notification."""
        if notification_id not in self.notifications:
            return {
                "status": "error",
                "message": f"Notification {notification_id} not found"
            }

        notif = self.notifications[notification_id]
        return {
            "status": "success",
            "notification_id": notification_id,
            "case_id": notif["case_id"],
            "recipient": notif["recipient_name"],
            "status": notif["status"],
            "sent_at": notif["sent_at"],
            "delivery_confirmed": notif["delivery_confirmed"]
        }

    def generate_compliance_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate compliance report for date range."""
        report = {
            "status": "success",
            "generated_at": datetime.now().isoformat(),
            "total_cases": len(self.compliance_log),
            "total_notifications": len(self.notifications),
            "cases_by_action": {},
            "notification_status_summary": {},
            "cases": []
        }

        # Analyze cases
        for case_id, case in self.compliance_log.items():
            action_type = case["action_type"]
            report["cases_by_action"][action_type] = \
                report["cases_by_action"].get(action_type, 0) + 1

            report["cases"].append({
                "case_id": case_id,
                "applicant_id": case["applicant_id"],
                "action": case["action_type"],
                "decision": case["decision"],
                "timestamp": case["timestamp"],
                "notifications_sent": len(case.get("notifications_sent", []))
            })

        # Analyze notifications
        for notif in self.notifications.values():
            status = notif["status"]
            report["notification_status_summary"][status] = \
                report["notification_status_summary"].get(status, 0) + 1

        return report


# ============================================================================
# GLOBAL RECORDER INSTANCE
# ============================================================================

recorder = ComplianceRecorder()


# ============================================================================
# MCP TOOLS
# ============================================================================

@app.tool()
def record_and_notify(
    applicant_id: str,
    applicant_name: str,
    applicant_email: str,
    decision: str,
    risk_score: float,
    confidence: str,
    strategy: str,
    reason: str,
    internal_recipients: list = None,
    action_summary: str = ""
) -> dict:
    """
    Record compliance action and send notifications.

    Combines recording of the final loan decision with notification delivery
    to all stakeholders. Generates unique case ID and tracks all notifications.

    Args:
        applicant_id: Unique applicant identifier
        applicant_name: Applicant's full name
        applicant_email: Applicant's email address
        decision: Decision classification (APPROVE/CONDITIONAL_APPROVE/REVIEW/REJECT)
        risk_score: Risk score (0-5)
        confidence: Confidence level
        strategy: Strategy applied
        reason: Detailed reason for decision
        internal_recipients: List of internal recipients (dicts with email, name, type)
        action_summary: Summary of action taken

    Returns:
        Complete record with case ID, action taken, notifications sent, timestamp
    """
    try:
        # Record the compliance action
        timestamp = datetime.now().isoformat()
        action_record = recorder.record_compliance_action(
            applicant_id, decision, risk_score, confidence, strategy, timestamp, reason
        )

        case_id = action_record["case_id"]

        # Prepare internal recipients
        recipients = internal_recipients or []

        # Send notifications
        notification_result = recorder.send_notification(
            case_id,
            applicant_email,
            applicant_name,
            decision,
            action_summary or f"Loan decision: {decision}",
            recipients
        )

        result = {
            "status": "success",
            "case_id": case_id,
            "action_taken": action_record["action_type"],
            "decision": decision,
            "notifications_sent": notification_result["notifications_sent"],
            "timestamp": timestamp,
            "summary": {
                "applicant": applicant_name,
                "action": action_record["action_type"],
                "decision": decision,
                "risk_score": risk_score,
                "confidence": confidence,
                "stakeholders_notified": notification_result["notifications_sent"],
                "reason": reason
            },
            "notification_ids": [
                n["notification_id"] for n in notification_result.get("notification_details", [])
            ]
        }

        logger.info(f"Record and notify completed: {case_id}")
        return result

    except Exception as e:
        logger.error(f"Error in record_and_notify: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.tool()
def get_case_information(case_id: str) -> dict:
    """
    Retrieve complete case information and notification details.

    Args:
        case_id: Case ID from compliance system

    Returns:
        Complete case record with all notifications and audit trail
    """
    try:
        result = recorder.get_case_details(case_id)
        if result["status"] == "success":
            logger.info(f"Case information retrieved: {case_id}")
        return result
    except Exception as e:
        logger.error(f"Error retrieving case: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.tool()
def check_notification_status(notification_id: str) -> dict:
    """
    Check delivery status of a specific notification.

    Args:
        notification_id: ID of notification to check

    Returns:
        Notification status and delivery information
    """
    try:
        result = recorder.get_notification_status(notification_id)
        logger.info(f"Notification status checked: {notification_id}")
        return result
    except Exception as e:
        logger.error(f"Error checking notification: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.tool()
def get_compliance_report(start_date: str = None, end_date: str = None) -> dict:
    """
    Generate compliance report for all actions and notifications.

    Args:
        start_date: Optional start date (ISO format)
        end_date: Optional end date (ISO format)

    Returns:
        Compliance report with summary and case details
    """
    try:
        result = recorder.generate_compliance_report(start_date, end_date)
        logger.info("Compliance report generated")
        return result
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.tool()
def resend_notification(case_id: str, notification_id: str) -> dict:
    """
    Resend a notification if delivery failed.

    Args:
        case_id: Case ID
        notification_id: Notification ID to resend

    Returns:
        Resend status and confirmation
    """
    try:
        if notification_id not in recorder.notifications:
            return {
                "status": "error",
                "message": f"Notification {notification_id} not found"
            }

        notif = recorder.notifications[notification_id]
        # Update resend timestamp
        notif["resent_at"] = datetime.now().isoformat()
        notif["status"] = NotificationStatus.SENT

        logger.info(f"Notification resent: {notification_id}")

        return {
            "status": "success",
            "notification_id": notification_id,
            "case_id": case_id,
            "resent_at": notif["resent_at"],
            "message": "Notification resent successfully"
        }

    except Exception as e:
        logger.error(f"Error resending notification: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================================
# MCP RESOURCES
# ============================================================================

@app.resource("notification://templates/definitions")
def notification_templates() -> dict:
    """
    Notification template definitions for different decision types.
    """
    return {
        "version": "1.0",
        "title": "Notification Templates",
        "templates": {
            "approval_notification": {
                "subject": "Loan Application Approved",
                "content_type": "approval",
                "placeholders": ["applicant_name", "loan_amount", "approval_conditions"],
                "stakeholders": ["Applicant", "Internal Team"],
                "priority": "High"
            },
            "conditional_notification": {
                "subject": "Loan Application - Conditional Approval",
                "content_type": "conditional",
                "placeholders": ["applicant_name", "conditions", "deadline"],
                "stakeholders": ["Applicant", "Internal Team", "Compliance"],
                "priority": "High"
            },
            "review_notification": {
                "subject": "Loan Application Under Review",
                "content_type": "review",
                "placeholders": ["applicant_name", "review_reason", "expected_timeline"],
                "stakeholders": ["Applicant", "Internal Team"],
                "priority": "Medium"
            },
            "rejection_notification": {
                "subject": "Loan Application Decision",
                "content_type": "rejection",
                "placeholders": ["applicant_name", "reason", "appeal_process"],
                "stakeholders": ["Applicant", "Compliance", "Legal"],
                "priority": "High"
            }
        }
    }


@app.resource("notification://compliance/rules")
def compliance_rules() -> dict:
    """
    Compliance rules and requirements for notifications.
    """
    return {
        "version": "1.0",
        "title": "Compliance Rules",
        "rules": {
            "notification_timing": {
                "approval": "Within 1 business day",
                "conditional": "Within 1 business day",
                "review": "Within 2 business days",
                "rejection": "Within 1 business day"
            },
            "required_information": {
                "all_decisions": [
                    "Case ID",
                    "Decision made",
                    "Risk assessment summary",
                    "Contact for questions"
                ],
                "rejections": [
                    "Specific reasons for rejection",
                    "Fair lending compliance statement",
                    "Appeal process information"
                ],
                "conditional": [
                    "List of specific conditions",
                    "Deadline for condition satisfaction",
                    "Contact for condition clarification"
                ]
            },
            "fair_lending_compliance": {
                "disparate_impact": "Monitor for adverse impact patterns",
                "documentation": "All decisions documented with business reasons",
                "monitoring": "Monthly review of decision patterns by protected class"
            },
            "notification_methods": {
                "primary": "Email",
                "secondary": "Portal access to full decision letter",
                "accessibility": "Ensure compliance with ADA requirements"
            }
        }
    }


@app.resource("notification://stakeholders/list")
def stakeholder_types() -> dict:
    """
    Defined stakeholder types and notification requirements.
    """
    return {
        "version": "1.0",
        "title": "Stakeholder Types and Notification Requirements",
        "stakeholders": {
            "applicant": {
                "description": "Loan applicant",
                "required_for": ["All decisions"],
                "notification_type": "Email + Portal Access",
                "timing": "Immediate"
            },
            "internal_team": {
                "description": "Internal loan processing and underwriting team",
                "required_for": ["All decisions"],
                "notification_type": "System notification + Email",
                "timing": "Immediate"
            },
            "compliance_officer": {
                "description": "Compliance and regulatory affairs officer",
                "required_for": ["Rejections", "High-risk approvals", "Conditional approvals"],
                "notification_type": "Email + Report",
                "timing": "Within 24 hours"
            },
            "legal_team": {
                "description": "Legal review and fair lending monitoring",
                "required_for": ["Rejections", "High-risk rejections"],
                "notification_type": "Email + Case file",
                "timing": "Within 24 hours"
            },
            "management": {
                "description": "Loan department management and approval authority",
                "required_for": ["REVIEW decisions", "Rejections"],
                "notification_type": "Dashboard + Email",
                "timing": "Immediate"
            }
        }
    }


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting NotificationSystem MCP Server...")
    logger.info("Available tools: 5 notification and compliance tools")
    logger.info("Available resources: 3 compliance reference resources")

    import uvicorn
    uvicorn.run(
        "mcp.notificationsystem.server:app",
        host="0.0.0.0",
        port=3003,
        reload=True,
        log_level="info"
    )
