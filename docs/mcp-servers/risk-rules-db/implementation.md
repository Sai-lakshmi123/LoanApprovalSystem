# RiskRulesDB - Financial Risk Evaluation Engine

## 📋 Overview

**RiskRulesDB** is a comprehensive FastMCP server that evaluates financial risk for loan applications. It provides advanced analytics including:

- **Debt-to-Income (DTI) Ratio Analysis** - Monthly debt vs. income evaluation
- **Credit Score Risk Assessment** - Adjusted for delinquencies and inquiries
- **Loan Amount Risk Evaluation** - LTI, LTV, and debt burden analysis
- **Anomaly Detection** - Identifies unusual patterns and risk flags
- **Scenario Analysis** - Tests different loan amounts and conditions
- **Comprehensive Risk Reports** - Integrates all metrics into actionable insights

---

## 🎯 Key Features

✅ **6 Risk Evaluation Tools**
✅ **5 Reference Resources**
✅ **Sophisticated Scoring Algorithms**
✅ **Anomaly Detection System**
✅ **Scenario Analysis Capability**
✅ **Production-Ready Error Handling**
✅ **Comprehensive Documentation**
✅ **Working Demonstrations**

---

## 🛠️ 6 Available Tools

### Tool 1: `evaluate_dti_ratio`
**Purpose**: Calculate and assess Debt-to-Income ratio
**Parameters**:
- `monthly_income`: Gross monthly income
- `monthly_debt`: Total monthly debt obligations

**Returns**:
```json
{
  "dti_ratio": 0.3500,
  "dti_percentage": 35.00,
  "risk_level": "Low",
  "category": "Good",
  "acceptable_for_conventional": true,
  "acceptable_for_fha": true,
  "reasoning": "DTI of 35.0% indicates good debt levels..."
}
```

**DTI Thresholds**:
- < 20%: Very Low Risk (Excellent)
- 20-36%: Low Risk (Good)
- 36-43%: Medium Risk (Acceptable)
- 43-50%: High Risk
- > 50%: Very High Risk

---

### Tool 2: `evaluate_credit_risk`
**Purpose**: Assess credit score risk with adjustments
**Parameters**:
- `credit_score`: Credit score (300-850)
- `delinquencies`: Number of delinquencies (default: 0)
- `inquiries_last_6_months`: Recent inquiries (default: 0)

**Returns**:
```json
{
  "credit_score": 750,
  "base_risk_level": "Very Low",
  "base_risk_score": 5,
  "adjusted_risk_score": 15,
  "final_risk_level": "Low",
  "category": "Excellent",
  "reasoning": "Credit score of 750 adjusted for delinquencies and inquiries..."
}
```

**Credit Categories**:
- 750-850: Excellent (Very Low Risk)
- 700-749: Good (Low Risk)
- 650-699: Fair (Medium Risk)
- 600-649: Poor (High Risk)
- < 600: Very Poor (Very High Risk)

---

### Tool 3: `evaluate_loan_amount_risk`
**Purpose**: Assess risk based on loan size relative to income/property
**Parameters**:
- `loan_amount`: Requested loan amount
- `annual_income`: Applicant's annual income
- `property_value`: Property value (optional, for LTV)
- `existing_loans`: Number of existing loans
- `credit_score`: Applicant's credit score

**Returns**:
```json
{
  "loan_amount": 300000,
  "annual_income": 150000,
  "lti_percentage": 2.0,
  "lti_risk": "Very Low",
  "ltv_percentage": 75.0,
  "ltv_risk": "Low",
  "overall_loan_risk": "Low",
  "reasoning": "Loan amount represents 2.0% of annual income..."
}
```

**Metrics**:
- **LTI (Loan-to-Income)**: Loan amount as % of annual income
- **LTV (Loan-to-Value)**: Loan amount as % of property value
- **Debt Burden**: Impact of existing loans

---

### Tool 4: `detect_risk_anomalies`
**Purpose**: Identify unusual patterns and risk flags
**Parameters**:
- `applicant_data`: Full applicant profile
- `loan_request`: Loan request details

**Anomaly Types**:
- High DTI (> 50%)
- Low Credit Score (< 620)
- Recent Delinquency
- Excessive Credit Inquiries (> 5 in 6 months)
- High Credit Utilization (> 80%)
- Unusual Loan Request (LTI > 10%)
- Short Employment Tenure (< 6 months)
- Age-Employment Mismatch

