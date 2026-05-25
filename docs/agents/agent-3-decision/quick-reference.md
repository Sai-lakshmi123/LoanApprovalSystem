# Agent3: Loan Decision Agent - Quick Reference Guide

## 30-Second Setup

```bash
# 1. Start DecisionSynthesis server (separate terminal)
python mcp/decisionsynthesis/server.py

# 2. Import and create agent
from agents.loan_decision_agent import LoanDecisionAgent

agent = LoanDecisionAgent()

# 3. Make a decision
result = agent.make_decision(
    applicant_id="APP001",
    applicant_data={...},                # Applicant profile
    applicant_analysis={...},            # Agent1 output
    risk_analysis={...},                 # Agent2 output
    strategy="Balanced"
)
```

---

## What Agent3 Does

Agent3 synthesizes final loan decisions by combining:
- **Agent1 Output**: Applicant profile analysis (income, employment, credit, completeness)
- **Agent2 Output**: Financial risk analysis (DTI, credit risk, loan risk, anomalies)
- **Decision Logic**: Synthesizes data into classification with reasoning

**Returns:**
- ✅ Decision classification (APPROVE/CONDITIONAL_APPROVE/REVIEW/REJECT)
- ✅ Risk score (0-5) synthesized from all factors
- ✅ Confidence level with percentage
- ✅ Key decision factors with impact analysis
- ✅ Risk summary (strengths, concerns, mitigating factors, critical factors)
- ✅ Compliance notes and audit trail

---

## Decision Classifications

### 1. APPROVE ✅
- **Condition**: Risk score < 1.5, no critical violations
- **Profile**: Strong financial profile across all dimensions
- **Repayment**: Clear path to repayment
- **Requirements**: Minimal to no conditions

### 2. CONDITIONAL_APPROVE ✅
- **Condition**: Risk score 1.5-2.5 with minor concerns
- **Profile**: Good overall profile with specific issues
- **Conditions**: Specific, actionable conditions required
- **Approval**: Conditional on meeting stated requirements

### 3. REVIEW ⚠️
- **Condition**: Risk score 2.5-3.5 with mixed signals
- **Profile**: Concerns that may be resolvable
- **Review**: Senior underwriter input recommended
- **Status**: Not automatically approved or rejected

### 4. REJECT ❌
- **Condition**: Risk score > 3.5 or critical violations
- **Profile**: Multiple high-risk factors identified
- **Mitigation**: Insufficient mitigating factors
- **Status**: Does not meet lending criteria

---

## Risk Score (0-5 Scale)

| Score | Level | Status |
|-------|-------|--------|
| 0-1.5 | Very Low | APPROVE ✅ |
| 1.5-2.5 | Low | CONDITIONAL ✅ |
| 2.5-3.5 | Medium | REVIEW ⚠️ |
| 3.5-4.5 | High | UNDERWRITING ❌ |
| 4.5-5.0 | Very High | DECLINE ❌ |

---

## Confidence Levels

| Level | Range | Meaning |
|-------|-------|---------|
| Very High | 85-100% | Complete data, strong agreement |
| High | 70-84% | Good data quality, minor inconsistencies |
| Moderate | 55-69% | Acceptable data, some concerns |
| Low | 40-54% | Limited data or conflicting signals |
| Very Low | <40% | Incomplete data, major inconsistencies |

---

## 4 Available Tools

### Tool 1: synthesize_loan_decision
```python
agent.decision_db.synthesize_loan_decision(
    applicant_id="APP001",
    applicant_data={...},
    application_analysis={...},      # From Agent1
    risk_assessment={...},           # From Agent2
    strategy="Balanced"              # Conservative/Balanced/Aggressive
)
```
**Purpose**: Combine analyses and make final decision
**Returns**: Complete decision with classification and reasoning

### Tool 2: evaluate_multiple_scenarios
```python
agent.decision_db.evaluate_multiple_scenarios(
    applicant_id="APP001",
    applicant_data={...},
    application_analysis={...},
    base_risk_assessment={...},
    scenario_results=[...]           # Different loan amounts
)
```
**Purpose**: Compare outcomes across different loan scenarios
**Returns**: Decision outcomes for each scenario

