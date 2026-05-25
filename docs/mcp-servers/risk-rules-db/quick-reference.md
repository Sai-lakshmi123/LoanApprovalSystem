# RiskRulesDB - Quick Reference

## 🚀 30-Second Setup

```bash
# Start server
python mcp/riskrulesdb/server.py

# Run demo (in another terminal)
python examples/riskrulesdb_demo.py

# Use in code
from mcp.riskrulesdb.client import RiskRulesDBSyncClient
client = RiskRulesDBSyncClient()
report = client.generate_risk_report("APP001", applicant, loan_request)
```

---

## 📊 What RiskRulesDB Does

Evaluates **financial risk** for loan applications by analyzing:

1. **DTI Ratio** (Debt-to-Income)
2. **Credit Score Risk** (with adjustments)
3. **Loan Amount Risk** (LTI, LTV ratios)
4. **Anomaly Detection** (unusual patterns)
5. **Scenario Analysis** (alternative loan amounts)
6. **Comprehensive Reports** (all metrics combined)

---

## 🛠️ 6 Tools Available

| Tool | What It Does |
|------|------------|
| `evaluate_dti_ratio()` | Calculate monthly debt vs. income |
| `evaluate_credit_risk()` | Assess credit score with adjustments |
| `evaluate_loan_amount_risk()` | Evaluate loan size vs. income/property |
| `detect_risk_anomalies()` | Find unusual patterns/red flags |
| `generate_risk_report()` | ⭐ Get everything in one report |
| `evaluate_with_scenario_analysis()` | Test different loan amounts |

---

## 💡 Basic Examples

### Get Full Risk Assessment
```python
from mcp.riskrulesdb.client import RiskRulesDBSyncClient

client = RiskRulesDBSyncClient()

report = client.generate_risk_report(
    "APP001",
    {
        "annual_income": 100000,
        "monthly_expenses": 3000,
        "existing_monthly_debt": 1000,
        "credit_score": 750,
        "delinquencies": 0,
        "inquiries_last_6_months": 1,
        "credit_utilization": 0.35,
        "years_at_current_job": 5,
        "existing_loans": 1
    },
    {
        "loan_amount": 300000,
        "property_value": 500000
    }
)

# Key results
print(f"DTI: {report['dti_with_new_loan']['dti_percentage']:.1f}%")
print(f"Overall Risk: {report['overall_risk_assessment']['overall_risk_level']}")
print(f"Recommendation: {report['overall_risk_assessment']['approval_recommendation']}")
```

### Just Check DTI
```python
result = client.evaluate_dti_ratio(5000, 1500)
print(f"DTI: {result['analysis']['dti_percentage']:.1f}%")
print(f"Risk: {result['analysis']['risk_level']}")
```

### Just Check Credit Risk
```python
result = client.evaluate_credit_risk(750, 0, 1)
print(f"Risk Level: {result['analysis']['final_risk_level']}")
print(f"Risk Score: {result['analysis']['adjusted_risk_score']}/100")
```

### Detect Anomalies
```python
result = client.detect_risk_anomalies(applicant, loan)
print(f"Anomalies Found: {result['analysis']['anomaly_count']}")
for anomaly in result['analysis']['anomalies']:
    print(f"  • {anomaly['type']}")
```

### Test Different Loan Amounts
```python
scenarios = [
    {"name": "250k", "loan_amount": 250000},
    {"name": "300k", "loan_amount": 300000},
    {"name": "350k", "loan_amount": 350000},
]

result = client.evaluate_with_scenario_analysis(
    "APP001", applicant, base_loan, scenarios
)

for scenario in result['alternative_scenarios']:
    print(f"{scenario['scenario']}: DTI {scenario['dti_percentage']:.1f}%")
```

---

## 📈 Risk Levels

### DTI Thresholds
- **< 20%** → Very Low Risk ✅
- **20-36%** → Low Risk ✅
- **36-43%** → Medium Risk ⚠️
- **43-50%** → High Risk ❌
- **> 50%** → Very High Risk ❌❌

### Credit Score Categories
- **750-850** → Excellent (Very Low Risk) ✅
- **700-749** → Good (Low Risk) ✅
- **650-699** → Fair (Medium Risk) ⚠️
- **600-649** → Poor (High Risk) ❌
- **< 600** → Very Poor (Very High Risk) ❌❌

### Loan-to-Income (LTI)
- **< 3%** → Very Low Risk ✅
- **3-5%** → Low Risk ✅
- **5-8%** → Medium Risk ⚠️
- **8-12%** → High Risk ❌
- **> 12%** → Very High Risk ❌

