# Agent4: Compliance & Action Orchestrator - Complete Technical Implementation Guide

## Overview

Agent4 is the **Compliance & Action Orchestrator** in the four-agent loan approval system. It records final lending decisions, ensures regulatory compliance, and orchestrates notifications to stakeholders using the Anthropic Agent SDK with Claude Sonnet 4.6.

**Key Role**: Record decisions in compliance system, verify fair lending and regulatory requirements, generate case IDs, and orchestrate notifications to all stakeholders.

---

## Architecture

### System Design

```
INPUT SOURCES:
├─ Agent3 Output (Loan Decision)
│  ├─ Decision Classification
│  ├─ Risk Score
│  ├─ Confidence Level
│  ├─ Key Factors
│  ├─ Compliance Notes
│  └─ Recommendations
├─ Applicant Data
└─ Applicant Profile

                   ↓

        AGENT4 - COMPLIANCE & ACTION ORCHESTRATION
        ├─ Record decision with case ID
        ├─ Verify compliance
        ├─ Determine stakeholders
        ├─ Send notifications
        ├─ Create case management
        └─ Generate compliance report

                   ↓

OUTPUT STRUCTURE:
├─ Case ID (CASE-YYYYMMDD-XXXXX)
├─ Decision Record (Recorded, Verified)
├─ Notifications (Sent, Delivery Status)
├─ Compliance Certification
├─ Case Management (Status, Next Action)
├─ Compliance Report
└─ Action Summary
```

---

## System Prompt (140+ Lines)

The system prompt defines Agent4's behavior across seven dimensions:

### 1. Role Definition
```
"You are a compliance and action orchestrator responsible for recording 
loan decisions, ensuring regulatory compliance, and orchestrating 
notifications to all stakeholders."
```

**Responsibilities:**
- Decision recording in compliance system
- Case management and tracking
- Compliance verification
- Notification orchestration
- Stakeholder communication
- Status tracking
- Documentation generation

### 2. Stakeholder Management

**Six Stakeholder Types:**

**Applicant**
- Decision notification
- Next steps
- Conditions (if applicable)
- Appeal process (if rejected)
- Document submission (if conditional)

**Loan Officer**
- Decision summary
- Action items
- Case assignment
- Timeline and deadlines
- Follow-up tasks

**Underwriter**
- Complete decision details
- Conditions (if applicable)
- Review request (if review)
- Documentation requirements
- Escalation information

**Compliance Officer**
- Compliance certification
- Fair lending verification
- Documentation completeness
- Audit trail
- Regulatory notes

**Management**
- Portfolio summary
- Decision metrics
- Compliance status
- Case count by classification
- Escalations

**Legal**
- Regulatory documentation
- Appeal process (if rejected)
- Compliance notes
- Fair lending compliance
- Documentation requirements

### 3. Action Classification

**APPROVE**
- Notify applicant of approval
- Assign to loan officer for closing
- Provide closing timeline
- Request document preparation
- Set closing deadline

**CONDITIONAL_APPROVE**
- Notify applicant with conditions
- Request condition documentation
- Assign to underwriter for approval
- Track condition satisfaction
- Set satisfaction deadline

**REVIEW**
- Escalate to senior underwriter
- Create review task
- Set review deadline
- Request additional documentation
- Track review progress

**REJECT**
- Notify applicant of denial
- Provide appeal process information
- Create documentation
- Offer alternative products
- Set appeal window (typically 30 days)

### 4. Case ID Management

**Format**: CASE-YYYYMMDD-XXXXX

**Components:**
- **CASE**: Identifier prefix
- **YYYY**: Year (e.g., 2026)
- **MM**: Month (01-12)
- **DD**: Day (01-31)
- **XXXXX**: Random 5-digit sequence (00000-99999)

**Example**: CASE-20260525-34527

**Characteristics:**
- Generated at decision recording
- Immutable once assigned
- Unique within organization
- Includes decision date
- Random suffix prevents collisions

### 5. Notification Strategy

**Decision-Based Selection:**

**APPROVE Notifications:**
- Applicant: Approval congratulations + next steps
- Loan Officer: Assignment + closing tasks
- Underwriter: Approval confirmation
- Compliance: Fair lending verification
- Management: Portfolio update

