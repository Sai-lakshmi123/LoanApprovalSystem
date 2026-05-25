# Financial Risk Analysis Agent (Agent2) - Implementation Guide

## Overview

Agent2 is an intelligent financial risk analyzer powered by Claude Sonnet 4.6 and built with the Anthropic Agent SDK. It analyzes loan applications from a financial risk perspective and returns comprehensive risk assessment.

**Technology Stack:**
- LLM: Claude Sonnet 4.6 (claude-sonnet-4-6-20250514)
- Framework: Anthropic Agent SDK
- Integration: RiskRulesDB MCP Server
- Language: Python
- Patterns: Tool use, multi-turn conversations, structured output

---

## System Prompt

Agent2 operates with a comprehensive system prompt that guides financial risk analysis.

### Key Components

#### 1. Role Definition
```
Expert financial risk analyst specializing in loan underwriting
Evaluates financial capacity and risk using RiskRulesDB system
```

#### 2. Analysis Framework

**Debt-to-Income (DTI) Ratio (0-100%)**
- Categories:
  - < 20%: Very Low Risk ✅
  - 20-36%: Low Risk ✅
  - 36-43%: Medium Risk ⚠️
  - 43-50%: High Risk ❌
  - > 50%: Very High Risk ❌❌

**Credit Score Risk**
- Excellent (750+): Very Low Risk
- Good (700-749): Low Risk
- Fair (650-699): Medium Risk
- Poor (600-649): High Risk
- Very Poor (<600): Very High Risk
- Adjustments for delinquencies and inquiries

**Loan Amount Risk (LTI & LTV)**
- Loan-to-Income (LTI):
  - < 3%: Very Low ✅
  - 3-5%: Low ✅
  - 5-8%: Medium ⚠️
  - 8-12%: High ❌
  - > 12%: Very High ❌❌
- Loan-to-Value (LTV):
  - < 60%: Excellent ✅
  - 60-80%: Good ✅
  - 80-95%: Acceptable ⚠️
  - > 95%: High Risk ❌

**Anomaly Detection (9 Types)**
- Critical: High DTI (>50%), Recent delinquency (<6 months)
- High: Low credit (<620), Unusual loan (LTI >10%)
- Medium: Excessive inquiries (>5 in 6 months), High utilization (>80%), Short tenure (<6 months)
- Low: Income inconsistency, Age-employment mismatch

**Aggregate Risk Score (0-5)**
- 0-1.5: Very Low (APPROVE)
- 1.5-2.5: Low (CONDITIONAL)
- 2.5-3.5: Medium (REVIEW)
- 3.5-4.5: High (UNDERWRITING)
- 4.5-5: Very High (DECLINE)

#### 3. Output Specification

Exact JSON structure with:
- applicant_id
- analysis_timestamp
- dti_analysis {...}
- credit_risk {...}
- loan_amount_risk {...}
- anomaly_detection {...}
- aggregate_risk_assessment {...}
- financial_summary
- key_findings []
- recommended_conditions []
- next_steps []

#### 4. Analysis Guidelines

- Use actual RiskRulesDB data
- Be systematic and thorough
- Provide clear reasoning
- Flag critical factors
- Consider compensating factors
- Maintain fair lending compliance
- Provide actionable insights

---

## Architecture

### Component Overview

```
FinancialRiskAnalysisAgent
├── Client (Anthropic SDK)
│   └── Claude Sonnet 4.6 LLM
├── Tool Definitions (6 tools)
│   └── Tool calling via agent iteration
└── RiskRulesDBClient
    └── HTTP calls to RiskRulesDB MCP Server (port 3001)
```

### Data Flow

```
analyze_financial_risk(applicant_id, applicant_data, loan_request)
    ↓
Send to Claude with system prompt
    ↓
Claude identifies needed risk metrics → Tool calls
    ↓
Agent processes tool calls → RiskRulesDB
    ↓
Tool results returned to Claude
    ↓
Claude analyzes results → More tool calls if needed
    ↓
Claude synthesizes risk analysis → Structured JSON
    ↓
Return final analysis
```

---

## 6 Available Tools

### 1. evaluate_dti_ratio

**Purpose:** Calculate debt-to-income ratio with risk assessment

**Input:**
```python
{
    "monthly_income": 12500,
    "monthly_debt": 3000
}
```

**Output:**
```python
{
    "analysis": {
        "dti_ratio": 0.24,
        "dti_percentage": 24.0,
        "risk_level": "Low",
        "category": "Good",
        "reasoning": "..."
    }
}
```

### 2. evaluate_credit_risk

**Purpose:** Assess credit score risk with adjustments

**Input:**
```python
{
    "credit_score": 760,
    "delinquencies": 0,
    "inquiries_last_6_months": 1
}
```

