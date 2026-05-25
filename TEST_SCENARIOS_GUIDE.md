# Test Scenarios Guide - Loan Approval System

Complete guide to the 3 test scenarios for validating the loan approval system.

---

## Overview

The test script (`tests/test_loan_scenarios.py`) executes 3 comprehensive test scenarios:

1. **Scenario 1** - Strong Applicant → Expected: **APPROVE** ✅
2. **Scenario 2** - Weak Applicant → Expected: **REJECT** ❌
3. **Scenario 3** - Moderate Applicant → Expected: **REVIEW** ⚠️

Each scenario includes:
- Detailed test data (applicant profile)
- Expected decision classification
- Expected confidence range
- Key metrics to validate
- Detailed reasoning and factors

---

## Scenario 1: Strong Applicant - APPROVE

### Description
A financially healthy applicant with excellent credit, stable employment, and strong income-to-debt ratio. Should be automatically approved.

### Test Data

```json
{
  "applicant_id": "SCENARIO1_STRONG",
  "age": 45,
  "annual_income": 200000,
  "employment_type": "employed",
  "credit_score": 780,
  "loan_amount": 300000,
  "tenure_months": 360,
  "existing_liabilities": 1000,
  "location": "CA",
  "monthly_expenses": 4000,
  "delinquencies": 0,
  "inquiries_last_6_months": 0,
  "credit_utilization": 0.20,
  "years_at_current_job": 10,
  "existing_loans": 1,
  "property_value": 600000,
  "email": "strong.applicant@example.com",
  "phone": "+1-555-0100"
}
```

### Profile Analysis

**Applicant Profile:**
- 45 years old (prime lending age)
- Excellent credit score: **780** (Excellent tier)
- Annual income: **$200,000** (Strong)
- Employment: **Employed for 10 years** (Very stable)
- Monthly income: **$16,667**

**Financial Situation:**
- Current monthly debt: **$1,000** (Low)
- Monthly expenses: **$4,000** (Reasonable)
- Debt-to-income ratio: **0.06** (Excellent - far below 0.36 threshold)

**Loan Details:**
- Requested loan: **$300,000** (1.5x annual income - reasonable)
- Loan term: **360 months** (30 years - standard)
- Monthly payment: **~$833** (at ~3.3% APR)
- **New DTI with loan: 0.27** (Still excellent, well below 0.36 threshold)

**Credit History:**
- Delinquencies: **0** (Clean history)
- Recent inquiries: **0** (Not shopping around)
- Credit utilization: **20%** (Excellent - well below 30% threshold)
- Existing loans: **1** (Manageable)

**Property:**
- Property value: **$600,000**
- LTV: **50%** (0.50 - Low risk, well below 0.80 threshold)

### Agent1 Expected Output

```json
{
  "profile_assessment": {
    "income_stability": {
      "stability_score": 4.8,
      "stability_level": "very_stable",
      "assessment": "Excellent income stability with 10 years at current position..."
    },
    "credit_profile": {
      "quality_score": 4.8,
      "quality_level": "excellent",
      "assessment": "Exceptional credit profile with 780 score, no delinquencies..."
    }
  },
  "profile_flags": {
    "red_flags": [],
    "special_cases": [],
    "data_quality_issues": []
  },
  "overall_profile_strength": 4.8
}
```

### Agent2 Expected Output

```json
{
  "risk_analysis": {
    "financial_metrics": {
      "debt_to_income_ratio": 0.27,
      "loan_to_value_ratio": 0.50,
      "financial_viability": "strong",
      "repayment_capacity": "excellent"
    },
    "credit_risk": {
      "credit_risk_score": 1.2
    }
  },
  "risk_assessment": {
    "overall_risk_score": 1.5,
    "overall_risk_level": "low",
    "risk_category": "auto_approve",
    "primary_risk_drivers": []
  },
  "threshold_analysis": {
    "dti_status": {
      "dti_with_loan": 0.27,
      "status": "excellent"
    },
    "ltv_status": {
      "ltv_ratio": 0.50,
      "status": "low_risk"
    }
  }
}
```

### Agent3 Expected Output

```json
{
  "decision": {
    "classification": "APPROVE",
    "confidence_percentage": 88,
    "confidence_level": "High",
    "decision_rationale": "Strong financial profile with excellent credit, stable employment, low DTI..."
  },
  "key_decision_factors": [
    "Excellent credit score (780)",
    "Low DTI ratio (0.27)",
    "Stable long-term employment (10 years)",
    "Strong income relative to loan amount",
    "Low property LTV (50%)"
  ]
}
```