**Returns**:
```json
{
  "has_anomalies": true,
  "anomaly_count": 3,
  "anomalies": [
    {
      "type": "High DTI",
      "severity": "High",
      "score": 80,
      "description": "..."
    }
  ],
  "overall_anomaly_score": 65.0,
  "overall_anomaly_risk_level": "High"
}
```

---

### Tool 5: `generate_risk_report` ⭐ (Most Useful)
**Purpose**: Generate comprehensive financial risk assessment
**Parameters**:
- `applicant_id`: Unique applicant identifier
- `applicant_data`: Full applicant profile
- `loan_request`: Loan request details

**Returns**:
Complete report including:
- DTI analysis (current and with new loan)
- Credit score risk assessment
- Loan amount risk evaluation
- Anomaly detection results
- Overall risk level and score
- Approval recommendation
- Detailed reasoning

---

### Tool 6: `evaluate_with_scenario_analysis`
**Purpose**: Test multiple loan amounts and conditions
**Parameters**:
- `applicant_id`: Unique applicant identifier
- `applicant_data`: Applicant profile
- `loan_request`: Base loan request
- `scenarios`: Alternative scenarios (optional)

**Returns**:
```json
{
  "base_scenario": { /* full risk report */ },
  "alternative_scenarios": [
    {
      "scenario": "Conservative (80%)",
      "loan_amount": 200000,
      "risk_level": "Medium",
      "dti_percentage": 35.5
    }
  ]
}
```

---

## 📚 5 Reference Resources

### Resource 1: `risk://dti/guidelines`
DTI thresholds and guidelines by risk category

### Resource 2: `risk://credit/assessment_criteria`
Credit score assessment with default probabilities

### Resource 3: `risk://loan/risk_assessment`
Loan-to-Income and Loan-to-Value guidelines

### Resource 4: `risk://anomalies/detection_rules`
Anomaly types and detection criteria

### Resource 5: `risk://regulatory/compliance`
Fair lending and regulatory requirements

---

## 🚀 Quick Start

### 1. Start the Server
```bash
python mcp/riskrulesdb/server.py
```

### 2. Run the Demo
```bash
python examples/riskrulesdb_demo.py
```

### 3. Use in Code
```python
from mcp.riskrulesdb.client import RiskRulesDBSyncClient

client = RiskRulesDBSyncClient()

# Generate comprehensive risk report
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
        "loan_term_months": 360,
        "property_value": 500000
    }
)

# Access results
dti = report['dti_with_new_loan']['dti_percentage']
credit_risk = report['credit_score_risk']['final_risk_level']
loan_risk = report['loan_amount_risk']['overall_loan_risk']
overall_risk = report['overall_risk_assessment']['overall_risk_level']
recommendation = report['overall_risk_assessment']['approval_recommendation']

print(f"DTI: {dti:.2f}%")
print(f"Credit Risk: {credit_risk}")
print(f"Loan Risk: {loan_risk}")
print(f"Overall Risk: {overall_risk}")
print(f"Recommendation: {recommendation}")
```

---

## 💡 Usage Examples

### Example 1: Evaluate DTI Ratio
```python
client = RiskRulesDBSyncClient()

# Monthly: $5000 income, $1500 debt
result = client.evaluate_dti_ratio(5000, 1500)
print(f"DTI: {result['analysis']['dti_percentage']:.2f}%")
print(f"Risk: {result['analysis']['risk_level']}")
```

### Example 2: Assess Credit Risk
```python
# Credit score 700, 1 delinquency, 2 recent inquiries
result = client.evaluate_credit_risk(700, 1, 2)
print(f"Risk: {result['analysis']['final_risk_level']}")
print(f"Score: {result['analysis']['adjusted_risk_score']}/100")
```

### Example 3: Evaluate Loan Amount
```python
# $300k loan, $100k income, $400k property, 1 existing loan
result = client.evaluate_loan_amount_risk(
    300000, 100000, 400000, 1, 700
)
print(f"LTI: {result['analysis']['lti_percentage']:.2f}%")
print(f"LTV: {result['analysis']['ltv_percentage']:.2f}%")
print(f"Risk: {result['analysis']['overall_loan_risk']}")
```

