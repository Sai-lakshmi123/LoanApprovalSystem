# Error Handling & Retry Logic - Complete Guide

## Overview

The enhanced LangGraph Orchestration Engine includes comprehensive error handling and intelligent retry logic to make the loan approval workflow more robust and resilient.

**Key Features:**
- Automatic retry with exponential backoff
- Error categorization (transient vs permanent)
- Circuit breaker pattern to prevent cascading failures
- Manual review escalation on critical failures
- Comprehensive error tracking and logging
- Fallback decision mechanisms

---

## Error Categorization

### Error Types

All errors are categorized into one of three categories:

#### TRANSIENT Errors (Retry Recommended)
**Definition**: Temporary issues that may resolve on retry

**Examples:**
- Connection timeouts
- Service unavailable (503)
- Rate limiting
- Temporary network issues
- DNS resolution failures

**Action**: Retry with exponential backoff

**Example:**
```
❌ Connection timeout to RiskRulesDB
⚠️ Attempt 1 failed (Transient): Connection timed out
⏳ Retrying in 1.0s...
```

#### PERMANENT Errors (No Retry)
**Definition**: Errors that won't resolve on retry

**Examples:**
- Invalid API key
- Authentication failures
- Bad request (400)
- Not found (404)
- Invalid data format
- Business logic violations

**Action**: Fail immediately, escalate to manual review

**Example:**
```
❌ Permanent error - no retry: Invalid applicant data
Agent escalated to manual review due to permanent error
```

#### UNKNOWN Errors (Retry with Caution)
**Definition**: Unclear categorization

**Examples:**
- Unexpected exceptions
- Custom error messages
- Unclassified failures

**Action**: Retry with exponential backoff, with limit

---

## Retry Configuration

### Per-Agent Retry Settings

Each agent has its own retry configuration optimized for its function:

```python
RETRY_CONFIGS = {
    "agent1": RetryConfig(max_retries=3, base_delay=1.0, backoff_factor=2.0),
    "agent2": RetryConfig(max_retries=3, base_delay=2.0, backoff_factor=2.0),
    "agent3": RetryConfig(max_retries=2, base_delay=1.5, backoff_factor=2.0),
    "agent4": RetryConfig(max_retries=1, base_delay=1.0, backoff_factor=2.0),
}
```

### Exponential Backoff Strategy

Delay between retries = `base_delay * (backoff_factor ^ attempt_number)`

**Agent1 Example:**
```
Attempt 1: Immediate
Attempt 2: 1.0s delay
Attempt 3: 2.0s delay
Attempt 4: 4.0s delay
```

**Agent2 Example (longer delays for network operations):**
```
Attempt 1: Immediate
Attempt 2: 2.0s delay
Attempt 3: 4.0s delay
Attempt 4: 8.0s delay
```

### Customizing Retry Configuration

```python
# Modify in LoanDecisionOrchestrator class
RETRY_CONFIGS = {
    "agent1": RetryConfig(max_retries=5, base_delay=0.5, backoff_factor=2.0),
    # ... other agents
}
```

---

## State Tracking

### New State Fields

All agents now track retry attempts and history:

```python
state["profile_retry_count"]       # Number of retries performed
state["profile_retry_history"]     # List of all retry attempts with details
state["risk_retry_count"]
state["risk_retry_history"]
state["decision_retry_count"]
state["decision_retry_history"]
state["action_retry_count"]
state["action_retry_history"]

# Error tracking
state["critical_errors"]           # List of critical errors
state["error_escalation"]          # Whether escalated to manual review
state["manual_review_reason"]      # Reason for escalation
```

### Retry History Structure

Each retry attempt is tracked:

```python
{
    "attempt": 1,
    "error": "Connection timeout",
    "exception_type": "TimeoutError",
    "timestamp": "2026-05-25T10:30:01"
}
```

---

## Execution Flows

### Successful Path (No Retries)

```
Agent1_Profile_✅
  ↓
Agent2_Risk_✅
  ↓
Routing_auto_approve
  ↓
Agent3_Decision_✅
  ↓
Agent4_Compliance_✅
  ↓
workflow_status: success
```

### Transient Error Path (Retry Succeeds)

```
Agent1 Attempt 1 ❌ (Transient error: timeout)
  ↓ Wait 1.0s
Agent1 Attempt 2 ❌ (Transient error: timeout)
  ↓ Wait 2.0s
Agent1 Attempt 3 ✅ (Success)
  ↓
Agent1_Profile_✅
```

### Permanent Error Path (Immediate Escalation)

```
Agent2 Attempt 1 ❌ (Permanent error: Invalid data)
  ↓ No retry
Agent2_Risk_PermanentError
  ↓
Routing_ManualReview (Error escalation)
  ↓
Agent3 receives manual_review routing
  ↓
Fallback REVIEW decision
```

