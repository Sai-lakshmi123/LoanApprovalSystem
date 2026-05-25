# Test Script Summary - Loan Approval System

Complete test implementation with 3 sample loan applications.

---

## 📋 What Was Created

**File:** `tests/test_loan_scenarios.py` (600+ lines)

A comprehensive test script that:
- ✅ Submits 3 realistic loan applications to the system
- ✅ Validates decisions against expected outcomes
- ✅ Verifies all 4 agents produce correct outputs
- ✅ Provides detailed test reporting
- ✅ Generates test result summaries
- ✅ Supports colored terminal output
- ✅ Saves results to JSON files

**Documentation:** `TEST_SCENARIOS_GUIDE.md` (400+ lines)

Complete guide including:
- Detailed test data for each scenario
- Expected outputs at each agent stage
- Expected metrics and confidence ranges
- Validation criteria
- How to interpret results

---

## 🎯 3 Test Scenarios

### Scenario 1: Strong Applicant → APPROVE ✅

**Test Data:**
```
Age: 45
Income: $200,000/year
Credit Score: 780 (Excellent)
Employment: 10 years (Very stable)
Loan Amount: $300,000
Debt: $1,000/month
DTI: 0.27 (Excellent)
```

**Expected Decision: APPROVE**
- Confidence: 85-95%
- Risk Level: Low
- Risk Score: < 2.0
- Next Steps: Prepare closing documents

**Why Approved:**
- Excellent credit (780)
- Low DTI (0.27 - far below 0.36 threshold)
- Stable employment (10 years)
- Strong income relative to loan
- No red flags

---

### Scenario 2: Weak Applicant → REJECT ❌

**Test Data:**
```
Age: 35
Income: $50,000/year
Credit Score: 580 (Poor)
Employment: 1 month (Very unstable)
Loan Amount: $300,000 (6x income!)
Debt: $2,500/month
DTI: 0.80 (Critical!)
Delinquencies: 2 (Recent)
Inquiries: 6 in 6 months (Shopping)
```

**Expected Decision: REJECT**
- Confidence: 75-95%
- Risk Level: High
- Risk Score: > 4.0
- Rejection Reason: Multiple escalation triggers

**Why Rejected:**
- ❌ DTI 0.80 (far exceeds 0.50 limit)
- ❌ LTV 0.94 (exceeds thresholds)
- ❌ Poor credit score (580)
- ❌ Recent delinquencies (2)
- ❌ Job tenure 1 month (unstable)
- ❌ Loan 6x annual income
- ❌ High credit utilization (85%)

**Escalation Triggers Hit:**
1. DTI > 0.50 ✓
2. LTV > 0.80 ✓
3. Credit score < 620 ✓
4. Multiple recent delinquencies ✓
5. Employment < 6 months ✓

---

### Scenario 3: Moderate Applicant → REVIEW ⚠️

**Test Data:**
```
Age: 40
Income: $120,000/year
Credit Score: 720 (Good)
Employment: 5 years (Stable)
Loan Amount: $280,000
Debt: $1,500/month
DTI: 0.39 (Borderline)
Delinquencies: 0 (Clean)
Inquiries: 2 in 6 months (Normal)
```

**Expected Decision: REVIEW**
- Confidence: 40-75%
- Risk Level: Medium
- Risk Score: 2.0-3.5
- Next Steps: Escalate to senior underwriter

**Why Review Required:**
- ⚠️ DTI 0.39 (just above 0.36 threshold)
- ✅ Clean credit history
- ✅ Stable employment (5 years)
- ✅ Good credit score (720)
- ⚠️ Mixed signals require human judgment

**Possible Approval with Conditions:**
- Reduce loan to $250,000 to bring DTI below 0.36
- Verify income (recent pay stubs, tax returns)
- Request additional documentation

---

## 🏃 How to Run

### Prerequisites

Ensure all 6 services are running:

```bash
# Terminal 1-5: Start services
python mcp/server.py
python mcp/riskrulesdb/server.py
python mcp/decisionsynthesis/server.py
python mcp/notificationsystem/server.py
python src/api/main.py
```

### Run Test Script

```bash
cd /path/to/LoanApprovalSystem/LoanApprovalSystem

# Basic run
python tests/test_loan_scenarios.py

# With verbose output
python tests/test_loan_scenarios.py --verbose

# Save results to JSON
python tests/test_loan_scenarios.py --save-results

# Combine options
python tests/test_loan_scenarios.py --verbose --save-results
```

### Expected Output (Summary)