### Agent4 Expected Output

```json
{
  "decision_recording": {
    "case_id": "CASE-SCENARIO1_STRONG-{timestamp}",
    "decision_classification": "APPROVE",
    "decision_timestamp": "2026-05-25T..."
  },
  "applicant_notification": {
    "notification_type": "approval",
    "message_preview": "Congratulations! Your loan application has been approved..."
  }
}
```

### Expected Metrics

| Metric | Expected Value | Actual Value |
|--------|-----------------|--------------|
| **Decision** | APPROVE | ? |
| **Confidence** | 85-95% | ? |
| **Risk Score** | < 2.0 | ? |
| **Risk Level** | Low | ? |
| **DTI** | 0.27 | ? |
| **Credit Score** | 780 | ? |

### Expected Next Steps
1. Prepare loan documents
2. Schedule closing appointment
3. Arrange final verification

---

## Scenario 2: Weak Applicant - REJECT

### Description
A financially distressed applicant with poor credit, recent job change, very high debt relative to income, and multiple red flags. Should be rejected.

### Test Data

```json
{
  "applicant_id": "SCENARIO2_WEAK",
  "age": 35,
  "annual_income": 50000,
  "employment_type": "employed",
  "credit_score": 580,
  "loan_amount": 300000,
  "tenure_months": 360,
  "existing_liabilities": 2500,
  "location": "TX",
  "monthly_expenses": 2500,
  "delinquencies": 2,
  "inquiries_last_6_months": 6,
  "credit_utilization": 0.85,
  "years_at_current_job": 0.08,
  "existing_loans": 3,
  "property_value": 320000,
  "email": "weak.applicant@example.com",
  "phone": "+1-555-0200"
}
```

### Profile Analysis

**Applicant Profile:**
- 35 years old (working years)
- Poor credit score: **580** (Poor tier - below 620)
- Annual income: **$50,000** (Modest)
- Employment: **~1 month at current job** (Very unstable)
- Monthly income: **$4,167**

**Financial Situation:**
- Current monthly debt: **$2,500** (Extremely high)
- Monthly expenses: **$2,500**
- Debt-to-income ratio: **0.60** (Critical - far exceeds 0.43 threshold)

**Loan Details:**
- Requested loan: **$300,000** (6x annual income - unrealistic)
- Loan term: **360 months** (30 years)
- Monthly payment: **~$833**
- **New DTI with loan: 0.80** ⚠️ **EXCEEDS ALL THRESHOLDS**

**Credit History:**
- Delinquencies: **2** (Recent problems)
- Recent inquiries: **6 in 6 months** (Desperate credit shopping)
- Credit utilization: **85%** (Very high - near limits)
- Existing loans: **3** (Over-extended)

**Property:**
- Property value: **$320,000**
- LTV: **94%** (0.94 - Very high risk, near 0.95 auto-escalate threshold)

### Multiple Escalation Triggers

1. ❌ **DTI > 0.50** (Actual: 0.80) - Auto-escalate trigger
2. ❌ **LTV > 0.80** (Actual: 0.94) - Auto-escalate trigger
3. ❌ **Credit score < 620** (Actual: 580) - Poor credit
4. ❌ **Recent delinquencies** (2 in recent years)
5. ❌ **Recent job change < 1 year** (Actual: 1 month)
6. ❌ **Multiple recent inquiries** (6 in 6 months)
7. ❌ **High credit utilization** (85%)

### Agent1 Expected Output

```json
{
  "profile_assessment": {
    "income_stability": {
      "stability_score": 1.2,
      "stability_level": "very_unstable",
      "assessment": "Critical instability - employment tenure of only 1 month..."
    },
    "credit_profile": {
      "quality_score": 1.3,
      "quality_level": "poor",
      "assessment": "Poor credit profile with 580 score, 2 recent delinquencies..."
    }
  },
  "profile_flags": {
    "red_flags": [
      {
        "flag": "Recent employment change",
        "severity": "critical",
        "description": "Employment tenure of only 1 month"
      },
      {
        "flag": "Multiple recent delinquencies",
        "severity": "critical",
        "description": "2 delinquencies in recent years"
      },
      {
        "flag": "High credit utilization",
        "severity": "high",
        "description": "Using 85% of available credit"
      }
    ]
  },
  "overall_profile_strength": 1.5
}
```

### Agent2 Expected Output

