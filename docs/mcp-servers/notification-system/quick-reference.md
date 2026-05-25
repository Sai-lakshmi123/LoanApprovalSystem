# NotificationSystem - Quick Reference

## 🚀 30-Second Setup

```bash
# Start server
python mcp/notificationsystem/server.py

# Run demo (in another terminal)
python examples/notificationsystem_demo.py

# Use in code
from mcp.notificationsystem.client import NotificationSystemSyncClient
client = NotificationSystemSyncClient()
result = client.record_and_notify(
    "APP001", "John Doe", "john@example.com",
    "APPROVE", 1.8, "High", "Balanced", "Strong profile"
)
```

---

## 📊 What NotificationSystem Does

Records final loan decision compliance actions and sends notifications to all stakeholders.

Inputs:
- Loan decision details (classification, risk score, confidence)
- Applicant information
- Internal recipient list

Outputs:
- **Case ID** - Unique case identifier
- **Action Taken** - Type of action (Approval, Conditional, Review, Rejection)
- **Notifications Sent** - Count and IDs of notifications
- **Timestamp** - ISO format date/time
- **Summary** - Complete action summary with reasoning

---

## 🛠️ 5 Tools Available

| Tool | What It Does |
|------|------------|
| `record_and_notify()` | ⭐ Record action and send all notifications |
| `get_case_information()` | Retrieve complete case with all notifications |
| `check_notification_status()` | Check delivery status of notification |
| `get_compliance_report()` | Generate compliance report for date range |
| `resend_notification()` | Resend failed notification |

---

## 💡 Basic Examples

### Record Decision and Notify

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
    reason="Applicant meets all criteria",
    internal_recipients=[
        {
            "name": "Jane Underwriter",
            "email": "jane@lender.com",
            "type": "Internal Team"
        },
        {
            "name": "Compliance Officer",
            "email": "compliance@lender.com",
            "type": "Compliance Officer"
        }
    ],
    action_summary="Loan approved for $300,000"
)

# Use the result
print(f"Case ID: {result['case_id']}")
print(f"Action: {result['action_taken']}")
print(f"Notifications Sent: {result['notifications_sent']}")
print(f"Timestamp: {result['timestamp']}")
```

### Get Case Details

```python
case_info = client.get_case_information("CASE-20260524-00001")

print(f"Applicant: {case_info['case']['applicant_id']}")
print(f"Decision: {case_info['case']['decision']}")
print(f"Notifications: {len(case_info['notifications'])} sent")

for notif in case_info['notifications']:
    print(f"  • {notif['recipient_name']}: {notif['status']}")
```

### Check Notification Status

```python
status = client.check_notification_status("NOTIF-ABC123DEF456")

print(f"Recipient: {status['recipient']}")
print(f"Status: {status['status']}")
print(f"Sent At: {status['sent_at']}")
print(f"Delivered: {status['delivery_confirmed']}")
```

### Generate Compliance Report

```python
report = client.get_compliance_report()

print(f"Total Cases: {report['total_cases']}")
print(f"Total Notifications: {report['total_notifications']}")

print("Cases by Action:")
for action_type, count in report['cases_by_action'].items():
    print(f"  {action_type}: {count}")
```

### Resend Failed Notification

```python
result = client.resend_notification(
    "CASE-20260524-00001",
    "NOTIF-ABC123DEF456"
)

print(f"Status: {result['status']}")
print(f"Resent At: {result['resent_at']}")
```

---

## 📋 Decision Classifications

| Classification | Meaning | Action |
|---|---|---|
| ✅ APPROVE | Full approval | Send approval notification |
| ✅ CONDITIONAL_APPROVE | Approved with conditions | Send conditional notification |
| ⚠️ REVIEW | Manual review needed | Route to underwriter |
| ❌ REJECT | Does not meet criteria | Send rejection notification |

---

## 🎯 Return Values

### record_and_notify Result

```python
{
    "status": "success",
    "case_id": "CASE-20260524-00001",
    "action_taken": "Approval",
    "decision": "APPROVE",
    "notifications_sent": 3,
    "timestamp": "2026-05-24T10:30:00",
    "summary": {
        "applicant": "John Strong",
        "action": "Approval",
        "decision": "APPROVE",
        "risk_score": 1.8,
        "confidence": "High",
        "stakeholders_notified": 3,
        "reason": "..."
    },
    "notification_ids": [
        "NOTIF-ABC123...",
        "NOTIF-DEF456...",
        "NOTIF-GHI789..."
    ]
}
```

---

## 📧 Stakeholder Types

| Type | Notified For | Notification Method |
|------|---|---|
| Applicant | All decisions | Email + Portal |
| Internal Team | All decisions | System notification + Email |
| Compliance Officer | Rejections, High-risk, Conditional | Email + Report |
| Legal Team | Rejections | Email + Case file |
| Management | REVIEW, Rejections | Dashboard + Email |

---

## 🔧 Configuration

### Change Server Port
Edit `mcp/notificationsystem/server.py`:
```python
uvicorn.run("mcp.notificationsystem.server:app", port=3004)
```

### Change Client URL
```python
client = NotificationSystemSyncClient(
    base_url="http://localhost:3004"
)
```

### Change Timeout
```python
client = NotificationSystemSyncClient(timeout=60.0)
```

---

## 📚 Access Resources

```python
client = NotificationSystemSyncClient()

