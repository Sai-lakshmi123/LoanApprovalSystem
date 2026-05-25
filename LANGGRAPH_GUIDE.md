# LangGraph Orchestration Engine - Complete Guide

## Overview

The LangGraph Orchestration Engine coordinates all 4 agents in a multi-step loan approval workflow. It uses LangGraph's StateGraph to manage state transitions and implements intelligent conditional routing based on financial risk assessment.

**Architecture**: LangGraph StateGraph with 6 nodes and conditional routing  
**State Management**: TypedDict schema (LoanDecisionState) with complete data lineage  
**Routing Logic**: Risk-based decision routing with 4 paths (ESCALATE, CONDITIONAL, AUTO_APPROVE, REVIEW)

---

## Workflow Architecture

### Execution Flow Diagram

```
START
  ↓
┌──────────────────────────────────────────────────────────┐
│ AGENT1: APPLICANT PROFILE ANALYSIS                       │
│ → Analyzes income stability, employment, credit history  │
│ → Returns: Profile analysis with completeness score      │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│ AGENT2: FINANCIAL RISK ANALYSIS                          │
│ → Evaluates DTI, credit risk, loan amount, anomalies     │
│ → Returns: Risk score (0-5), risk level, key findings    │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│ ROUTING DECISION (Conditional Edge)                      │
├──────────────────────────────────────────────────────────┤
│ Risk Score > 3.5  → ESCALATE (Conservative strategy)     │
│ Risk Score 2.5-3.5 → CONDITIONAL (Balanced strategy)     │
│ Risk Score 1.5-2.5 → REVIEW (Balanced strategy)          │
│ Risk Score < 1.5  → AUTO_APPROVE (Aggressive strategy)   │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│ AGENT3: LOAN DECISION SYNTHESIS                          │
│ → Makes final decision based on routing strategy          │
│ → Returns: Classification, risk score, confidence, key   │
│   factors, conditions (if applicable)                    │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│ AGENT4: COMPLIANCE & ACTION ORCHESTRATION                │
│ → Records decision in compliance system                   │
│ → Generates case ID (CASE-YYYYMMDD-XXXXX)               │
│ → Orchestrates notifications to stakeholders             │
│ → Returns: Case ID, compliance certification, status     │
└──────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────┐
│ FINALIZE: Structure final decision result                │
│ → Compile execution path                                 │
│ → Build executive summary                                │
│ → Determine next steps                                   │
│ → Return to caller                                       │
└──────────────────────────────────────────────────────────┘
  ↓
END
```

---

## State Schema

### LoanDecisionState (TypedDict)

```python
class LoanDecisionState(TypedDict):
    """Complete state for loan decision workflow."""
    
    # INPUT SECTION
    applicant_id: str
    applicant_data: dict
    loan_request: dict
    
    # AGENT1 OUTPUT
    profile_analysis: dict
    profile_status: str          # success, error, skipped
    profile_error: str
    
    # AGENT2 OUTPUT
    risk_analysis: dict
    risk_status: str             # success, error, skipped
    risk_error: str
    risk_score: float            # 0-5 scale
    risk_level: str              # Very Low, Low, Medium, High, Very High
    
    # ROUTING
    routing_decision: str        # escalate, conditional, auto_approve, review
    
    # AGENT3 OUTPUT
    decision_data: dict
    decision_status: str         # success, error, skipped
    decision_error: str
    
    # AGENT4 OUTPUT
    action_result: dict
    action_status: str           # success, error, skipped
    action_error: str
    case_id: str                 # CASE-YYYYMMDD-XXXXX
    
    # FINAL RESULT
    final_decision: dict
    workflow_status: str         # success, error
    execution_path: list         # Track nodes executed
    timestamp: str
```

### State Lineage

The state maintains complete lineage of all agent outputs:

```
Initial State
  ↓ Agent1 adds → profile_analysis, profile_status, profile_error
  ↓ Agent2 adds → risk_analysis, risk_status, risk_error, risk_score, risk_level
  ↓ Routing adds → routing_decision (based on risk_score)
  ↓ Agent3 adds → decision_data, decision_status, decision_error
  ↓ Agent4 adds → action_result, action_status, action_error, case_id
  ↓ Finalize adds → final_decision, workflow_status, execution_path, timestamp
  ↓
Final State (returned to caller)
```

---

## Routing Logic

### Decision Points

The routing decision node evaluates the risk score and determines which execution strategy to use:

#### ESCALATE Path (Risk Score > 3.5)
```
Triggered: When risk score exceeds 3.5 (high risk)
Strategy: Conservative (higher risk tolerance threshold)
Agent3 Behavior:
  - More strict evaluation criteria
  - Likely outcome: REVIEW or REJECT
  - Conditions: Extensive, specific conditions if approved
Next Steps:
  - Escalate to senior underwriter
  - Request additional documentation
  - Manual review required
```

#### CONDITIONAL Path (Risk Score 2.5-3.5)
```
Triggered: When risk score is 2.5-3.5 (medium risk)
Strategy: Balanced (moderate risk tolerance)
Agent3 Behavior:
  - Standard evaluation criteria
  - Likely outcome: CONDITIONAL_APPROVE or REVIEW
  - Conditions: Reasonable conditions for approval
Next Steps:
  - Request condition documentation
  - Underwriter verification
  - Timeline: 10 days to satisfy conditions
```

#### REVIEW Path (Risk Score 1.5-2.5)
```
Triggered: When risk score is 1.5-2.5 (low-medium risk)
Strategy: Balanced (moderate risk tolerance)
Agent3 Behavior:
  - Standard evaluation criteria
  - Likely outcome: CONDITIONAL_APPROVE or APPROVE
  - Conditions: Minor conditions if any
Next Steps:
  - Standard processing
  - Quick underwriter review (5 days)
  - May proceed with approval
```

#### AUTO_APPROVE Path (Risk Score < 1.5)
```
Triggered: When risk score is below 1.5 (very low risk)
Strategy: Aggressive (lower risk tolerance threshold)
Agent3 Behavior:
  - Favorable evaluation criteria
  - Likely outcome: APPROVE
  - Conditions: Minimal to no conditions
Next Steps:
  - Schedule closing immediately
  - Prepare documents
  - Process loan
```

### Routing Decision Tree

```
Risk Score
  ├─ > 3.5 ──────────────→ ESCALATE
  │                       (Conservative)
  │
  ├─ 2.5-3.5 ────────────→ CONDITIONAL
  │                       (Balanced)
  │
  ├─ 1.5-2.5 ────────────→ REVIEW
  │                       (Balanced)
  │
  └─ < 1.5 ──────────────→ AUTO_APPROVE
                          (Aggressive)
```

---

## Node Implementations

### Node 1: Agent1 Profile Analysis

```python
def agent1_profile_analysis(state: LoanDecisionState) -> LoanDecisionState:
    """
    Analyzes applicant profile.
    
    Input: applicant_id from state
    Process:
      1. Call ApplicationProfileAgent.analyze_applicant()
      2. Extract income stability, employment risk, credit, completeness
    Output: Updates state with:
      - profile_analysis: Complete analysis from Agent1
      - profile_status: 'success', 'error', or 'skipped'
      - profile_error: Error message if failed
    """
```

**Key Extractions:**
- Income Stability Score (0-100)
- Employment Risk Level
- Credit Score and History
- Application Completeness %

---

### Node 2: Agent2 Risk Analysis

```python
def agent2_risk_analysis(state: LoanDecisionState) -> LoanDecisionState:
    """
    Evaluates financial risk.
    
    Input: applicant_data, loan_request from state
    Process:
      1. Call FinancialRiskAnalysisAgent.analyze_financial_risk()
      2. Extract DTI, credit risk, loan amount risk, anomalies
      3. Extract aggregate risk score for routing
    Output: Updates state with:
      - risk_analysis: Complete analysis from Agent2
      - risk_status: 'success', 'error', or 'skipped'
      - risk_score: 0-5 scale (critical for routing!)
      - risk_level: Very Low/Low/Medium/High/Very High
    """
```

**Key Extractions:**
- DTI Ratio (current and with new loan)
- Credit Risk Level
- Loan Amount Risk (LTI, LTV)
- Anomaly Count and Severity
- **Aggregate Risk Score (0-5)** ← Used for routing

---

### Node 3: Routing Decision

```python
def routing_decision(state: LoanDecisionState) -> LoanDecisionState:
    """
    Makes routing decision based on risk score.
    
    Input: risk_score from Agent2 output
    Process:
      1. Evaluate risk_score against thresholds
      2. Determine routing path (escalate, conditional, auto_approve, review)
      3. Determine strategy for Agent3 (Conservative/Balanced/Aggressive)
    Output: Updates state with:
      - routing_decision: Next execution path
    
    Routing Thresholds:
      Risk > 3.5   → 'escalate' (Conservative)
      2.5 ≤ Risk ≤ 3.5 → 'conditional' (Balanced)
      1.5 ≤ Risk < 2.5 → 'review' (Balanced)
      Risk < 1.5   → 'auto_approve' (Aggressive)
    """
```

