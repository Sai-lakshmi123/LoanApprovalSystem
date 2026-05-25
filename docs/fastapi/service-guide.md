# FastAPI Loan Evaluation Microservice

A production-ready FastAPI microservice that evaluates loan applications using a multi-agent orchestration system with intelligent routing, error handling, and comprehensive decision reporting.

## 🎯 Overview

This microservice provides a REST API endpoint that:
- ✅ Accepts loan application data with comprehensive validation
- ✅ Processes applications through 4 specialized agents (Profile, Risk, Decision, Compliance)
- ✅ Implements intelligent decision routing based on risk scores
- ✅ Handles errors with automatic retry logic and fallback decisions
- ✅ Returns structured decisions with detailed reasoning and next steps
- ✅ Tracks all applications with case IDs for auditing

**Tech Stack:**
- FastAPI (async REST framework)
- Pydantic (data validation)
- LangGraph (orchestration engine)
- Claude Sonnet 4.6 (LLM)
- MCP (Tool Protocol)

---

## 📦 Project Structure

```
src/api/
├── main.py                          # FastAPI application with all endpoints
└── requirements.txt                 # FastAPI dependencies

examples/
├── api_test_loan_evaluation.py      # Comprehensive test suite
└── curl_tests.sh                    # cURL test scripts

orchestration/
└── orchestration_engine.py          # LangGraph workflow engine

mcp/                                  # MCP servers for agent tools
├── server.py
├── riskrulesdb/
├── decisionsynthesis/
└── notificationsystem/

API_QUICKSTART.md                    # Quick start guide (5 minutes)
API_DOCUMENTATION.md                 # Complete API reference
FASTAPI_SERVICE_README.md            # This file
ERROR_HANDLING_GUIDE.md              # Error handling & retry logic
```

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

```bash
# Ensure Python 3.8+ and pip are installed
python3 --version
pip3 --version
```

### Step 1: Install Dependencies

```bash
cd /path/to/LoanApprovalSystem

# Install all requirements
pip install fastapi uvicorn pydantic httpx python-dotenv langgraph langchain
```

### Step 2: Start All Services (5 Terminals)

**Terminal 1: MCP Application Server**
```bash
python mcp/server.py
```

**Terminal 2: MCP Risk Rules Database**
```bash
python mcp/riskrulesdb/server.py
```

**Terminal 3: MCP Decision Synthesis**
```bash
python mcp/decisionsynthesis/server.py
```

**Terminal 4: MCP Notification System**
```bash
python mcp/notificationsystem/server.py
```

**Terminal 5: FastAPI Server**
```bash
python src/api/main.py
```

### Step 3: Test the API

**Option A: Interactive Swagger UI**
```
Open browser to: http://localhost:8000/docs
```

**Option B: cURL Command**
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST001",
    "age": 45,
    "annual_income": 200000,
    "employment_type": "employed",
    "credit_score": 780,
    "loan_amount": 300000,
    "tenure_months": 360,
    "existing_liabilities": 1000,
    "location": "CA"
  }'
```

**Option C: Run Full Test Suite**
```bash
python examples/api_test_loan_evaluation.py
```

---

## 📚 API Reference

### Endpoints

#### 1. Health Check
```http
GET /health
```
Returns API health status

#### 2. Evaluate Loan Application
```http
POST /evaluate-loan
```
Submits a loan application for evaluation

**Request:**
```json
{
  "applicant_id": "string (required)",
  "age": 35,
  "annual_income": 100000,
  "employment_type": "employed",
  "credit_score": 700,
  "loan_amount": 250000,
  "tenure_months": 360,
  "existing_liabilities": 1000,
  "location": "CA"
}
```

**Response:**
```json
{
  "success": true,
  "applicant_id": "string",
  "decision": {
    "classification": "APPROVE|REJECT|REVIEW",
    "risk_score": 1.8,
    "confidence_percentage": 85,
    "reasoning": "string"
  },
  "case_id": "CASE-...",
  "next_steps": ["string"],
  "processing_time_ms": 2500
}
```

#### 3. List Agents
```http
GET /agents
```
Returns available agents and their status

---

## 🔍 Request Validation

All inputs are validated according to business rules:

| Field | Type | Validation | Default |
|-------|------|-----------|---------|
| applicant_id | string | Required, non-empty | - |
| age | integer | 18-100 | - |
| annual_income | number | > 0 | - |
| employment_type | string | employed, self-employed, retired, student, unemployed | - |
| credit_score | integer | 300-850 | - |
| loan_amount | number | > 0 | - |
| tenure_months | integer | 12-360 | - |
| existing_liabilities | number | >= 0 | 0 |
| location | string | Min 2 chars | - |
| monthly_expenses | number | Optional | Auto-calculated |
| delinquencies | integer | >= 0 | 0 |
| inquiries_last_6_months | integer | >= 0 | 0 |
| credit_utilization | number | 0-1 | 0.5 |
| years_at_current_job | integer | >= 0 | 1 |
| existing_loans | integer | >= 0 | 0 |
| property_value | number | Optional | 1.5x loan_amount |
| email | string | Optional | Generated |
| phone | string | Optional | Generated |

---

## 🤖 Agent Pipeline

The system processes loans through 4 sequential agents:

```
┌─────────────────────────────────────────────────────────────┐
│                    LOAN EVALUATION PIPELINE                  │
└─────────────────────────────────────────────────────────────┘