---

## 🔴 Anomalies Detected

🚩 Critical:
- High DTI (> 50%)
- Recent delinquency (< 6 months)

⚠️ High:
- Low credit score (< 620)
- Unusual loan request (LTI > 10%)

🟡 Medium:
- Excessive inquiries (> 5 in 6 months)
- High credit utilization (> 80%)
- Short employment tenure (< 6 months)

---

## 📚 Access Reference Rules

```python
client = RiskRulesDBSyncClient()

# Get guidelines
dti_rules = client.get_dti_guidelines()
credit_rules = client.get_credit_assessment_criteria()
loan_rules = client.get_loan_risk_criteria()
anomaly_rules = client.get_anomaly_rules()
compliance_rules = client.get_regulatory_rules()
```

---

## 🔄 Integration

### With Application DB
```python
from mcp.clients.mcp_client import SyncMCPClient as AppDB
from mcp.riskrulesdb.client import RiskRulesDBSyncClient

app_db = AppDB()
risk_db = RiskRulesDBSyncClient()

# Get applicant info
applicant = app_db.get_applicant_profile("APP001")['data']

# Assess risk
risk = risk_db.generate_risk_report("APP001", applicant, loan)
```

### With LangChain Agents
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

client = RiskRulesDBSyncClient()
model = ChatAnthropic()

report = client.generate_risk_report("APP001", applicant, loan)

response = model.invoke([
    HumanMessage(content=f"""
    Risk assessment:
    - DTI: {report['dti_with_new_loan']['dti_percentage']:.1f}%
    - Overall Risk: {report['overall_risk_assessment']['overall_risk_level']}
    
    Approve or reject?
    """)
])
```

### With FastAPI
```python
from fastapi import FastAPI

app = FastAPI()
client = RiskRulesDBSyncClient()

@app.post("/approve-loan")
async def approve_loan(applicant: dict, loan: dict):
    report = client.generate_risk_report("APP", applicant, loan)
    return {
        "recommendation": report['overall_risk_assessment']['approval_recommendation'],
        "risk_level": report['overall_risk_assessment']['overall_risk_level'],
        "dti": report['dti_with_new_loan']['dti_percentage']
    }
```

---

## 📋 Report Contents

Full report includes:

```
✅ DTI Analysis (current & with new loan)
✅ Credit Score Risk (with adjustments)
✅ Loan Amount Risk (LTI, LTV)
✅ Anomaly Detection (count & types)
✅ Overall Risk Level & Score
✅ Approval Recommendation
✅ Detailed Reasoning
✅ Summary Statement
```

---

## 🎯 Recommendations

| Overall Risk | Recommendation |
|---|---|
| Very Low | ✅ APPROVE |
| Low | ✅ APPROVE (with conditions) |
| Medium | ⚠️ CONDITIONAL (manual review) |
| High | ❌ REVIEW (higher scrutiny) |
| Very High | ❌ DECLINE |

---

## 🔧 Configuration

### Change Server Port
Edit `mcp/riskrulesdb/server.py`:
```python
uvicorn.run("mcp.riskrulesdb.server:app", port=3002)
```

### Change Client URL
```python
client = RiskRulesDBSyncClient(base_url="http://localhost:3002")
```

---

## 🆘 Troubleshooting

**Connection refused?**
```bash
python mcp/riskrulesdb/server.py
```

**Tool not found?**
Check tool name matches exactly

**Timeout?**
```python
client.timeout = 60
```

---

## 📊 Quick Metrics

| Metric | Excellent | Good | Fair | Poor | Very Poor |
|--------|---|---|---|---|---|
| DTI | < 20% | 20-36% | 36-43% | 43-50% | > 50% |
| Credit | 750+ | 700-749 | 650-699 | 600-649 | < 600 |
| LTI | < 3% | 3-5% | 5-8% | 8-12% | > 12% |

---

## ✨ Key Strengths

✅ Comprehensive risk evaluation
✅ Anomaly detection catches red flags
✅ Scenario analysis tests limits
✅ Easy integration with agents
✅ Regulatory compliance ready
✅ Production-grade quality
✅ Well-documented

---

## 🎓 Next Steps

1. Start server: `python mcp/riskrulesdb/server.py`
2. Run demo: `python examples/riskrulesdb_demo.py`
3. Use in your agents/services
4. Combine with Application DB
5. Deploy to production

---

## 📞 Support

- **Documentation**: `RISKRULESDB_IMPLEMENTATION.md`
- **Examples**: `examples/riskrulesdb_demo.py`
- **Source**: `mcp/riskrulesdb/server.py`

