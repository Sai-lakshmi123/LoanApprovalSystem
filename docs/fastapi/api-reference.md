# FastAPI Loan Evaluation Service - API Documentation

## Overview

The Loan Evaluation Service is a FastAPI microservice that provides a REST API for evaluating loan applications using a multi-agent orchestration system. It accepts loan application data, processes it through 4 specialized agents (Profile Analysis, Risk Analysis, Decision Synthesis, and Compliance), and returns a comprehensive evaluation with loan decision, risk assessment, and recommended next steps.

**Base URL:** `http://localhost:8000`

**API Version:** 2.0.0

---

## Quick Start

### 1. Start the FastAPI Server

```bash
cd /path/to/LoanApprovalSystem
python src/api/main.py
```

Output:
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

### 2. Access the API Documentation

- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc (Alternative Docs):** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Evaluate a loan
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

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Purpose:** Check if the API service is running and healthy

**Response:**
```json
{
  "status": "healthy",
  "service": "Loan Approval System API",
  "timestamp": "2026-05-25T10:30:01.234567"
}
```

**Status Code:** `200 OK`

---

### 2. Evaluate Loan Application

**Endpoint:** `POST /evaluate-loan`

**Purpose:** Submit a loan application for evaluation through the multi-agent orchestration system

**Request Body:**

```json
{
  "applicant_id": "string (required)",
  "age": "integer (required, 18-100)",
  "annual_income": "number (required, > 0)",
  "employment_type": "string (required, employed|self-employed|retired|student|unemployed)",
  "credit_score": "integer (required, 300-850)",
  "loan_amount": "number (required, > 0)",
  "tenure_months": "integer (required, 12-360)",
  "existing_liabilities": "number (optional, default: 0)",
  "location": "string (required, min 2 chars)",
  "monthly_expenses": "number (optional)",
  "delinquencies": "integer (optional, default: 0)",
  "inquiries_last_6_months": "integer (optional, default: 0)",
  "credit_utilization": "number (optional, 0-1, default: 0.5)",
  "years_at_current_job": "integer (optional, default: 1)",
  "existing_loans": "integer (optional, default: 0)",
  "property_value": "number (optional)",
  "email": "string (optional)",
  "phone": "string (optional)",
  "timestamp": "string (optional, ISO 8601 format)"
}
```

**Request Example:**

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
  "location": "CA",
  "delinquencies": 0,
  "inquiries_last_6_months": 0,
  "credit_utilization": 0.20,
  "years_at_current_job": 10,
  "existing_loans": 1,
  "property_value": 600000,
  "email": "john.strong@example.com",
  "phone": "+1-555-0100"
}
```

**Response:**

```json
{
  "success": true,
  "applicant_id": "APPL001",
  "decision": {
    "classification": "APPROVE",
    "risk_score": 1.8,
    "confidence_level": "High",
    "confidence_percentage": 85,
    "reasoning": "Strong financial profile with excellent credit history and low risk indicators",
    "key_factors": [
      "Excellent credit score (780)",
      "Stable employment (10 years)",
      "Low debt-to-income ratio",
      "Strong income relative to loan amount"
    ]
  },
  "risk_score": 1.8,
  "risk_level": "Low",
  "next_steps": [
    "Prepare loan documents",
    "Schedule closing appointment",
    "Arrange final verification"
  ],
  "case_id": "CASE-APPL001-1716633001",
  "error_handling": null,
  "workflow_status": "success",
  "execution_path": [
    "Agent1_Profile",
    "Agent2_Risk",
    "Agent3_Decision",
    "Agent4_Compliance"
  ],
  "timestamp": "2026-05-25T10:30:05.123456",
  "processing_time_ms": 2845.67
}
```

**Status Code:** `200 OK`

**Status Codes:**

| Code | Meaning |
|------|---------|
| `200` | Successful evaluation |
| `422` | Validation error (invalid input) |
| `500` | Server error during evaluation |

---

### 3. List Available Agents

**Endpoint:** `GET /agents`

**Purpose:** Get information about available agents in the system

**Response:**

```json
{
  "agents": [
    {
      "name": "Agent1",
      "type": "Profile Analysis",
      "status": "active",
      "description": "Analyzes applicant profile and financial stability"
    },
    {
      "name": "Agent2",
      "type": "Risk Analysis",
      "status": "active",
      "description": "Evaluates financial risk and metrics"
    },
    {
      "name": "Agent3",
      "type": "Decision Synthesis",
      "status": "active",
      "description": "Synthesizes decision based on profile and risk analysis"
    },
    {
      "name": "Agent4",
      "type": "Compliance Orchestration",
      "status": "active",
      "description": "Records decision and compliance information"
    }
  ],
  "orchestration_engine": "LangGraph",
  "llm_model": "Claude Sonnet 4.6"
}
```

**Status Code:** `200 OK`

---

## Request Validation

All inputs to the `/evaluate-loan` endpoint are validated:

### Required Fields
- `applicant_id` - Unique identifier (non-empty string)
- `age` - Must be between 18 and 100
- `annual_income` - Must be positive number
- `employment_type` - Must be one of: `employed`, `self-employed`, `retired`, `student`, `unemployed`
- `credit_score` - Must be between 300 and 850
- `loan_amount` - Must be positive number
- `tenure_months` - Must be between 12 and 360 months
- `location` - Must be at least 2 characters

### Optional Fields with Defaults
- `existing_liabilities` - Default: 0
- `delinquencies` - Default: 0
- `inquiries_last_6_months` - Default: 0
- `credit_utilization` - Default: 0.5
- `years_at_current_job` - Default: 1
- `existing_loans` - Default: 0
- `monthly_expenses` - Automatically calculated from existing_liabilities if not provided
- `property_value` - Defaults to 1.5x loan amount if not provided

### Validation Errors

**Example: Invalid Age**
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{"applicant_id": "TEST", "age": 15, ...}'
```

**Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is greater than or equal to 18",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

---

## Response Models

### LoanEvaluationResponse

The main response model for successful loan evaluations:

```python
{
  "success": bool,              # Whether evaluation was successful
  "applicant_id": str,          # Applicant ID from request
  "decision": DecisionDetails,  # Loan decision details
  "risk_score": float,          # Overall risk score (0-5)
  "risk_level": str,            # Risk level (Low/Medium/High)
  "next_steps": List[str],      # Recommended next steps
  "case_id": str,               # Generated case ID for tracking
  "error_handling": Optional[ErrorHandlingInfo],  # Error info if errors occurred
  "workflow_status": str,       # Status: success/error/error_with_fallback/partial_success
  "execution_path": List[str],  # Path through agents
  "timestamp": str,             # Response timestamp (ISO 8601)
  "processing_time_ms": float   # Processing time in milliseconds
}
```

### DecisionDetails

```python
{
  "classification": str,        # APPROVE/REJECT/REVIEW
  "risk_score": float,          # Risk score (0-5)
  "confidence_level": str,      # Confidence level
  "confidence_percentage": int, # Confidence (0-100)
  "reasoning": str,             # Decision reasoning
  "key_factors": List[str]      # Key decision factors
}
```

### ErrorHandlingInfo

```python
{
  "critical_errors": List[Dict],  # Errors encountered
  "error_count": int,             # Number of errors
  "error_escalation": bool,       # Manual review flag
  "retry_statistics": Dict        # Retry attempt statistics
}
```

---

## Example Usage Scenarios

### Scenario 1: Strong Applicant (Auto-Approve)

**Request:**
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "STRONG001",
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

**Expected Response:**
```json
{
  "success": true,
  "applicant_id": "STRONG001",
  "decision": {
    "classification": "APPROVE",
    "confidence_percentage": 85,
    "risk_score": 1.8
  },
  "workflow_status": "success",
  "processing_time_ms": 2500
}
```

---

### Scenario 2: High-Risk Applicant (Escalation)

**Request:**
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "RISK001",
    "age": 35,
    "annual_income": 60000,
    "employment_type": "employed",
    "credit_score": 580,
    "loan_amount": 300000,
    "tenure_months": 360,
    "existing_liabilities": 2500,
    "location": "TX",
    "delinquencies": 2,
    "inquiries_last_6_months": 5,
    "credit_utilization": 0.85,
    "existing_loans": 3
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "applicant_id": "RISK001",
  "decision": {
    "classification": "REVIEW",
    "confidence_percentage": 45,
    "risk_score": 3.8
  },
  "risk_level": "High",
  "workflow_status": "success",
  "next_steps": [
    "Escalate to senior underwriter",
    "Request additional documentation",
    "Contact applicant for verification"
  ]
}
```

---

### Scenario 3: Validation Error

**Request (Missing required field):**
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "INVALID",
    "age": 35,
    "annual_income": 100000
  }'
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "employment_type"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Integration Guide

### Python (requests)

```python
import requests
import json

