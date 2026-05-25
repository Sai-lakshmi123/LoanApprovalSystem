# NotificationSystem MCP Server - Implementation Guide

## Overview

NotificationSystem is the final compliance layer in the loan approval system. It records all loan decision actions with full audit trails and manages notifications to applicants and internal stakeholders.

**Key Features:**
- Records compliance actions with unique case IDs
- Sends notifications to multiple stakeholder types
- Tracks notification delivery status
- Generates compliance reports
- Maintains fair lending audit trails
- Supports resending failed notifications

---

## Architecture

### System Integration

```
DecisionSynthesis (Port 3002)
    ↓ (final decision)
    
    NotificationSystem (Port 3003)
    
    ↓ (case ID, notifications)
    
Compliance Records & Stakeholder Notifications
```

NotificationSystem is the final step in the loan approval pipeline:
1. Receives final decision from DecisionSynthesis
2. Records decision as compliance action
3. Generates unique case ID
4. Sends notifications to all stakeholders
5. Tracks delivery and maintains audit trail

### Core Components

**ComplianceRecorder Class**
- Manages compliance action recording
- Generates case IDs and notification IDs
- Sends notifications to stakeholders
- Tracks delivery status
- Generates compliance reports

**Case ID Generation**
- Format: `CASE-YYYYMMDD-XXXXX`
- Example: `CASE-20260524-00001`
- Unique sequential number per day
- Timestamp-based organization

**Notification Management**
- Generate unique notification IDs
- Track delivery status
- Support resending
- Monitor by stakeholder type

---

## Data Flow

### Input Schema

#### Decision Input (from DecisionSynthesis)
```python
decision_input = {
    "applicant_id": str,
    "applicant_name": str,
    "applicant_email": str,
    "decision": str,           # APPROVE, CONDITIONAL_APPROVE, REVIEW, REJECT
    "risk_score": float,       # 0-5
    "confidence": str,         # Very High, High, Moderate, Low, Very Low
    "strategy": str,           # Conservative, Balanced, Aggressive
    "reason": str,             # Detailed explanation
    "internal_recipients": [   # Optional
        {
            "name": str,
            "email": str,
            "type": str        # Internal Team, Compliance, Legal, etc.
        }
    ],
    "action_summary": str      # Summary of action taken
}
```

### Output Schema

#### record_and_notify Response
```python
{
    "status": "success",
    "case_id": str,                    # CASE-20260524-00001
    "action_taken": str,               # Approval, Conditional Approval, Review, Rejection
    "decision": str,                   # Original decision classification
    "notifications_sent": int,         # Count of notifications
    "timestamp": str,                  # ISO format
    "summary": {
        "applicant": str,
        "action": str,
        "decision": str,
        "risk_score": float,
        "confidence": str,
        "stakeholders_notified": int,
        "reason": str
    },
    "notification_ids": [str]          # List of notification IDs
}
```

#### get_case_information Response
```python
{
    "status": "success",
    "case": {
        "case_id": str,
        "applicant_id": str,
        "action_type": str,
        "decision": str,
        "risk_score": float,
        "confidence_level": str,
        "strategy_applied": str,
        "timestamp": str,
        "reason": str,
        "recorded_at": str,
        "notifications_sent": [str],
        "audit_trail": {
            "created_by": str,
            "created_at": str,
            "last_modified": str,
            "fair_lending_compliant": bool
        }
    },
    "notifications": [
        {
            "notification_id": str,
            "case_id": str,
            "recipient_type": str,
            "recipient_email": str,
            "recipient_name": str,
            "subject": str,
            "template": str,
            "summary": str,
            "status": str,
            "sent_at": str,
            "delivery_confirmed": bool,
            "delivery_time": str
        }
    ]
}
```

---

## Case ID Management

### Generation Process

```python
Case ID = CASE-{YYYYMMDD}-{XXXXX}

Example: CASE-20260524-00001

Components:
  CASE       = Fixed prefix
  YYYYMMDD   = Current date (2026-05-24)
  XXXXX      = Sequential counter (5 digits, zero-padded)
```