```json
{
  "risk_analysis": {
    "financial_metrics": {
      "debt_to_income_ratio": 0.60,
      "loan_to_value_ratio": 0.94,
      "debt_to_income_with_new_loan": 0.80,
      "financial_viability": "unviable",
      "repayment_capacity": "inadequate"
    }
  },
  "risk_assessment": {
    "overall_risk_score": 4.8,
    "overall_risk_level": "high",
    "risk_category": "escalate"
  },
  "threshold_analysis": {
    "dti_status": {
      "dti_with_loan": 0.80,
      "status": "high_risk"
    },
    "ltv_status": {
      "ltv_ratio": 0.94,
      "status": "high_risk"
    }
  }
}
```

### Agent3 Expected Output

```json
{
  "decision": {
    "classification": "REJECT",
    "confidence_percentage": 92,
    "confidence_level": "Very High",
    "decision_rationale": "Multiple critical risk factors: DTI 0.80 (exceeds threshold), LTV 0.94 (near escalation), poor credit (580), recent delinquencies, employment less than 1 month..."
  },
  "key_decision_factors": [
    "Debt-to-income ratio 0.80 (far exceeds 0.50 limit)",
    "LTV ratio 0.94 (high risk)",
    "Poor credit score (580)",
    "Recent delinquencies (2)",
    "Recent job change (1 month)",
    "High credit utilization (85%)",
    "Loan amount 6x annual income"
  ]
}
```

### Expected Metrics

| Metric | Expected Value | Actual Value |
|--------|-----------------|--------------|
| **Decision** | REJECT | ? |
| **Confidence** | 75-95% | ? |
| **Risk Score** | > 4.0 | ? |
| **Risk Level** | High | ? |
| **DTI** | 0.80 | ? |
| **Credit Score** | 580 | ? |

### Expected Rejection Reasons
1. DTI exceeds lending threshold
2. LTV exceeds lending threshold
3. Poor credit history
4. Recent delinquencies
5. Inadequate employment history
6. High credit utilization

---

## Scenario 3: Moderate Applicant - REVIEW

### Description
A borderline applicant with mixed signals: fair credit, stable employment, but borderline DTI and moderate overall profile. Requires manual review by underwriter to make final decision.

### Test Data

```json
{
  "applicant_id": "SCENARIO3_MODERATE",
  "age": 40,
  "annual_income": 120000,
  "employment_type": "employed",
  "credit_score": 720,
  "loan_amount": 280000,
  "tenure_months": 360,
  "existing_liabilities": 1500,
  "location": "NY",
  "monthly_expenses": 3000,
  "delinquencies": 0,
  "inquiries_last_6_months": 2,
  "credit_utilization": 0.45,
  "years_at_current_job": 5,
  "existing_loans": 2,
  "property_value": 450000,
  "email": "moderate.applicant@example.com",
  "phone": "+1-555-0300"
}
```

### Profile Analysis

**Applicant Profile:**
- 40 years old
- Fair credit score: **720** (Good tier - borderline)
- Annual income: **$120,000** (Moderate)
- Employment: **5 years at current job** (Stable)
- Monthly income: **$10,000**

**Financial Situation:**
- Current monthly debt: **$1,500** (Moderate)
- Monthly expenses: **$3,000** (Reasonable)
- Debt-to-income ratio: **0.15** (Excellent)

**Loan Details:**
- Requested loan: **$280,000** (2.3x annual income - reasonable)
- Loan term: **360 months**
- Monthly payment: **~$778**
- **New DTI with loan: 0.39** ⚠️ **Borderline - just above 0.36 threshold**

**Credit History:**
- Delinquencies: **0** (Clean)
- Recent inquiries: **2 in 6 months** (Moderate - acceptable)
- Credit utilization: **45%** (Good - moderate)
- Existing loans: **2** (Manageable)

**Property:**
- Property value: **$450,000**
- LTV: **62%** (0.62 - Moderate risk)

### Why REVIEW?

**Positive Factors:**
- ✅ Clean credit history (no delinquencies)
- ✅ Stable employment (5 years)
- ✅ Good credit score (720)
- ✅ Reasonable income
- ✅ Manageable credit utilization

**Concerns:**
- ⚠️ DTI after loan is borderline (0.39 vs 0.36 threshold)
- ⚠️ Credit score is fair tier, not good tier (720 vs 740)
- ⚠️ Multiple existing obligations (2 loans)
- ⚠️ DTI falls in 0.36-0.43 "concerning" range

**Decision**: Neither clear APPROVE nor REJECT. Requires senior underwriter judgment.

### Agent1 Expected Output

