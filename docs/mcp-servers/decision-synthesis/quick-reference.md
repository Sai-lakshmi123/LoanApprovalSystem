# DecisionSynthesis - Quick Reference

## 🚀 30-Second Setup

```bash
# Start server
python mcp/decisionsynthesis/server.py

# Run demo (in another terminal)
python examples/decisionsynthesis_demo.py

# Use in code
from mcp.decisionsynthesis.client import DecisionSynthesisSyncClient
client = DecisionSynthesisSyncClient()
decision = client.synthesize_loan_decision("APP001", app_data, app_analysis, risk_assessment)
```

---

## 📊 What DecisionSynthesis Does

Synthesizes outputs from **Application DB** + **RiskRulesDB** into **final loan decisions**.

Inputs:
- Applicant profile (Application DB)
- Financial risk assessment (RiskRulesDB)

Outputs:
- Decision classification (APPROVE/CONDITIONAL_APPROVE/REVIEW/REJECT)
- Risk score (0-5 scale)
- Confidence level
- Key decision factors
- Detailed explanation

---

## 🛠️ 4 Tools Available

| Tool | What It Does |
|------|------------|
| `synthesize_loan_decision()` | ⭐ Get final decision with all details |
| `evaluate_multiple_scenarios()` | Compare decisions across loan amounts |
| `explain_decision()` | Get detailed explanation of decision |
| `compare_applicants()` | Compare multiple applicants side-by-side |

---

## 💡 Basic Examples

### Get Loan Decision

```python
from mcp.decisionsynthesis.client import DecisionSynthesisSyncClient
from mcp.clients.mcp_client import SyncMCPClient
from mcp.riskrulesdb.client import RiskRulesDBSyncClient

# Initialize clients
app_db = SyncMCPClient()
risk_db = RiskRulesDBSyncClient()
decision_db = DecisionSynthesisSyncClient()

# Get applicant data from Application DB
applicant = app_db.get_applicant_profile("APP001")['data']
app_analysis = app_db.get_complete_applicant_analysis("APP001")

# Get risk assessment from RiskRulesDB
risk_assessment = risk_db.generate_risk_report("APP001", applicant, loan_request)

# Get decision from DecisionSynthesis
decision = decision_db.synthesize_loan_decision(
    "APP001",
    applicant,
    app_analysis['analysis'],
    risk_assessment,
    strategy="Balanced"
)

# Use the decision
print(f"Decision: {decision['decision']['classification']}")
print(f"Risk Score: {decision['decision']['risk_score']}/5")
print(f"Confidence: {decision['decision']['confidence_level']}")
print(f"Explanation: {decision['decision']['reasoning']}")
```

### Compare Different Strategies

```python
for strategy in ["Conservative", "Balanced", "Aggressive"]:
    result = decision_db.synthesize_loan_decision(
        "APP001", applicant, app_analysis['analysis'], risk_assessment,
        strategy=strategy
    )
    print(f"{strategy}: {result['decision']['classification']}")
```

### Get Detailed Explanation

```python
explanation = decision_db.explain_decision(
    "APP001", applicant, app_analysis['analysis'], risk_assessment
)

print(f"Decision: {explanation['decision']}")
print(f"Confidence: {explanation['confidence']}")
print(f"Explanation: {explanation['explanation']}")

for factor in explanation['key_factors']:
    print(f"• {factor['category']}: {factor['value']}")
    print(f"  Impact: {factor['impact']}")
```

### Compare Applicants

```python
applicants = [
    {
        "applicant_id": "APP001",
        "applicant_data": app1_data,
        "application_analysis": app1_analysis,
        "risk_assessment": app1_risk
    },
    {
        "applicant_id": "APP002",
        "applicant_data": app2_data,
        "application_analysis": app2_analysis,
        "risk_assessment": app2_risk
    }
]

comparison = decision_db.compare_applicants(applicants)

for result in comparison['results']:
    print(f"{result['applicant_id']}: {result['decision']}")
```

---

## 📈 Decision Classifications