### Sequential Numbering

- Each day starts fresh counter at 00001
- Increments for each case recorded
- Maintains uniqueness within day
- Allows 99,999 cases per day

### Storage

Cases stored in memory (in-memory dict):
```python
compliance_log = {
    "CASE-20260524-00001": {...},
    "CASE-20260524-00002": {...},
    ...
}
```

---

## Notification Management

### Notification ID Format

```
NOTIF-{12-char hex identifier}

Example: NOTIF-ABC123DEF456
```

### Stakeholder Notification Rules

| Stakeholder | Notifications For | Priority | Method |
|---|---|---|---|
| Applicant | All | High | Email + Portal |
| Internal Team | All | High | System + Email |
| Compliance Officer | Reject, Conditional, High-risk | High | Email + Report |
| Legal Team | Rejections | High | Email + Case File |
| Management | REVIEW, Reject | Medium | Dashboard + Email |

### Notification Status

```python
NotificationStatus:
  - SENT        = Successfully sent
  - PENDING     = Queued for sending
  - FAILED      = Delivery failed
  - DELIVERED   = Confirmed delivery
  - BOUNCED     = Email bounced
```

### Template Selection

Templates selected based on decision:

| Decision | Template | Subject |
|---|---|---|
| APPROVE | approval_notification | "Loan Application Approved" |
| CONDITIONAL_APPROVE | conditional_notification | "Loan Application - Conditional Approval" |
| REVIEW | review_notification | "Loan Application Under Review" |
| REJECT | rejection_notification | "Loan Application Decision" |

---

## 5 Core Tools

### 1. record_and_notify (Main Tool)

**Purpose:** Record compliance action and send all notifications in one operation.

**Parameters:**
- `applicant_id` (str): Unique applicant identifier
- `applicant_name` (str): Full name
- `applicant_email` (str): Email address
- `decision` (str): APPROVE, CONDITIONAL_APPROVE, REVIEW, or REJECT
- `risk_score` (float): Risk score 0-5
- `confidence` (str): Confidence level
- `strategy` (str): Strategy applied
- `reason` (str): Detailed reason
- `internal_recipients` (list): Internal stakeholders (optional)
- `action_summary` (str): Summary of action (optional)

**Returns:**
- Complete record with case ID, action taken, notifications sent, timestamp, and summary

**Example:**
```python
from mcp.notificationsystem.client import NotificationSystemSyncClient

client = NotificationSystemSyncClient()

result = client.record_and_notify(
    applicant_id="APP001",
    applicant_name="John Strong",
    applicant_email="john@example.com",
    decision="APPROVE",
    risk_score=1.8,
    confidence="High",
    strategy="Balanced",
    reason="Strong financial profile, meets all criteria",
    internal_recipients=[
        {
            "name": "Jane Underwriter",
            "email": "jane@lender.com",
            "type": "Internal Team"
        }
    ],
    action_summary="Loan approved for $300,000"
)

case_id = result['case_id']
print(f"Case recorded: {case_id}")
print(f"Notifications sent: {result['notifications_sent']}")
```

### 2. get_case_information

**Purpose:** Retrieve complete case details with all notifications and audit trail.

**Parameters:**
- `case_id` (str): Case ID from compliance system

**Returns:**
- Complete case record including all notifications and audit trail

**Example:**
```python
case_info = client.get_case_information("CASE-20260524-00001")

print(f"Decision: {case_info['case']['decision']}")
print(f"Notifications sent: {len(case_info['notifications'])}")

for notif in case_info['notifications']:
    print(f"  {notif['recipient_name']}: {notif['status']}")
```

### 3. check_notification_status

**Purpose:** Check delivery status of specific notification.

**Parameters:**
- `notification_id` (str): Notification ID to check

**Returns:**
- Notification status, delivery info, and timestamps