### Example 4: Detect Anomalies
```python
applicant = {
    "credit_score": 600,
    "delinquencies": 2,
    "inquiries_last_6_months": 6,
    "credit_utilization": 0.95,
    "annual_income": 50000,
}

loan = {
    "loan_amount": 400000,
}

result = client.detect_risk_anomalies(applicant, loan)
print(f"Anomalies: {result['analysis']['anomaly_count']}")
for anomaly in result['analysis']['anomalies']:
    print(f"  • {anomaly['type']}: {anomaly['description']}")
```

### Example 5: Generate Full Report
```python
report = client.generate_risk_report(
    "APP_TEST",
    applicant_data,
    loan_request
)

# Extract key metrics
dti = report['dti_with_new_loan']['dti_percentage']
credit_risk = report['credit_score_risk']['final_risk_level']
anomalies = report['anomaly_detection']['anomaly_count']
overall_risk = report['overall_risk_assessment']['overall_risk_level']
recommendation = report['overall_risk_assessment']['approval_recommendation']

print(f"DTI: {dti:.2f}%")
print(f"Credit Risk: {credit_risk}")
print(f"Anomalies: {anomalies}")
print(f"Overall Risk: {overall_risk}")
print(f"Recommendation: {recommendation}")
```

### Example 6: Scenario Analysis
```python
scenarios = [
    {"name": "Conservative (250k)", "loan_amount": 250000},
    {"name": "Moderate (300k)", "loan_amount": 300000},
    {"name": "Aggressive (350k)", "loan_amount": 350000},
]

result = client.evaluate_with_scenario_analysis(
    "APP_SCENARIOS",
    applicant,
    base_loan_request,
    scenarios
)

for scenario in result['alternative_scenarios']:
    print(f"{scenario['scenario']}: DTI {scenario['dti_percentage']:.1f}%, Risk {scenario['risk_level']}")
```

---

## 🔌 Integration Examples

### With LangChain Agents
```python
from mcp.riskrulesdb.client import RiskRulesDBSyncClient
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

client = RiskRulesDBSyncClient()
model = ChatAnthropic()

# Get risk analysis
report = client.generate_risk_report("APP001", applicant, loan_request)

# Use with Claude for intelligent decision
response = model.invoke([
    HumanMessage(content=f"""
    Based on this financial risk assessment:
    - DTI: {report['dti_with_new_loan']['dti_percentage']:.1f}%
    - Credit Risk: {report['credit_score_risk']['final_risk_level']}
    - Loan Risk: {report['loan_amount_risk']['overall_loan_risk']}
    - Anomalies: {report['anomaly_detection']['anomaly_count']}
    - Overall Risk: {report['overall_risk_assessment']['overall_risk_level']}
    
    Should we approve this loan? Provide detailed reasoning.
    """)
])

print(response.content)
```

### With FastAPI
```python
from fastapi import FastAPI, Depends
from mcp.riskrulesdb.client import RiskRulesDBSyncClient

app = FastAPI()

def get_risk_client():
    return RiskRulesDBSyncClient()

@app.post("/evaluate-risk")
async def evaluate_risk(
    applicant: dict,
    loan: dict,
    client = Depends(get_risk_client)
):
    """Evaluate loan application risk."""
    report = client.generate_risk_report("APP", applicant, loan)
    
    return {
        "overall_risk": report['overall_risk_assessment']['overall_risk_level'],
        "recommendation": report['overall_risk_assessment']['approval_recommendation'],
        "dti": report['dti_with_new_loan']['dti_percentage'],
        "credit_risk": report['credit_score_risk']['final_risk_level'],
        "loan_risk": report['loan_amount_risk']['overall_loan_risk'],
        "anomalies": report['anomaly_detection']['anomaly_count']
    }
```

### With LangGraph
```python
from langgraph.graph import StateGraph
from mcp.riskrulesdb.client import RiskRulesDBSyncClient

client = RiskRulesDBSyncClient()

def risk_evaluation_node(state):
    """Evaluate financial risk."""
    report = client.generate_risk_report(
        state['application_id'],
        state['applicant'],
        state['loan_request']
    )
    
    state['risk_report'] = report
    state['overall_risk'] = report['overall_risk_assessment']['overall_risk_level']
    
    return state

# Add to graph
graph = StateGraph(ApplicationState)
graph.add_node("risk_evaluation", risk_evaluation_node)
```

---

## 📊 Scoring Algorithms

### DTI Calculation
```
DTI Ratio = Total Monthly Debt / Gross Monthly Income
DTI Percentage = DTI Ratio * 100

Risk Levels:
- < 20%: Very Low
- 20-36%: Low
- 36-43%: Medium
- 43-50%: High
- > 50%: Very High
```