**CONDITIONAL_APPROVE Notifications:**
- Applicant: Conditional approval + specific conditions
- Loan Officer: Follow-up required + timeline
- Underwriter: Conditions to verify
- Compliance: Fair lending verification
- Management: Portfolio update

**REVIEW Notifications:**
- Underwriter: Review request + analysis needed
- Loan Officer: Escalation + timeline
- Compliance: Decision pending
- Management: Portfolio update

**REJECT Notifications:**
- Applicant: Denial + appeal process + alternatives
- Loan Officer: Denial documentation
- Compliance: Fair lending verification
- Legal: Appeal process + documentation
- Management: Portfolio update

### 6. Compliance Verification

**Fair Lending Checks:**
1. Decision based on credit-related factors
2. No discrimination by protected classes
3. Consistent standards applied
4. Documented reasoning provided

**Documentation Requirements:**
1. Decision recorded with timestamp
2. Reasoning captured
3. Key factors documented
4. Conditions specified (if applicable)
5. Audit trail maintained

**Regulatory Compliance:**
1. All required fields present
2. Decision classification valid
3. Risk score within range (0-5)
4. Compliance notes provided
5. Appeal process documented (if rejected)

### 7. Case Management

**Status Tracking:**
- **Open**: Case created, initial recording
- **In Progress**: Actions being taken
- **Pending Action**: Awaiting applicant/underwriter action
- **Resolved**: Action completed
- **Closed**: Case completed or appeal period expired

**Priority Levels:**
- **Critical**: Requires same-day action
- **High**: 1-2 day response required
- **Medium**: 3-5 day standard timeline
- **Low**: 1-2 week standard timeline

**Deadline Management:**
- Set based on decision type and regulations
- APPROVE: 10 business days to closing
- CONDITIONAL: 10 days for condition satisfaction
- REVIEW: 5 business days for underwriter review
- REJECT: 30 day appeal window

### 8. Output JSON Schema

The prompt specifies exact output structure:

```json
{
    "applicant_id": "string",
    "case_id": "string (CASE-YYYYMMDD-XXXXX)",
    "action_timestamp": "ISO8601 datetime",
    "decision_record": {
        "classification": "APPROVE | CONDITIONAL_APPROVE | REVIEW | REJECT",
        "risk_score": number(0-5),
        "recorded_at": "ISO8601 datetime",
        "compliance_verified": boolean
    },
    "notifications": {
        "sent_to": ["array of stakeholder types"],
        "total_notifications": number,
        "notification_template": "string - template used",
        "delivery_status": [
            {
                "stakeholder": "string",
                "status": "sent | pending | failed",
                "timestamp": "ISO datetime",
                "template_id": "string"
            }
        ]
    },
    "compliance_certification": {
        "fair_lending_compliant": boolean,
        "documentation_complete": boolean,
        "regulatory_requirements_met": boolean,
        "audit_trail_created": boolean,
        "certification_timestamp": "ISO datetime"
    },
    "case_management": {
        "case_id": "string",
        "status": "Open | In Progress | Pending Action | Resolved | Closed",
        "next_action": "string - specific action required",
        "assigned_to": "string - responsible party",
        "deadline": "ISO datetime",
        "priority": "Low | Medium | High | Critical"
    },
    "compliance_report": {
        "decision_summary": "string - executive summary",
        "key_compliance_factors": ["array of factors"],
        "regulatory_notes": "string - regulatory considerations",
        "recommendations": ["array of recommendations"]
    },
    "action_summary": "string - what was accomplished",
    "next_steps": ["array of specific next steps"],
    "escalations": ["array of escalations if any"]
}
```

### 9. Decision Guidelines

The prompt provides specific guidelines:

1. **Recording**: Record all decisions immediately
2. **Verification**: Verify compliance for all decisions
3. **Notifications**: Send appropriate notifications by decision type
4. **Documentation**: Create complete audit trail
5. **Case Management**: Assign case and set deadlines
6. **Stakeholders**: Notify appropriate parties
7. **Compliance**: Ensure fair lending and regulatory compliance
8. **Escalation**: Flag any compliance concerns

---

## Agent Implementation

### Class: ComplianceActionAgent

**Initialization:**
```python
agent = ComplianceActionAgent(api_key=None)
```

