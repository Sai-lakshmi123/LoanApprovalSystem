# Agent3: Loan Decision Agent - Complete Technical Implementation Guide

## Overview

Agent3 is the **Decision Synthesis Agent** in the four-agent loan approval system. It synthesizes final lending decisions by integrating outputs from Agent1 (Application Profile) and Agent2 (Financial Risk Analysis) using the Anthropic Agent SDK with Claude Sonnet 4.6.

**Key Role**: Make final loan decisions (APPROVE/CONDITIONAL_APPROVE/REVIEW/REJECT) with clear reasoning, confidence levels, and compliance documentation.

---

## Architecture

### System Design

```
INPUT SOURCES:
├─ Agent1 Output (Application Profile Analysis)
│  ├─ Income Stability Score
│  ├─ Employment Risk Level
│  ├─ Credit History Summary
│  └─ Application Completeness
├─ Agent2 Output (Financial Risk Analysis)
│  ├─ DTI Analysis
│  ├─ Credit Risk Assessment
│  ├─ Loan Amount Risk
│  ├─ Anomaly Detection
│  └─ Aggregate Risk Score
└─ Applicant Data

                   ↓

        AGENT3 - DECISION SYNTHESIS
        ├─ Integrate all data sources
        ├─ Apply decision rules
        ├─ Calculate confidence
        ├─ Identify key factors
        └─ Generate conditions

                   ↓

OUTPUT STRUCTURE:
├─ Decision Classification
├─ Risk Score (0-5)
├─ Confidence Level & Percentage
├─ Key Factors with Impacts
├─ Risk Summary (Strengths/Concerns)
├─ Compliance Notes
└─ Next Steps
```

---

## System Prompt (150+ Lines)

The system prompt defines Agent3's behavior across seven dimensions:

### 1. Role Definition
```
"You are an expert loan decision analyst responsible for making final 
lending decisions. Your role is to synthesize outputs from applicant 
profile analysis and financial risk analysis to produce a comprehensive, 
well-reasoned loan decision."
```

**Responsibilities:**
- Decision synthesis from multiple data sources
- Risk evaluation across financial dimensions
- Confidence assessment based on data quality
- Condition generation for conditional approvals
- Reasoning documentation for audit trail
- Fair lending and regulatory compliance
- Complete decision documentation

### 2. Analysis Framework

#### Decision Classifications
The framework defines four decision categories:

**APPROVE** (Risk < 1.5)
- Strong financial profile
- Clear repayment path
- No critical violations
- Minimal conditions

**CONDITIONAL_APPROVE** (Risk 1.5-2.5)
- Good profile with minor concerns
- Specific conditions required
- High success probability with conditions

**REVIEW** (Risk 2.5-3.5)
- Mixed signals and concerns
- Requires senior underwriter judgment
- Resolvable issues identified

**REJECT** (Risk > 3.5)
- Multiple high-risk factors
- Insufficient mitigating factors
- Does not meet lending criteria

#### Confidence Level Assessment
```
Very High (85-100%):    Complete data, strong metric agreement
High (70-84%):          Good data quality, minor inconsistencies
Moderate (55-69%):      Acceptable data, some concerns
Low (40-54%):           Limited data or conflicting signals
Very Low (<40%):        Incomplete data, major inconsistencies
```

#### Key Decision Factors (7 Dimensions)
1. **Income Stability & Employment Security**
   - From Agent1: Income Stability Score (0-100)
   - Employment Risk Level (Very Low → Very High)
   - Years at current job
   - Job security indicators

2. **Debt Management Capacity**
   - From Agent2: DTI Ratio (current & projected)
   - Monthly debt obligations
   - Monthly income available
   - Ability to service new loan

3. **Credit History & Payment Discipline**
   - From Agent1 & Agent2: Credit Score (300-850)
   - From Agent2: Delinquencies count
   - Payment history pattern
   - Recent inquiries

4. **Loan Amount Appropriateness**
   - From Agent2: LTI (Loan-to-Income)
   - From Agent2: LTV (Loan-to-Value)
   - Loan amount relative to income
   - Property value protection

5. **Collateral Protection**
   - From Agent2: LTV percentage
   - Equity cushion
   - Property value stability

6. **Anomaly & Red Flags**
   - From Agent2: Anomaly count
   - Severity levels (Critical, High, Medium, Low)
   - Pattern analysis
   - Behavioral red flags

7. **Compensating Factors**
   - Strong income despite concerns
   - Low debt despite other factors
   - Excellent credit offsetting income concerns
   - Stable employment offsetting high DTI

#### Risk Score Integration (0-5 Scale)