### Max Retries Exceeded Path

```
Agent3 Attempt 1 ❌ (Transient error)
  ↓ Wait 1.5s
Agent3 Attempt 2 ❌ (Transient error)
  ↓ No more retries (max_retries=2)
Agent3_Decision_MaxRetriesExceeded
  ↓
Fallback REVIEW decision with confidence=20%
  ↓
Agent4 processes fallback decision
```

### Error Escalation Path

```
Agent2 fails with permanent error
  ↓
routing_decision = "manual_review"
error_escalation = True
manual_review_reason = "Agent2 permanent error: ..."
  ↓
Agent3 creates fallback REVIEW decision
  ↓
Agent4 records with escalation flag
  ↓
workflow_status = "error_with_fallback"
```

---

## Fallback Mechanisms

### Agent3 Fallback Decision

If Agent3 fails (error or max retries), a fallback decision is created:

```python
state["decision_data"] = {
    "decision": {
        "classification": "REVIEW",
        "risk_score": state["risk_score"],
        "confidence_level": "Low" or "Very Low",
        "confidence_percentage": 20 or 10,
        "reasoning": "Decision synthesis failed: [error message]"
    }
}
state["decision_status"] = "fallback"
```

**Fallback Decision Routing:**
```
Transient Error:
  classification: REVIEW
  confidence_percentage: 20
  
Permanent Error:
  classification: REVIEW
  confidence_percentage: 10
  
Exception:
  classification: REVIEW
  confidence_percentage: 10
```

### Agent4 Non-Critical Failure

If Agent4 fails after decision is made:
- Decision data persists
- Notifications may not be sent
- Case ID may not be generated
- status = "error"
- But workflow continues to finalize

---

## Manual Review Escalation

### When Manual Review is Triggered

1. **Agent1 Permanent Error**
   - Invalid applicant data
   - Data format errors
   - Missing required fields

2. **Agent2 Permanent Error**
   - Invalid financial data
   - Cannot calculate risk metrics
   - Escalates routing to "manual_review"

3. **Critical Error During Processing**
   - Multiple agent failures
   - error_escalation flag set
   - Manual review reason recorded

### Manual Review Behavior

When routing = "manual_review":

```
Agent3 Strategy: Conservative
  └─ More strict criteria
  └─ Likely outcome: REVIEW or conditional with conditions

Agent3 Fallback Decision:
  └─ classification: REVIEW
  └─ confidence_percentage: 20-30
  └─ reasoning: "Manual review required"

Next Steps Include:
  └─ "Escalate to senior underwriter"
  └─ "Request additional documentation"
  └─ "Manual underwriter review required"
```

---

## Error Reporting

### Final Decision Error Summary

```python
state["final_decision"]["error_handling"] = {
    "critical_errors": [
        {
            "agent": "Agent2",
            "error": "Connection to RiskRulesDB failed",
            "exception_type": "ConnectionError",
            "category": "transient"
        }
    ],
    "error_count": 1,
    "error_escalation": True,
    "retry_statistics": {
        "agent1_retries": 0,
        "agent2_retries": 3,
        "agent3_retries": 0,
        "agent4_retries": 0,
        "total_retries": 3
    }
}
```

### Workflow Status Values

```
success                    # All agents succeeded, no errors
error                     # Fatal error, no fallback
error_with_fallback       # Error but fallback decision created
partial_success           # Some agents failed, workflow continued
```

---

## Example Scenarios

### Scenario 1: Transient Connection Error (RECOVERED)

**Flow:**
```
Agent2 - Risk Analysis
  Attempt 1: ❌ Timeout (Connection refused)
  Wait: 2.0s
  Attempt 2: ❌ Timeout (Connection refused)
  Wait: 4.0s
  Attempt 3: ✅ Success

workflow_status: success
retry_statistics.agent2_retries: 3
critical_errors: []
```

**Output:**
```
⚠️  Attempt 1 failed (Transient): Connection refused
⏳ Retrying in 2.0s...
⚠️  Attempt 2 failed (Transient): Connection refused
⏳ Retrying in 4.0s...
✅ Risk analysis complete (Attempt 3)
```

### Scenario 2: Permanent API Error (ESCALATED)

**Flow:**
```
Agent2 - Risk Analysis
  Attempt 1: ❌ Invalid API Key (Permanent)
  No retry

routing_decision: manual_review
error_escalation: True
critical_errors: [Agent2 error]

Agent3: Creates fallback REVIEW decision
workflow_status: error_with_fallback
```

**Output:**
```
❌ Permanent error - no retry: Invalid API key
Agent2_Risk_PermanentError

🔀 Routing Decision
⚠️  Critical errors detected - Escalating to manual review

⚖️  Decision Synthesis
Decision using fallback (error escalation)
Classification: REVIEW
Confidence: 20%

workflow_status: error_with_fallback
```

