# Financial Risk Analysis Agent (Agent2) - Quick Reference

## 🚀 30-Second Setup

```bash
# 1. Make sure RiskRulesDB server is running (separate terminal)
python mcp/riskrulesdb/server.py

# 2. Run Agent2
python agents/financial_risk_analysis_agent.py
```

---

## 📊 What Agent2 Does

Agent2 is an intelligent financial risk analyst powered by Claude Sonnet 4.6. It:
- Connects to RiskRulesDB MCP Server
- Analyzes loan financial risk comprehensively
- Returns structured analysis with all risk metrics
- Provides risk-based recommendations

**LLM Model:** Claude Sonnet 4.6 (claude-sonnet-4-6-20250514)
**Framework:** Anthropic Agent SDK
**Port:** Connects to RiskRulesDB on port 3001

---

## 📋 Structured Output

Agent2 returns analysis with these exact fields:

```json
{
    "applicant_id": "APP001",
    "analysis_timestamp": "2026-05-24T10:30:00",
    "dti_analysis": {
        "current_dti_percentage": 24.0,
        "dti_with_new_loan_percentage": 35.5,
        "dti_risk_level": "Low",
        "analysis": "..."
    },
    "credit_risk": {
        "credit_score": 760,
        "base_risk_level": "Excellent",
        "adjusted_risk_level": "Excellent",
        "delinquencies": 0,
        "inquiry_count": 1,
        "analysis": "..."
    },
    "loan_amount_risk": {
        "loan_amount": 300000,
        "annual_income": 150000,
        "property_value": 500000,
        "lti_percentage": 2.0,
        "ltv_percentage": 60.0,
        "overall_loan_risk": "Very Low",
        "analysis": "..."
    },
    "anomaly_detection": {
        "anomaly_count": 0,
        "has_critical_anomalies": false,
        "anomalies": [],
        "overall_anomaly_score": 0,
        "analysis": "..."
    },
    "aggregate_risk_assessment": {
        "overall_risk_score": 1.8,
        "overall_risk_level": "Very Low",
        "primary_risk_factors": [],
        "mitigating_factors": ["Strong income", "Low DTI", "Excellent credit"],
        "recommendation": "APPROVE"
    },
    "financial_summary": "...",
    "key_findings": [...],
    "recommended_conditions": [],
    "next_steps": [...]
}
```

---

## 🛠️ 6 Tools Agent Has Access To

| Tool | Purpose |
|------|---------|
| `evaluate_dti_ratio` | Calculate debt-to-income ratio with risk level |
| `evaluate_credit_risk` | Assess credit risk with adjustments |
| `evaluate_loan_amount_risk` | Evaluate LTI and LTV ratios |
| `detect_risk_anomalies` | Identify unusual patterns and red flags |
| `generate_risk_report` | Get comprehensive financial risk report |
| `evaluate_with_scenario_analysis` | Test different loan amount scenarios |

---

## 💡 Basic Examples

### Get Financial Risk Analysis

```python
from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent

agent = FinancialRiskAnalysisAgent()

result = agent.analyze_financial_risk(
    applicant_id="APP001",
    applicant_data={
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
    loan_request={
        "loan_amount": 300000,
        "property_value": 500000,
        "loan_term_months": 360
    }
)

# Use the analysis
if result["status"] == "success":
    analysis = result["analysis"]
    print(f"DTI Risk: {analysis['dti_analysis']['dti_risk_level']}")
    print(f"Credit Risk: {analysis['credit_risk']['adjusted_risk_level']}")
    print(f"Loan Risk: {analysis['loan_amount_risk']['overall_loan_risk']}")
    print(f"Overall Risk Score: {analysis['aggregate_risk_assessment']['overall_risk_score']}/5")
    print(f"Recommendation: {analysis['aggregate_risk_assessment']['recommendation']}")
```

### Extract Risk Metrics

```python
analysis = result["analysis"]

# Extract specific values
dti = analysis["dti_analysis"]["dti_with_new_loan_percentage"]
credit = analysis["credit_risk"]["credit_score"]
lti = analysis["loan_amount_risk"]["lti_percentage"]
ltv = analysis["loan_amount_risk"]["ltv_percentage"]
anomalies = analysis["anomaly_detection"]["anomaly_count"]
risk_score = analysis["aggregate_risk_assessment"]["overall_risk_score"]

print(f"DTI: {dti}%")
print(f"Credit: {credit}")
print(f"LTI: {lti}%")
print(f"LTV: {ltv}%")
print(f"Anomalies: {anomalies}")
print(f"Risk Score: {risk_score}/5")
```

### Access Key Findings

```python
analysis = result["analysis"]

print("Key Findings:")
for finding in analysis["key_findings"]:
    print(f"  • {finding}")

print("\nRecommended Conditions:")
for condition in analysis["recommended_conditions"]:
    print(f"  • {condition}")

print("\nNext Steps:")
for step in analysis["next_steps"]:
    print(f"  • {step}")
```

