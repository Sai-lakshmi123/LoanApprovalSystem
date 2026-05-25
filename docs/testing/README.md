# 🧪 Testing Documentation

Test scenarios, guidelines, and examples for the Loan Approval System.

## 📖 Overview

This folder contains:
- Test scenarios with sample data
- Testing guidelines
- cURL examples for API testing
- Test result analysis

## 📑 Files in This Folder

| File | Purpose |
|------|---------|
| [test-scenarios.md](test-scenarios.md) | 3 sample loan applications to test |
| [implementation-guide.md](implementation-guide.md) | How to run tests |
| [curl-examples.sh](curl-examples.sh) | cURL commands for API testing |

## 🎯 Test Scenarios

The system includes 3 sample loan applications:

### Scenario 1: Strong Applicant (APPROVE Expected)
**Profile:**
- Applicant ID: APPL_001
- Age: 45
- Annual Income: $200,000
- Employment: Salaried, 10+ years
- Credit Score: 780 (Excellent)
- Loan Amount: $300,000
- Debt-to-Income: 0.27 (Good)

**Expected Decision:** ✅ APPROVE  
**Confidence:** 90%  
**Reasoning:** Strong income, excellent credit, stable employment

---

### Scenario 2: Weak Applicant (REJECT Expected)
**Profile:**
- Applicant ID: APPL_002
- Age: 35
- Annual Income: $50,000
- Employment: Unemployed/Recently unemployed
- Credit Score: 580 (Poor)
- Loan Amount: $200,000
- Debt-to-Income: 0.80 (High)
- Credit Issues: 2 delinquencies

**Expected Decision:** ❌ REJECT  
**Confidence:** 85%  
**Reasoning:** High debt-to-income, poor credit, unemployment concerns

---

### Scenario 3: Moderate Applicant (REVIEW Expected)
**Profile:**
- Applicant ID: APPL_003
- Age: 40
- Annual Income: $120,000
- Employment: Salaried, 5 years
- Credit Score: 720 (Good)
- Loan Amount: $150,000
- Debt-to-Income: 0.39 (Borderline)
- Mixed factors: Some positive, some concerning

**Expected Decision:** 🔄 REVIEW  
**Confidence:** 50-60%  
**Reasoning:** Moderate profile - requires manual review for borderline cases

---

## 🚀 How to Run Tests

### Option 1: Python Test Script (Recommended)

```bash
# Run all test scenarios
python tests/test_loan_scenarios.py

# Expected output:
# [✓ PASS] Scenario 1: Strong Applicant
# [✓ PASS] Scenario 2: Weak Applicant
# [✓ PASS] Scenario 3: Moderate Applicant
```

### Option 2: cURL Commands

```bash
# Test Scenario 1
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APPL_001",
    "age": 45,
    "annual_income": 200000,
    ...
  }'
```

See [curl-examples.sh](curl-examples.sh) for all test commands.

### Option 3: Streamlit UI

1. Open http://localhost:8501
2. Go to "📋 New Application" tab
3. Fill in test data manually
4. Click "Submit"
5. Verify results match expectations

---

## 📊 Test Coverage

| Component | Test Type | Status |
|-----------|-----------|--------|
| Agents | Integration | ✅ Tested |
| MCP Servers | Integration | ✅ Tested |
| FastAPI | Unit + Integration | ✅ Tested |
| Streamlit | Manual | ✅ Tested |
| Decision Logic | Integration | ✅ Tested |
| Error Handling | Manual | ✅ Tested |

---

## 🧪 Manual Testing Guide

### Test 1: Submit Valid Loan Application

**Steps:**
1. Open Streamlit UI: http://localhost:8501
2. Go to "📋 New Application" tab
3. Fill form with Scenario 1 data (strong applicant)
4. Click "Submit Application"
5. Wait for result

**Expected:**
- ✅ APPROVE decision
- Risk Score: 1-2
- Confidence: 80-90%
- Result displays in "📊 Results" tab

---

### Test 2: Check Application History

**Steps:**
1. Submit 2-3 applications via UI
2. Go to "📈 History" tab
3. View all submitted applications