**Example:**
```python
status = client.check_notification_status("NOTIF-ABC123DEF456")

print(f"Status: {status['status']}")
print(f"Recipient: {status['recipient']}")
print(f"Delivered: {status['delivery_confirmed']}")
```

### 4. get_compliance_report

**Purpose:** Generate compliance report for all cases and notifications.

**Parameters:**
- `start_date` (str, optional): ISO format start date
- `end_date` (str, optional): ISO format end date

**Returns:**
- Comprehensive report with case counts, action types, and notification status

**Example:**
```python
report = client.get_compliance_report()

print(f"Total cases: {report['total_cases']}")
print(f"Total notifications: {report['total_notifications']}")

print("Cases by action:")
for action, count in report['cases_by_action'].items():
    print(f"  {action}: {count}")
```

### 5. resend_notification

**Purpose:** Resend notification if delivery failed.

**Parameters:**
- `case_id` (str): Case ID
- `notification_id` (str): Notification ID to resend

**Returns:**
- Resend status and confirmation

**Example:**
```python
result = client.resend_notification(
    "CASE-20260524-00001",
    "NOTIF-ABC123DEF456"
)

print(f"Status: {result['status']}")
print(f"Resent at: {result['resent_at']}")
```

---

## 3 Reference Resources

### 1. notification://templates/definitions

**What it provides:**
- All notification templates
- Placeholder variables
- Stakeholder requirements
- Priority levels

**Accessing:**
```python
templates = client.get_notification_templates()
```

**Content:**
```
Templates:
  - approval_notification
  - conditional_notification
  - review_notification
  - rejection_notification

Each template includes:
  - Subject line
  - Placeholder variables
  - Required stakeholders
  - Priority level
```

### 2. notification://compliance/rules

**What it provides:**
- Notification timing requirements
- Required information by decision type
- Fair lending compliance rules
- Notification methods

**Accessing:**
```python
rules = client.get_compliance_rules()
```

**Content:**
```
Rules:
  - Notification timing (approval: 1 day, etc.)
  - Required information by decision
  - Fair lending monitoring requirements
  - Accessibility requirements
```

### 3. notification://stakeholders/list

**What it provides:**
- All defined stakeholder types
- Notification requirements per stakeholder
- Notification methods and timing

**Accessing:**
```python
stakeholders = client.get_stakeholder_list()
```

**Content:**
```
Stakeholders:
  - Applicant
  - Internal Team
  - Compliance Officer
  - Legal Team
  - Management

For each:
  - Description
  - When notified
  - Notification method
  - Timing requirements
```

---

## Integration Patterns

### With DecisionSynthesis

```python
from mcp.decisionsynthesis.client import DecisionSynthesisSyncClient
from mcp.notificationsystem.client import NotificationSystemSyncClient

decision_db = DecisionSynthesisSyncClient()
notif_db = NotificationSystemSyncClient()

# Get decision
decision = decision_db.synthesize_loan_decision(
    "APP001", applicant, app_analysis, risk_assessment
)

# Record and notify
result = notif_db.record_and_notify(
    applicant_id="APP001",
    applicant_name=applicant['name'],
    applicant_email=applicant['email'],
    decision=decision['decision']['classification'],
    risk_score=decision['decision']['risk_score'],
    confidence=decision['decision']['confidence_level'],
    strategy=decision['strategy_applied'],
    reason=decision['decision']['reasoning']
)

# Use case ID
print(f"Case ID: {result['case_id']}")
```

### With FastAPI

```python
from fastapi import FastAPI

app = FastAPI()
client = NotificationSystemSyncClient()

@app.post("/record-decision")
async def record_decision(request: dict):
    result = client.record_and_notify(
        applicant_id=request['applicant_id'],
        applicant_name=request['applicant_name'],
        applicant_email=request['applicant_email'],
        decision=request['decision'],
        risk_score=request['risk_score'],
        confidence=request['confidence'],
        strategy=request['strategy'],
        reason=request['reason']
    )
    return result
```

### With LangGraph Workflow