---

## 📈 Risk Level Thresholds

### DTI (Debt-to-Income) Ratio

| DTI Range | Risk Level | Action |
|---|---|---|
| < 20% | Very Low | ✅ APPROVE |
| 20-36% | Low | ✅ APPROVE |
| 36-43% | Medium | ⚠️ CONDITIONAL |
| 43-50% | High | ❌ REVIEW |
| > 50% | Very High | ❌ DECLINE |

### Credit Score Risk

| Score | Category | Risk Level |
|---|---|---|
| 750+ | Excellent | Very Low |
| 700-749 | Good | Low |
| 650-699 | Fair | Medium |
| 600-649 | Poor | High |
| < 600 | Very Poor | Very High |

### Loan-to-Income (LTI)

| LTI % | Risk Level |
|---|---|
| < 3% | Very Low ✅ |
| 3-5% | Low ✅ |
| 5-8% | Medium ⚠️ |
| 8-12% | High ❌ |
| > 12% | Very High ❌ |

### Loan-to-Value (LTV)

| LTV % | Risk Level |
|---|---|
| < 60% | Excellent ✅ |
| 60-80% | Good ✅ |
| 80-95% | Acceptable ⚠️ |
| > 95% | High Risk ❌ |

### Aggregate Risk Score

| Score | Level | Action |
|---|---|---|
| 0-1.5 | Very Low | ✅ APPROVE |
| 1.5-2.5 | Low | ✅ CONDITIONAL |
| 2.5-3.5 | Medium | ⚠️ REVIEW |
| 3.5-4.5 | High | ❌ UNDERWRITING |
| 4.5-5 | Very High | ❌ DECLINE |

---

## 🔴 9 Anomalies Detected

| Type | Severity | Trigger |
|---|---|---|
| High DTI | Critical | DTI > 50% |
| Recent Delinquency | Critical | < 6 months ago |
| Low Credit Score | High | < 620 |
| Unusual Loan Request | High | LTI > 10% |
| Excessive Inquiries | Medium | > 5 in 6 months |
| High Utilization | Medium | > 80% |
| Short Employment | Medium | < 6 months |
| Income Inconsistency | Low | Variable income |
| Age-Employment Mismatch | Low | Unusual pattern |

---

## 🔧 Configuration

### Change Server Port
Edit `agents/financial_risk_analysis_agent.py`:
```python
self.risk_db = RiskRulesDBClient(
    base_url="http://localhost:3002"  # Different port
)
```

### Change Client URL
```python
agent.risk_db = RiskRulesDBClient(
    base_url="http://localhost:3002"
)
```

### Change Timeout
```python
agent.risk_db = RiskRulesDBClient(timeout=60)
```

---

## 📊 Decision by Risk Score

| Risk Score | Typical Decision |
|---|---|
| 0.0-1.5 | ✅ APPROVE |
| 1.5-2.5 | ✅ CONDITIONAL APPROVE |
| 2.5-3.5 | ⚠️ MANUAL REVIEW |
| 3.5-4.5 | ❌ UNDERWRITING REQUIRED |
| 4.5-5.0 | ❌ DECLINE |

---

## 🔌 Integration with Other Agents

Agent2 provides risk analysis for downstream agents:

```
Agent1 (Application Profile)
    ↓ (Income, Employment, Credit, Completeness)
Agent2 (Financial Risk Analysis) ← YOU ARE HERE
    ↓ (DTI, Credit Risk, Loan Risk, Anomalies, Risk Score)
Agent3 (Decision Synthesis)
    ↓ (APPROVE/REJECT/CONDITIONAL/REVIEW)
Agent4 (Notification)
```

---

## 🆘 Troubleshooting

**Connection refused?**
```bash
python mcp/riskrulesdb/server.py
```

**Timeout?**
```python
agent.risk_db = RiskRulesDBClient(timeout=60)
```

**Tool not found?**
Ensure RiskRulesDB has all 6 tools available

**Missing applicant data?**
Ensure all required fields in applicant_data dict

---

## 📞 Support

- **Full Documentation**: `agents/AGENT2_IMPLEMENTATION.md`
- **Examples**: `examples/agent2_usage_example.py`
- **Source**: `agents/financial_risk_analysis_agent.py`
- **README**: `agents/README_AGENT2.md`

---

## 🎯 Key Strengths

✅ Claude Sonnet 4.6 intelligent analysis
✅ Comprehensive risk assessment across 4 dimensions
✅ 9 different anomaly types detected
✅ Aggregate risk scoring (0-5 scale)
✅ Scenario analysis capability
✅ Production-grade implementation
✅ Fair lending compliance built-in
✅ Detailed reasoning for all assessments

---

## 🚀 Next Steps

1. Start server: `python mcp/riskrulesdb/server.py`
2. Run agent: `python agents/financial_risk_analysis_agent.py`
3. Use in your systems
4. Integrate with Agent1 output
5. Pass to Agent3 for decisions