| Classification | Meaning | Action |
|---|---|---|
| ✅ APPROVE | Full approval | Issue approval letter |
| ✅ CONDITIONAL_APPROVE | Approved with requirements | Issue conditional letter |
| ⚠️ REVIEW | Requires manual review | Route to underwriter |
| ❌ REJECT | Does not meet criteria | Issue denial letter |

---

## 🎯 Strategies

### Conservative
- Strictest criteria
- Lowest approval rate
- Minimal risk
- DTI < 36%, Credit > 700, Risk < 2.5
- **Use for:** Prime lending, risk-averse institutions

### Balanced
- Moderate criteria
- Standard approval rate
- Managed risk
- DTI < 43%, Credit > 650, Risk < 3.0
- **Use for:** Standard lending, conventional loans

### Aggressive
- Relaxed criteria
- Higher approval rate
- Managed growth
- DTI < 50%, Credit > 600, Risk < 3.5
- **Use for:** Growth-focused, alternative lending

---

## 💯 Risk Score (0-5 Scale)

Components:
- **Income Stability** (0-5): How stable applicant's income is
- **Employment Risk** (0-5): How risky their employment is
- **Credit Score** (0-5): Credit profile assessment
- **DTI Ratio** (0-5): Debt management capacity
- **Anomalies** (0-5): Unusual patterns detected

**Aggregate** = Average of all components

---

## 🔒 Confidence Level

How confident is the decision?

- **Very High** (>0.85): All data strong, no contradictions
- **High** (0.70-0.85): Good data quality, minimal concerns
- **Moderate** (0.55-0.70): Acceptable data, some concerns
- **Low** (0.40-0.55): Limited data or some contradictions
- **Very Low** (<0.40): Incomplete data, many concerns

**Factors:**
- Application completeness (35%)
- Metric alignment (40%)
- Anomalies detected (25%)

---

## 📋 Key Factors

Decision includes key factors influencing the result:

```python
for factor in decision['key_factors']:
    {
        "category": str,         # Income Stability, Employment Risk, etc.
        "value": any,           # The actual value
        "impact": str,          # Positive, Concern, Major Concern
        "description": str      # Human-readable explanation
    }
```

---

## 🔧 Configuration

### Change Server Port
Edit `mcp/decisionsynthesis/server.py`:
```python
uvicorn.run("mcp.decisionsynthesis.server:app", port=3003)
```

### Change Client URL
```python
client = DecisionSynthesisSyncClient(
    base_url="http://localhost:3003"
)
```

### Change Timeout
```python
client = DecisionSynthesisSyncClient(timeout=60.0)
```

---

## 📚 Access Resources

```python
client = DecisionSynthesisSyncClient()

# Get strategy definitions
strategies = client.get_decision_strategies()

# Get classification definitions
classifications = client.get_decision_classifications()

# Get confidence calibration
calibration = client.get_confidence_calibration()
```

---

## 🔄 Complete Workflow

```python
from mcp.clients.mcp_client import SyncMCPClient
from mcp.riskrulesdb.client import RiskRulesDBSyncClient
from mcp.decisionsynthesis.client import DecisionSynthesisSyncClient

# 1. Initialize all clients
app_db = SyncMCPClient()
risk_db = RiskRulesDBSyncClient()
decision_db = DecisionSynthesisSyncClient()

# 2. Get applicant data from Application DB
applicant = app_db.get_applicant_profile("APP001")['data']
app_analysis = app_db.get_complete_applicant_analysis("APP001")

# 3. Evaluate financial risk with RiskRulesDB
risk_assessment = risk_db.generate_risk_report(
    "APP001",
    applicant,
    {"loan_amount": 300000, "property_value": 500000}
)

# 4. Synthesize decision with DecisionSynthesis
decision = decision_db.synthesize_loan_decision(
    "APP001",
    applicant,
    app_analysis['analysis'],
    risk_assessment,
    strategy="Balanced"
)

# 5. Use the decision
classification = decision['decision']['classification']
risk_score = decision['decision']['risk_score']
confidence = decision['decision']['confidence_level']

print(f"Decision: {classification}")
print(f"Risk: {risk_score}/5")
print(f"Confidence: {confidence}")
```