The prompt guides synthesis of risk from multiple sources:

**From Agent1:**
- Income Stability Score → 0-5 risk contribution
- Employment Risk Level → 0-5 risk contribution
- Credit Profile Quality → 0-5 risk contribution
- Completeness Percentage → Confidence impact

**From Agent2:**
- Aggregate Risk Score (already 0-5)
- DTI Risk Level → Component weight
- Credit Risk → Component weight
- Loan Amount Risk → Component weight
- Anomaly Score → Component weight

**Synthesis:**
- Weighted average of all components
- Compensating factors adjustment
- Primary risk factors emphasis
- Final 0-5 score with reasoning

### 3. Output JSON Schema

The prompt specifies exact output structure:

```json
{
    "applicant_id": "string",
    "analysis_timestamp": "ISO8601 datetime",
    "decision": {
        "classification": "APPROVE | CONDITIONAL_APPROVE | REVIEW | REJECT",
        "risk_score": number(0-5),
        "confidence_level": "Very High | High | Moderate | Low | Very Low",
        "confidence_percentage": number(0-100),
        "reasoning": "string - detailed explanation",
        "conditions": ["array of strings - if CONDITIONAL_APPROVE"],
        "appeal_process": "string - information if needed"
    },
    "key_factors": [
        {
            "category": "string",
            "impact": "Positive | Neutral | Concern | Critical",
            "description": "string",
            "score": number(0-100)
        }
    ],
    "risk_summary": {
        "strengths": ["array of strings"],
        "concerns": ["array of strings"],
        "mitigating_factors": ["array of strings"],
        "critical_factors": ["array of strings"]
    },
    "metrics_integration": {
        "income_stability_score": number,
        "employment_risk_level": "string",
        "credit_score": number,
        "dti_percentage": number,
        "loan_amount_risk": "string",
        "anomaly_count": number,
        "application_completeness": number
    },
    "recommendation_rationale": "executive summary",
    "next_steps": ["array of strings"],
    "compliance_notes": {
        "fair_lending_compliant": boolean,
        "documentation_complete": boolean,
        "audit_trail_created": boolean
    }
}
```

### 4. Decision Guidelines

The prompt provides specific guidelines:

1. **Integration**: Combine Agent1 and Agent2 outputs into cohesive analysis
2. **Reasoning**: Provide clear, documented reasoning for all decisions
3. **Fair Lending**: Balance risk mitigation with fair lending principles
4. **Holistic View**: Consider complete applicant profile, not isolated factors
5. **Inconsistencies**: Flag any inconsistencies between analyses
6. **Specificity**: Identify specific, actionable conditions
7. **Compliance**: Ensure adherence to lending regulations
8. **Audit Trail**: Create documented decision trail

---

## Agent Implementation

### Class: LoanDecisionAgent

**Initialization:**
```python
agent = LoanDecisionAgent(api_key=None)
```

**Attributes:**
```python
self.client          # Anthropic client
self.model           # Model name (default: claude-sonnet-4-6-20250514)
self.decision_db     # DecisionSynthesisClient instance
```

### Method: define_tools()

Returns list of 4 tools:

#### Tool 1: synthesize_loan_decision
```json
{
    "name": "synthesize_loan_decision",
    "description": "Synthesize final loan decision from applicant profile and risk analysis",
    "input_schema": {
        "type": "object",
        "properties": {
            "applicant_id": "string - unique applicant identifier",
            "applicant_data": "object - applicant profile data",
            "application_analysis": "object - Agent1 output",
            "risk_assessment": "object - Agent2 output",
            "strategy": "string - Conservative/Balanced/Aggressive"
        },
        "required": ["applicant_id", "applicant_data", "application_analysis", "risk_assessment"]
    }
}
```

**Execution Flow:**
1. POST to `/tools/synthesize_loan_decision/execute`
2. Includes all applicant data and analyses
3. Returns decision with classification and reasoning
4. Strategy influences risk thresholds and condition generation

#### Tool 2: evaluate_multiple_scenarios
```json
{
    "name": "evaluate_multiple_scenarios",
    "description": "Evaluate decision outcomes across multiple loan amount scenarios",
    "input_schema": {
        "type": "object",
        "properties": {
            "applicant_id": "string",
            "applicant_data": "object",
            "application_analysis": "object",
            "base_risk_assessment": "object",
            "scenario_results": "array - different loan amounts"
        },
        "required": ["applicant_id", "applicant_data", "application_analysis", "base_risk_assessment"]
    }
}
```

**Use Case:** Test if applicant would approve at different loan amounts

