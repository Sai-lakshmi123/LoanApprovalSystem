"""
NotificationSystem MCP Server Package
Records compliance actions and manages notifications for loan decisions
"""

__version__ = "1.0.0"
__author__ = "Loan Approval System"

from mcp.notificationsystem.client import (
    NotificationSystemAsyncClient,
    NotificationSystemSyncClient
)

__all__ = [
    "NotificationSystemAsyncClient",
    "NotificationSystemSyncClient"
]
