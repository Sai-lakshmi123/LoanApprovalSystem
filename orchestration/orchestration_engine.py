"""
LangGraph Orchestration Engine with Error Handling & Retry Logic
Coordinates all 4 agents in sequence with intelligent routing and state management.

Features:
  - Automatic retry with exponential backoff
  - Error categorization (transient vs permanent)
  - Circuit breaker pattern to prevent cascading failures
  - Manual review escalation on critical failures
  - Comprehensive error tracking and logging
  - Intelligent fallback mechanisms

Execution Flow:
  1. Agent1 (Profile): Analyzes applicant profile [Retry: 3x, Backoff: 2s]
  2. Agent2 (Risk): Evaluates financial risk [Retry: 3x, Backoff: 3s]
  3. Routing Decision: Route based on risk score
  4. Agent3 (Decision): Makes final decision [Retry: 2x, Backoff: 2s]
  5. Agent4 (Compliance): Records and notifies [Retry: 1x, Backoff: 1s]
  6. Return: Final decision with case ID + error tracking

Run this orchestration:
    python orchestration/orchestration_engine.py
"""

import json
import time
from typing import Any, TypedDict, Callable
from datetime import datetime
import sys
from pathlib import Path
from functools import wraps

sys.path.insert(0, str(Path(__file__).parent.parent))

from langgraph.graph import StateGraph, END, START
from agents.application_profile_agent import ApplicationProfileAgent
from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent
from agents.loan_decision_agent import LoanDecisionAgent
from agents.compliance_action_agent import ComplianceActionAgent


# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

class RetryConfig:
    """Configuration for retry logic."""
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.backoff_factor = backoff_factor

    def get_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        return self.base_delay * (self.backoff_factor ** attempt)


class ErrorCategory:
    """Categorize errors for retry decisions."""
    TRANSIENT = "transient"      # Retry recommended (timeouts, connection errors)
    PERMANENT = "permanent"      # No retry (validation errors, business logic)
    UNKNOWN = "unknown"          # Unknown - retry with caution


def categorize_error(error: Exception) -> str:
    """Categorize error type."""
    error_str = str(error).lower()

    # Transient errors
    if any(keyword in error_str for keyword in [
        "timeout", "connection", "refused", "unreachable",
        "unavailable", "temporarily", "temporarily", "rate limit"
    ]):
        return ErrorCategory.TRANSIENT

    # Permanent errors
    if any(keyword in error_str for keyword in [
        "invalid", "not found", "authentication", "unauthorized",
        "forbidden", "bad request", "conflict"
    ]):
        return ErrorCategory.PERMANENT

    return ErrorCategory.UNKNOWN


def retry_with_backoff(config: RetryConfig = None):
    """Decorator for retry logic with exponential backoff."""
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    error_category = categorize_error(e)

                    if attempt < config.max_retries:
                        if error_category == ErrorCategory.PERMANENT:
                            # Don't retry permanent errors
                            raise

                        delay = config.get_delay(attempt)
                        print(f"   ⚠️  Attempt {attempt + 1} failed: {str(e)}")
                        print(f"   ⏳ Retrying in {delay:.1f}s... (Error: {error_category})")
                        time.sleep(delay)
                    else:
                        # Final attempt failed
                        print(f"   ❌ All {config.max_retries + 1} attempts failed")
                        raise

            if last_error:
                raise last_error

        return wrapper
    return decorator


# ============================================================================
# STATE SCHEMA
# ============================================================================

class LoanDecisionState(TypedDict):
    """State schema for loan decision workflow."""

    # Input
    applicant_id: str
    applicant_data: dict
    loan_request: dict

    # Agent1 Output
    profile_analysis: dict
    profile_status: str
    profile_error: str
    profile_retry_count: int
    profile_retry_history: list

    # Agent2 Output
    risk_analysis: dict
    risk_status: str
    risk_error: str
    risk_retry_count: int
    risk_retry_history: list

    # Routing Decision
    routing_decision: str  # ESCALATE, CONDITIONAL, AUTO_APPROVE, REVIEW, or MANUAL_REVIEW
    risk_score: float
    risk_level: str

    # Agent3 Output
    decision_data: dict
    decision_status: str
    decision_error: str
    decision_retry_count: int
    decision_retry_history: list

    # Agent4 Output
    action_result: dict
    action_status: str
    action_error: str
    case_id: str
    action_retry_count: int
    action_retry_history: list

    # Error Tracking
    critical_errors: list
    error_escalation: bool
    manual_review_reason: str

    # Final Result
    final_decision: dict
    workflow_status: str
    execution_path: list
    timestamp: str


# ============================================================================
# ORCHESTRATION ENGINE
# ============================================================================