```json
{
  "profile_assessment": {
    "income_stability": {
      "stability_score": 3.8,
      "stability_level": "stable",
      "assessment": "Stable employment history with 5 years at current position..."
    },
    "credit_profile": {
      "quality_score": 3.6,
      "quality_level": "good",
      "assessment": "Good credit profile with 720 score, no delinquencies..."
    }
  },
  "profile_flags": {
    "red_flags": [],
    "special_cases": []
  },
  "overall_profile_strength": 3.7
}
```

### Agent2 Expected Output

```json
{
  "risk_analysis": {
    "financial_metrics": {
      "debt_to_income_ratio": 0.15,
      "loan_to_value_ratio": 0.62,
      "debt_to_income_with_new_loan": 0.39,
      "financial_viability": "adequate",
      "repayment_capacity": "adequate"
    },
    "credit_risk": {
      "credit_risk_score": 2.8
    }
  },
  "risk_assessment": {
    "overall_risk_score": 2.6,
    "overall_risk_level": "medium",
    "risk_category": "manual_review"
  },
  "threshold_analysis": {
    "dti_status": {
      "dti_with_loan": 0.39,
      "status": "concerning"
    }
  }
}
```

### Agent3 Expected Output

```json
{
  "decision": {
    "classification": "REVIEW",
    "confidence_percentage": 58,
    "confidence_level": "Medium",
    "decision_rationale": "Borderline case with mixed signals. DTI of 0.39 exceeds standard threshold but applicant has stable employment, clean credit, and adequate income. Requires manual underwriter review..."
  },
  "key_decision_factors": [
    "DTI ratio 0.39 (borderline - above 0.36 threshold)",
    "Good credit score (720)",
    "Stable employment (5 years)",
    "No delinquencies",
    "Moderate LTV (62%)"
  ],
  "approval_conditions": {
    "classification": "CONDITIONAL_APPROVE",
    "conditions_if_conditional": [
      {
        "condition": "Income verification",
        "requirement": "Recent pay stubs and tax returns"
      },
      {
        "condition": "Lower loan amount",
        "requirement": "Reduce to $250,000 to bring DTI below 0.36"
      }
    ]
  }
}
```

### Expected Metrics

| Metric | Expected Value | Actual Value |
|--------|-----------------|--------------|
| **Decision** | REVIEW | ? |
| **Confidence** | 40-75% | ? |
| **Risk Score** | 2.0-3.5 | ? |
| **Risk Level** | Medium | ? |
| **DTI** | 0.39 | ? |
| **Credit Score** | 720 | ? |

### Expected Next Steps
1. Escalate to senior underwriter
2. Request additional documentation
3. Verify income (pay stubs, tax returns)
4. Consider conditions for approval
5. Consider alternative loan amount

---

## Running the Test Script

### Prerequisites

Ensure all 6 services are running:

```bash
# Terminal 1: MCP App Server
python mcp/server.py

# Terminal 2: MCP Risk DB
python mcp/riskrulesdb/server.py

# Terminal 3: MCP Decision Synthesis
python mcp/decisionsynthesis/server.py

# Terminal 4: MCP Notification System
python mcp/notificationsystem/server.py

# Terminal 5: FastAPI Server
python src/api/main.py

# Terminal 6: Streamlit UI (optional)
streamlit run src/ui/streamlit_app.py
```

### Run the Test

```bash
cd /path/to/LoanApprovalSystem/LoanApprovalSystem

# Run basic test
python tests/test_loan_scenarios.py

# Run with verbose output
python tests/test_loan_scenarios.py --verbose

# Save results to JSON file
python tests/test_loan_scenarios.py --save-results
```

### Expected Output

