"""
DecisionSynthesis MCP Server Package
Synthesizes loan decisions from Application DB and RiskRulesDB
"""

__version__ = "1.0.0"
__author__ = "Loan Approval System"

from mcp.decisionsynthesis.client import (
    DecisionSynthesisAsyncClient,
    DecisionSynthesisSyncClient
)

__all__ = [
    "DecisionSynthesisAsyncClient",
    "DecisionSynthesisSyncClient"
]