### Scenario 3: Max Retries Exceeded (FALLBACK)

**Flow:**
```
Agent3 - Decision Synthesis
  Attempt 1: ❌ Transient error
  Wait: 1.5s
  Attempt 2: ❌ Transient error
  No more retries (max_retries=2)

Creates fallback decision
workflow_status: error_with_fallback
```

**Output:**
```
⚠️  Attempt 1 failed (Transient): Timeout
⏳ Retrying in 1.5s...
⚠️  Attempt 2 failed (Transient): Timeout
❌ All 3 attempts failed

Agent3_Decision_MaxRetriesExceeded
Creating fallback REVIEW decision
Confidence: 20%
```

---

## Monitoring & Debugging

### Check Retry History

```python
# Agent1 retry history
for attempt in final_state["profile_retry_history"]:
    print(f"Attempt {attempt['attempt']}: {attempt['error']}")

# Total retries across all agents
total = final_state["final_decision"]["error_handling"]["retry_statistics"]["total_retries"]
print(f"Total retries: {total}")
```

### Check Critical Errors

```python
# See all critical errors
for error in final_state["critical_errors"]:
    print(f"{error['agent']}: {error['error']}")
    print(f"  Category: {error['category']}")
    print(f"  Exception: {error.get('exception_type', 'N/A')}")
```

### Check Error Escalation

```python
if final_state["error_escalation"]:
    print(f"Manual review escalation: {final_state['manual_review_reason']}")
```

---

## Best Practices

### 1. Monitor Retry Counts
- High retry counts indicate infrastructure issues
- Consider increasing base_delay if retries are frequent
- May indicate need for system improvements

### 2. Analyze Error Categories
- Track which errors are transient vs permanent
- Transient → System reliability issue
- Permanent → Data validation or integration issue

### 3. Review Fallback Decisions
- Fallback decisions should be rare
- High fallback rate indicates system reliability issues
- May need manual review queue for quality assurance

### 4. Adjust Retry Configuration
```python
# For unreliable network
"agent2": RetryConfig(max_retries=5, base_delay=3.0, backoff_factor=2.0)

# For reliable services, reduce retries
"agent1": RetryConfig(max_retries=2, base_delay=0.5, backoff_factor=2.0)
```

### 5. Log and Alert
- Log all critical errors for operational visibility
- Alert on high error rates
- Track error trends over time

---

## Configuration Recommendations

### Development Environment
```python
RETRY_CONFIGS = {
    "agent1": RetryConfig(max_retries=2, base_delay=0.5, backoff_factor=1.5),
    "agent2": RetryConfig(max_retries=2, base_delay=1.0, backoff_factor=1.5),
    "agent3": RetryConfig(max_retries=1, base_delay=0.5, backoff_factor=1.5),
    "agent4": RetryConfig(max_retries=0, base_delay=0, backoff_factor=1.0),
}
```

### Production Environment
```python
RETRY_CONFIGS = {
    "agent1": RetryConfig(max_retries=3, base_delay=1.0, backoff_factor=2.0),
    "agent2": RetryConfig(max_retries=4, base_delay=2.0, backoff_factor=2.0),
    "agent3": RetryConfig(max_retries=2, base_delay=1.5, backoff_factor=2.0),
    "agent4": RetryConfig(max_retries=2, base_delay=1.0, backoff_factor=2.0),
}
```

### High-Availability Environment
```python
RETRY_CONFIGS = {
    "agent1": RetryConfig(max_retries=5, base_delay=1.0, backoff_factor=2.0),
    "agent2": RetryConfig(max_retries=5, base_delay=3.0, backoff_factor=2.0),
    "agent3": RetryConfig(max_retries=3, base_delay=2.0, backoff_factor=2.0),
    "agent4": RetryConfig(max_retries=3, base_delay=1.5, backoff_factor=2.0),
}
```

---

## Troubleshooting

### High Retry Count (> 5 retries per workflow)
**Possible Causes:**
- Network latency
- Service overload
- DNS issues
- Firewall/proxy problems

**Solutions:**
- Increase `base_delay`
- Check service health
- Review network connectivity
- Implement circuit breaker

### Frequent Fallback Decisions
**Possible Causes:**
- Service unavailability
- Data quality issues
- Integration problems

**Solutions:**
- Check service logs
- Validate data format
- Review error messages
- Implement monitoring

### Permanent Errors on First Attempt
**Possible Causes:**
- Invalid API key
- Bad request data
- Schema validation failure

**Solutions:**
- Verify credentials
- Validate input data
- Check API compatibility
- Review error messages

---

**Last Updated:** 2026-05-25  
**Version:** 1.0.0