**Expected:**
- All applications listed with timestamps
- Decisions shown (APPROVE/REJECT/REVIEW)
- Statistics updated (total, approved count, etc.)

---

### Test 3: Test API Directly

**Steps:**
```bash
# Send request to API
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d @test_payload.json

# View response
# Should contain: decision, risk_score, confidence, case_id
```

**Expected:**
- 200 OK response
- Valid JSON response
- All required fields present

---

### Test 4: Test Form Validation

**Steps:**
1. Go to "📋 New Application" tab
2. Leave required field empty (e.g., Age)
3. Click "Submit Application"

**Expected:**
- ❌ Validation error message
- Form not submitted
- Error message clear and helpful

---

### Test 5: Test Error Handling

**Steps:**
1. Stop FastAPI server: `pkill -f "python.*main.py"`
2. Try to submit loan via Streamlit
3. Observe error message
4. Restart FastAPI
5. Try again - should work

**Expected:**
- Graceful error message (not crash)
- Clear message about API unavailable
- Retry option provided

---

## 📈 Test Results Analysis

### Sample Test Output

```
================================================================================
LOAN APPROVAL SYSTEM - TEST RESULTS
================================================================================

[1/3] Scenario 1: Strong Applicant
      ✓ Profile Analysis: Passed
      ✓ Risk Analysis: Passed
      ✓ Decision: APPROVE (Expected: APPROVE) ✓
      ✓ Confidence: 90% ✓
      ✓ Time: 0.8s ✓

[2/3] Scenario 2: Weak Applicant
      ✓ Profile Analysis: Passed
      ✓ Risk Analysis: Passed
      ✓ Decision: REJECT (Expected: REJECT) ✓
      ✓ Confidence: 85% ✓
      ✓ Time: 0.9s ✓

[3/3] Scenario 3: Moderate Applicant
      ✓ Profile Analysis: Passed
      ✓ Risk Analysis: Passed
      ✓ Decision: REVIEW (Expected: REVIEW) ✓
      ✓ Confidence: 55% ✓
      ✓ Time: 0.8s ✓

================================================================================
SUMMARY: 3/3 tests passed ✓
Average response time: 0.83 seconds
================================================================================
```

---

## 🐛 Testing Common Issues

### "Cannot connect to API"
**Cause:** FastAPI not running  
**Fix:**
```bash
# Start FastAPI
python src/api/main.py
```

### "Request timeout"
**Cause:** MCP servers slow or API overloaded  
**Fix:**
```bash
# Check MCP servers are running
lsof -i :3001
lsof -i :3002
lsof -i :3003
lsof -i :3004
```

### "Agent returned unexpected result"
**Cause:** Model response changed or logic issue  
**Fix:**
- Check agent system prompts
- Review MCP server responses
- See [Error Handling Guide](../api-integration/error-handling-guide.md)

---

## 📋 Test Checklist

Before deployment, verify:

- [ ] All 3 test scenarios pass with expected decisions
- [ ] Response time < 1 second per request
- [ ] Streamlit UI displays results correctly
- [ ] Form validation works (rejects invalid input)
- [ ] Error handling graceful (no crashes)
- [ ] Application history tracks correctly
- [ ] API docs available at /docs
- [ ] Health check endpoint responds

---

## 🔗 Related Documentation

- **Implementation:** [implementation-guide.md](implementation-guide.md)
- **Test Scenarios:** [test-scenarios.md](test-scenarios.md)
- **cURL Examples:** [curl-examples.sh](curl-examples.sh)
- **Error Handling:** [Error Handling Guide](../api-integration/error-handling-guide.md)
- **API Documentation:** [API Reference](../fastapi/api-reference.md)

---

## 🚀 Next Steps

1. **Run Python Test Script**
   ```bash
   python tests/test_loan_scenarios.py
   ```

2. **Test via Streamlit UI**
   - Open http://localhost:8501
   - Submit test applications

3. **Test via cURL**
   - See [curl-examples.sh](curl-examples.sh)
   - Run example commands

4. **Verify All Passes**
   - Check test output
   - Review results match expectations

---

**Ready to test? Run: `python tests/test_loan_scenarios.py` 🧪**
