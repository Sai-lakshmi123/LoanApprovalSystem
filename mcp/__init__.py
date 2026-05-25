"""
MCP (Model Context Protocol) Integration Layer

Provides tools and resources for applicant data access and analysis.
"""

from mcp.clients.mcp_client import MCPClient, SyncMCPClient

__all__ = [
    "MCPClient",
    "SyncMCPClient",
]