### Tool 3: explain_decision
```python
agent.decision_db.explain_decision(
    applicant_id="APP001",
    applicant_data={...},
    application_analysis={...},
    risk_assessment={...}
)
```
**Purpose**: Get detailed explanation of decision
**Returns**: Key factors, reasoning, compliance notes

### Tool 4: compare_applicants
```python
agent.decision_db.compare_applicants(
    applicants=[
        {"id": "APP001", "data": {...}, "analysis": {...}},
        {"id": "APP002", "data": {...}, "analysis": {...}}
    ]
)
```
**Purpose**: Compare decisions across multiple applicants
**Returns**: Comparative risk profiles and recommendations

---

## Key Decision Factors

Agent3 evaluates:

1. **Income Stability** (from Agent1)
   - Score: 0-100
   - Category: Very Unstable → Very Stable

2. **Employment Risk** (from Agent1)
   - Risk Score: 0-100
   - Level: Very Low → Very High

3. **Credit Profile** (from Agent1 + Agent2)
   - Credit Score (300-850)
   - History Pattern
   - Payment Discipline

4. **Debt Management** (from Agent2)
   - DTI Ratio (0-100%)
   - Current and projected
   - Capacity to service new loan

5. **Loan Appropriateness** (from Agent2)
   - LTI Ratio (Loan-to-Income)
   - LTV Ratio (Loan-to-Value)
   - Amount relative to capacity

6. **Anomalies & Red Flags** (from Agent2)
   - Unusual patterns
   - Severity classification
   - Count and types

7. **Compensating Factors**
   - Strong income
   - Low debt
   - Good credit
   - Stable employment

---

## Output Structure

```json
{
    "applicant_id": "APP001",
    "analysis_timestamp": "2026-05-24T10:30:00",
    "decision": {
        "classification": "APPROVE",
        "risk_score": 1.8,
        "confidence_level": "Very High",
        "confidence_percentage": 92,
        "reasoning": "...",
        "conditions": []
    },
    "key_factors": [
        {
            "category": "Income Stability",
            "impact": "Positive",
            "description": "...",
            "score": 85
        }
    ],
    "risk_summary": {
        "strengths": [...],
        "concerns": [...],
        "mitigating_factors": [...],
        "critical_factors": [...]
    },
    "metrics_integration": {
        "income_stability_score": 85,
        "employment_risk_level": "Very Low",
        "credit_score": 760,
        "dti_percentage": 35.5,
        "loan_amount_risk": "Very Low",
        "anomaly_count": 0,
        "application_completeness": 100
    },
    "recommendation_rationale": "...",
    "next_steps": [...],
    "compliance_notes": {
        "fair_lending_compliant": true,
        "documentation_complete": true,
        "audit_trail_created": true
    }
}
```

---

## Configuration

### Change Model
```python
agent = LoanDecisionAgent()
agent.model = "claude-opus-4-7-20250805"     # Most capable
agent.model = "claude-sonnet-4-6-20250514"   # Default
agent.model = "claude-haiku-4-5-20251001"    # Fast
```

### Change DecisionSynthesis URL
```python
from agents.loan_decision_agent import DecisionSynthesisClient

agent.decision_db = DecisionSynthesisClient(
    base_url="http://192.168.1.100:3002"
)
```

### Adjust Timeout
```python
agent.decision_db = DecisionSynthesisClient(timeout=60)
```

### Change Decision Strategy
```python
result = agent.make_decision(
    ...,
    strategy="Conservative"    # Conservative/Balanced/Aggressive
)
```

---

## Decision Strategies

### Conservative
- Higher risk tolerance threshold
- More conditions for approval
- Favors REVIEW decisions
- Lower approval rate

### Balanced (Default)
- Medium risk tolerance
- Reasonable conditions
- Mixed approval rates
- Fair lending focus

### Aggressive
- Lower risk tolerance threshold
- Fewer conditions required
- More APPROVE decisions
- Higher approval rate

---

## Common Patterns

### Extract Decision Classification
```python
result = agent.make_decision(...)
decision = result["decision"]["decision"]
classification = decision["classification"]
print(f"Decision: {classification}")
```

### Check Risk Score
```python
risk_score = decision["risk_score"]
confidence = decision["confidence_percentage"]
print(f"Risk: {risk_score}/5 (Confidence: {confidence}%)")
```

### Review Key Factors
```python
factors = decision.get("key_factors", [])
for factor in factors:
    print(f"{factor['category']}: {factor['impact']}")
```