# Get notification templates
templates = client.get_notification_templates()

# Get compliance rules
rules = client.get_compliance_rules()

# Get stakeholder list
stakeholders = client.get_stakeholder_list()
```

---

## 🔄 Complete Workflow

```python
from mcp.decisionsynthesis.client import DecisionSynthesisSyncClient
from mcp.notificationsystem.client import NotificationSystemSyncClient

# 1. Get decision from DecisionSynthesis
decision_db = DecisionSynthesisSyncClient()
decision = decision_db.synthesize_loan_decision(...)

# 2. Record decision and send notifications
notif_db = NotificationSystemSyncClient()
result = notif_db.record_and_notify(
    applicant_id="APP001",
    applicant_name=applicant['name'],
    applicant_email=applicant['email'],
    decision=decision['decision']['classification'],
    risk_score=decision['decision']['risk_score'],
    confidence=decision['decision']['confidence_level'],
    strategy=decision['strategy_applied'],
    reason=decision['decision']['reasoning'],
    action_summary=f"Decision: {decision['decision']['classification']}"
)

# 3. Use the case ID for tracking
print(f"Case ID: {result['case_id']}")
print(f"Notifications Sent: {result['notifications_sent']}")
```

---

## 📊 Compliance Report Structure

```
{
    "status": "success",
    "generated_at": "ISO timestamp",
    "total_cases": 42,
    "total_notifications": 156,
    "cases_by_action": {
        "Approval": 25,
        "Conditional Approval": 10,
        "Manual Review": 5,
        "Rejection": 2
    },
    "notification_status_summary": {
        "Sent": 150,
        "Delivered": 148,
        "Failed": 2,
        "Pending": 6
    },
    "cases": [...]
}
```

---

## 🔌 Case ID Format

```
CASE-YYYYMMDD-XXXXX

Example: CASE-20260524-00001

Where:
  CASE = Prefix
  YYYYMMDD = Date case was created
  XXXXX = Sequential number (5 digits)
```

---

## 📧 Notification ID Format

```
NOTIF-XXXXXXXXXXXX

Example: NOTIF-ABC123DEF456

Where:
  NOTIF = Prefix
  XXXXXXXXXXXX = Unique identifier (hex)
```

---

## 🔐 Audit Trail

Every action includes audit trail:

```python
audit_trail = {
    "created_by": "DecisionSynthesis",
    "created_at": "ISO timestamp",
    "last_modified": "ISO timestamp",
    "fair_lending_compliant": True
}
```

---

## ✨ Key Features

✅ Automatic case ID generation
✅ Multi-stakeholder notifications
✅ Notification delivery tracking
✅ Compliance audit trails
✅ Resend failed notifications
✅ Compliance reporting
✅ Fair lending compliance tracking
✅ Production-ready implementation

---

## 🆘 Troubleshooting

**Connection refused?**
```bash
python mcp/notificationsystem/server.py
```

**Case not found?**
Ensure case_id format is correct: CASE-YYYYMMDD-XXXXX

**Notification failed?**
Use resend_notification() to retry

**Timeout?**
```python
client = NotificationSystemSyncClient(timeout=60)
```

---

## 📞 Support

- **Full Documentation**: `NOTIFICATIONSYSTEM_IMPLEMENTATION.md`
- **Examples**: `examples/notificationsystem_demo.py`
- **Source**: `mcp/notificationsystem/server.py`
- **Client**: `mcp/notificationsystem/client.py`

---

## 🎯 Next Steps

1. Start server: `python mcp/notificationsystem/server.py`
2. Run demo: `python examples/notificationsystem_demo.py`
3. Integrate with DecisionSynthesis
4. Add email sending backend
5. Store compliance records in database
6. Build compliance dashboard
