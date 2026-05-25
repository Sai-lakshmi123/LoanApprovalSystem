"""
DecisionSynthesis MCP Client
Async and Sync clients for loan decision synthesis
"""

import asyncio
import httpx
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class DecisionSynthesisAsyncClient:
    """Async client for DecisionSynthesis MCP server."""

    def __init__(self, base_url: str = "http://localhost:3002", timeout: float = 30.0):
        """Initialize async client."""
        self.base_url = base_url
        self.timeout = timeout

    async def synthesize_loan_decision(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        risk_assessment: dict,
        strategy: str = "Balanced"
    ) -> dict:
        """
        Synthesize loan decision from Application DB and RiskRulesDB inputs.

        Args:
            applicant_id: Unique applicant identifier
            applicant_data: Applicant profile dictionary
            application_analysis: Results from Application DB analysis
            risk_assessment: Results from RiskRulesDB assessment
            strategy: Decision strategy (Conservative/Balanced/Aggressive)

        Returns:
            Final decision with classification, risk score, confidence, factors, and explanation
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/synthesize_loan_decision/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant_data,
                    "application_analysis": application_analysis,
                    "risk_assessment": risk_assessment,
                    "strategy": strategy
                }
            )
            response.raise_for_status()
            return response.json()

    async def evaluate_multiple_scenarios(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        base_risk_assessment: dict,
        scenario_results: list
    ) -> dict:
        """
        Evaluate multiple loan scenarios and compare decisions.

        Args:
            applicant_id: Unique applicant identifier
            applicant_data: Applicant profile
            application_analysis: Application DB analysis
            base_risk_assessment: Base risk assessment
            scenario_results: List of scenario results from RiskRulesDB

        Returns:
            Comparison of decisions across scenarios
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/evaluate_multiple_scenarios/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant_data,
                    "application_analysis": application_analysis,
                    "base_risk_assessment": base_risk_assessment,
                    "scenario_results": scenario_results
                }
            )
            response.raise_for_status()
            return response.json()

    async def explain_decision(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        risk_assessment: dict
    ) -> dict:
        """
        Get detailed explanation of decision rationale.

        Args:
            applicant_id: Unique applicant identifier
            applicant_data: Applicant profile
            application_analysis: Application DB analysis
            risk_assessment: RiskRulesDB assessment

        Returns:
            Detailed explanation with key factors and decision rationale
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/explain_decision/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant_data,
                    "application_analysis": application_analysis,
                    "risk_assessment": risk_assessment
                }
            )
            response.raise_for_status()
            return response.json()

    async def compare_applicants(self, applicants: list) -> dict:
        """
        Compare multiple applicants and their decisions.

        Args:
            applicants: List of applicant data dicts with analyses

        Returns:
            Comparative analysis of applicants
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/tools/compare_applicants/execute",
                json={"applicants": applicants}
            )
            response.raise_for_status()
            return response.json()

    async def get_decision_strategies(self) -> dict:
        """Get decision strategies resource."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/resources/decision%3A%2F%2Fstrategies%2Fdefinitions"
            )
            response.raise_for_status()
            return response.json()

    async def get_decision_classifications(self) -> dict:
        """Get decision classifications resource."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/resources/decision%3A%2F%2Fclassification%2Fdefinitions"
            )
            response.raise_for_status()
            return response.json()

    async def get_confidence_calibration(self) -> dict:
        """Get confidence calibration resource."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/resources/decision%3A%2F%2Fconfidence%2Fcalibration"
            )
            response.raise_for_status()
            return response.json()


class DecisionSynthesisSyncClient:
    """Sync client for DecisionSynthesis MCP server."""

    def __init__(self, base_url: str = "http://localhost:3002", timeout: float = 30.0):
        """Initialize sync client."""
        self.base_url = base_url
        self.timeout = timeout
        self._async_client = DecisionSynthesisAsyncClient(base_url, timeout)

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

    def synthesize_loan_decision(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        risk_assessment: dict,
        strategy: str = "Balanced"
    ) -> dict:
        """
        Synthesize loan decision from Application DB and RiskRulesDB inputs.

        Args:
            applicant_id: Unique applicant identifier
            applicant_data: Applicant profile dictionary
            application_analysis: Results from Application DB analysis
            risk_assessment: Results from RiskRulesDB assessment
            strategy: Decision strategy (Conservative/Balanced/Aggressive)

        Returns:
            Final decision with classification, risk score, confidence, factors, and explanation
        """
        return self._run_async(
            self._async_client.synthesize_loan_decision(
                applicant_id, applicant_data, application_analysis, risk_assessment, strategy
            )
        )

    def evaluate_multiple_scenarios(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        base_risk_assessment: dict,
        scenario_results: list
    ) -> dict:
        """
        Evaluate multiple loan scenarios and compare decisions.

        Args:
            applicant_id: Unique applicant identifier
            applicant_data: Applicant profile
            application_analysis: Application DB analysis
            base_risk_assessment: Base risk assessment
            scenario_results: List of scenario results from RiskRulesDB

        Returns:
            Comparison of decisions across scenarios
        """
        return self._run_async(
            self._async_client.evaluate_multiple_scenarios(
                applicant_id, applicant_data, application_analysis, base_risk_assessment, scenario_results
            )
        )

    def explain_decision(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        risk_assessment: dict
    ) -> dict:
        """
        Get detailed explanation of decision rationale.

        Args:
            applicant_id: Unique applicant identifier
            applicant_data: Applicant profile
            application_analysis: Application DB analysis
            risk_assessment: RiskRulesDB assessment

        Returns:
            Detailed explanation with key factors and decision rationale
        """
        return self._run_async(
            self._async_client.explain_decision(
                applicant_id, applicant_data, application_analysis, risk_assessment
            )
        )

    def compare_applicants(self, applicants: list) -> dict:
        """
        Compare multiple applicants and their decisions.

        Args:
            applicants: List of applicant data dicts with analyses

        Returns:
            Comparative analysis of applicants
        """
        return self._run_async(self._async_client.compare_applicants(applicants))

    def get_decision_strategies(self) -> dict:
        """Get decision strategies resource."""
        return self._run_async(self._async_client.get_decision_strategies())

    def get_decision_classifications(self) -> dict:
        """Get decision classifications resource."""
        return self._run_async(self._async_client.get_decision_classifications())

    def get_confidence_calibration(self) -> dict:
        """Get confidence calibration resource."""
        return self._run_async(self._async_client.get_confidence_calibration())