---

## ✨ Output Structure

Every decision includes:

```
decision['decision']
├─ classification: APPROVE | CONDITIONAL_APPROVE | REVIEW | REJECT
├─ risk_score: 0-5
├─ confidence_level: Very High | High | Moderate | Low | Very Low
├─ reasoning: Detailed explanation
└─ conditions: [str] (only for CONDITIONAL_APPROVE)

decision['key_factors']
├─ category: Income Stability, Employment Risk, etc.
├─ value: The actual metric value
├─ impact: Positive, Concern, Major Concern
└─ description: Human-readable description

decision['audit_trail']
├─ decision_timestamp: ISO format
├─ strategy_used: Conservative | Balanced | Aggressive
├─ metrics_evaluated: {...}
├─ aggregate_risk_score: 0-5
├─ application_complete: boolean
└─ fair_lending_compliant: boolean
```

---

## 🔌 Integration Examples

### With LangChain
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

model = ChatAnthropic()
decision = client.synthesize_loan_decision(...)

response = model.invoke([
    HumanMessage(content=f"""
    Loan Decision: {decision['decision']['classification']}
    Risk: {decision['decision']['risk_score']}/5
    
    What are the next steps?
    """)
])
```

### With FastAPI
```python
from fastapi import FastAPI

app = FastAPI()
client = DecisionSynthesisSyncClient()

@app.post("/decide")
async def decide(applicant_id: str, ...):
    return client.synthesize_loan_decision(...)
```

### With LangGraph
```python
def decision_node(state):
    decision = client.synthesize_loan_decision(
        state['applicant_id'],
        state['applicant_data'],
        state['application_analysis'],
        state['risk_assessment']
    )
    state['decision'] = decision
    return state
```

---

## 📊 Decision by Risk Score

| Risk Score | Strategy | Typical Decision |
|---|---|---|
| 0.0-1.5 | All | ✅ APPROVE |
| 1.5-2.5 | Conservative | ✅ CONDITIONAL |
| 1.5-2.5 | Balanced/Aggressive | ✅ APPROVE |
| 2.5-3.0 | Conservative | ⚠️ REVIEW |
| 2.5-3.0 | Balanced | ✅ CONDITIONAL |
| 2.5-3.0 | Aggressive | ✅ APPROVE |
| 3.0-3.5 | Conservative/Balanced | ⚠️ REVIEW |
| 3.0-3.5 | Aggressive | ✅ CONDITIONAL |
| 3.5-4.5 | Conservative | ❌ REJECT |
| 3.5-4.5 | Balanced/Aggressive | ⚠️ REVIEW |
| 4.5+ | All | ❌ REJECT |

---

## 🆘 Troubleshooting

**Connection refused?**
```bash
python mcp/decisionsynthesis/server.py
```

**Timeout?**
```python
client = DecisionSynthesisSyncClient(timeout=60)
```

**Invalid strategy?**
Use: "Conservative", "Balanced", or "Aggressive"

**Missing metrics?**
Ensure all required fields in applicant_data, application_analysis, and risk_assessment

---

## 📞 Support

- **Full Documentation**: `DECISIONSYNTHESIS_IMPLEMENTATION.md`
- **Examples**: `examples/decisionsynthesis_demo.py`
- **Source**: `mcp/decisionsynthesis/server.py`
- **Client**: `mcp/decisionsynthesis/client.py`

---

## 🎯 Key Strengths

✅ Combines multiple data sources intelligently
✅ Flexible strategies for different risk appetites
✅ Explainable decisions with full reasoning
✅ Confidence scoring shows decision quality
✅ Audit trails for compliance
✅ Scenario analysis for testing alternatives
✅ Production-grade implementation
✅ Easy integration with agents

---

## 🚀 Next Steps

1. Start server: `python mcp/decisionsynthesis/server.py`
2. Run demo: `python examples/decisionsynthesis_demo.py`
3. Use in your agents/services
4. Combine with Application DB + RiskRulesDB
5. Deploy to production with FastAPI or LangGraph