**Output:**
```python
{
    "analysis": {
        "credit_score": 760,
        "category": "Excellent",
        "base_risk_level": "Very Low",
        "adjusted_risk_score": 5,
        "final_risk_level": "Excellent",
        "reasoning": "..."
    }
}
```

### 3. evaluate_loan_amount_risk

**Purpose:** Evaluate loan size relative to income and property

**Input:**
```python
{
    "loan_amount": 300000,
    "annual_income": 150000,
    "property_value": 500000,
    "existing_loans": 1,
    "credit_score": 760
}
```

**Output:**
```python
{
    "analysis": {
        "loan_amount": 300000,
        "lti_ratio": 0.02,
        "lti_percentage": 2.0,
        "lti_risk": "Very Low",
        "ltv_ratio": 0.6,
        "ltv_percentage": 60.0,
        "ltv_risk": "Excellent",
        "overall_loan_risk": "Very Low",
        "reasoning": "..."
    }
}
```

### 4. detect_risk_anomalies

**Purpose:** Identify unusual patterns and red flags

**Input:**
```python
{
    "applicant": {
        "credit_score": 760,
        "delinquencies": 0,
        "inquiries_last_6_months": 1,
        "credit_utilization": 0.30,
        "years_at_current_job": 8
    },
    "loan": {
        "loan_amount": 300000,
        "property_value": 500000
    }
}
```

**Output:**
```python
{
    "analysis": {
        "has_anomalies": false,
        "anomaly_count": 0,
        "anomalies": [],
        "overall_anomaly_score": 0,
        "overall_anomaly_risk_level": "No Anomalies",
        "reasoning": "..."
    }
}
```

### 5. generate_risk_report

**Purpose:** Comprehensive financial risk assessment

**Input:**
```python
{
    "applicant_id": "APP001",
    "applicant_data": {...},
    "loan_request": {...}
}
```

**Output:**
```python
{
    "status": "success",
    "dti_analysis": {...},
    "dti_with_new_loan": {...},
    "credit_score_risk": {...},
    "loan_amount_risk": {...},
    "anomaly_detection": {...},
    "overall_risk_assessment": {
        "overall_risk_level": "Very Low",
        "overall_risk_score": 1.8,
        "approval_recommendation": "APPROVE"
    }
}
```

### 6. evaluate_with_scenario_analysis

**Purpose:** Compare risk across different loan amounts

**Input:**
```python
{
    "applicant_id": "APP001",
    "applicant_data": {...},
    "base_loan_request": {"loan_amount": 300000, ...},
    "scenarios": [
        {"name": "Conservative", "loan_amount": 250000},
        {"name": "Requested", "loan_amount": 300000},
        {"name": "Aggressive", "loan_amount": 350000}
    ]
}
```

**Output:**
```python
{
    "alternative_scenarios": [
        {
            "scenario": "Conservative",
            "loan_amount": 250000,
            "dti_percentage": 30.5,
            "risk_level": "Low"
        },
        ...
    ]
}
```

---

## Agent Initialization

### Creating an Agent Instance

```python
from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent

# Initialize agent
agent = FinancialRiskAnalysisAgent(api_key="sk-...")  # Optional

# Configure if needed
agent.model = "claude-sonnet-4-6-20250514"  # Default model
agent.risk_db = RiskRulesDBClient(base_url="http://localhost:3001")
```

---

## Analysis Process

### Step 1: Initialize Agent

```python
agent = FinancialRiskAnalysisAgent()
```

### Step 2: Call analyze_financial_risk()

```python
result = agent.analyze_financial_risk(
    applicant_id="APP001",
    applicant_data={...},
    loan_request={...}
)
```

### Step 3: Agent Execution Loop

1. **Initial Message**: Agent receives task with system prompt
2. **Tool Identification**: Claude identifies needed metrics
3. **Tool Execution**: Agent calls RiskRulesDB via HTTP
4. **Result Processing**: Tool results added to conversation
5. **Iteration**: Claude analyzes results, may call more tools
6. **Completion**: Claude synthesizes analysis
7. **JSON Extraction**: Final response parsed

### Step 4: Return Results

```python
{
    "status": "success",
    "analysis": {
        "applicant_id": "APP001",
        "dti_analysis": {...},
        "credit_risk": {...},
        "loan_amount_risk": {...},
        "anomaly_detection": {...},
        "aggregate_risk_assessment": {...},
        "financial_summary": "...",
        "key_findings": [...],
        "recommended_conditions": [...],
        "next_steps": [...]
    },
    "raw_response": "..."
}
```

---

## Usage Examples

### Analyze Single Applicant

```python
from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent

agent = FinancialRiskAnalysisAgent()

result = agent.analyze_financial_risk(
    "APP001",
    {
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
    {
        "loan_amount": 300000,
        "property_value": 500000,
        "loan_term_months": 360
    }
)

if result["status"] == "success":
    analysis = result["analysis"]
    print(f"DTI Risk: {analysis['dti_analysis']['dti_risk_level']}")
    print(f"Credit Risk: {analysis['credit_risk']['adjusted_risk_level']}")
    print(f"Risk Score: {analysis['aggregate_risk_assessment']['overall_risk_score']}/5")
```