#### Tool 3: explain_decision
```json
{
    "name": "explain_decision",
    "description": "Get detailed explanation of the decision with key factors",
    "input_schema": {
        "type": "object",
        "properties": {
            "applicant_id": "string",
            "applicant_data": "object",
            "application_analysis": "object",
            "risk_assessment": "object"
        },
        "required": ["applicant_id", "applicant_data", "application_analysis", "risk_assessment"]
    }
}
```

**Returns:** Detailed explanation with key factors and reasoning

#### Tool 4: compare_applicants
```json
{
    "name": "compare_applicants",
    "description": "Compare decisions across multiple applicants",
    "input_schema": {
        "type": "object",
        "properties": {
            "applicants": "array - list of applicants with analyses"
        },
        "required": ["applicants"]
    }
}
```

**Use Case:** Comparative risk analysis for portfolio decisions

### Method: process_tool_call(tool_name, tool_input)

Handles execution of each tool:

```python
def process_tool_call(self, tool_name: str, tool_input: dict) -> dict:
    if tool_name == "synthesize_loan_decision":
        return self.decision_db.synthesize_loan_decision(...)
    elif tool_name == "evaluate_multiple_scenarios":
        return self.decision_db.evaluate_multiple_scenarios(...)
    elif tool_name == "explain_decision":
        return self.decision_db.explain_decision(...)
    elif tool_name == "compare_applicants":
        return self.decision_db.compare_applicants(...)
```

**Error Handling:**
- Catches connection errors
- Returns error JSON with descriptive message
- Allows agent to retry or provide fallback reasoning

### Method: make_decision(applicant_id, applicant_data, applicant_analysis, risk_analysis, strategy)

Main method for synthesizing final decision:

**Signature:**
```python
def make_decision(
    self,
    applicant_id: str,                    # Unique applicant ID
    applicant_data: dict,                 # Applicant profile
    applicant_analysis: dict,             # Agent1 output
    risk_analysis: dict,                  # Agent2 output
    strategy: str = "Balanced"            # Decision strategy
) -> dict
```

**Execution Loop:**
1. Initialize messages with user prompt containing all data
2. Enter agentic loop (max 10 iterations)
3. Call Claude with system prompt and tools
4. Check response stop reason
5. If `tool_use`:
   - Extract tool calls
   - Process each tool
   - Add results to conversation
   - Continue loop
6. If `end_turn`:
   - Extract final response
   - Parse JSON
   - Return decision
7. Return error if max iterations exceeded

**Return Structure:**
```python
{
    "status": "success" | "error",
    "decision": {...},           # Parsed JSON if success
    "raw_response": "...",       # Claude's full response
    "message": "error message"   # If status is error
}
```

---

## DecisionSynthesisClient Class

HTTP client for DecisionSynthesis MCP Server communication.

**Initialization:**
```python
client = DecisionSynthesisClient(
    base_url="http://localhost:3002",
    timeout=30.0
)
```

**Methods:**

### synthesize_loan_decision()
```python
result = client.synthesize_loan_decision(
    applicant_id="APP001",
    applicant_data={...},
    application_analysis={...},
    risk_assessment={...},
    strategy="Balanced"
)
```

**HTTP Call:**
```
POST http://localhost:3002/tools/synthesize_loan_decision/execute
Content-Type: application/json

{
    "applicant_id": "APP001",
    "applicant_data": {...},
    "application_analysis": {...},
    "risk_assessment": {...},
    "strategy": "Balanced"
}
```

### evaluate_multiple_scenarios()
```python
result = client.evaluate_multiple_scenarios(
    applicant_id="APP001",
    applicant_data={...},
    application_analysis={...},
    base_risk_assessment={...},
    scenario_results=[...]
)
```

**Purpose:** Test decision outcomes across different loan amounts

### explain_decision()
```python
result = client.explain_decision(
    applicant_id="APP001",
    applicant_data={...},
    application_analysis={...},
    risk_assessment={...}
)
```

**Purpose:** Get detailed explanation with key factors

### compare_applicants()
```python
result = client.compare_applicants(
    applicants=[
        {"id": "APP001", "data": {...}, ...},
        {"id": "APP002", "data": {...}, ...}
    ]
)
```

**Purpose:** Compare risk profiles across applicants

---

## Decision Strategies

### Conservative Strategy

**Risk Thresholds:**
- Very High Risk (>4.5) → REJECT
- High Risk (3.5-4.5) → REVIEW
- Medium Risk (2.5-3.5) → REVIEW
- Low Risk (1.5-2.5) → CONDITIONAL
- Very Low (<1.5) → APPROVE