**Conditional Edge:**
```python
workflow.add_conditional_edges(
    "routing",
    route_decision,
    {
        "escalate": "agent3_decision",
        "conditional": "agent3_decision",
        "auto_approve": "agent3_decision",
        "review": "agent3_decision"
    }
)
```

All paths lead to Agent3, but with different strategies.

---

### Node 4: Agent3 Decision Synthesis

```python
def agent3_decision_synthesis(state: LoanDecisionState) -> LoanDecisionState:
    """
    Makes final decision with routing-determined strategy.
    
    Input:
      - All prior analysis (profile, risk)
      - routing_decision: Which strategy to use
    Process:
      1. Map routing to strategy:
         - escalate → Conservative
         - conditional → Balanced
         - auto_approve → Aggressive
         - review → Balanced
      2. Call LoanDecisionAgent.make_decision() with strategy
    Output: Updates state with:
      - decision_data: Complete decision from Agent3
      - decision_status: 'success', 'error', or 'skipped'
    """
```

**Decision Output:**
- Classification: APPROVE, CONDITIONAL_APPROVE, REVIEW, REJECT
- Risk Score: 0-5
- Confidence Level: Very High → Very Low
- Key Factors: 7 dimensions evaluated
- Conditions: If conditional approval

---

### Node 5: Agent4 Compliance Orchestration

```python
def agent4_compliance_orchestration(state: LoanDecisionState) -> LoanDecisionState:
    """
    Records decision and orchestrates notifications.
    
    Input: Complete decision from Agent3
    Process:
      1. Call ComplianceActionAgent.orchestrate_action()
      2. Record decision in compliance system
      3. Generate case ID (CASE-YYYYMMDD-XXXXX)
      4. Send notifications to stakeholders
      5. Verify fair lending compliance
    Output: Updates state with:
      - action_result: Complete action orchestration result
      - action_status: 'success', 'error', or 'skipped'
      - case_id: Generated case ID
    """
```

**Case ID Format:** `CASE-20260525-12345`
- CASE: Prefix
- YYYY: Year (2026)
- MM: Month (05)
- DD: Day (25)
- XXXXX: Random sequence

---

### Node 6: Finalize Result

```python
def finalize_result(state: LoanDecisionState) -> LoanDecisionState:
    """
    Finalizes and structures the result.
    
    Process:
      1. Determine overall workflow_status (success/error)
      2. Build execution_path (track nodes executed)
      3. Create executive summary
      4. Determine next_steps based on decision
      5. Compile final_decision for return to caller
    Output:
      - final_decision: Structured result with all key information
      - workflow_status: Overall workflow success/failure
      - execution_path: Node execution sequence
    """
```

---

## State Management

### Data Flow Example

```
Initial State:
{
    "applicant_id": "APP001",
    "applicant_data": {...},
    "loan_request": {...},
    "profile_analysis": {},      ← Will be filled by Agent1
    "risk_analysis": {},         ← Will be filled by Agent2
    "decision_data": {},         ← Will be filled by Agent3
    "action_result": {},         ← Will be filled by Agent4
    "final_decision": {},        ← Will be filled by Finalize
    ...
}

After Agent1:
{
    ...(previous data)...,
    "profile_analysis": {
        "income_stability": {...},
        "employment_risk": {...},
        "credit_history": {...}
    },
    "profile_status": "success"
}

After Agent2:
{
    ...(previous data)...,
    "risk_analysis": {
        "dti_analysis": {...},
        "credit_risk": {...},
        "aggregate_risk_assessment": {"overall_risk_score": 1.8}
    },
    "risk_status": "success",
    "risk_score": 1.8         ← Used for routing!
}

After Routing:
{
    ...(previous data)...,
    "routing_decision": "auto_approve"  ← Routes to Agent3 with strategy
}

After Agent3:
{
    ...(previous data)...,
    "decision_data": {
        "decision": {
            "classification": "APPROVE",
            "risk_score": 1.8
        }
    },
    "decision_status": "success"
}

After Agent4:
{
    ...(previous data)...,
    "action_result": {
        "case_id": "CASE-20260525-12345",
        "notifications": {...}
    },
    "action_status": "success",
    "case_id": "CASE-20260525-12345"
}

After Finalize:
{
    ...(all previous data)...,
    "final_decision": {
        "workflow_status": "success",
        "applicant_id": "APP001",
        "profile_analysis": {...},
        "risk_analysis": {...},
        "routing": {...},
        "decision": {...},
        "compliance": {...},
        "summary": "Profile: Very Stable | Risk: 1.8/5 | Decision: APPROVE",
        "next_steps": [
            "Schedule closing appointment",
            "Prepare closing documents",
            ...
        ]
    },
    "workflow_status": "success",
    "execution_path": ["Agent1_Profile_✅", "Agent2_Risk_✅", ...]
}
```

