"""
MCP Client for communicating with the Application DB MCP Server
"""

import httpx
import json
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class MCPClient:
    """
    Client for interacting with the MCP Server.
    Provides methods to call tools and access resources.
    """

    def __init__(self, base_url: str = "http://localhost:3000"):
        """
        Initialize MCP Client.

        Args:
            base_url: Base URL of MCP server (default: http://localhost:3000)
        """
        self.base_url = base_url
        self.timeout = 30

    async def call_tool(
        self,
        tool_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call an MCP tool asynchronously.

        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool

        Returns:
            Tool result as dictionary
        """
        url = f"{self.base_url}/tools/{tool_name}/call"
        payload = {"arguments": kwargs}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.info(f"Tool call successful: {tool_name}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Tool call failed: {tool_name} - {str(e)}")
            return {"status": "error", "message": str(e)}

    async def read_resource(
        self,
        resource_uri: str
    ) -> Dict[str, Any]:
        """
        Read an MCP resource asynchronously.

        Args:
            resource_uri: URI of the resource (e.g., 'applicant://credit/scoring_rules')

        Returns:
            Resource content as dictionary
        """
        url = f"{self.base_url}/resources/read"
        payload = {"uri": resource_uri}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.info(f"Resource read successful: {resource_uri}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Resource read failed: {resource_uri} - {str(e)}")
            return {"status": "error", "message": str(e)}

    async def list_tools(self) -> Dict[str, Any]:
        """
        List all available tools on the MCP server.

        Returns:
            List of available tools
        """
        url = f"{self.base_url}/tools"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                logger.info("Tools listed successfully")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to list tools: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def list_resources(self) -> Dict[str, Any]:
        """
        List all available resources on the MCP server.

        Returns:
            List of available resources
        """
        url = f"{self.base_url}/resources"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                logger.info("Resources listed successfully")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to list resources: {str(e)}")
            return {"status": "error", "message": str(e)}

    # ========================================================================
    # Convenience Methods for Specific Tools
    # ========================================================================

    async def get_applicant_profile(self, applicant_id: str) -> Dict[str, Any]:
        """Get applicant profile data."""
        return await self.call_tool("get_applicant_profile", applicant_id=applicant_id)

    async def get_income_stability_score(self, applicant_id: str) -> Dict[str, Any]:
        """Get income stability score."""
        return await self.call_tool("get_income_stability_score", applicant_id=applicant_id)

    async def get_employment_risk(self, applicant_id: str) -> Dict[str, Any]:
        """Get employment risk assessment."""
        return await self.call_tool("get_employment_risk", applicant_id=applicant_id)

    async def get_credit_history_summary(self, applicant_id: str) -> Dict[str, Any]:
        """Get credit history summary."""
        return await self.call_tool("get_credit_history_summary", applicant_id=applicant_id)

    async def check_application_completeness(self, applicant_id: str) -> Dict[str, Any]:
        """Check application completeness."""
        return await self.call_tool(
            "check_application_completeness_tool",
            applicant_id=applicant_id
        )

    async def get_complete_analysis(self, applicant_id: str) -> Dict[str, Any]:
        """Get complete applicant analysis."""
        return await self.call_tool(
            "get_complete_applicant_analysis",
            applicant_id=applicant_id
        )

    async def list_all_applicants(self) -> Dict[str, Any]:
        """List all available applicants."""
        return await self.call_tool("list_all_applicants")

    async def get_credit_scoring_rules(self) -> Dict[str, Any]:
        """Get credit scoring rules resource."""
        return await self.read_resource("applicant://credit/scoring_rules")

    async def get_employment_stability_factors(self) -> Dict[str, Any]:
        """Get employment stability factors resource."""
        return await self.read_resource("applicant://employment/stability_factors")

    async def get_regulatory_requirements(self) -> Dict[str, Any]:
        """Get regulatory requirements resource."""
        return await self.read_resource("applicant://compliance/regulatory_requirements")


class SyncMCPClient:
    """
    Synchronous wrapper for MCP Client (useful when async is not available).
    """

    def __init__(self, base_url: str = "http://localhost:3000"):
        """Initialize sync MCP client."""
        self.client = MCPClient(base_url)

    def get_applicant_profile(self, applicant_id: str) -> Dict[str, Any]:
        """Get applicant profile data (sync)."""
        import asyncio
        return asyncio.run(self.client.get_applicant_profile(applicant_id))

    def get_income_stability_score(self, applicant_id: str) -> Dict[str, Any]:
        """Get income stability score (sync)."""
        import asyncio
        return asyncio.run(self.client.get_income_stability_score(applicant_id))

    def get_employment_risk(self, applicant_id: str) -> Dict[str, Any]:
        """Get employment risk (sync)."""
        import asyncio
        return asyncio.run(self.client.get_employment_risk(applicant_id))

    def get_credit_history_summary(self, applicant_id: str) -> Dict[str, Any]:
        """Get credit history summary (sync)."""
        import asyncio
        return asyncio.run(self.client.get_credit_history_summary(applicant_id))

    def check_application_completeness(self, applicant_id: str) -> Dict[str, Any]:
        """Check application completeness (sync)."""
        import asyncio
        return asyncio.run(self.client.check_application_completeness(applicant_id))

    def get_complete_analysis(self, applicant_id: str) -> Dict[str, Any]:
        """Get complete analysis (sync)."""
        import asyncio
        return asyncio.run(self.client.get_complete_analysis(applicant_id))

    def list_all_applicants(self) -> Dict[str, Any]:
        """List all applicants (sync)."""
        import asyncio
        return asyncio.run(self.client.list_all_applicants())

    def get_credit_scoring_rules(self) -> Dict[str, Any]:
        """Get credit scoring rules (sync)."""
        import asyncio
        return asyncio.run(self.client.get_credit_scoring_rules())

    def get_regulatory_requirements(self) -> Dict[str, Any]:
        """Get regulatory requirements (sync)."""
        import asyncio
        return asyncio.run(self.client.get_regulatory_requirements())