**Condition Intensity:** Higher
**Approval Rate:** Lower
**Use Case:** Risk-averse lending environment

### Balanced Strategy (Default)

**Risk Thresholds:**
- Very High Risk (>4.5) → REJECT
- High Risk (3.5-4.5) → REVIEW
- Medium Risk (2.5-3.5) → REVIEW or CONDITIONAL
- Low Risk (1.5-2.5) → CONDITIONAL or APPROVE
- Very Low (<1.5) → APPROVE

**Condition Intensity:** Moderate
**Approval Rate:** Balanced
**Use Case:** Standard lending operations

### Aggressive Strategy

**Risk Thresholds:**
- Very High Risk (>4.5) → REVIEW
- High Risk (3.5-4.5) → CONDITIONAL
- Medium Risk (2.5-3.5) → CONDITIONAL
- Low Risk (1.5-2.5) → APPROVE
- Very Low (<1.5) → APPROVE

**Condition Intensity:** Lower
**Approval Rate:** Higher
**Use Case:** Growth-focused lending

---

## Key Decision Factors

Agent3 evaluates and ranks factors across these categories:

### 1. Income Stability Factors
- **Score Source**: Agent1 Income Stability Score
- **Range**: 0-100
- **Categories**:
  - Very Unstable (0-20): Frequent job changes, inconsistent income
  - Unstable (20-40): Some income variation, recent employment
  - Moderate (40-60): Stable employment, normal variation
  - Stable (60-80): Consistent income, established employment
  - Very Stable (80-100): Long-term employment, steady income

### 2. Employment Risk Factors
- **Score Source**: Agent1 Employment Risk Level
- **Range**: 0-100 (0 = very low risk, 100 = very high risk)
- **Categories**:
  - Very Low Risk (0-20): Established position, secure industry
  - Low Risk (20-40): Stable position, good industry outlook
  - Medium Risk (40-60): Some volatility, standard role
  - High Risk (60-80): Volatile position, uncertain industry
  - Very High Risk (80-100): Precarious employment, layoff risk

### 3. Credit Profile Factors
- **Score Source**: Agent1 & Agent2 Credit Data
- **Credit Score Range**: 300-850
- **Categories**:
  - Excellent (750+): Excellent payment history
  - Good (700-749): Good payment record
  - Fair (650-699): Acceptable history with minor issues
  - Poor (600-649): Multiple issues, payment concerns
  - Very Poor (<600): Significant credit problems

### 4. Debt Management Factors
- **Score Source**: Agent2 DTI Analysis
- **DTI Range**: 0-100%
- **Categories**:
  - Very Low Risk (<20%): Minimal debt burden
  - Low Risk (20-36%): Manageable debt
  - Medium Risk (36-43%): Moderate debt concern
  - High Risk (43-50%): Substantial debt burden
  - Very High Risk (>50%): Unsustainable debt

### 5. Loan Amount Factors
- **Score Source**: Agent2 Loan Amount Risk
- **LTI Range**: 0%+ (Loan-to-Income)
- **LTV Range**: 0-100%+ (Loan-to-Value)
- **Categories**:
  - Very Low Risk: LTI <3%, LTV <60%
  - Low Risk: LTI 3-5%, LTV 60-80%
  - Medium Risk: LTI 5-8%, LTV 80-95%
  - High Risk: LTI 8-12%, LTV 95-110%
  - Very High Risk: LTI >12%, LTV >110%

### 6. Anomaly & Red Flags
- **Score Source**: Agent2 Anomaly Detection
- **Categories**:
  - Critical (Severity 100): Recent delinquency, high DTI
  - High (Severity 80): Low credit score, unusual loan
  - Medium (Severity 60): High utilization, short employment
  - Low (Severity 40): Income inconsistency, age mismatch
  - None: No anomalies detected

### 7. Compensating Factors
- High income offsetting high DTI
- Excellent credit offsetting employment concerns
- Strong collateral offsetting income concerns
- Multiple years of employment offsetting other concerns

---

## Integration Patterns

### Pattern 1: Full Pipeline (Agent1 → Agent2 → Agent3)

```python
from agents.application_profile_agent import ApplicationProfileAgent
from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent
from agents.loan_decision_agent import LoanDecisionAgent

# Get applicant profile analysis
profile_agent = ApplicationProfileAgent()
profile_result = profile_agent.analyze_applicant("APP001")

# Get financial risk analysis
risk_agent = FinancialRiskAnalysisAgent()
risk_result = risk_agent.analyze_financial_risk(
    "APP001",
    applicant_data,
    loan_request
)

# Make decision
decision_agent = LoanDecisionAgent()
decision_result = decision_agent.make_decision(
    "APP001",
    applicant_data,
    profile_result["analysis"],
    risk_result["analysis"]
)
```