```
================================================================================
  LOAN APPROVAL SYSTEM - COMPREHENSIVE TEST SUITE
================================================================================

>>> Pre-Test Verification
────────────────────────────────────────────────────────────────────────────────
ℹ️  Checking API connectivity...
✅ API is healthy and running

================================================================================
  Running Test Scenarios
================================================================================

>>> Scenario 1: Strong Applicant
────────────────────────────────────────────────────────────────────────────────
ℹ️  Excellent credit, stable employment, high income, low debt -> APPROVE

Test Data Summary:
  Applicant ID: SCENARIO1_STRONG
  Age: 45
  Income: $200,000
  Credit Score: 780
  ...

📤 Submitting application...
✅ Response received in 2.34s

Decision Details:
  Classification: APPROVE
  Confidence: 88%
  Risk Score: 1.80/5.0
  Risk Level: Low
  Case ID: CASE-SCENARIO1_STRONG-1716633001

🔍 Validation Checks:
✅ Output structure valid
✅ Decision matches (expected APPROVE, got APPROVE)
✅ Confidence 88% is within range [85%, 95%]
✅ Risk level matches (Low)

✅ Scenario 1: Strong Applicant PASSED

>>> Scenario 2: Weak Applicant
────────────────────────────────────────────────────────────────────────────────
ℹ️  Poor credit, recent job, low income, high debt, delinquencies -> REJECT

...

✅ Response received in 2.56s

Decision Details:
  Classification: REJECT
  Confidence: 92%
  Risk Score: 4.75/5.0
  Risk Level: High
  Case ID: CASE-SCENARIO2_WEAK-1716633004

🔍 Validation Checks:
✅ Output structure valid
✅ Decision matches (expected REJECT, got REJECT)
✅ Confidence 92% is within range [75%, 95%]
✅ Risk level matches (High)

✅ Scenario 2: Weak Applicant PASSED

>>> Scenario 3: Moderate Applicant
────────────────────────────────────────────────────────────────────────────────
ℹ️  Fair credit, stable employment, moderate income -> REVIEW

...

✅ Response received in 2.41s

Decision Details:
  Classification: REVIEW
  Confidence: 58%
  Risk Score: 2.61/5.0
  Risk Level: Medium
  Case ID: CASE-SCENARIO3_MODERATE-1716633007

🔍 Validation Checks:
✅ Output structure valid
✅ Decision matches (expected REVIEW, got REVIEW)
✅ Confidence 58% is within range [40%, 75%]
✅ Risk level matches (Medium)

✅ Scenario 3: Moderate Applicant PASSED

================================================================================
  TEST SUMMARY
================================================================================

Total Scenarios: 3
✅ Passed: 3
⚠️  Partial: 0
❌ Failed: 0
❌ Error: 0

Scenario Results
✅ Scenario 1: Strong Applicant
   Expected: APPROVE
   Actual: APPROVE
   Status: PASS

✅ Scenario 2: Weak Applicant
   Expected: REJECT
   Actual: REJECT
   Status: PASS

✅ Scenario 3: Moderate Applicant
   Expected: REVIEW
   Actual: REVIEW
   Status: PASS

✅ Results saved to test_results_20260525_143000.json
```

---

## Test Validation Criteria

### Scenario 1 Success Criteria

✅ Decision = APPROVE (or CONDITIONAL_APPROVE)
✅ Confidence between 85-95%
✅ Risk level = Low
✅ DTI <= 0.36
✅ No escalation triggers
✅ Clear approval reasoning

### Scenario 2 Success Criteria

✅ Decision = REJECT
✅ Confidence between 75-95%
✅ Risk level = High
✅ DTI > 0.50 (or other escalation trigger)
✅ Multiple risk factors documented
✅ Clear rejection reasoning

### Scenario 3 Success Criteria

✅ Decision = REVIEW (or CONDITIONAL_APPROVE with conditions)
✅ Confidence between 40-75%
✅ Risk level = Medium
✅ DTI in borderline range (0.36-0.43)
✅ Mixed positive/negative factors
✅ Clear escalation reasoning

---

## Interpreting Results

### If All Tests Pass ✅

The system is working correctly:
- Agent1 accurately analyzes profiles
- Agent2 calculates risk metrics correctly
- Agent3 makes appropriate decisions
- Agent4 records decisions properly
- Complete pipeline is functional

### If Some Tests Fail ❌

Check:
1. Are all MCP servers running?
2. Is FastAPI server running?
3. Are there API errors in logs?
4. Are decision thresholds correct?
5. Are calculations accurate?

### If Results Are Unexpected ⚠️

Possible issues:
- Threshold values may differ from defaults
- Scoring methodology may be customized
- Agent prompts may be modified
- Risk calculation may vary
- Confidence calculation may differ

---

## Customizing Test Data

To add more scenarios or modify existing ones:

1. Create new test data function
2. Create new TestScenario object
3. Add to SCENARIOS list
4. Run test script

Example:

```python
def create_custom_applicant_data():
    return {
        "applicant_id": "CUSTOM_001",
        "age": 45,
        # ... your test data
    }

custom_scenario = TestScenario(
    name="Custom Scenario",
    description="Your description",
    test_data=create_custom_applicant_data(),
    expected_decision="APPROVE",
    expected_confidence_min=85,
    expected_confidence_max=95,
    # ... other fields
)

SCENARIOS.append(custom_scenario)
```

---

**Version:** 2.0.0  
**Last Updated:** 2026-05-25  
**Status:** Ready for Testing ✅