---

## Error Handling

### Skipping Nodes

If a prior node fails, subsequent nodes are skipped:

```python
def agent2_risk_analysis(state):
    if state["profile_status"] != "success":
        print("Skipping Agent2 - Agent1 failed")
        state["risk_status"] = "skipped"
        return state
```

### Final Status Determination

```python
if (profile_status == "success" AND
    risk_status == "success" AND
    decision_status == "success" AND
    action_status == "success"):
    workflow_status = "success"
else:
    workflow_status = "error"
```

---

## Execution Paths

### Successful Path (Happy Path)

```
Agent1_Profile_✅ 
  → Agent2_Risk_✅
  → Routing_auto_approve
  → Agent3_Decision_✅
  → Agent4_Compliance_✅
  → workflow_status: SUCCESS
```

### High Risk Path

```
Agent1_Profile_✅
  → Agent2_Risk_✅
  → Routing_escalate
  → Agent3_Decision_✅ (Conservative strategy)
  → Agent4_Compliance_✅
  → workflow_status: SUCCESS
  → Decision: REVIEW or REJECT
```

### Failure Path

```
Agent1_Profile_✅
  → Agent2_Risk_❌ (Error)
  → Agent3_Decision_Skipped
  → Agent4_Compliance_Skipped
  → workflow_status: ERROR
```

---

## Next Steps Determination

Based on final decision classification:

### APPROVE
```
✅ Loan approved
→ Schedule closing appointment
→ Prepare closing documents
→ Coordinate with applicant
```

### CONDITIONAL_APPROVE
```
✅ Loan conditionally approved
→ Request condition documentation from applicant
→ Underwriter to verify conditions
→ Update decision once conditions satisfied
```

### REVIEW
```
⏳ Loan requires manual review
→ Escalate to senior underwriter
→ Request additional documentation
→ Update decision within 5 business days
```

### REJECT
```
❌ Loan denied
→ Applicant can appeal within 30 days
→ Explore alternative loan products
→ Provide feedback to applicant
```

---

## Running the Orchestration

### Basic Usage

```python
from orchestration.orchestration_engine import LoanDecisionOrchestrator

# Initialize
orchestrator = LoanDecisionOrchestrator()
workflow = orchestrator.create_workflow()

# Create state
initial_state = {
    "applicant_id": "APP001",
    "applicant_data": {...},
    "loan_request": {...},
    # ... other fields initialized
}

# Run workflow
final_state = workflow.invoke(initial_state)

# Access results
final_decision = final_state["final_decision"]
case_id = final_state["case_id"]
workflow_status = final_state["workflow_status"]
```

---

## Customization

### Modifying Risk Thresholds

```python
def routing_decision(self, state):
    risk_score = state["risk_score"]
    
    # Customize thresholds here
    if risk_score > 4.0:  # Changed from 3.5
        routing = "escalate"
    elif risk_score >= 2.0:  # Changed from 2.5
        routing = "conditional"
    # ...
```

### Adding Custom Nodes

```python
# Add new node
workflow.add_node("custom_node", custom_function)

# Add edge
workflow.add_edge("agent4_compliance", "custom_node")
```

### Changing Strategies

```python
strategy_map = {
    "escalate": "SuperConservative",  # Custom strategy
    "conditional": "Custom",
    "auto_approve": "Liberal",
    "review": "Balanced"
}
```

---

## Performance Metrics

- **Agent1 Execution**: 5-15 seconds
- **Agent2 Execution**: 15-40 seconds
- **Routing Decision**: < 1 second
- **Agent3 Execution**: 20-45 seconds
- **Agent4 Execution**: 10-25 seconds
- **Finalize**: < 1 second
- **Total Workflow**: 50-120 seconds

---

## Debugging

### View Execution Path

```python
final_state["execution_path"]
# Output: ["Agent1_Profile_✅", "Agent2_Risk_✅", ...]
```

### Check Node Statuses

```python
final_state["profile_status"]     # success, error, skipped
final_state["risk_status"]        # success, error, skipped
final_state["decision_status"]    # success, error, skipped
final_state["action_status"]      # success, error, skipped
```

### View Errors

```python
final_state["profile_error"]
final_state["risk_error"]
final_state["decision_error"]
final_state["action_error"]
```

---

**Last Updated:** 2026-05-25  
**Version:** 1.0.0