INPUT: Loan Application
   │
   ▼
┌──────────────────────────────────────┐
│ AGENT 1: Profile Analysis            │
│ - Income stability score             │
│ - Employment risk assessment         │
│ - Credit history analysis            │
│ - Application completeness           │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│ AGENT 2: Financial Risk Analysis     │
│ - Debt-to-income ratio               │
│ - Credit score risk level            │
│ - Loan amount risk assessment        │
│ - Anomaly detection                  │
└──────────────────────────────────────┘
   │
   ▼
   ┌─────────────────────────────┐
   │ ROUTING DECISION            │
   │ Based on Risk Score:        │
   │ - Low (< 2.5): Auto-Approve │
   │ - Medium (2.5-3.5): Review  │
   │ - High (> 3.5): Escalate    │
   └─────────────────────────────┘
   │
   ├─────────────────────┬──────────────────────┬─────────────┐
   │                     │                      │             │
   ▼                     ▼                      ▼             ▼
 AUTO-              REVIEW PATH           ESCALATION      MANUAL
 APPROVE            (Agent 3)             (Agent 3)       REVIEW
   │                     │                      │             │
   ▼                     ▼                      ▼             ▼
┌──────────────────────────────────────┐
│ AGENT 3: Decision Synthesis          │
│ - Classification: APPROVE/REJECT/REVIEW
│ - Risk score & confidence            │
│ - Decision reasoning                 │
│ - Key decision factors               │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│ AGENT 4: Compliance & Orchestration  │
│ - Record decision                    │
│ - Generate case ID                   │
│ - Send notifications                 │
│ - Prepare next steps                 │
└──────────────────────────────────────┘
   │
   ▼
OUTPUT: Structured Decision with Case ID
```

---

## ⚠️ Error Handling

The system implements comprehensive error handling:

### Retry Logic
- **Transient Errors** (timeouts, connection issues): Automatic retry with exponential backoff
- **Permanent Errors** (invalid data, auth failures): Immediate escalation to manual review
- **Unknown Errors**: Retry with caution

### Fallback Decisions
When an agent fails:
- Creates REVIEW decision automatically
- Low confidence (20%)
- Escalates to senior underwriter
- Application never left without decision

See `ERROR_HANDLING_GUIDE.md` for complete documentation.

---

## 📊 Response Examples

### Example 1: Strong Applicant (Auto-Approve)
```json
{
  "success": true,
  "applicant_id": "STRONG001",
  "decision": {
    "classification": "APPROVE",
    "risk_score": 1.8,
    "confidence_percentage": 85,
    "confidence_level": "High",
    "reasoning": "Strong financial profile with excellent credit history and low risk indicators",
    "key_factors": [
      "Excellent credit score (780)",
      "Stable employment (10 years)",
      "Low debt-to-income ratio"
    ]
  },
  "risk_level": "Low",
  "next_steps": [
    "Prepare loan documents",
    "Schedule closing appointment",
    "Arrange final verification"
  ],
  "case_id": "CASE-STRONG001-1716633001",
  "workflow_status": "success",
  "processing_time_ms": 2500
}
```

### Example 2: High-Risk Applicant (Escalation)
```json
{
  "success": true,
  "applicant_id": "HIGHRISK001",
  "decision": {
    "classification": "REVIEW",
    "risk_score": 3.8,
    "confidence_percentage": 45,
    "confidence_level": "Medium",
    "reasoning": "High-risk profile requiring manual underwriter review"
  },
  "risk_level": "High",
  "next_steps": [
    "Escalate to senior underwriter",
    "Request additional documentation",
    "Contact applicant for verification"
  ],
  "case_id": "CASE-HIGHRISK001-1716633002",
  "workflow_status": "success",
  "processing_time_ms": 3200
}
```

---

## 🧪 Testing

### Run Full Test Suite
```bash
python examples/api_test_loan_evaluation.py
```

### Run cURL Tests
```bash
bash examples/curl_tests.sh
```

### Test Scenarios
- ✅ Strong applicant (auto-approve)
- ✅ High-risk applicant (escalation)
- ✅ Moderate applicant (review)
- ✅ Input validation
- ✅ Error handling

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| `API_QUICKSTART.md` | 5-minute setup guide |
| `API_DOCUMENTATION.md` | Complete API reference |
| `ERROR_HANDLING_GUIDE.md` | Error handling & retry logic |
| `ERROR_HANDLING_QUICKREF.md` | Quick reference for errors |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# API Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Logging
LOG_LEVEL=INFO

# MCP Server URLs (if different)
MCP_APP_URL=http://localhost:5001
MCP_RISK_URL=http://localhost:5002
MCP_DECISION_URL=http://localhost:5003
MCP_NOTIFICATION_URL=http://localhost:5004
```