**Attributes:**
```python
self.client              # Anthropic client
self.model              # Model name (default: claude-sonnet-4-6-20250514)
self.notification_system # NotificationSystemClient instance
```

### Method: define_tools()

Returns list of 5 tools:

#### Tool 1: record_and_notify
```json
{
    "name": "record_and_notify",
    "description": "Record decision and send initial notifications",
    "input_schema": {
        "type": "object",
        "properties": {
            "applicant_id": "string - unique identifier",
            "applicant_data": "object - applicant profile",
            "decision_data": "object - complete Agent3 decision",
            "action_type": "string - type of action"
        },
        "required": ["applicant_id", "applicant_data", "decision_data"]
    }
}
```

**Execution Flow:**
1. POST to `/tools/record_and_notify/execute`
2. Includes complete decision and applicant data
3. NotificationSystem generates case ID
4. Records decision with timestamp
5. Sends initial notifications
6. Returns case ID and status

#### Tool 2: get_case_information
```json
{
    "name": "get_case_information",
    "description": "Retrieve case details and current status",
    "input_schema": {
        "type": "object",
        "properties": {
            "case_id": "string - case ID (CASE-YYYYMMDD-XXXXX)"
        },
        "required": ["case_id"]
    }
}
```

**Use Case:** Track case progress, get status updates

#### Tool 3: check_notification_status
```json
{
    "name": "check_notification_status",
    "description": "Check notification delivery status",
    "input_schema": {
        "type": "object",
        "properties": {
            "case_id": "string - case ID"
        },
        "required": ["case_id"]
    }
}
```

**Returns:** Delivery status for each stakeholder notification

#### Tool 4: get_compliance_report
```json
{
    "name": "get_compliance_report",
    "description": "Generate compliance documentation",
    "input_schema": {
        "type": "object",
        "properties": {
            "case_id": "string - case ID"
        },
        "required": ["case_id"]
    }
}
```

**Returns:** Complete compliance documentation and audit trail

#### Tool 5: resend_notification
```json
{
    "name": "resend_notification",
    "description": "Resend notification to specific stakeholder",
    "input_schema": {
        "type": "object",
        "properties": {
            "case_id": "string - case ID",
            "stakeholder_type": "string - Applicant/LoanOfficer/Underwriter/Compliance/Management/Legal"
        },
        "required": ["case_id", "stakeholder_type"]
    }
}
```

**Use Case:** Resend if initial delivery failed

### Method: process_tool_call(tool_name, tool_input)

Handles execution of each tool:

```python
def process_tool_call(self, tool_name: str, tool_input: dict) -> dict:
    if tool_name == "record_and_notify":
        return self.notification_system.record_and_notify(...)
    elif tool_name == "get_case_information":
        return self.notification_system.get_case_information(...)
    # ... etc
```

**Error Handling:**
- Catches connection errors
- Returns error JSON
- Allows agent to retry or provide fallback

### Method: orchestrate_action(applicant_id, applicant_data, decision_data)

Main method for orchestrating compliance and notifications:

**Signature:**
```python
def orchestrate_action(
    self,
    applicant_id: str,              # Unique applicant ID
    applicant_data: dict,           # Applicant profile
    decision_data: dict             # Agent3 decision output
) -> dict
```

**Execution Loop:**
1. Initialize messages with Agent3 decision
2. Enter agentic loop (max 10 iterations)
3. Call Claude with system prompt and tools
4. Check response stop reason
5. If `tool_use`:
   - Extract tool calls
   - Process each tool
   - Add results to conversation
   - Continue loop
6. If `end_turn`:
   - Extract final response
   - Parse JSON
   - Return action result
7. Return error if max iterations exceeded

**Return Structure:**
```python
{
    "status": "success" | "error",
    "result": {...},                # Parsed JSON if success
    "raw_response": "...",          # Claude's full response
    "message": "error message"      # If status is error
}
```

---

## NotificationSystemClient Class

HTTP client for NotificationSystem MCP Server communication.

**Initialization:**
```python
client = NotificationSystemClient(
    base_url="http://localhost:3003",
    timeout=30.0
)
```

**Methods:**

### record_and_notify()
```python
result = client.record_and_notify(
    applicant_id="APP001",
    applicant_data={...},
    decision_data={...},
    action_type="decision_notification"
)
```

