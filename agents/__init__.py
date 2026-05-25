"""
Multi-Agent Loan Approval System
Anthropic Agent SDK with Claude models

Agents:
  Agent1: Application Profile Agent - Analyzes loan applicant profiles
  Agent2: Financial Risk Analysis Agent - Evaluates financial risk
  Agent3: Decision Synthesis Agent - Makes final decisions
  Agent4: Compliance & Action Orchestrator - Records decisions and notifies
"""

__version__ = "1.0.0"
__author__ = "Loan Approval System"

from agents.application_profile_agent import (
    ApplicationProfileAgent,
    ApplicationDBClient
)
from agents.financial_risk_analysis_agent import (
    FinancialRiskAnalysisAgent,
    RiskRulesDBClient
)
from agents.loan_decision_agent import (
    LoanDecisionAgent,
    DecisionSynthesisClient
)
from agents.compliance_action_agent import (
    ComplianceActionAgent,
    NotificationSystemClient
)

__all__ = [
    "ApplicationProfileAgent",
    "ApplicationDBClient",
    "FinancialRiskAnalysisAgent",
    "RiskRulesDBClient",
    "LoanDecisionAgent",
    "DecisionSynthesisClient",
    "ComplianceActionAgent",
    "NotificationSystemClient"
]