### Retry Configuration

Modify in `orchestration/orchestration_engine.py`:

```python
RETRY_CONFIGS = {
    "agent1": RetryConfig(max_retries=3, base_delay=1.0, backoff_factor=2.0),
    "agent2": RetryConfig(max_retries=3, base_delay=2.0, backoff_factor=2.0),
    "agent3": RetryConfig(max_retries=2, base_delay=1.5, backoff_factor=2.0),
    "agent4": RetryConfig(max_retries=1, base_delay=1.0, backoff_factor=2.0),
}
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Install all dependencies: `pip install -r requirements.txt`
- [ ] Verify MCP servers are running and healthy
- [ ] Set appropriate logging level (INFO or WARNING)
- [ ] Configure environment variables
- [ ] Adjust retry configurations for your infrastructure
- [ ] Set up monitoring for retry metrics
- [ ] Configure alerting for high error rates
- [ ] Test with production-like data
- [ ] Document expected SLAs
- [ ] Plan for scalability

### Performance Considerations

- **Average Response Time:** 2-4 seconds
- **Range:** 1-15 seconds (depending on complexity)
- **Timeout:** 60 seconds
- **Concurrent Requests:** Limited by system resources

### Scaling

For high-volume deployments:
1. Run multiple FastAPI instances behind a load balancer
2. Use Gunicorn or uvicorn with multiple workers
3. Implement database connection pooling
4. Consider async database operations
5. Monitor queue depths and response times

---

## 🔐 Security

### Best Practices

- ✅ Input validation on all fields
- ✅ Error messages don't leak sensitive data
- ✅ CORS configured (customize for production)
- ✅ Rate limiting recommended (add to production)
- ✅ Authentication recommended (add to production)
- ✅ HTTPS required for production
- ✅ Audit logging for all decisions

### Production Security

Add to `src/api/main.py` for production:

```python
# Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Authentication
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.post("/evaluate-loan", dependencies=[Depends(security)])
async def evaluate_loan(request: LoanEvaluationRequest):
    ...
```

---

## 📊 Monitoring

### Key Metrics

- Total requests per minute
- Average response time
- Error rate
- Retry rate
- Fallback decision rate
- Decision distribution (APPROVE/REJECT/REVIEW)

### Logging

All requests and decisions are logged:

```python
logger.info(f"✅ Evaluation complete for {request.applicant_id}: {response.decision.classification}")
logger.error(f"❌ Error evaluating loan for {request.applicant_id}: {str(e)}")
```

---

## 🐛 Troubleshooting

### Connection Refused
**Problem:** Cannot connect to API
**Solution:** Ensure API is running: `python src/api/main.py`

### MCP Servers Not Available
**Problem:** API cannot reach MCP servers
**Solution:** Start all 4 MCP servers

### Slow Response Times
**Problem:** Response takes > 10 seconds
**Solution:** Check MCP server performance and system resources

### Validation Errors
**Problem:** 422 status code
**Solution:** Check field types and values against documentation

---

## 📚 Related Documentation

- [ERROR_HANDLING_GUIDE.md](ERROR_HANDLING_GUIDE.md) - Comprehensive error handling documentation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- [API_QUICKSTART.md](API_QUICKSTART.md) - Quick start guide
- [AGENT3_SUMMARY.txt](AGENT3_SUMMARY.txt) - Agent implementation details

---

## 🤝 Integration Examples

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/evaluate-loan",
    json={
        "applicant_id": "APPL001",
        "age": 45,
        "annual_income": 200000,
        "employment_type": "employed",
        "credit_score": 780,
        "loan_amount": 300000,
        "tenure_months": 360,
        "existing_liabilities": 1000,
        "location": "CA"
    }
)
result = response.json()
print(f"Decision: {result['decision']['classification']}")
```

### JavaScript
```javascript
const response = await fetch("http://localhost:8000/evaluate-loan", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    applicant_id: "APPL001",
    age: 45,
    annual_income: 200000,
    employment_type: "employed",
    credit_score: 780,
    loan_amount: 300000,
    tenure_months: 360,
    existing_liabilities: 1000,
    location: "CA"
  })
});
const result = await response.json();
console.log(`Decision: ${result.decision.classification}`);
```

---

## 📝 License & Support

**Version:** 2.0.0  
**Last Updated:** 2026-05-25  
**Status:** Production-Ready

**API Documentation:** http://localhost:8000/docs  
**Support:** Check ERROR_HANDLING_GUIDE.md for troubleshooting

---

## 🎓 Learning Path

1. **Start Here:** Read API_QUICKSTART.md (5 min)
2. **Understand Endpoints:** Review API_DOCUMENTATION.md
3. **Learn Error Handling:** Read ERROR_HANDLING_GUIDE.md
4. **Test It:** Run api_test_loan_evaluation.py
5. **Integrate It:** Use curl_tests.sh or Python examples
6. **Deploy It:** Follow deployment checklist

---

**Ready to evaluate loans? Start the API and visit http://localhost:8000/docs!**