```
================================================================================
  LOAN APPROVAL SYSTEM - COMPREHENSIVE TEST SUITE
================================================================================

>>> Pre-Test Verification
✅ API is healthy and running

>>> Running Test Scenarios
✅ Scenario 1: Strong Applicant PASSED
✅ Scenario 2: Weak Applicant PASSED
✅ Scenario 3: Moderate Applicant PASSED

================================================================================
  TEST SUMMARY
================================================================================

Total Scenarios: 3
✅ Passed: 3
❌ Failed: 0
```

---

## 📊 Test Data Details

### Scenario 1: Strong Applicant

| Field | Value | Notes |
|-------|-------|-------|
| applicant_id | SCENARIO1_STRONG | Unique ID |
| age | 45 | Prime lending age |
| annual_income | $200,000 | High income |
| employment_type | employed | Stable |
| credit_score | 780 | Excellent |
| delinquencies | 0 | Clean history |
| credit_utilization | 0.20 | Excellent usage |
| years_at_job | 10 | Very stable |
| existing_liabilities | $1,000/month | Low debt |
| loan_amount | $300,000 | 1.5x annual income |
| property_value | $600,000 | LTV = 50% |
| inquiries_6m | 0 | Not shopping |

### Scenario 2: Weak Applicant

| Field | Value | Notes |
|-------|-------|-------|
| applicant_id | SCENARIO2_WEAK | Unique ID |
| age | 35 | Working years |
| annual_income | $50,000 | Low income |
| employment_type | employed | But very new |
| credit_score | 580 | Poor |
| delinquencies | 2 | Recent issues |
| credit_utilization | 0.85 | Very high |
| years_at_job | 0.08 | 1 month! |
| existing_liabilities | $2,500/month | Very high |
| loan_amount | $300,000 | 6x income! |
| property_value | $320,000 | LTV = 94% |
| inquiries_6m | 6 | Desperate shopping |

### Scenario 3: Moderate Applicant

| Field | Value | Notes |
|-------|-------|-------|
| applicant_id | SCENARIO3_MODERATE | Unique ID |
| age | 40 | Working years |
| annual_income | $120,000 | Moderate income |
| employment_type | employed | Stable |
| credit_score | 720 | Good (not great) |
| delinquencies | 0 | Clean |
| credit_utilization | 0.45 | Moderate |
| years_at_job | 5 | Stable |
| existing_liabilities | $1,500/month | Moderate |
| loan_amount | $280,000 | 2.3x income |
| property_value | $450,000 | LTV = 62% |
| inquiries_6m | 2 | Normal |

---

## ✅ Validation Checks

### For Each Scenario, Test Verifies:

1. **Output Structure**
   - ✅ Valid JSON format
   - ✅ All required fields present
   - ✅ Decision object has correct fields
   - ✅ All arrays present (even if empty)

2. **Decision Classification**
   - ✅ Is APPROVE, REJECT, REVIEW, or CONDITIONAL_APPROVE
   - ✅ Matches expected decision
   - ✅ Consistent with risk assessment

3. **Confidence Level**
   - ✅ Is numeric percentage (0-100)
   - ✅ Is within expected range for decision
   - ✅ APPROVE: 85-95%, REVIEW: 40-75%, REJECT: 75-95%

4. **Risk Assessment**
   - ✅ Risk score is 1-5 scale
   - ✅ Risk level matches score (Low, Medium, High)
   - ✅ Consistent with decision

5. **Key Metrics**
   - ✅ Credit score matches input
   - ✅ DTI calculated correctly
   - ✅ LTV calculated correctly
   - ✅ All financial metrics present

6. **Decision Factors**
   - ✅ Key factors list provided
   - ✅ Factors are specific and relevant
   - ✅ Reasoning explains decision

---

## 📈 Expected Confidence Ranges

| Decision | Min | Max | Notes |
|----------|-----|-----|-------|
| APPROVE | 85% | 95% | Clear positive case |
| CONDITIONAL_APPROVE | 50% | 75% | Approval with conditions |
| REVIEW | 40% | 75% | Manual review needed |
| REJECT | 75% | 95% | Clear negative case |

---

## 🔍 Test Interpretation

### All Tests Pass ✅

System is working correctly:
- Scenario 1: APPROVE decision rendered
- Scenario 2: REJECT decision rendered
- Scenario 3: REVIEW decision rendered
- All agents functioning
- All calculations correct
- All validations pass

**Next Steps:** Deploy to production

---

### Some Tests Fail ❌