### Pattern 2: Batch Decision Processing

```python
agent = LoanDecisionAgent()
results = []

for applicant_id in applicant_ids:
    # Get analyses from Agent1 & Agent2
    profile = get_profile_analysis(applicant_id)
    risk = get_risk_analysis(applicant_id)
    
    # Make decision
    decision = agent.make_decision(
        applicant_id,
        applicant_data[applicant_id],
        profile,
        risk
    )
    results.append(decision)
```

### Pattern 3: Scenario Comparison

```python
agent = LoanDecisionAgent()

# Compare decision across strategies
for strategy in ["Conservative", "Balanced", "Aggressive"]:
    result = agent.make_decision(
        applicant_id,
        applicant_data,
        applicant_analysis,
        risk_analysis,
        strategy=strategy
    )
    decisions[strategy] = result
```

---

## Error Handling

### Connection Errors

**Cause**: DecisionSynthesis server not running

```python
try:
    result = agent.make_decision(...)
except ConnectionError:
    # Start server: python mcp/decisionsynthesis/server.py
```

### Timeout Errors

**Cause**: Slow network or server response

```python
agent.decision_db = DecisionSynthesisClient(timeout=60)
```

### API Key Errors

**Cause**: ANTHROPIC_API_KEY not set

```bash
export ANTHROPIC_API_KEY=sk-...
```

### JSON Parse Errors

**Cause**: Claude response doesn't contain valid JSON

```python
if result.get("status") == "success" and "decision" not in result:
    # Fall back to raw_response
    raw = result.get("raw_response")
```

---

## Performance Characteristics

- **Average Decision Time**: 20-45 seconds
- **Tool Calls per Decision**: 2-4 calls
- **Agent Iterations**: 2-4 iterations
- **Max Iterations**: 10 (safety limit)
- **Memory per Instance**: ~50MB
- **Concurrent Decisions**: Limited by rate limits

---

## Compliance and Fair Lending

Agent3 ensures compliance through:

1. **Fair Lending Checks**
   - Decisions based on credit-related factors
   - No discrimination by protected classes
   - Consistent application of standards

2. **Documentation**
   - Complete decision reasoning
   - Key factors and justification
   - Appeal process information

3. **Audit Trail**
   - Timestamp of decision
   - All input data recorded
   - Tool execution logged
   - Compliance notes captured

4. **Transparency**
   - Clear conditions if applicable
   - Explainable decision factors
   - Reasoned recommendations

---

## Configuration Options

### Model Selection
```python
agent.model = "claude-opus-4-7-20250805"      # Most capable
agent.model = "claude-sonnet-4-6-20250514"    # Balanced (default)
agent.model = "claude-haiku-4-5-20251001"     # Fast, cost-effective
```

### Server Connection
```python
from agents.loan_decision_agent import DecisionSynthesisClient

agent.decision_db = DecisionSynthesisClient(
    base_url="http://custom-server:3002",
    timeout=30.0
)
```

### Max Iterations
Modify in `make_decision()` method:
```python
max_iterations = 10  # Default
max_iterations = 5   # Faster
max_iterations = 15  # More thorough
```

---

## Testing the Implementation

### Test 1: Single Decision
```python
agent = LoanDecisionAgent()
result = agent.make_decision(
    "TEST001",
    applicant_data,
    applicant_analysis,
    risk_analysis
)
assert result["status"] == "success"
assert "decision" in result
```

### Test 2: Decision Classification
```python
decision = result["decision"]["decision"]
valid_classifications = [
    "APPROVE",
    "CONDITIONAL_APPROVE",
    "REVIEW",
    "REJECT"
]
assert decision["classification"] in valid_classifications
```

### Test 3: Risk Score Range
```python
risk_score = decision["risk_score"]
assert 0 <= risk_score <= 5
```

### Test 4: Compliance
```python
compliance = decision.get("compliance_notes", {})
assert compliance.get("fair_lending_compliant") is True
assert compliance.get("documentation_complete") is True
```

---

## Next Steps

1. ✅ Deploy Agent3: `python agents/loan_decision_agent.py`
2. 📊 Review decision quality and accuracy
3. 🔗 Create Agent4 (Notification Agent)
4. 🌐 Build LangGraph orchestration
5. 🎨 Integrate with Streamlit UI

---

**Last Updated:** 2026-05-24  
**Status:** ✅ Production Ready
