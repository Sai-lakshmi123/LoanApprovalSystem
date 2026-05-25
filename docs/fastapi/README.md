# 🔌 FastAPI Documentation

REST API server for loan evaluation. Single endpoint processes applications and returns decisions.

## 📖 Quick Overview

- **Framework:** FastAPI (Python)
- **Port:** 8000
- **Main Endpoint:** `POST /evaluate-loan`
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Health Check:** GET `/health`

## 📑 Files in This Folder

| File | Purpose |
|------|---------|
| [overview.md](overview.md) | Service introduction and features |
| [api-reference.md](api-reference.md) | Complete endpoint documentation |
| [quick-start.md](quick-start.md) | Get the API running in 5 minutes |
| [implementation-summary.md](implementation-summary.md) | Technical implementation details |
| [service-guide.md](service-guide.md) | Service architecture guide |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create .env File
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Start the Server
```bash
python src/api/main.py
```

Server starts at: `http://localhost:8000`

### 4. Test the API
```bash
# Check if server is running
curl http://localhost:8000/health

# Submit a loan application
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST_001",
    "age": 45,
    "annual_income": 200000,
    "employment_type": "salaried",
    "credit_score": 750,
    "loan_amount": 300000,
    "tenure_months": 360,
    "existing_liabilities": 50000,
    "location": "NY"
  }'
```

## 🔌 Main Endpoint

### POST `/evaluate-loan`

**Purpose:** Evaluate a loan application and return approval decision

**Request Body:**
```json
{
  "applicant_id": "APPL_001",
  "age": 45,
  "annual_income": 200000,
  "employment_type": "salaried",
  "credit_score": 750,
  "loan_amount": 300000,
  "tenure_months": 360,
  "existing_liabilities": 50000,
  "location": "NY"
}
```

**Response:**
```json
{
  "decision": "APPROVE",
  "risk_score": 2,
  "confidence": 90,
  "key_factors": ["Strong income", "Good credit history"],
  "reasoning": "Applicant shows strong financial profile...",
  "next_steps": ["Proceed with documentation"],
  "case_id": "CASE-APPL_001-1234567890"
}
```

## 📋 Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| applicant_id | string | Yes | Unique applicant identifier |
| age | integer | Yes | Age in years (18-80) |
| annual_income | integer | Yes | Annual income in dollars |
| employment_type | string | Yes | "salaried", "self_employed", "unemployed" |
| credit_score | integer | Yes | Credit score (300-850) |
| loan_amount | integer | Yes | Requested loan amount |
| tenure_months | integer | Yes | Loan tenure in months |
| existing_liabilities | integer | Yes | Total existing debt |
| location | string | No | Geographic location |

## 🎯 Decision Classifications

| Decision | Meaning | Next Step |
|----------|---------|-----------|
| APPROVE | Loan approved | Proceed with documentation |
| REJECT | Loan rejected | No further action |
| REVIEW | Requires manual review | Route to loan officer |

## 📊 Response Fields

| Field | Type | Description |
|-------|------|-------------|
| decision | string | APPROVE, REJECT, or REVIEW |
| risk_score | integer | 1-5 scale (1=low, 5=high) |
| confidence | integer | 0-100% decision confidence |
| key_factors | array | List of decision factors |
| reasoning | string | Detailed explanation |
| next_steps | array | Recommended actions |
| case_id | string | Unique case identifier |

## ✅ Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Loan Approval System API",
  "version": "2.0.0"
}
```

## 📖 Full Documentation

- **Complete API Reference:** [api-reference.md](api-reference.md)
- **Implementation Details:** [implementation-summary.md](implementation-summary.md)
- **Service Architecture:** [service-guide.md](service-guide.md)

## 🔐 Security

- API Key: Set `ANTHROPIC_API_KEY` in `.env`
- CORS: Configured for local development
- Input Validation: Pydantic validation on all inputs
- Rate Limiting: Can be added via middleware

See [Security Best Practices](../setup-deployment/security-best-practices.md)

## 🧪 Testing

### Manual Testing with cURL
```bash
# Submit a sample application
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{"applicant_id":"TEST","age":45,"annual_income":200000,...}'
```

### Using Swagger UI
1. Navigate to: http://localhost:8000/docs
2. Find `/evaluate-loan` endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using the Python Test Script
```bash
python tests/test_loan_scenarios.py
```

## 🔄 Workflow

```
User Request
    ↓
Streamlit UI / External Client
    ↓
FastAPI /evaluate-loan endpoint
    ↓
Input Validation (Pydantic)
    ↓
LangGraph Orchestration Engine
    ↓
4 Agents + 4 MCP Servers
    ↓
Decision Result
    ↓
Response to Client
```

## ⚡ Performance

- **Average Response Time:** < 1 second
- **Max Response Time:** 30 seconds
- **Timeout:** 120 seconds
- **Concurrent Requests:** Limited by LLM rate limits

## 🐛 Error Handling

| Status Code | Meaning |
|------------|---------|
| 200 | Success |
| 400 | Bad request (validation error) |
| 500 | Server error |
| 503 | Service unavailable |

See [Error Handling Guide](../api-integration/error-handling-guide.md) for detailed error types.

## 📚 Code Structure

**File:** `src/api/main.py`

```python
# Main components:
- FastAPI app initialization
- LoanEvaluationRequest (Pydantic model)
- LoanEvaluationResponse (Pydantic model)
- /health endpoint
- /evaluate-loan POST endpoint
- Integration with fast_orchestration
```

## 🔗 Related Documentation

- **Architecture:** [System Design](../architecture/system-design.md)
- **Agents:** [Agent Documentation](../agents/)
- **MCP Servers:** [MCP Documentation](../mcp-servers/)
- **Orchestration:** [LangGraph Guide](../architecture/langgraph-orchestration.md)
- **Testing:** [Testing Guide](../testing/)

## 🚀 Deployment

### Local Development
```bash
python src/api/main.py
```

### Production
See [Deployment Guide](../setup-deployment/installation-guide.md)

---

**Next Steps:**
1. Read [quick-start.md](quick-start.md) to start the server
2. Check [api-reference.md](api-reference.md) for all endpoints
3. Test with cURL or Swagger UI
4. See it integrated with Streamlit UI

Ready to integrate? 🚀