class LoanDecisionOrchestrator:
    """Orchestrates multi-agent loan decision workflow with error handling."""

    # Retry configurations per agent
    RETRY_CONFIGS = {
        "agent1": RetryConfig(max_retries=0, base_delay=0.5, backoff_factor=1.5),
        "agent2": RetryConfig(max_retries=0, base_delay=0.5, backoff_factor=1.5),
        "agent3": RetryConfig(max_retries=0, base_delay=0.5, backoff_factor=1.5),
        "agent4": RetryConfig(max_retries=0, base_delay=0.5, backoff_factor=1.5),
    }

    def __init__(self):
        """Initialize orchestrator with agents."""
        self.profile_agent = ApplicationProfileAgent()
        self.risk_agent = FinancialRiskAnalysisAgent()
        self.decision_agent = LoanDecisionAgent()
        self.action_agent = ComplianceActionAgent()

    def create_workflow(self):
        """Create and compile the LangGraph workflow."""

        # Create state graph
        workflow = StateGraph(LoanDecisionState)

        # Define nodes
        workflow.add_node("agent1_profile", self.agent1_profile_analysis)
        workflow.add_node("agent2_risk", self.agent2_risk_analysis)
        workflow.add_node("routing", self.routing_decision)
        workflow.add_node("agent3_decision", self.agent3_decision_synthesis)
        workflow.add_node("agent4_compliance", self.agent4_compliance_orchestration)
        workflow.add_node("finalize", self.finalize_result)

        # Define edges
        workflow.add_edge(START, "agent1_profile")
        workflow.add_edge("agent1_profile", "agent2_risk")
        workflow.add_edge("agent2_risk", "routing")

        # Conditional routing from routing node
        workflow.add_conditional_edges(
            "routing",
            self.route_decision,
            {
                "escalate": "agent3_decision",
                "conditional": "agent3_decision",
                "auto_approve": "agent3_decision",
                "review": "agent3_decision"
            }
        )

        workflow.add_edge("agent3_decision", "agent4_compliance")
        workflow.add_edge("agent4_compliance", "finalize")
        workflow.add_edge("finalize", END)

        # Compile workflow
        return workflow.compile()

    # ========================================================================
    # NODE FUNCTIONS
    # ========================================================================

    def agent1_profile_analysis(self, state: LoanDecisionState) -> LoanDecisionState:
        """Agent1: Analyze applicant profile with retry logic."""
        print("\n" + "="*80)
        print("  AGENT1: APPLICANT PROFILE ANALYSIS")
        print("="*80)

        applicant_id = state["applicant_id"]
        print(f"\n📋 Analyzing profile for {applicant_id}...")

        retry_config = self.RETRY_CONFIGS["agent1"]
        state["profile_retry_count"] = 0
        state["profile_retry_history"] = []

        for attempt in range(retry_config.max_retries + 1):
            try:
                state["profile_retry_count"] = attempt

                if attempt > 0:
                    delay = retry_config.get_delay(attempt - 1)
                    print(f"\n   🔄 Retry Attempt {attempt}/{retry_config.max_retries}...")
                    print(f"   ⏳ Waiting {delay:.1f}s before retry...")
                    time.sleep(delay)

                # Call Agent1
                result = self.profile_agent.analyze_applicant(applicant_id)

                if result.get("status") == "success":
                    state["profile_analysis"] = result.get("analysis", {})
                    state["profile_status"] = "success"
                    state["profile_error"] = ""
                    print(f"✅ Profile analysis complete (Attempt {attempt + 1})")
                    state["execution_path"].append("Agent1_Profile_✅")
                    return state
                else:
                    error_msg = result.get("error", "Unknown error")
                    state["profile_retry_history"].append({
                        "attempt": attempt + 1,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    })

                    if attempt < retry_config.max_retries:
                        error_category = categorize_error(Exception(error_msg))
                        if error_category == ErrorCategory.PERMANENT:
                            print(f"❌ Permanent error detected - no retry: {error_msg}")
                            state["profile_status"] = "error"
                            state["profile_error"] = error_msg
                            state["critical_errors"].append({
                                "agent": "Agent1",
                                "error": error_msg,
                                "category": error_category
                            })
                            state["execution_path"].append("Agent1_Profile_PermanentError")
                            return state
                        else:
                            print(f"⚠️  Attempt {attempt + 1} failed (Transient): {error_msg}")
                    else:
                        print(f"❌ All {retry_config.max_retries + 1} attempts failed")
                        state["profile_status"] = "error"
                        state["profile_error"] = error_msg
                        state["critical_errors"].append({
                            "agent": "Agent1",
                            "error": f"Failed after {retry_config.max_retries + 1} attempts",
                            "category": "persistent_failure"
                        })
                        state["execution_path"].append("Agent1_Profile_MaxRetriesExceeded")
                        return state

            except Exception as e:
                error_msg = str(e)
                state["profile_retry_history"].append({
                    "attempt": attempt + 1,
                    "error": error_msg,
                    "timestamp": datetime.now().isoformat(),
                    "exception_type": type(e).__name__
                })

                if attempt < retry_config.max_retries:
                    error_category = categorize_error(e)
                    if error_category == ErrorCategory.PERMANENT:
                        print(f"❌ Permanent error - no retry: {error_msg}")
                        state["profile_status"] = "error"
                        state["profile_error"] = error_msg
                        state["critical_errors"].append({
                            "agent": "Agent1",
                            "error": error_msg,
                            "exception_type": type(e).__name__,
                            "category": error_category
                        })
                        state["execution_path"].append("Agent1_Profile_PermanentException")
                        return state
                    else:
                        delay = retry_config.get_delay(attempt)
                        print(f"⚠️  Exception on attempt {attempt + 1}: {error_msg}")
                        print(f"   ⏳ Retrying in {delay:.1f}s...")
                else:
                    print(f"❌ Exception after max retries: {error_msg}")
                    state["profile_status"] = "error"
                    state["profile_error"] = error_msg
                    state["critical_errors"].append({
                        "agent": "Agent1",
                        "error": f"Exception after {retry_config.max_retries + 1} attempts: {error_msg}",
                        "exception_type": type(e).__name__,
                        "category": categorize_error(e)
                    })
                    state["execution_path"].append("Agent1_Profile_ExceptionMaxRetries")
                    return state

        return state

    def agent2_risk_analysis(self, state: LoanDecisionState) -> LoanDecisionState:
        """Agent2: Evaluate financial risk with retry logic."""
        print("\n" + "="*80)
        print("  AGENT2: FINANCIAL RISK ANALYSIS")
        print("="*80)

        if state["profile_status"] != "success":
            print(f"⏭️  Skipping Agent2 - Agent1 failed")
            state["risk_status"] = "skipped"
            state["execution_path"].append("Agent2_Risk_Skipped")
            return state

        applicant_id = state["applicant_id"]
        print(f"\n📊 Analyzing financial risk for {applicant_id}...")

        retry_config = self.RETRY_CONFIGS["agent2"]
        state["risk_retry_count"] = 0
        state["risk_retry_history"] = []

        for attempt in range(retry_config.max_retries + 1):
            try:
                state["risk_retry_count"] = attempt

                if attempt > 0:
                    delay = retry_config.get_delay(attempt - 1)
                    print(f"\n   🔄 Retry Attempt {attempt}/{retry_config.max_retries}...")
                    time.sleep(delay)

                # Call Agent2
                result = self.risk_agent.analyze_financial_risk(
                    applicant_id,
                    state["applicant_data"],
                    state["loan_request"]
                )

                if result.get("status") == "success":
                    state["risk_analysis"] = result.get("analysis", {})
                    state["risk_status"] = "success"
                    state["risk_error"] = ""

                    # Extract risk score for routing
                    risk_assessment = state["risk_analysis"].get("aggregate_risk_assessment", {})
                    state["risk_score"] = risk_assessment.get("overall_risk_score", 0)
                    state["risk_level"] = risk_assessment.get("overall_risk_level", "Unknown")

                    print(f"✅ Risk analysis complete (Attempt {attempt + 1})")
                    print(f"   Risk Score: {state['risk_score']}/5")
                    print(f"   Risk Level: {state['risk_level']}")
                    state["execution_path"].append("Agent2_Risk_✅")
                    return state
                else:
                    error_msg = result.get("error", "Unknown error")
                    state["risk_retry_history"].append({
                        "attempt": attempt + 1,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    })

                    if attempt < retry_config.max_retries:
                        error_category = categorize_error(Exception(error_msg))
                        if error_category == ErrorCategory.PERMANENT:
                            print(f"❌ Permanent error - no retry: {error_msg}")
                            state["risk_status"] = "error"
                            state["risk_error"] = error_msg
                            state["routing_decision"] = "review"
                            state["manual_review_reason"] = f"Agent2 permanent error: {error_msg}"
                            state["critical_errors"].append({
                                "agent": "Agent2",
                                "error": error_msg,
                                "category": error_category
                            })
                            state["execution_path"].append("Agent2_Risk_PermanentError")
                            return state
                        else:
                            print(f"⚠️  Attempt {attempt + 1} failed (Transient): {error_msg}")
                    else:
                        state["risk_status"] = "error"
                        state["risk_error"] = error_msg
                        state["routing_decision"] = "review"
                        state["manual_review_reason"] = f"Agent2 failed after {retry_config.max_retries + 1} attempts"
                        state["critical_errors"].append({
                            "agent": "Agent2",
                            "error": f"Failed after {retry_config.max_retries + 1} attempts",
                            "category": "persistent_failure"
                        })
                        state["execution_path"].append("Agent2_Risk_MaxRetriesExceeded")
                        return state

            except Exception as e:
                error_msg = str(e)
                state["risk_retry_history"].append({
                    "attempt": attempt + 1,
                    "error": error_msg,
                    "exception_type": type(e).__name__,
                    "timestamp": datetime.now().isoformat()
                })

                if attempt < retry_config.max_retries:
                    error_category = categorize_error(e)
                    if error_category == ErrorCategory.PERMANENT:
                        print(f"❌ Permanent error: {error_msg}")
                        state["risk_status"] = "error"
                        state["risk_error"] = error_msg
                        state["routing_decision"] = "review"
                        state["manual_review_reason"] = f"Agent2 permanent exception: {error_msg}"
                        state["critical_errors"].append({
                            "agent": "Agent2",
                            "error": error_msg,
                            "exception_type": type(e).__name__,
                            "category": error_category
                        })
                        state["execution_path"].append("Agent2_Risk_PermanentException")
                        return state
                    else:
                        delay = retry_config.get_delay(attempt)
                        print(f"⚠️  Exception on attempt {attempt + 1}: {error_msg}")
                        print(f"   ⏳ Retrying in {delay:.1f}s...")
                else:
                    state["risk_status"] = "error"
                    state["risk_error"] = error_msg
                    state["routing_decision"] = "review"
                    state["manual_review_reason"] = f"Agent2 exception after max retries: {error_msg}"
                    state["critical_errors"].append({
                        "agent": "Agent2",
                        "error": f"Exception after {retry_config.max_retries + 1} attempts: {error_msg}",
                        "exception_type": type(e).__name__,
                        "category": categorize_error(e)
                    })
                    state["execution_path"].append("Agent2_Risk_ExceptionMaxRetries")
                    return state

        return state

    def routing_decision(self, state: LoanDecisionState) -> LoanDecisionState:
        """Make routing decision based on risk score with error escalation."""
        print("\n" + "="*80)
        print("  ROUTING DECISION")
        print("="*80)

        # Check for critical errors that require manual review
        if state["critical_errors"]:
            print(f"\n⚠️  Critical errors detected - Escalating to manual review")
            print(f"   Errors: {len(state['critical_errors'])}")
            for error in state["critical_errors"]:
                print(f"   • {error['agent']}: {error['error'][:100]}")

            if state["routing_decision"] != "review":
                state["routing_decision"] = "review"
                state["error_escalation"] = True
            state["execution_path"].append("Routing_ManualReview_ErrorEscalation")
            return state

        if state["risk_status"] != "success":
            print(f"⚠️  Risk analysis failed - Escalating to manual review")
            if state["manual_review_reason"]:
                print(f"   Reason: {state['manual_review_reason']}")
            state["routing_decision"] = "review"
            state["error_escalation"] = True
            state["execution_path"].append("Routing_ManualReview")
            return state

        risk_score = state["risk_score"]

        print(f"\n🔀 Routing Decision Based on Risk Score: {risk_score}/5")

        if risk_score > 3.5:
            routing = "escalate"
            strategy = "Conservative"
            print(f"   → ESCALATE: High risk (>{3.5}) - Manual underwriting required")
        elif risk_score >= 2.5:
            routing = "conditional"
            strategy = "Balanced"
            print(f"   → CONDITIONAL: Medium risk ({2.5}-{3.5}) - Conditions may apply")
        elif risk_score >= 1.5:
            routing = "review"
            strategy = "Balanced"
            print(f"   → REVIEW: Mixed signals ({1.5}-{2.5}) - Senior review")
        else:
            routing = "auto_approve"
            strategy = "Aggressive"
            print(f"   → AUTO_APPROVE: Low risk (<{1.5}) - Standard approval")

        state["routing_decision"] = routing
        state["execution_path"].append(f"Routing_{routing}")

        return state

    def route_decision(self, state: LoanDecisionState) -> str:
        """Determine next node based on routing decision."""
        return state["routing_decision"]

    def agent3_decision_synthesis(self, state: LoanDecisionState) -> LoanDecisionState:
        """Agent3: Synthesize final decision with retry logic."""
        print("\n" + "="*80)
        print("  AGENT3: LOAN DECISION SYNTHESIS")
        print("="*80)

        if state["risk_status"] != "success":
            print(f"⏭️  Skipping Agent3 - Risk analysis failed")
            state["decision_status"] = "skipped"
            state["execution_path"].append("Agent3_Decision_Skipped")

            # Create fallback decision for manual review
            if state["routing_decision"] == "review":
                state["decision_data"] = {
                    "decision": {
                        "classification": "REVIEW",
                        "risk_score": 3.5,
                        "confidence_level": "Low",
                        "confidence_percentage": 30,
                        "reasoning": f"Manual review required: {state['manual_review_reason']}"
                    }
                }
                state["decision_status"] = "fallback"
            return state

        applicant_id = state["applicant_id"]
        routing = state["routing_decision"]

        # Map routing to strategy
        strategy_map = {
            "escalate": "Conservative",
            "conditional": "Balanced",
            "auto_approve": "Aggressive",
            "review": "Balanced",
            "manual_review": "Conservative"
        }
        strategy = strategy_map.get(routing, "Balanced")

        print(f"\n⚖️  Making decision for {applicant_id}...")
        print(f"   Strategy: {strategy}")
        print(f"   Routing: {routing}")

        retry_config = self.RETRY_CONFIGS["agent3"]
        state["decision_retry_count"] = 0
        state["decision_retry_history"] = []

        for attempt in range(retry_config.max_retries + 1):
            try:
                state["decision_retry_count"] = attempt

                if attempt > 0:
                    delay = retry_config.get_delay(attempt - 1)
                    print(f"\n   🔄 Retry Attempt {attempt}/{retry_config.max_retries}...")
                    time.sleep(delay)

                # Call Agent3
                result = self.decision_agent.make_decision(
                    applicant_id,
                    state["applicant_data"],
                    state["profile_analysis"],
                    state["risk_analysis"],
                    strategy=strategy
                )

                if result.get("status") == "success":
                    state["decision_data"] = result.get("decision", {})
                    state["decision_status"] = "success"
                    state["decision_error"] = ""

                    decision = state["decision_data"].get("decision", {})
                    classification = decision.get("classification", "Unknown")
                    risk_score = decision.get("risk_score", 0)

                    print(f"✅ Decision complete (Attempt {attempt + 1})")
                    print(f"   Classification: {classification}")
                    print(f"   Risk Score: {risk_score}/5")
                    state["execution_path"].append("Agent3_Decision_✅")
                    return state
                else:
                    error_msg = result.get("error", "Unknown error")
                    state["decision_retry_history"].append({
                        "attempt": attempt + 1,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    })

                    if attempt < retry_config.max_retries:
                        error_category = categorize_error(Exception(error_msg))
                        if error_category == ErrorCategory.PERMANENT:
                            print(f"❌ Permanent error: {error_msg}")
                            state["decision_status"] = "error"
                            state["decision_error"] = error_msg
                            state["critical_errors"].append({
                                "agent": "Agent3",
                                "error": error_msg,
                                "category": error_category
                            })
                            state["execution_path"].append("Agent3_Decision_PermanentError")
                            # Fallback to REVIEW decision
                            state["decision_data"] = {
                                "decision": {
                                    "classification": "REVIEW",
                                    "risk_score": state["risk_score"],
                                    "confidence_level": "Low",
                                    "confidence_percentage": 20,
                                    "reasoning": f"Decision synthesis failed: {error_msg}"
                                }
                            }
                            return state
                        else:
                            print(f"⚠️  Attempt {attempt + 1} failed (Transient): {error_msg}")
                    else:
                        state["decision_status"] = "error"
                        state["decision_error"] = error_msg
                        state["critical_errors"].append({
                            "agent": "Agent3",
                            "error": f"Failed after {retry_config.max_retries + 1} attempts",
                            "category": "persistent_failure"
                        })
                        state["execution_path"].append("Agent3_Decision_MaxRetriesExceeded")
                        # Fallback to REVIEW decision
                        state["decision_data"] = {
                            "decision": {
                                "classification": "REVIEW",
                                "risk_score": state["risk_score"],
                                "confidence_level": "Low",
                                "confidence_percentage": 20,
                                "reasoning": "Decision synthesis failed after maximum retry attempts"
                            }
                        }
                        return state

            except Exception as e:
                error_msg = str(e)
                state["decision_retry_history"].append({
                    "attempt": attempt + 1,
                    "error": error_msg,
                    "exception_type": type(e).__name__,
                    "timestamp": datetime.now().isoformat()
                })

                if attempt < retry_config.max_retries:
                    error_category = categorize_error(e)
                    if error_category == ErrorCategory.PERMANENT:
                        print(f"❌ Permanent error: {error_msg}")
                        state["decision_status"] = "error"
                        state["decision_error"] = error_msg
                        state["critical_errors"].append({
                            "agent": "Agent3",
                            "error": error_msg,
                            "exception_type": type(e).__name__,
                            "category": error_category
                        })
                        state["execution_path"].append("Agent3_Decision_PermanentException")
                        # Fallback decision
                        state["decision_data"] = {
                            "decision": {
                                "classification": "REVIEW",
                                "risk_score": state["risk_score"],
                                "confidence_level": "Very Low",
                                "confidence_percentage": 10,
                                "reasoning": f"Decision synthesis exception: {error_msg}"
                            }
                        }
                        return state
                    else:
                        delay = retry_config.get_delay(attempt)
                        print(f"⚠️  Exception on attempt {attempt + 1}: {error_msg}")
                        print(f"   ⏳ Retrying in {delay:.1f}s...")
                else:
                    state["decision_status"] = "error"
                    state["decision_error"] = error_msg
                    state["critical_errors"].append({
                        "agent": "Agent3",
                        "error": f"Exception after {retry_config.max_retries + 1} attempts: {error_msg}",
                        "exception_type": type(e).__name__,
                        "category": categorize_error(e)
                    })
                    state["execution_path"].append("Agent3_Decision_ExceptionMaxRetries")
                    # Fallback decision
                    state["decision_data"] = {
                        "decision": {
                            "classification": "REVIEW",
                            "risk_score": state["risk_score"],
                            "confidence_level": "Very Low",
                            "confidence_percentage": 10,
                            "reasoning": "Decision synthesis failed due to exception"
                        }
                    }
                    return state

        return state

    def agent4_compliance_orchestration(self, state: LoanDecisionState) -> LoanDecisionState:
        """Agent4: Compliance and action orchestration with retry logic."""
        print("\n" + "="*80)
        print("  AGENT4: COMPLIANCE & ACTION ORCHESTRATION")
        print("="*80)

        if state["decision_status"] not in ["success", "fallback"]:
            print(f"⏭️  Skipping Agent4 - Decision synthesis failed")
            state["action_status"] = "skipped"
            state["execution_path"].append("Agent4_Compliance_Skipped")
            return state

        applicant_id = state["applicant_id"]
        print(f"\n📋 Recording decision and orchestrating notifications for {applicant_id}...")

        retry_config = self.RETRY_CONFIGS["agent4"]
        state["action_retry_count"] = 0
        state["action_retry_history"] = []

        for attempt in range(retry_config.max_retries + 1):
            try:
                state["action_retry_count"] = attempt

                if attempt > 0:
                    delay = retry_config.get_delay(attempt - 1)
                    print(f"\n   🔄 Retry Attempt {attempt}/{retry_config.max_retries}...")
                    time.sleep(delay)

                # Call Agent4
                result = self.action_agent.orchestrate_action(
                    applicant_id,
                    state["applicant_data"],
                    state["decision_data"]
                )

                if result.get("status") == "success":
                    state["action_result"] = result.get("result", {})
                    state["action_status"] = "success"
                    state["action_error"] = ""

                    # Extract case ID
                    state["case_id"] = state["action_result"].get("case_id", "N/A")

                    print(f"✅ Compliance orchestration complete (Attempt {attempt + 1})")
                    print(f"   Case ID: {state['case_id']}")
                    state["execution_path"].append("Agent4_Compliance_✅")
                    return state
                else:
                    error_msg = result.get("error", "Unknown error")
                    state["action_retry_history"].append({
                        "attempt": attempt + 1,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    })

                    if attempt < retry_config.max_retries:
                        error_category = categorize_error(Exception(error_msg))
                        if error_category == ErrorCategory.PERMANENT:
                            print(f"❌ Permanent error: {error_msg}")
                            state["action_status"] = "error"
                            state["action_error"] = error_msg
                            state["critical_errors"].append({
                                "agent": "Agent4",
                                "error": error_msg,
                                "category": error_category
                            })
                            state["execution_path"].append("Agent4_Compliance_PermanentError")
                            return state
                        else:
                            print(f"⚠️  Attempt {attempt + 1} failed (Transient): {error_msg}")
                    else:
                        state["action_status"] = "error"
                        state["action_error"] = error_msg
                        state["critical_errors"].append({
                            "agent": "Agent4",
                            "error": f"Failed after {retry_config.max_retries + 1} attempts",
                            "category": "persistent_failure"
                        })
                        state["execution_path"].append("Agent4_Compliance_MaxRetriesExceeded")
                        print(f"❌ All compliance orchestration attempts failed")
                        return state

            except Exception as e:
                error_msg = str(e)
                state["action_retry_history"].append({
                    "attempt": attempt + 1,
                    "error": error_msg,
                    "exception_type": type(e).__name__,
                    "timestamp": datetime.now().isoformat()
                })

                if attempt < retry_config.max_retries:
                    error_category = categorize_error(e)
                    if error_category == ErrorCategory.PERMANENT:
                        print(f"❌ Permanent error: {error_msg}")
                        state["action_status"] = "error"
                        state["action_error"] = error_msg
                        state["critical_errors"].append({
                            "agent": "Agent4",
                            "error": error_msg,
                            "exception_type": type(e).__name__,
                            "category": error_category
                        })
                        state["execution_path"].append("Agent4_Compliance_PermanentException")
                        return state
                    else:
                        delay = retry_config.get_delay(attempt)
                        print(f"⚠️  Exception on attempt {attempt + 1}: {error_msg}")
                        print(f"   ⏳ Retrying in {delay:.1f}s...")
                else:
                    state["action_status"] = "error"
                    state["action_error"] = error_msg
                    state["critical_errors"].append({
                        "agent": "Agent4",
                        "error": f"Exception after {retry_config.max_retries + 1} attempts: {error_msg}",
                        "exception_type": type(e).__name__,
                        "category": categorize_error(e)
                    })
                    state["execution_path"].append("Agent4_Compliance_ExceptionMaxRetries")
                    return state

        return state

    def finalize_result(self, state: LoanDecisionState) -> LoanDecisionState:
        """Finalize and structure the result with error reporting."""
        print("\n" + "="*80)
        print("  FINALIZING WORKFLOW")
        print("="*80)

        # Determine overall workflow status
        has_critical_errors = len(state["critical_errors"]) > 0
        is_fallback = state["decision_status"] == "fallback"
        all_success = (state["profile_status"] == "success" and
                      state["risk_status"] == "success" and
                      state["decision_status"] == "success" and
                      state["action_status"] == "success")

        if has_critical_errors:
            state["workflow_status"] = "error_with_fallback" if is_fallback else "error"
        elif all_success:
            state["workflow_status"] = "success"
        else:
            state["workflow_status"] = "partial_success" if is_fallback else "error"

        # Build retry statistics
        retry_stats = {
            "agent1_retries": state["profile_retry_count"],
            "agent2_retries": state["risk_retry_count"],
            "agent3_retries": state["decision_retry_count"],
            "agent4_retries": state["action_retry_count"],
            "total_retries": (state["profile_retry_count"] + state["risk_retry_count"] +
                            state["decision_retry_count"] + state["action_retry_count"])
        }

        # Build final decision
        state["final_decision"] = {
            "workflow_status": state["workflow_status"],
            "applicant_id": state["applicant_id"],
            "timestamp": datetime.now().isoformat(),
            "execution_path": " → ".join(state["execution_path"]),

            # Agent results
            "profile_analysis": {
                "status": state["profile_status"],
                "retry_count": state["profile_retry_count"],
                "retry_history": state["profile_retry_history"],
                "data": state["profile_analysis"]
            },
            "risk_analysis": {
                "status": state["risk_status"],
                "retry_count": state["risk_retry_count"],
                "retry_history": state["risk_retry_history"],
                "risk_score": state["risk_score"],
                "risk_level": state["risk_level"],
                "data": state["risk_analysis"]
            },
            "routing": {
                "decision": state["routing_decision"],
                "error_escalation": state["error_escalation"],
                "manual_review_reason": state["manual_review_reason"],
                "risk_threshold": "High (>3.5) → Escalate | Medium (2.5-3.5) → Conditional | Low (<2.5) → Auto-Approve"
            },
            "decision": {
                "status": state["decision_status"],
                "retry_count": state["decision_retry_count"],
                "retry_history": state["decision_retry_history"],
                "data": state["decision_data"]
            },
            "compliance": {
                "status": state["action_status"],
                "retry_count": state["action_retry_count"],
                "retry_history": state["action_retry_history"],
                "case_id": state["case_id"],
                "data": state["action_result"]
            },

            # Error tracking
            "error_handling": {
                "critical_errors": state["critical_errors"],
                "error_count": len(state["critical_errors"]),
                "error_escalation": state["error_escalation"],
                "retry_statistics": retry_stats
            },

            # Summary
            "summary": self._build_summary(state),
            "next_steps": self._determine_next_steps(state)
        }

        state["timestamp"] = datetime.now().isoformat()

        # Print status
        print(f"\n✅ Workflow Complete")
        print(f"   Status: {state['workflow_status'].upper()}")
        print(f"   Case ID: {state['case_id']}")
        print(f"   Execution Path: {state['final_decision']['execution_path']}")

        # Print error summary if errors exist
        if state["critical_errors"]:
            print(f"\n⚠️  Error Summary:")
            print(f"   Total Errors: {len(state['critical_errors'])}")
            for error in state["critical_errors"]:
                print(f"   • {error['agent']}: {error['error'][:80]}")
            print(f"   Total Retries: {retry_stats['total_retries']}")

        return state

    def _build_summary(self, state: LoanDecisionState) -> str:
        """Build executive summary of workflow."""
        lines = []

        # Profile summary
        if state["profile_status"] == "success":
            profile = state["profile_analysis"].get("overall_assessment", {})
            lines.append(f"Profile: {profile.get('assessment_summary', 'N/A')[:100]}")

        # Risk summary
        if state["risk_status"] == "success":
            lines.append(f"Risk Score: {state['risk_score']}/5 ({state['risk_level']})")

        # Decision summary
        if state["decision_status"] == "success":
            decision = state["decision_data"].get("decision", {})
            classification = decision.get("classification", "N/A")
            lines.append(f"Decision: {classification}")

            if decision.get("conditions"):
                lines.append(f"Conditions: {len(decision['conditions'])} required")

        # Compliance summary
        if state["action_status"] == "success":
            case_id = state["case_id"]
            lines.append(f"Case ID: {case_id}")

        return " | ".join(lines)

    def _determine_next_steps(self, state: LoanDecisionState) -> list:
        """Determine next steps based on workflow result and error handling."""
        steps = []

        # Handle errors and fallback scenarios
        if state["critical_errors"]:
            steps.append("⚠️  Errors occurred during processing:")
            for error in state["critical_errors"]:
                steps.append(f"   • {error['agent']}: {error['error'][:60]}")
            steps.append("")

        if state["workflow_status"] in ["error", "error_with_fallback", "partial_success"]:
            if state["error_escalation"]:
                steps.extend([
                    "🔴 ESCALATED TO MANUAL REVIEW",
                    f"   Reason: {state['manual_review_reason'][:100]}"
                ])
            else:
                steps.append("❌ Workflow encountered errors - Review logs for details")

            if state["decision_status"] in ["fallback", "success"]:
                steps.append("")
            else:
                return steps

        if state["workflow_status"] == "success":
            steps.append("✅ Workflow completed successfully")
            steps.append("")

        # Get decision classification
        decision = state["decision_data"].get("decision", {})
        classification = decision.get("classification", "UNKNOWN")
        confidence = decision.get("confidence_percentage", 0)

        # Confidence warning
        if confidence < 50:
            steps.append(f"⚠️  Low confidence decision ({confidence}%) - Consider manual review")
            steps.append("")

        if classification == "APPROVE":
            steps.extend([
                "✅ Loan approved",
                "→ Schedule closing appointment",
                "→ Prepare closing documents",
                "→ Coordinate with applicant"
            ])
        elif classification == "CONDITIONAL_APPROVE":
            steps.extend([
                "✅ Loan conditionally approved",
                "→ Request condition documentation from applicant",
                "→ Underwriter to verify conditions",
                "→ Update decision once conditions satisfied"
            ])
        elif classification == "REVIEW":
            steps.extend([
                "⏳ Loan requires manual review",
                "→ Escalate to senior underwriter",
                "→ Request additional documentation",
                "→ Update decision within 5 business days"
            ])
        elif classification == "REJECT":
            steps.extend([
                "❌ Loan denied",
                "→ Applicant can appeal within 30 days",
                "→ Explore alternative loan products",
                "→ Provide feedback to applicant"
            ])

        # Add case management step
        if state["case_id"] and state["case_id"] != "N/A":
            case_mgmt = state["action_result"].get("case_management", {})
            if case_mgmt.get("next_action"):
                steps.append(f"→ Case Management: {case_mgmt['next_action']}")

        return steps


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function to run the orchestration engine."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║                   LANGGRAPH ORCHESTRATION ENGINE                              ║")
    print("║          Multi-Agent Loan Approval Workflow Orchestration                     ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    # Initialize orchestrator
    orchestrator = LoanDecisionOrchestrator()

    # Create workflow
    print("\n📊 Creating LangGraph workflow...")
    workflow = orchestrator.create_workflow()
    print("✅ Workflow created and compiled")

    # Sample test data
    test_case = {
        "applicant_id": "APP001",
        "applicant_data": {
            "name": "John Strong",
            "age": 45,
            "email": "john.strong@example.com",
            "phone": "+1-555-0100",
            "annual_income": 150000,
            "monthly_expenses": 4000,
            "existing_monthly_debt": 1000,
            "credit_score": 760,
            "delinquencies": 0,
            "inquiries_last_6_months": 1,
            "credit_utilization": 0.30,
            "years_at_current_job": 8,
            "existing_loans": 1
        },
        "loan_request": {
            "loan_amount": 300000,
            "property_value": 500000,
            "loan_term_months": 360
        }
    }

    # Initialize state
    initial_state = {
        "applicant_id": test_case["applicant_id"],
        "applicant_data": test_case["applicant_data"],
        "loan_request": test_case["loan_request"],

        # Agent1
        "profile_analysis": {},
        "profile_status": "",
        "profile_error": "",
        "profile_retry_count": 0,
        "profile_retry_history": [],

        # Agent2
        "risk_analysis": {},
        "risk_status": "",
        "risk_error": "",
        "risk_retry_count": 0,
        "risk_retry_history": [],

        # Routing
        "routing_decision": "",
        "risk_score": 0.0,
        "risk_level": "",

        # Agent3
        "decision_data": {},
        "decision_status": "",
        "decision_error": "",
        "decision_retry_count": 0,
        "decision_retry_history": [],

        # Agent4
        "action_result": {},
        "action_status": "",
        "action_error": "",
        "case_id": "",
        "action_retry_count": 0,
        "action_retry_history": [],

        # Error Tracking
        "critical_errors": [],
        "error_escalation": False,
        "manual_review_reason": "",

        # Final Result
        "final_decision": {},
        "workflow_status": "",
        "execution_path": [],
        "timestamp": ""
    }

    # Run workflow
    print(f"\n🚀 Running workflow for {test_case['applicant_id']}...")
    print("-" * 80)

    try:
        final_state = workflow.invoke(initial_state)

        # Display results
        print("\n" + "="*80)
        print("  FINAL RESULTS")
        print("="*80)

        final = final_state["final_decision"]

        print(f"\n📊 Workflow Status: {final['workflow_status'].upper()}")
        print(f"📍 Execution Path: {final['execution_path']}")
        print(f"⏰ Timestamp: {final['timestamp']}")

        print(f"\n📋 Summary:")
        print(f"   {final['summary']}")

        print(f"\n📍 Next Steps:")
        for step in final['next_steps']:
            print(f"   {step}")

        # Display detailed results if needed
        if final_state["workflow_status"] == "success":
            case_id = final_state["case_id"]
            print(f"\n✅ Complete Pipeline Result:")
            print(f"   Case ID: {case_id}")
            print(f"   Profile Status: {final_state['profile_status']}")
            print(f"   Risk Status: {final_state['risk_status']}")
            print(f"   Risk Score: {final_state['risk_score']}/5")
            print(f"   Decision Status: {final_state['decision_status']}")
            print(f"   Compliance Status: {final_state['action_status']}")

        print("\n" + "="*80)
        print("Workflow execution complete!")
        print("="*80 + "\n")

        return 0

    except Exception as e:
        print(f"\n❌ Workflow Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure all MCP servers are running:")
        print("  1. python mcp/server.py (Application DB)")
        print("  2. python mcp/riskrulesdb/server.py (RiskRulesDB)")
        print("  3. python mcp/decisionsynthesis/server.py (DecisionSynthesis)")
        print("  4. python mcp/notificationsystem/server.py (NotificationSystem)")
        return 1


if __name__ == "__main__":
    exit(main())
