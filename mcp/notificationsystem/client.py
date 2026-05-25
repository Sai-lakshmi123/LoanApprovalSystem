"""
NotificationSystem MCP Client
Async and Sync clients for compliance notifications and action recording
"""

import asyncio
import httpx
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class NotificationSystemAsyncClient:
    """Async client for NotificationSystem MCP server."""

    def __init__(self, base_url: str = "http://localhost:3003", timeout: float = 30.0):
        """Initialize async client."""
        self.base_url = base_url
        self.timeout = timeout

    async def record_and_notify(
        self,
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

        Args:
            applicant_id: Unique applicant identifier
            applicant_name: Applicant's full name
            applicant_email: Applicant's email address
            decision: Decision classification
            risk_score: Risk score (0-5)
            confidence: Confidence level
            strategy: Strategy applied
            reason: Detailed reason for decision
            internal_recipients: List of internal recipients
            action_summary: Summary of action taken

        Returns:
            Complete record with case ID, notifications, timestamp
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/record_and_notify/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_name": applicant_name,
                    "applicant_email": applicant_email,
                    "decision": decision,
                    "risk_score": risk_score,
                    "confidence": confidence,
                    "strategy": strategy,
                    "reason": reason,
                    "internal_recipients": internal_recipients or [],
                    "action_summary": action_summary
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_case_information(self, case_id: str) -> dict:
        """
        Retrieve complete case information and notification details.

        Args:
            case_id: Case ID from compliance system

        Returns:
            Complete case record with all notifications
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/get_case_information/execute",
                json={"case_id": case_id}
            )
            response.raise_for_status()
            return response.json()

    async def check_notification_status(self, notification_id: str) -> dict:
        """
        Check delivery status of a specific notification.

        Args:
            notification_id: ID of notification to check

        Returns:
            Notification status and delivery information
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/check_notification_status/execute",
                json={"notification_id": notification_id}
            )
            response.raise_for_status()
            return response.json()

    async def get_compliance_report(self, start_date: str = None, end_date: str = None) -> dict:
        """
        Generate compliance report for all actions and notifications.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            Compliance report with summary and case details
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/get_compliance_report/execute",
                json={
                    "start_date": start_date,
                    "end_date": end_date
                }
            )
            response.raise_for_status()
            return response.json()

    async def resend_notification(self, case_id: str, notification_id: str) -> dict:
        """
        Resend a notification if delivery failed.

        Args:
            case_id: Case ID
            notification_id: Notification ID to resend

        Returns:
            Resend status and confirmation
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/resend_notification/execute",
                json={
                    "case_id": case_id,
                    "notification_id": notification_id
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_notification_templates(self) -> dict:
        """Get notification template definitions."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/resources/notification%3A%2F%2Ftemplates%2Fdefinitions"
            )
            response.raise_for_status()
            return response.json()

    async def get_compliance_rules(self) -> dict:
        """Get compliance rules resource."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/resources/notification%3A%2F%2Fcompliance%2Frules"
            )
            response.raise_for_status()
            return response.json()

    async def get_stakeholder_list(self) -> dict:
        """Get stakeholder types and requirements."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/resources/notification%3A%2F%2Fstakeholders%2Flist"
            )
            response.raise_for_status()
            return response.json()


class NotificationSystemSyncClient:
    """Sync client for NotificationSystem MCP server."""

    def __init__(self, base_url: str = "http://localhost:3003", timeout: float = 30.0):
        """Initialize sync client."""
        self.base_url = base_url
        self.timeout = timeout
        self._async_client = NotificationSystemAsyncClient(base_url, timeout)

    def _run_async(self, coro):
        """Run async coroutine in sync context."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                raise RuntimeError("Cannot use sync client from async context")
            return loop.run_until_complete(coro)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()

    def record_and_notify(
        self,
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

        Args:
            applicant_id: Unique applicant identifier
            applicant_name: Applicant's full name
            applicant_email: Applicant's email address
            decision: Decision classification
            risk_score: Risk score (0-5)
            confidence: Confidence level
            strategy: Strategy applied
            reason: Detailed reason for decision
            internal_recipients: List of internal recipients
            action_summary: Summary of action taken

        Returns:
            Complete record with case ID, notifications, timestamp
        """
        return self._run_async(
            self._async_client.record_and_notify(
                applicant_id, applicant_name, applicant_email, decision, risk_score,
                confidence, strategy, reason, internal_recipients, action_summary
            )
        )

    def get_case_information(self, case_id: str) -> dict:
        """
        Retrieve complete case information and notification details.

        Args:
            case_id: Case ID from compliance system

        Returns:
            Complete case record with all notifications
        """
        return self._run_async(self._async_client.get_case_information(case_id))

    def check_notification_status(self, notification_id: str) -> dict:
        """
        Check delivery status of a specific notification.

        Args:
            notification_id: ID of notification to check

        Returns:
            Notification status and delivery information
        """
        return self._run_async(self._async_client.check_notification_status(notification_id))

    def get_compliance_report(self, start_date: str = None, end_date: str = None) -> dict:
        """
        Generate compliance report for all actions and notifications.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)

        Returns:
            Compliance report with summary and case details
        """
        return self._run_async(
            self._async_client.get_compliance_report(start_date, end_date)
        )

    def resend_notification(self, case_id: str, notification_id: str) -> dict:
        """
        Resend a notification if delivery failed.

        Args:
            case_id: Case ID
            notification_id: Notification ID to resend

        Returns:
            Resend status and confirmation
        """
        return self._run_async(
            self._async_client.resend_notification(case_id, notification_id)
        )

    def get_notification_templates(self) -> dict:
        """Get notification template definitions."""
        return self._run_async(self._async_client.get_notification_templates())

    def get_compliance_rules(self) -> dict:
        """Get compliance rules resource."""
        return self._run_async(self._async_client.get_compliance_rules())

    def get_stakeholder_list(self) -> dict:
        """Get stakeholder types and requirements."""
        return self._run_async(self._async_client.get_stakeholder_list())
