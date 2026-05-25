"""
RiskRulesDB MCP Client
For communicating with the RiskRulesDB MCP Server
"""

import httpx
import asyncio
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class RiskRulesDBAsyncClient:
    """
    Async client for RiskRulesDB MCP Server.
    """

    def __init__(self, base_url: str = "http://localhost:3001", timeout: int = 30):
        """
        Initialize async client.

        Args:
            base_url: Base URL of RiskRulesDB server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout

    async def evaluate_dti_ratio(
        self,
        monthly_income: float,
        monthly_debt: float
    ) -> Dict[str, Any]:
        """
        Evaluate Debt-to-Income ratio.

        Args:
            monthly_income: Gross monthly income
            monthly_debt: Total monthly debt

        Returns:
            DTI analysis
        """
        return await self._call_tool("evaluate_dti_ratio", {
            "monthly_income": monthly_income,
            "monthly_debt": monthly_debt
        })

    async def evaluate_credit_risk(
        self,
        credit_score: int,
        delinquencies: int = 0,
        inquiries_last_6_months: int = 0
    ) -> Dict[str, Any]:
        """
        Evaluate credit score risk.

        Args:
            credit_score: Applicant's credit score
            delinquencies: Number of delinquencies
            inquiries_last_6_months: Recent credit inquiries

        Returns:
            Credit risk analysis
        """
        return await self._call_tool("evaluate_credit_risk", {
            "credit_score": credit_score,
            "delinquencies": delinquencies,
            "inquiries_last_6_months": inquiries_last_6_months
        })

    async def evaluate_loan_amount_risk(
        self,
        loan_amount: float,
        annual_income: float,
        property_value: Optional[float] = None,
        existing_loans: int = 0,
        credit_score: int = 0
    ) -> Dict[str, Any]:
        """
        Evaluate loan amount risk.

        Args:
            loan_amount: Requested loan amount
            annual_income: Applicant's annual income
            property_value: Property value (for LTV)
            existing_loans: Number of existing loans
            credit_score: Applicant's credit score

        Returns:
            Loan amount risk analysis
        """
        return await self._call_tool("evaluate_loan_amount_risk", {
            "loan_amount": loan_amount,
            "annual_income": annual_income,
            "property_value": property_value,
            "existing_loans": existing_loans,
            "credit_score": credit_score
        })

    async def detect_risk_anomalies(
        self,
        applicant_data: Dict[str, Any],
        loan_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detect anomalies in applicant data and loan request.

        Args:
            applicant_data: Applicant profile dictionary
            loan_request: Loan request details

        Returns:
            Anomaly detection results
        """
        return await self._call_tool("detect_risk_anomalies", {
            "applicant_data": applicant_data,
            "loan_request": loan_request
        })

    async def generate_risk_report(
        self,
        applicant_id: str,
        applicant_data: Dict[str, Any],
        loan_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive risk report.

        Args:
            applicant_id: Unique applicant ID
            applicant_data: Applicant profile
            loan_request: Loan request details

        Returns:
            Complete risk assessment report
        """
        return await self._call_tool("generate_risk_report", {
            "applicant_id": applicant_id,
            "applicant_data": applicant_data,
            "loan_request": loan_request
        })

    async def evaluate_with_scenario_analysis(
        self,
        applicant_id: str,
        applicant_data: Dict[str, Any],
        loan_request: Dict[str, Any],
        scenarios: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate with scenario analysis.

        Args:
            applicant_id: Unique applicant ID
            applicant_data: Applicant profile
            loan_request: Loan request details
            scenarios: Alternative scenarios to evaluate

        Returns:
            Risk assessment with scenarios
        """
        return await self._call_tool("evaluate_with_scenario_analysis", {
            "applicant_id": applicant_id,
            "applicant_data": applicant_data,
            "loan_request": loan_request,
            "scenarios": scenarios
        })

    async def get_dti_guidelines(self) -> Dict[str, Any]:
        """Get DTI guidelines resource."""
        return await self._read_resource("risk://dti/guidelines")

    async def get_credit_assessment_criteria(self) -> Dict[str, Any]:
        """Get credit assessment criteria resource."""
        return await self._read_resource("risk://credit/assessment_criteria")

    async def get_loan_risk_criteria(self) -> Dict[str, Any]:
        """Get loan risk assessment criteria resource."""
        return await self._read_resource("risk://loan/risk_assessment")

    async def get_anomaly_rules(self) -> Dict[str, Any]:
        """Get anomaly detection rules resource."""
        return await self._read_resource("risk://anomalies/detection_rules")

    async def get_regulatory_rules(self) -> Dict[str, Any]:
        """Get regulatory compliance rules resource."""
        return await self._read_resource("risk://regulatory/compliance")

    async def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            Tool result
        """
        url = f"{self.base_url}/tools/{tool_name}/call"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json={"arguments": arguments})
                response.raise_for_status()
                logger.info(f"Tool call successful: {tool_name}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Tool call failed: {tool_name} - {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """
        Read a resource from the MCP server.

        Args:
            resource_uri: Resource URI

        Returns:
            Resource content
        """
        url = f"{self.base_url}/resources/read"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json={"uri": resource_uri})
                response.raise_for_status()
                logger.info(f"Resource read successful: {resource_uri}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Resource read failed: {resource_uri} - {str(e)}")
            return {"status": "error", "message": str(e)}


class RiskRulesDBSyncClient:
    """
    Synchronous client for RiskRulesDB MCP Server.
    """

    def __init__(self, base_url: str = "http://localhost:3001", timeout: int = 30):
        """Initialize sync client."""
        self.client = RiskRulesDBAsyncClient(base_url, timeout)

    def evaluate_dti_ratio(
        self,
        monthly_income: float,
        monthly_debt: float
    ) -> Dict[str, Any]:
        """Evaluate DTI ratio (sync)."""
        return asyncio.run(
            self.client.evaluate_dti_ratio(monthly_income, monthly_debt)
        )

    def evaluate_credit_risk(
        self,
        credit_score: int,
        delinquencies: int = 0,
        inquiries_last_6_months: int = 0
    ) -> Dict[str, Any]:
        """Evaluate credit risk (sync)."""
        return asyncio.run(
            self.client.evaluate_credit_risk(
                credit_score, delinquencies, inquiries_last_6_months
            )
        )

    def evaluate_loan_amount_risk(
        self,
        loan_amount: float,
        annual_income: float,
        property_value: Optional[float] = None,
        existing_loans: int = 0,
        credit_score: int = 0
    ) -> Dict[str, Any]:
        """Evaluate loan amount risk (sync)."""
        return asyncio.run(
            self.client.evaluate_loan_amount_risk(
                loan_amount, annual_income, property_value, existing_loans, credit_score
            )
        )

    def detect_risk_anomalies(
        self,
        applicant_data: Dict[str, Any],
        loan_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect anomalies (sync)."""
        return asyncio.run(
            self.client.detect_risk_anomalies(applicant_data, loan_request)
        )

    def generate_risk_report(
        self,
        applicant_id: str,
        applicant_data: Dict[str, Any],
        loan_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate risk report (sync)."""
        return asyncio.run(
            self.client.generate_risk_report(applicant_id, applicant_data, loan_request)
        )

    def evaluate_with_scenario_analysis(
        self,
        applicant_id: str,
        applicant_data: Dict[str, Any],
        loan_request: Dict[str, Any],
        scenarios: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Evaluate with scenarios (sync)."""
        return asyncio.run(
            self.client.evaluate_with_scenario_analysis(
                applicant_id, applicant_data, loan_request, scenarios
            )
        )

    def get_dti_guidelines(self) -> Dict[str, Any]:
        """Get DTI guidelines (sync)."""
        return asyncio.run(self.client.get_dti_guidelines())

    def get_credit_assessment_criteria(self) -> Dict[str, Any]:
        """Get credit criteria (sync)."""
        return asyncio.run(self.client.get_credit_assessment_criteria())

    def get_loan_risk_criteria(self) -> Dict[str, Any]:
        """Get loan risk criteria (sync)."""
        return asyncio.run(self.client.get_loan_risk_criteria())

    def get_anomaly_rules(self) -> Dict[str, Any]:
        """Get anomaly rules (sync)."""
        return asyncio.run(self.client.get_anomaly_rules())

    def get_regulatory_rules(self) -> Dict[str, Any]:
        """Get regulatory rules (sync)."""
        return asyncio.run(self.client.get_regulatory_rules())