# Submit loan application
applicant_data = {
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

response = requests.post(
    "http://localhost:8000/evaluate-loan",
    json=applicant_data
)

if response.status_code == 200:
    result = response.json()
    print(f"Decision: {result['decision']['classification']}")
    print(f"Confidence: {result['decision']['confidence_percentage']}%")
    print(f"Case ID: {result['case_id']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### JavaScript/Node.js

```javascript
const applicantData = {
  applicant_id: "APPL001",
  age: 45,
  annual_income: 200000,
  employment_type: "employed",
  credit_score: 780,
  loan_amount: 300000,
  tenure_months: 360,
  existing_liabilities: 1000,
  location: "CA"
};

fetch("http://localhost:8000/evaluate-loan", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(applicantData)
})
  .then(response => response.json())
  .then(result => {
    console.log(`Decision: ${result.decision.classification}`);
    console.log(`Confidence: ${result.decision.confidence_percentage}%`);
    console.log(`Case ID: ${result.case_id}`);
  })
  .catch(error => console.error("Error:", error));
```

### cURL

```bash
# Check health
curl http://localhost:8000/health

# Get agents
curl http://localhost:8000/agents

# Evaluate loan
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d @loan_application.json
```

---

## Decision Classifications

### APPROVE
- **Meaning:** Loan is approved for processing
- **Confidence:** Usually 70%+
- **Risk Score:** Typically < 2.5
- **Actions:** Prepare documents, schedule closing

### REJECT
- **Meaning:** Loan is rejected
- **Confidence:** Usually 80%+
- **Risk Score:** Typically > 4.0
- **Actions:** Notify applicant, provide reason

### REVIEW
- **Meaning:** Loan requires manual review by underwriter
- **Confidence:** Typically 40-70%
- **Risk Score:** 2.5-4.0
- **Actions:** Escalate to senior underwriter, request additional info

---

## Error Handling

### Error Response Structure

```json
{
  "detail": {
    "error": "Error type",
    "applicant_id": "APPL001",
    "message": "Detailed error message"
  }
}
```

### Common Errors

| Error | Status | Cause | Solution |
|-------|--------|-------|----------|
| Validation Error | 422 | Invalid input data | Check field values and formats |
| Connection Error | 500 | MCP server not running | Start MCP servers |
| Timeout | 500 | Processing took too long | Check system resources |
| Missing Field | 422 | Required field not provided | Include all required fields |

---

## Performance

### Processing Time

- **Average:** 2-4 seconds
- **Range:** 1-15 seconds (depending on complexity)
- **Timeout:** 60 seconds

### Optimization Tips

1. Pre-validate data before submission
2. Ensure MCP servers are running
3. Monitor system resources
4. Use connection pooling for multiple requests

---

## Testing

### Test Script

Run the comprehensive test suite:

```bash
# Terminal 1: Start API
python src/api/main.py

# Terminal 2: Run tests
python examples/api_test_loan_evaluation.py
```

### Test Coverage

The test suite covers:
- ✅ Health check
- ✅ Strong applicant (auto-approve)
- ✅ High-risk applicant (escalation)
- ✅ Moderate applicant (review)
- ✅ Input validation
- ✅ Error handling

---

## Configuration

### Environment Variables

```bash
# API Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Optional: Logging
LOG_LEVEL=INFO
```

### Customization

Edit `src/api/main.py` to customize:
- API title and description
- CORS settings
- Request/response models
- Error handling behavior

---

## Troubleshooting

### Issue: "Connection refused"

**Cause:** API server not running

**Solution:**
```bash
python src/api/main.py
```

### Issue: "MCP server not available"

**Cause:** Required MCP servers not running

**Solution:**
```bash
# Terminal 1
python mcp/server.py

# Terminal 2
python mcp/riskrulesdb/server.py

# Terminal 3
python mcp/decisionsynthesis/server.py

# Terminal 4
python mcp/notificationsystem/server.py
```

### Issue: Request timeout

**Cause:** Processing taking too long

**Solution:**
- Check MCP server performance
- Verify network connectivity
- Increase timeout in client code

---

## Support & Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Full Documentation:** See `API_DOCUMENTATION.md` (this file)
- **Error Handling Guide:** See `ERROR_HANDLING_GUIDE.md`
- **Orchestration Guide:** See `ERROR_HANDLING_GUIDE.md`

---

**Last Updated:** 2026-05-25  
**Version:** 2.0.0