### Extract Risk Metrics

```python
analysis = result["analysis"]

dti = analysis["dti_analysis"]["dti_with_new_loan_percentage"]
credit = analysis["credit_risk"]["credit_score"]
lti = analysis["loan_amount_risk"]["lti_percentage"]
anomalies = analysis["anomaly_detection"]["anomaly_count"]
risk_score = analysis["aggregate_risk_assessment"]["overall_risk_score"]
```

### Use with Agent1 Output

```python
# Agent1 provides applicant analysis
applicant_analysis = agent1_result["analysis"]

# Pass to Agent2
risk_result = agent2.analyze_financial_risk(
    applicant_id="APP001",
    applicant_data={
        "annual_income": applicant_analysis["income_stability"]["score"],
        ...
    },
    loan_request={...}
)
```

### Use with Agent3

```python
# Agent2 output feeds to Agent3
risk_analysis = agent2_result["analysis"]

# Pass to Agent3
from agents.decision_synthesis_agent import DecisionSynthesisAgent
decision_agent = DecisionSynthesisAgent()

decision = decision_agent.make_decision(
    applicant_id="APP001",
    applicant_analysis=applicant_analysis,
    risk_analysis=risk_analysis
)
```

---

## Error Handling

### Connection Errors

```python
try:
    result = agent.analyze_financial_risk(...)
except Exception as e:
    print(f"Error: {e}")
    # Check RiskRulesDB server is running
    # Check port 3001 is accessible
```

### Timeout Errors

```python
# Increase timeout if needed
agent.risk_db = RiskRulesDBClient(timeout=60)
```

### API Errors

```python
# Check API key is set
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-..."
```

---

## Configuration

### Model Selection

```python
agent.model = "claude-opus-4-7-20250805"  # Most capable
agent.model = "claude-sonnet-4-6-20250514"  # Default (balanced)
agent.model = "claude-haiku-4-5-20251001"  # Fast, cost-effective
```

### RiskRulesDB Connection

```python
from agents.financial_risk_analysis_agent import RiskRulesDBClient

# Custom URL
agent.risk_db = RiskRulesDBClient(
    base_url="http://192.168.1.100:3001"
)

# Longer timeout
agent.risk_db = RiskRulesDBClient(timeout=60)
```

---

## Integration with Multi-Agent System

Agent2 is the second component in a 4-agent system:

```
Agent1: Application Profile Agent (Income, Employment, Credit)
    ↓
Agent2: Financial Risk Analysis Agent (DTI, Risk Score, Anomalies) ← YOU ARE HERE
    ↓
Agent3: Decision Synthesis Agent (APPROVE/REJECT/CONDITIONAL/REVIEW)
    ↓
Agent4: Notification Agent (Case ID, Notifications Sent)
```

---

## Performance Metrics

- Average analysis time: 15-40 seconds
- Tool calls per analysis: 4-8 calls
- Agent iterations: 2-5 iterations
- API rate limit: Check Anthropic pricing

---

## Testing

### Unit Test Example

```python
def test_analyze_financial_risk():
    agent = FinancialRiskAnalysisAgent()
    result = agent.analyze_financial_risk(
        "APP001",
        {"annual_income": 150000, ...},
        {"loan_amount": 300000, ...}
    )
    
    assert result["status"] == "success"
    assert "analysis" in result
    assert "dti_analysis" in result["analysis"]
    assert "credit_risk" in result["analysis"]
    assert "aggregate_risk_assessment" in result["analysis"]
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | RiskRulesDB not running | `python mcp/riskrulesdb/server.py` |
| Invalid API key | Wrong or missing key | Set ANTHROPIC_API_KEY |
| JSON parse error | Agent output format invalid | Check Claude's response |
| Tool not found | RiskRulesDB missing tool | Verify all 6 tools available |
| Timeout | Slow server or network | Increase timeout |

---

## Files

- **Agent Code**: `agents/financial_risk_analysis_agent.py`
- **Quick Reference**: `agents/AGENT2_QUICKREF.md`
- **This Guide**: `agents/AGENT2_IMPLEMENTATION.md`
- **README**: `agents/README_AGENT2.md`
- **MCP Server**: `mcp/riskrulesdb/server.py`
- **System Prompt**: Lines 20-130 in agent code

---

## Key Takeaways

✅ Claude Sonnet 4.6 for intelligent risk analysis
✅ Anthropic Agent SDK manages tool use
✅ System prompt defines risk assessment framework
✅ 6 specialized tools from RiskRulesDB
✅ Structured JSON output for consistency
✅ Fair lending compliance built-in
✅ Production-ready implementation
✅ Foundation for decision synthesis