**HTTP Call:**
```
POST http://localhost:3003/tools/record_and_notify/execute
```

**Returns:**
- case_id (CASE-YYYYMMDD-XXXXX format)
- decision_record
- notification_status
- compliance_verified

### get_case_information()
```python
result = client.get_case_information(
    case_id="CASE-20260525-12345"
)
```

**Returns:** Complete case details, timeline, all actions

### check_notification_status()
```python
result = client.check_notification_status(
    case_id="CASE-20260525-12345"
)
```

**Returns:** Delivery status per stakeholder

### get_compliance_report()
```python
result = client.get_compliance_report(
    case_id="CASE-20260525-12345"
)
```

**Returns:** Compliance documentation, audit trail

### resend_notification()
```python
result = client.resend_notification(
    case_id="CASE-20260525-12345",
    stakeholder_type="Applicant"
)
```

**Returns:** Resend confirmation, delivery status

---

## Decision Flow & Notification Strategy

### APPROVE Flow

```
1. Record Decision
   ├─ Classification: APPROVE
   ├─ Risk Score: < 1.5
   └─ Case Status: In Progress

2. Send Notifications
   ├─ Applicant: Approval congratulations + next steps
   ├─ Loan Officer: Assignment + closing tasks
   ├─ Underwriter: Confirmation
   ├─ Compliance: Fair lending verification
   └─ Management: Portfolio update

3. Create Case Management
   ├─ Status: In Progress → Pending Action
   ├─ Next Action: Schedule closing
   ├─ Assigned to: Loan Officer
   ├─ Deadline: 10 business days
   └─ Priority: High

4. Generate Compliance Report
   ├─ Decision summary
   ├─ Key factors
   ├─ Regulatory notes
   └─ Audit trail
```

### CONDITIONAL_APPROVE Flow

```
1. Record Decision
   ├─ Classification: CONDITIONAL_APPROVE
   ├─ Risk Score: 1.5-2.5
   └─ Case Status: In Progress

2. Send Notifications
   ├─ Applicant: Conditions required + documentation needed
   ├─ Loan Officer: Follow-up required
   ├─ Underwriter: Condition verification
   ├─ Compliance: Fair lending verification
   └─ Management: Portfolio update

3. Create Case Management
   ├─ Status: In Progress → Pending Action
   ├─ Next Action: Obtain condition documentation
   ├─ Assigned to: Loan Officer
   ├─ Deadline: 10 days for condition satisfaction
   └─ Priority: High

4. Track Conditions
   ├─ Specific conditions documented
   ├─ Satisfaction tracked
   ├─ Underwriter approval required
   └─ Follow-up scheduled
```

### REVIEW Flow

```
1. Record Decision
   ├─ Classification: REVIEW
   ├─ Risk Score: 2.5-3.5
   └─ Case Status: Open → In Progress

2. Send Notifications
   ├─ Underwriter: Review request + analysis needed
   ├─ Loan Officer: Escalation + timeline
   ├─ Compliance: Decision pending
   └─ Management: Portfolio update

3. Create Case Management
   ├─ Status: In Progress
   ├─ Next Action: Underwriter review
   ├─ Assigned to: Senior Underwriter
   ├─ Deadline: 5 business days
   └─ Priority: High

4. Track Review
   ├─ Review progress
   ├─ Additional documentation requests
   ├─ Final decision update
   └─ Applicant notification
```

### REJECT Flow

```
1. Record Decision
   ├─ Classification: REJECT
   ├─ Risk Score: > 3.5
   └─ Case Status: Open → Closed

2. Send Notifications
   ├─ Applicant: Denial + appeal process + alternatives
   ├─ Loan Officer: Documentation + closure
   ├─ Compliance: Fair lending verification
   ├─ Legal: Appeal process + documentation
   └─ Management: Portfolio update

3. Create Case Management
   ├─ Status: Closed
   ├─ Next Action: Appeal window (30 days)
   ├─ Assigned to: Loan Officer
   ├─ Deadline: Appeal window close date
   └─ Priority: Medium

4. Appeal Documentation
   ├─ Denial reasoning documented
   ├─ Appeal process provided
   ├─ Alternative products offered
   └─ Follow-up scheduled
```

---

## Integration Patterns

### Pattern 1: Full 4-Agent Pipeline