Check for issues:

**If Scenario 1 Fails (Should APPROVE):**
- Are risk thresholds too strict?
- Is DTI calculation incorrect?
- Are escalation triggers too sensitive?

**If Scenario 2 Fails (Should REJECT):**
- Are escalation triggers not firing?
- Is risk scoring too lenient?
- Are validation checks missing?

**If Scenario 3 Fails (Should REVIEW):**
- Is Agent3 decision logic wrong?
- Are borderline cases being auto-approved?
- Is confidence calculation off?

---

### Unexpected Results ⚠️

Possible causes:
- Different threshold values than defaults
- Customized scoring formula
- Modified Agent prompts
- Different risk calculation method
- Threshold adjustments for your policy

**Solution:** 
1. Review Agent prompts
2. Check threshold values
3. Verify calculation methods
4. Adjust test data if needed

---

## 💾 Test Results Output

### Console Output

Real-time colored output showing:
- ✅ Green for PASS
- ❌ Red for FAIL
- ⚠️ Yellow for WARNINGS
- ℹ️ Blue for INFO

### JSON Results File

When using `--save-results`, creates file:
```
test_results_20260525_143000.json
```

Contains:
```json
{
  "test_suite": "Loan Approval System",
  "timestamp": "2026-05-25T14:30:00",
  "total_scenarios": 3,
  "summary": {
    "passed": 3,
    "failed": 0,
    "partial": 0,
    "error": 0
  },
  "results": [
    {
      "scenario": "Scenario 1: Strong Applicant",
      "expected_decision": "APPROVE",
      "actual_decision": "APPROVE",
      "result": "PASS",
      "details": { ... }
    },
    ...
  ]
}
```

---

## 🧪 Test Metrics

### Scenario 1 Expected Metrics

```json
{
  "decision": "APPROVE",
  "confidence": "88%",
  "risk_score": "1.8/5",
  "risk_level": "Low",
  "dti": "0.27",
  "credit_score": "780"
}
```

### Scenario 2 Expected Metrics

```json
{
  "decision": "REJECT",
  "confidence": "92%",
  "risk_score": "4.75/5",
  "risk_level": "High",
  "dti": "0.80",
  "credit_score": "580"
}
```

### Scenario 3 Expected Metrics

```json
{
  "decision": "REVIEW",
  "confidence": "58%",
  "risk_score": "2.61/5",
  "risk_level": "Medium",
  "dti": "0.39",
  "credit_score": "720"
}
```

---

## 📚 Related Documentation

| Document | Purpose |
|----------|---------|
| TEST_SCENARIOS_GUIDE.md | Detailed scenario definitions |
| test_loan_scenarios.py | Test script implementation |
| AGENT_SYSTEM_PROMPTS.md | Agent decision logic |
| API_DOCUMENTATION.md | API endpoint reference |
| STREAMLIT_QUICKSTART.md | UI testing guide |

---

## 🎓 Using Test Results

### For Validation
- Verify system works correctly
- Confirm decision logic is sound
- Check metric calculations
- Validate error handling

### For Debugging
- Identify which agents fail
- Check specific calculations
- Verify threshold values
- Debug decision logic

### For Documentation
- Show system capabilities
- Demonstrate different scenarios
- Provide test cases
- Validate requirements

### For Production
- Before deployment
- Regression testing
- After configuration changes
- After agent prompt updates

---

## 🚀 Next Steps After Testing

### If Tests Pass ✅
1. ✅ System is working correctly
2. ✅ Deploy to production
3. ✅ Set up monitoring
4. ✅ Start accepting real applications

### If Tests Fail ❌
1. ❌ Review test output
2. ❌ Check Agent prompts
3. ❌ Verify calculations
4. ❌ Adjust thresholds if needed
5. ❌ Re-run tests
6. ❌ Deploy when passing

### For Continuous Testing
1. Run tests regularly
2. Add more scenarios as needed
3. Monitor test results
4. Alert on failures
5. Update tests as rules change

---

## 📊 Test Statistics

| Metric | Value |
|--------|-------|
| Total Lines of Code | 600+ |
| Scenarios Tested | 3 |
| Validation Checks | 6+ per scenario |
| Test Data Points | 30+ per scenario |
| Expected Outputs | Fully defined |
| Documentation Lines | 400+ |

---

**Version:** 2.0.0  
**Status:** ✅ Ready for Testing  
**Last Updated:** 2026-05-25

**Run tests with:** `python tests/test_loan_scenarios.py --verbose --save-results`
