# Error Handling & Retry Logic - Quick Reference

## At a Glance

| Component | Retries | Delay | Purpose |
|-----------|---------|-------|---------|
| Agent1 (Profile) | 3x | 1-4s | Profile data analysis |
| Agent2 (Risk) | 3x | 2-8s | Financial risk assessment |
| Agent3 (Decision) | 2x | 1.5-6s | Decision synthesis |
| Agent4 (Compliance) | 1x | 1s | Compliance recording |

## Error Categories

### 🟢 TRANSIENT (Retry)
- Connection timeout
- Service unavailable (503)
- Rate limiting
- Network issues

**Result:** Automatic retry with backoff

### 🔴 PERMANENT (Escalate)
- Invalid API key
- Bad request (400)
- Not found (404)
- Invalid data

**Result:** Immediate escalation to manual review

### 🟡 UNKNOWN (Retry with Caution)
- Unexpected exceptions
- Custom errors

**Result:** Retry with backoff (limit 3x)

---

## Example: Retry Flow

```
Attempt 1: ❌ Timeout
  ↓ Wait 2s
Attempt 2: ❌ Timeout
  ↓ Wait 4s
Attempt 3: ✅ Success
```

---

## Manual Review Escalation

Triggered when:
- Agent2 permanent error
- Multiple critical errors
- System failure detected

Result:
- `routing_decision = "manual_review"`
- `error_escalation = True`
- Fallback REVIEW decision created
- Senior underwriter assigned

---

## Fallback Decisions

### When Created
- Agent3 fails (error or max retries)
- Agent4 connection lost

### What It Does
```json
{
    "classification": "REVIEW",
    "confidence_percentage": 20,
    "reasoning": "Decision synthesis failed: [error]"
}
```

### Result
- Application still gets decision
- Marked for manual review
- Low confidence score
- Escalated to underwriter

---

## State Tracking

### New Fields (All Agents)
```python
state["agent_X_retry_count"]        # Number of retries
state["agent_X_retry_history"]      # All attempts with errors
```

### Error Tracking
```python
state["critical_errors"]            # List of all errors
state["error_escalation"]           # Manual review flag
state["manual_review_reason"]       # Why escalated
```

### Final Report
```python
state["final_decision"]["error_handling"] = {
    "critical_errors": [...],
    "error_count": 1,
    "retry_statistics": {
        "total_retries": 3,
        "agent1_retries": 0,
        "agent2_retries": 3,
        ...
    }
}
```

---

## Workflow Status Values

| Status | Meaning |
|--------|---------|
| `success` | All agents succeeded ✅ |
| `error` | Fatal error, no fallback ❌ |
| `error_with_fallback` | Error + fallback decision ⚠️ |
| `partial_success` | Some agents failed, continued ⏳ |

---

## Output Examples

### Successful (No Retries)
```
Agent2: Risk Analysis
✅ Risk analysis complete (Attempt 1)
   Risk Score: 1.8/5
```

### Transient Error (Recovered)
```
Agent2: Risk Analysis
⚠️  Attempt 1 failed (Transient): Connection timeout
⏳ Retrying in 2.0s...
✅ Risk analysis complete (Attempt 2)
   Risk Score: 2.3/5
```

### Permanent Error (Escalated)
```
Agent2: Risk Analysis
❌ Permanent error - no retry: Invalid API key
Agent2_Risk_PermanentError

ROUTING DECISION
⚠️  Critical errors detected - Escalating to manual review

Routing: manual_review
error_escalation: True
```

### Max Retries (Fallback)
```
Agent3: Decision Synthesis
⚠️  Attempt 1 failed (Transient): Timeout
⏳ Retrying in 1.5s...
⚠️  Attempt 2 failed (Transient): Timeout
❌ All 3 attempts failed

Agent3_Decision_MaxRetriesExceeded
Creating fallback REVIEW decision
Confidence: 20%
```

---

## Customization

### Increase Retries for Unreliable Network
```python
RETRY_CONFIGS = {
    "agent2": RetryConfig(max_retries=5, base_delay=3.0, backoff_factor=2.0),
    ...
}
```

### Reduce Retries for Fast-Fail
```python
RETRY_CONFIGS = {
    "agent1": RetryConfig(max_retries=1, base_delay=0.5, backoff_factor=1.5),
    ...
}
```

---

## Debugging

### View Retry History
```python
for attempt in final_state["risk_retry_history"]:
    print(f"Attempt {attempt['attempt']}: {attempt['error']}")
```

### Check All Errors
```python
for error in final_state["critical_errors"]:
    print(f"{error['agent']}: {error['error']}")
```

### Check Escalation
```python
if final_state["error_escalation"]:
    print(f"Escalated: {final_state['manual_review_reason']}")
```

### View Retry Statistics
```python
retry_stats = final_state["final_decision"]["error_handling"]["retry_statistics"]
print(f"Total retries: {retry_stats['total_retries']}")
```

---

## Common Scenarios

### 🟢 Normal Success (No Issues)
```
Agent1 ✅ → Agent2 ✅ → Agent3 ✅ → Agent4 ✅
workflow_status: success
retry_statistics.total_retries: 0
```

### 🟡 Transient Failure, Recovered
```
Agent2 ❌ (timeout) → Retry → ✅
workflow_status: success
retry_statistics.agent2_retries: 2
```

### 🔴 Permanent Error, Escalated
```
Agent2 ❌ (Invalid API key) → No retry → Escalate
routing_decision: manual_review
error_escalation: True
workflow_status: error_with_fallback
```

### ⚠️ Max Retries, Fallback
```
Agent3 ❌ → Retry ❌ → Max retries → Fallback REVIEW
workflow_status: error_with_fallback
decision_status: fallback
confidence_percentage: 20
```

---

## Metrics to Monitor

### Health Indicators
- **Total retries per day** (should be < 5% of workflows)
- **Fallback decision rate** (should be < 1%)
- **Error escalation rate** (should be < 2%)
- **Average retries when they occur** (should be < 2)

### Red Flags
- ⚠️ Total retries > 10% of workflows
- ⚠️ Fallback rate > 5%
- ⚠️ Same error in multiple attempts
- ⚠️ Permanent errors > transient errors

---

## Checklist: Deployment

- [ ] Verify retry configurations for environment
- [ ] Set up monitoring for retry metrics
- [ ] Configure alerting for high error rates
- [ ] Document error handling for support team
- [ ] Test with intentional service failures
- [ ] Verify fallback decisions create manual review
- [ ] Check error escalation notification works
- [ ] Monitor first week of production

---

**More Details:** See `ERROR_HANDLING_GUIDE.md` for comprehensive documentation

**Last Updated:** 2026-05-25