```python
from agents.application_profile_agent import ApplicationProfileAgent
from agents.financial_risk_analysis_agent import FinancialRiskAnalysisAgent
from agents.loan_decision_agent import LoanDecisionAgent
from agents.compliance_action_agent import ComplianceActionAgent

# Step 1: Profile analysis
profile_agent = ApplicationProfileAgent()
profile = profile_agent.analyze_applicant("APP001")

# Step 2: Risk analysis
risk_agent = FinancialRiskAnalysisAgent()
risk = risk_agent.analyze_financial_risk("APP001", applicant_data, loan_request)

# Step 3: Decision synthesis
decision_agent = LoanDecisionAgent()
decision = decision_agent.make_decision(
    "APP001",
    applicant_data,
    profile["analysis"],
    risk["analysis"]
)

# Step 4: Compliance & action orchestration
action_agent = ComplianceActionAgent()
action = action_agent.orchestrate_action(
    "APP001",
    applicant_data,
    decision["decision"]
)

# Complete pipeline result
print(f"Case ID: {action['result']['case_id']}")
print(f"Status: {action['result']['case_management']['status']}")
```

### Pattern 2: Batch Processing

```python
agent = ComplianceActionAgent()

for applicant_id in applicant_ids:
    # Get decision from Agent3
    decision = get_decision(applicant_id)
    
    # Orchestrate action
    result = agent.orchestrate_action(
        applicant_id,
        applicant_data[applicant_id],
        decision
    )
    
    print(f"Case ID: {result['result']['case_id']}")
```

### Pattern 3: Notification Status Tracking

```python
agent = ComplianceActionAgent()

# Orchestrate action
result = agent.orchestrate_action(
    applicant_id,
    applicant_data,
    decision
)

case_id = result["result"]["case_id"]

# Later: Check notification status
status = agent.notification_system.check_notification_status(case_id)

for delivery in status["delivery_status"]:
    if delivery["status"] != "sent":
        # Resend if needed
        resend = agent.notification_system.resend_notification(
            case_id,
            delivery["stakeholder"]
        )
```

---

## Error Handling

### Connection Errors
**Cause**: NotificationSystem server not running

```python
try:
    result = agent.orchestrate_action(...)
except ConnectionError:
    # Start server: python mcp/notificationsystem/server.py
```

### Timeout Errors
**Cause**: Slow network or server response

```python
agent.notification_system = NotificationSystemClient(timeout=60)
```

### API Key Errors
**Cause**: ANTHROPIC_API_KEY not set

```bash
export ANTHROPIC_API_KEY=sk-...
```

### JSON Parse Errors
**Cause**: Claude response format invalid

```python
if result.get("status") == "success" and "result" not in result:
    raw = result.get("raw_response")
```

---

## Compliance & Fair Lending

Agent4 ensures compliance through:

1. **Fair Lending Verification**
   - Decisions based on credit-related factors
   - No discrimination by protected classes
   - Consistent standards applied

2. **Complete Documentation**
   - Decision recorded with timestamp
   - Reasoning documented
   - Key factors captured
   - Audit trail maintained

3. **Regulatory Compliance**
   - All required fields present
   - Decision classification valid
   - Risk score within range
   - Compliance notes provided
   - Appeal process documented

4. **Notification Tracking**
   - All stakeholders notified
   - Delivery status tracked
   - Failed notifications identified
   - Resend capability available

---

## Performance Characteristics

- **Average Orchestration Time**: 10-25 seconds
- **Tool Calls per Action**: 3-5 calls
- **Agent Iterations**: 2-4 iterations
- **Max Iterations**: 10 (safety limit)
- **Memory per Instance**: ~50MB
- **Concurrent Actions**: Limited by rate limits

---

## Configuration Options

### Model Selection
```python
agent.model = "claude-opus-4-7-20250805"      # Most capable
agent.model = "claude-sonnet-4-6-20250514"    # Balanced (default)
agent.model = "claude-haiku-4-5-20251001"     # Fast, cost-effective
```

### Server Connection
```python
from agents.compliance_action_agent import NotificationSystemClient

agent.notification_system = NotificationSystemClient(
    base_url="http://custom-server:3003",
    timeout=30.0
)
```

---

**Last Updated:** 2026-05-25  
**Status:** ✅ Production Ready