### Get Conditions (if applicable)
```python
conditions = decision.get("decision", {}).get("conditions", [])
if conditions:
    print("Required Conditions:")
    for cond in conditions:
        print(f"  • {cond}")
```

### Check Compliance
```python
compliance = decision.get("compliance_notes", {})
is_compliant = compliance.get("fair_lending_compliant")
print(f"Fair Lending Compliant: {is_compliant}")
```

---

## Integration with Agent1 & Agent2

```python
from agents.application_profile_agent import ApplicationProfileAgent
from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent
from agents.loan_decision_agent import LoanDecisionAgent

# Step 1: Agent1 - Profile Analysis
profile_agent = ApplicationProfileAgent()
profile_result = profile_agent.analyze_applicant("APP001")
applicant_analysis = profile_result["analysis"]

# Step 2: Agent2 - Risk Analysis
risk_agent = FinancialRiskAnalysisAgent()
risk_result = risk_agent.analyze_financial_risk(
    "APP001",
    applicant_data,
    loan_request
)
risk_analysis = risk_result["analysis"]

# Step 3: Agent3 - Decision Synthesis
decision_agent = LoanDecisionAgent()
decision_result = decision_agent.make_decision(
    "APP001",
    applicant_data,
    applicant_analysis,
    risk_analysis,
    strategy="Balanced"
)
```

---

## Error Handling

### Connection Error
```
Error: Connection refused
→ Ensure DecisionSynthesis server is running
  python mcp/decisionsynthesis/server.py
```

### API Key Error
```
Error: Invalid API key
→ Set ANTHROPIC_API_KEY environment variable
  export ANTHROPIC_API_KEY=sk-...
```

### Timeout Error
```
Error: Request timeout
→ Increase timeout in DecisionSynthesisClient
  client = DecisionSynthesisClient(timeout=60)
```

### JSON Parse Error
```
Error: Failed to parse decision JSON
→ Check Claude output format
→ Verify all required fields in response
```

---

## Performance

- **Average Decision Time**: 20-45 seconds
- **Tool Calls per Decision**: 2-4 calls
- **Agent Iterations**: 2-4 iterations
- **Memory Usage**: ~50MB per agent instance

---

## System Prompt

Agent3 operates with a **150+ line system prompt** that:

1. **Defines Role**: Expert loan decision analyst
2. **Outlines Framework**:
   - Decision classifications (APPROVE/CONDITIONAL/REVIEW/REJECT)
   - Confidence assessment (Very High → Very Low)
   - Key decision factors (7 dimensions)
   - Risk score integration (0-5 scale)
3. **Specifies Output**: Exact JSON structure required
4. **Provides Guidelines**:
   - Integration of Agent1 & Agent2 outputs
   - Fair lending compliance
   - Clear reasoning documentation
   - Condition generation for conditional approvals

---

## Troubleshooting

### Decision takes too long
- Check DecisionSynthesis server logs
- Verify network connectivity
- Try increasing timeout to 60 seconds

### Decision doesn't include all fields
- Check response JSON structure
- Verify all tool calls completed
- Review system prompt compliance

### Confidence level too low
- May indicate incomplete data
- Check Agent1 & Agent2 outputs for gaps
- Consider additional manual review

### Risk score unexpected
- Verify Agent1 & Agent2 calculations
- Review key factors and weightings
- Check for data inconsistencies

---

## Examples

See [../examples/agent3_usage_example.py](../examples/agent3_usage_example.py) for:
1. ✅ Single applicant decision
2. ✅ Batch decision processing
3. ✅ Decision comparison across strategies
4. ✅ Extracting key factors and conditions
5. ✅ JSON export and storage

---

## Next Steps

1. ✅ Run Agent3: `python agents/loan_decision_agent.py`
2. 📊 Review decision outputs
3. 🔗 Create Agent4 (Notification Agent)
4. 🌐 Build LangGraph orchestration
5. 🎨 Integrate with Streamlit UI

---

## System Requirements

- Python 3.8+
- anthropic >= 0.7.0
- httpx >= 0.24.0
- ANTHROPIC_API_KEY environment variable
- DecisionSynthesis MCP Server running on port 3002

---

**Last Updated:** 2026-05-24  
**Status:** ✅ Production Ready