```python
from langgraph.graph import StateGraph

def notification_node(state):
    result = client.record_and_notify(
        applicant_id=state['applicant_id'],
        applicant_name=state['applicant_name'],
        applicant_email=state['applicant_email'],
        decision=state['decision'],
        risk_score=state['risk_score'],
        confidence=state['confidence'],
        strategy=state['strategy'],
        reason=state['reasoning']
    )
    state['case_id'] = result['case_id']
    return state
```

---

## Compliance Features

### Audit Trail

Every action generates audit trail:
```python
audit_trail = {
    "created_by": "DecisionSynthesis",
    "created_at": "2026-05-24T10:30:00",
    "last_modified": "2026-05-24T10:30:00",
    "fair_lending_compliant": True
}
```

### Fair Lending Compliance

System supports:
- Decision documentation with reasoning
- Stakeholder notification tracking
- Consistent notification procedures
- Compliance reporting and monitoring

### Record Retention

Cases maintain:
- Original decision details
- All notifications sent
- Delivery status
- Timestamps for all actions
- Audit trail with creator info

---

## Configuration

### Server Configuration

**Default Port:** 3003

Change in `mcp/notificationsystem/server.py`:
```python
uvicorn.run(
    "mcp.notificationsystem.server:app",
    port=3004  # Change to desired port
)
```

### Client Configuration

```python
# Change connection URL
client = NotificationSystemSyncClient(
    base_url="http://localhost:3004"
)

# Change timeout
client = NotificationSystemSyncClient(
    timeout=60.0
)
```

---

## Error Handling

### Common Errors

**Connection Refused:**
```
Make sure server is running:
python mcp/notificationsystem/server.py
```

**Case Not Found:**
```
Ensure case_id format is correct: CASE-YYYYMMDD-XXXXX
```

**Notification Not Found:**
```
Ensure notification_id exists in system
```

### Validation

Server automatically:
- Validates decision classification
- Handles missing optional fields
- Provides defaults for calculations
- Logs all operations for audit trail

---

## Performance

- Average notification recording: <50ms
- Case retrieval: ~5ms
- Compliance report generation: ~20ms
- Resource usage: <30MB memory per instance

---

## Deployment

### Development
```bash
python mcp/notificationsystem/server.py
```

### Docker
```bash
docker build -t notificationsystem .
docker run -p 3003:3003 notificationsystem
```

### Docker Compose
```yaml
notificationsystem:
  build: .
  ports:
    - "3003:3003"
  depends_on:
    - decisionsynthesis
```

---

## Testing

### Unit Test Example
```python
def test_record_and_notify():
    client = NotificationSystemSyncClient()
    
    result = client.record_and_notify(
        "APP001", "John Doe", "john@example.com",
        "APPROVE", 1.8, "High", "Balanced", "Good profile"
    )
    
    assert result['status'] == 'success'
    assert result['case_id'].startswith('CASE-')
    assert result['notifications_sent'] > 0
```

### Integration Test Example
```python
def test_full_notification_flow():
    client = NotificationSystemSyncClient()
    
    # Record action
    result = client.record_and_notify(...)
    case_id = result['case_id']
    
    # Retrieve case
    case_info = client.get_case_information(case_id)
    assert case_info['status'] == 'success'
    assert case_info['case']['case_id'] == case_id
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server not running | `python mcp/notificationsystem/server.py` |
| Case not found | Invalid case ID | Check case ID format: CASE-YYYYMMDD-XXXXX |
| Timeout | Slow dependencies | Increase timeout: `client.timeout = 60` |
| Missing applicant data | Incomplete input | Ensure all required fields provided |

---

## Support

- **Documentation**: `NOTIFICATIONSYSTEM_IMPLEMENTATION.md` (this file)
- **Quick Reference**: `NOTIFICATIONSYSTEM_QUICKREF.md`
- **Examples**: `examples/notificationsystem_demo.py`
- **Source**: `mcp/notificationsystem/server.py`