### Credit Risk Scoring
```
Base Risk Score = Determined by credit score
Delinquency Penalty = Delinquencies * 15 points
Inquiry Penalty = Inquiries * 3 points (capped at 25)

Adjusted Risk Score = Base + Delinquency Penalty + Inquiry Penalty
```

### Loan Amount Risk
```
LTI Percentage = (Loan Amount / Annual Income) * 100
LTV Percentage = (Loan Amount / Property Value) * 100

Overall Risk = Average of LTI Risk, LTV Risk, and Debt Burden Risk
```

### Anomaly Scoring
```
Each detected anomaly assigned score (30-100)
Overall Score = Average of all anomaly scores
```

---

## 📁 Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `mcp/riskrulesdb/server.py` | 700+ | Main MCP server with 6 tools, 5 resources |
| `mcp/riskrulesdb/client.py` | 300+ | Async/Sync clients |
| `mcp/riskrulesdb/__init__.py` | 10 | Package initialization |
| `examples/riskrulesdb_demo.py` | 600+ | 7 complete demonstrations |
| `RISKRULESDB_IMPLEMENTATION.md` | 500+ | This file |

**Total**: ~2,100 lines of code and documentation

---

## ✨ Key Differences from Application DB

| Feature | Application DB | RiskRulesDB |
|---------|---|---|
| **Focus** | Applicant data retrieval | Risk evaluation |
| **Tools** | 7 data fetching tools | 6 risk analysis tools |
| **Metrics** | Income, employment, credit | DTI, risk scores, anomalies |
| **Port** | 3000 | 3001 |
| **Use Case** | Gather applicant info | Assess financial risk |
| **Recommendation** | Use together for complete evaluation |

---

## 🎯 When to Use RiskRulesDB

✅ Use when you need to:
- Assess financial risk of loan applications
- Calculate DTI ratios and evaluate acceptability
- Assess credit score risk with adjustments
- Evaluate loan amount relative to income
- Detect unusual patterns and anomalies
- Generate risk-based approval recommendations
- Test scenarios with different loan amounts
- Ensure regulatory compliance

---

## 🚀 Running the System

### Start Both MCP Servers
```bash
# Terminal 1: Application DB
python mcp/server.py

# Terminal 2: RiskRulesDB (in another directory or port)
python mcp/riskrulesdb/server.py
```

### Run Demo
```bash
python examples/riskrulesdb_demo.py
```

### Use Together
```python
from mcp.clients.mcp_client import SyncMCPClient as AppDB
from mcp.riskrulesdb.client import RiskRulesDBSyncClient

app_db = AppDB()
risk_db = RiskRulesDBSyncClient()

# Get applicant info
applicant = app_db.get_applicant_profile("APP001")['data']

# Assess financial risk
risk_report = risk_db.generate_risk_report(
    "APP001",
    applicant,
    {"loan_amount": 300000, "property_value": 500000}
)

print(f"Profile: {applicant['name']}")
print(f"Stability: {applicant['years_at_current_job']} years")
print(f"Risk Level: {risk_report['overall_risk_assessment']['overall_risk_level']}")
print(f"Recommendation: {risk_report['overall_risk_assessment']['approval_recommendation']}")
```

---

## 📞 Troubleshooting

### Server Won't Start
```
Error: Address already in use
Solution: Change port in server.py or kill existing process
```

### Connection Refused
```
Error: Cannot connect to server
Solution: Make sure server is running and port is correct
```

### Tool Call Fails
```
Error: Tool not found
Solution: Check tool name and parameters match documentation
```

---

## 🎓 Next Steps

1. **Start the server**: `python mcp/riskrulesdb/server.py`
2. **Run the demo**: `python examples/riskrulesdb_demo.py`
3. **Integrate with agents**: See integration examples above
4. **Add to FastAPI**: Use in approval decision endpoints
5. **Deploy**: Docker/Kubernetes ready

---

## 📝 Summary

**RiskRulesDB** provides enterprise-grade financial risk evaluation with:

✅ 6 comprehensive risk analysis tools
✅ 5 reference resources for compliance
✅ Sophisticated anomaly detection
✅ Scenario analysis capability
✅ Complete integration support
✅ Production-ready code
✅ Comprehensive documentation
✅ Working examples

Perfect for intelligent loan approval systems that need to assess financial risk accurately and comprehensively!

