# FastAPI Loan Evaluation Service - Quick Start Guide

## 5-Minute Setup

### Step 1: Start All Required Services

Open 5 terminals and run these commands in order:

**Terminal 1: MCP Application Server**
```bash
cd /home/ubuntu/Desktop/LoanApprovalSystem/LoanApprovalSystem
python mcp/server.py
```
Expected output: `MCP server running on http://localhost:5001`

**Terminal 2: MCP Risk Rules Database**
```bash
cd /home/ubuntu/Desktop/LoanApprovalSystem/LoanApprovalSystem
python mcp/riskrulesdb/server.py
```
Expected output: `Risk Rules DB server running on http://localhost:5002`

**Terminal 3: MCP Decision Synthesis**
```bash
cd /home/ubuntu/Desktop/LoanApprovalSystem/LoanApprovalSystem
python mcp/decisionsynthesis/server.py
```
Expected output: `Decision Synthesis server running on http://localhost:5003`

**Terminal 4: MCP Notification System**
```bash
cd /home/ubuntu/Desktop/LoanApprovalSystem/LoanApprovalSystem
python mcp/notificationsystem/server.py
```
Expected output: `Notification System server running on http://localhost:5004`

**Terminal 5: FastAPI Server**
```bash
cd /home/ubuntu/Desktop/LoanApprovalSystem/LoanApprovalSystem
python src/api/main.py
```
Expected output:
```
================================================================================
  LOAN APPROVAL SYSTEM API
================================================================================
  Starting FastAPI server...
  Host: 0.0.0.0
  Port: 8000
  API Docs: http://0.0.0.0:8000/docs
================================================================================
```

### Step 2: Access the API

**Interactive API Documentation:**
- Open browser to: http://localhost:8000/docs
- You'll see Swagger UI with all endpoints

### Step 3: Submit Your First Loan Application

**Using Swagger UI (Easiest):**
1. Go to http://localhost:8000/docs
2. Click on "POST /evaluate-loan"
3. Click "Try it out"
4. Paste this example in the Request body:

```json
{
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
```

5. Click "Execute"
6. See the response with decision details

**Using cURL:**
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APPL001",
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

### Step 4: Run Test Suite

```bash
python examples/api_test_loan_evaluation.py
```

This runs 3 test scenarios plus validation tests:
- ✅ Strong applicant (auto-approve)
- ✅ High-risk applicant (escalation)
- ✅ Moderate applicant (review)
- ✅ Input validation

---

## Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### List Agents
```bash
curl http://localhost:8000/agents
```

### Minimal Loan Evaluation (Required Fields Only)
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST001",
    "age": 35,
    "annual_income": 100000,
    "employment_type": "employed",
    "credit_score": 700,
    "loan_amount": 250000,
    "tenure_months": 360,
    "existing_liabilities": 1000,
    "location": "NY"
  }'
```

---

## Understanding the Response

### Decision Classification

```json
{
  "decision": {
    "classification": "APPROVE",        // APPROVE | REJECT | REVIEW
    "confidence_percentage": 85,         // 0-100
    "risk_score": 1.8,                   // 0-5 (lower is better)
    "confidence_level": "High",          // Very High | High | Medium | Low | Very Low
    "reasoning": "Strong financial profile...",
    "key_factors": [
      "Excellent credit score",
      "Stable employment",
      "Low debt-to-income ratio"
    ]
  }
}
```

### Risk Levels
- **Low** (score 0-2.0): Strong applicant, likely auto-approve
- **Medium** (score 2.0-3.0): Moderate risk, review recommended
- **High** (score 3.0-5.0): High risk, escalation required

---

## Common Test Scenarios

### Scenario 1: Excellent Applicant (Expected: APPROVE)
```json
{
  "applicant_id": "EXCELLENT001",
  "age": 45,
  "annual_income": 200000,
  "employment_type": "employed",
  "credit_score": 780,
  "loan_amount": 300000,
  "tenure_months": 360,
  "existing_liabilities": 1000,
  "location": "CA",
  "delinquencies": 0,
  "credit_utilization": 0.20,
  "years_at_current_job": 10,
  "existing_loans": 1
}
```

### Scenario 2: Weak Applicant (Expected: REVIEW or REJECT)
```json
{
  "applicant_id": "WEAK001",
  "age": 35,
  "annual_income": 60000,
  "employment_type": "employed",
  "credit_score": 580,
  "loan_amount": 300000,
  "tenure_months": 360,
  "existing_liabilities": 2500,
  "location": "TX",
  "delinquencies": 2,
  "credit_utilization": 0.85,
  "years_at_current_job": 1,
  "existing_loans": 3
}
```

### Scenario 3: Average Applicant (Expected: REVIEW or Conditional APPROVE)
```json
{
  "applicant_id": "AVERAGE001",
  "age": 40,
  "annual_income": 120000,
  "employment_type": "employed",
  "credit_score": 720,
  "loan_amount": 280000,
  "tenure_months": 360,
  "existing_liabilities": 1500,
  "location": "NY",
  "delinquencies": 0,
  "credit_utilization": 0.45,
  "years_at_current_job": 5,
  "existing_loans": 2
}
```

---

## Troubleshooting

### "Connection refused" on localhost:8000
**Problem:** API server not running
**Solution:** Run `python src/api/main.py` in Terminal 5

### "Cannot connect to MCP servers"
**Problem:** MCP servers not running
**Solution:** Start all 4 MCP servers (Terminals 1-4)

### "422 Unprocessable Entity"
**Problem:** Invalid request data
**Solution:** Check field types and values against API_DOCUMENTATION.md

### "Slow response (> 10 seconds)"
**Problem:** System resource issues
**Solution:** Check MCP server logs, restart services

---

## Next Steps

1. **Explore API Documentation:** http://localhost:8000/docs
2. **Read Full API Guide:** See `API_DOCUMENTATION.md`
3. **Understand Error Handling:** See `ERROR_HANDLING_GUIDE.md`
4. **Build Frontend:** See Streamlit UI guide
5. **Deploy to Production:** See deployment guide

---

## Environment Variables

Create a `.env` file to customize:

```bash
# API Server
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Logging
LOG_LEVEL=INFO

# MCP Servers (if different)
MCP_APP_URL=http://localhost:5001
MCP_RISK_URL=http://localhost:5002
MCP_DECISION_URL=http://localhost:5003
MCP_NOTIFICATION_URL=http://localhost:5004
```

---

## Performance Metrics

- **Average Processing Time:** 2-4 seconds
- **Response Time Range:** 1-15 seconds
- **Timeout:** 60 seconds
- **Concurrent Requests:** Limited by system resources

---

## Support

**API Documentation:** http://localhost:8000/docs
**Swagger UI:** http://localhost:8000/docs
**ReDoc:** http://localhost:8000/redoc

---

**Version:** 2.0.0  
**Last Updated:** 2026-05-25
