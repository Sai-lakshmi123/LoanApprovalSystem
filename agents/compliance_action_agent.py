"""
Compliance & Action Orchestrator Agent (Agent4)
Uses Anthropic Agent SDK with Claude Sonnet 4.6 to record decisions, ensure compliance,
and orchestrate notifications to stakeholders.
Connects to NotificationSystem MCP Server.

Run the NotificationSystem server first:
    python mcp/notificationsystem/server.py

Then run this agent:
    python agents/compliance_action_agent.py
"""

import anthropic
import json
import httpx
from typing import Any
from datetime import datetime

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are a compliance and action orchestrator responsible for recording loan decisions, ensuring regulatory compliance, and orchestrating notifications to all stakeholders.

## Your Responsibilities:

1. **Decision Recording**: Record final loan decision in compliance system
2. **Case Management**: Generate and track case IDs for all decisions
3. **Compliance Verification**: Ensure all decisions meet regulatory requirements
4. **Notification Orchestration**: Send notifications to appropriate stakeholders
5. **Documentation**: Create complete compliance and audit documentation
6. **Stakeholder Communication**: Ensure all parties informed appropriately
7. **Status Tracking**: Monitor notification delivery and provide updates

## Stakeholder Types:

- **Applicant**: Receives decision notification and next steps
- **Loan Officer**: Receives decision summary and action items
- **Underwriter**: Receives decision details and conditional approvals
- **Compliance Officer**: Receives compliance certification and documentation
- **Management**: Receives portfolio summary and metrics
- **Legal**: Receives compliance notes and regulatory documentation

## Analysis Framework:

### Decision Recording
1. **Case ID Generation**: CASE-YYYYMMDD-XXXXX format
   - Year-Month-Day: Decision date
   - Random sequence: Uniqueness within day
   - Immutable once assigned

2. **Compliance Verification**
   - Fair lending compliance check
   - Documentation completeness
   - Audit trail verification
   - Regulatory requirement satisfaction

3. **Action Classification**
   - **APPROVE**: Full approval, schedule closing
   - **CONDITIONAL_APPROVE**: Conditions required, request documentation
   - **REVIEW**: Manual review, escalate to underwriter
   - **REJECT**: Denial, prepare appeal process information

### Notification Strategy
Based on decision classification:
- **APPROVE**: Notify applicant, loan officer, underwriter, compliance
- **CONDITIONAL_APPROVE**: Notify applicant with conditions, underwriter, compliance
- **REVIEW**: Notify underwriter, loan officer, compliance
- **REJECT**: Notify applicant with appeal process, loan officer, compliance

### Compliance Documentation
1. **Decision Record**: Complete decision details
2. **Audit Trail**: All decisions and actions timestamped
3. **Notification Log**: Who was notified, when, how
4. **Compliance Certification**: Fair lending and regulatory compliance
5. **Appeal Process**: Information for rejected applicants

## Output Format:

Always structure your actions as valid JSON with these exact fields:
{
    "applicant_id": "string",
    "case_id": "string (CASE-YYYYMMDD-XXXXX format)",
    "action_timestamp": "ISO format datetime",
    "decision_record": {
        "classification": "string (APPROVE/CONDITIONAL_APPROVE/REVIEW/REJECT)",
        "risk_score": number (0-5),
        "recorded_at": "ISO datetime",
        "compliance_verified": boolean
    },
    "notifications": {
        "sent_to": ["array of stakeholders notified"],
        "total_notifications": number,
        "notification_template": "string - template used",
        "delivery_status": "array of delivery confirmations"
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
        "status": "string (Open/In Progress/Pending Action/Closed)",
        "next_action": "string",
        "assigned_to": "string",
        "deadline": "ISO datetime",
        "priority": "string (Low/Medium/High/Critical)"
    },
    "compliance_report": {
        "decision_summary": "string",
        "key_compliance_factors": ["array"],
        "regulatory_notes": "string",
        "recommendations": ["array"]
    },
    "action_summary": "string - executive summary of actions taken",
    "next_steps": ["string array"],
    "escalations": ["string array - any escalations if needed"]
}

## Guidelines:

- Record all decisions immediately with case ID
- Verify compliance for all decisions
- Send appropriate notifications based on decision type
- Create complete audit trail for regulatory compliance
- Generate case management tasks
- Ensure all stakeholders informed appropriately
- Maintain fair lending compliance
- Document all actions and decisions
- Flag any compliance concerns for escalation

## Tools Available:

- record_and_notify: Record decision and send initial notifications
- get_case_information: Retrieve case details and status
- check_notification_status: Check notification delivery status
- get_compliance_report: Generate compliance documentation
- resend_notification: Resend notification to specific stakeholder

Start by recording the decision with compliance verification, then orchestrate notifications."""


# ============================================================================
# NOTIFICATIONSYSTEM CLIENT
# ============================================================================

class NotificationSystemClient:
    """Client for NotificationSystem MCP Server."""

    def __init__(self, base_url: str = "http://localhost:3003", timeout: float = 30.0):
        """Initialize client."""
        self.base_url = base_url
        self.timeout = timeout

    def record_and_notify(
        self,
        applicant_id: str,
        applicant_data: dict,
        decision_data: dict,
        action_type: str = "decision_notification"
    ) -> dict:
        """Record decision and send initial notifications."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/record_and_notify/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant_data,
                    "decision_data": decision_data,
                    "action_type": action_type
                }
            )
            response.raise_for_status()
            return response.json()

    def get_case_information(
        self,
        case_id: str
    ) -> dict:
        """Retrieve case details and status."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/get_case_information/execute",
                json={"case_id": case_id}
            )
            response.raise_for_status()
            return response.json()

    def check_notification_status(
        self,
        case_id: str
    ) -> dict:
        """Check notification delivery status."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/check_notification_status/execute",
                json={"case_id": case_id}
            )
            response.raise_for_status()
            return response.json()

    def get_compliance_report(
        self,
        case_id: str
    ) -> dict:
        """Generate compliance documentation."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/get_compliance_report/execute",
                json={"case_id": case_id}
            )
            response.raise_for_status()
            return response.json()

    def resend_notification(
        self,
        case_id: str,
        stakeholder_type: str
    ) -> dict:
        """Resend notification to specific stakeholder."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/resend_notification/execute",
                json={
                    "case_id": case_id,
                    "stakeholder_type": stakeholder_type
                }
            )
            response.raise_for_status()
            return response.json()


# ============================================================================
# COMPLIANCE & ACTION ORCHESTRATOR AGENT
# ============================================================================

class ComplianceActionAgent:
    """Agent for recording decisions and orchestrating notifications."""

    def __init__(self, api_key: str = None):
        """Initialize agent with Anthropic client."""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"
        self.notification_system = NotificationSystemClient()

    def define_tools(self) -> list:
        """Define tools for the agent."""
        return [
            {
                "name": "record_and_notify",
                "description": "Record decision in compliance system and send initial notifications",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        },
                        "applicant_data": {
                            "type": "object",
                            "description": "Applicant profile data"
                        },
                        "decision_data": {
                            "type": "object",
                            "description": "Complete decision from Agent3"
                        },
                        "action_type": {
                            "type": "string",
                            "description": "Type of action (decision_notification, appeal_notification, etc)"
                        }
                    },
                    "required": ["applicant_id", "applicant_data", "decision_data"]
                }
            },
            {
                "name": "get_case_information",
                "description": "Retrieve case details and current status",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "case_id": {
                            "type": "string",
                            "description": "Case ID (CASE-YYYYMMDD-XXXXX format)"
                        }
                    },
                    "required": ["case_id"]
                }
            },
            {
                "name": "check_notification_status",
                "description": "Check notification delivery status for case",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "case_id": {
                            "type": "string",
                            "description": "Case ID"
                        }
                    },
                    "required": ["case_id"]
                }
            },
            {
                "name": "get_compliance_report",
                "description": "Generate compliance documentation for case",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "case_id": {
                            "type": "string",
                            "description": "Case ID"
                        }
                    },
                    "required": ["case_id"]
                }
            },
            {
                "name": "resend_notification",
                "description": "Resend notification to specific stakeholder",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "case_id": {
                            "type": "string",
                            "description": "Case ID"
                        },
                        "stakeholder_type": {
                            "type": "string",
                            "description": "Stakeholder type (Applicant/LoanOfficer/Underwriter/Compliance/Management/Legal)"
                        }
                    },
                    "required": ["case_id", "stakeholder_type"]
                }
            }
        ]

    def process_tool_call(self, tool_name: str, tool_input: dict) -> dict:
        """Process tool calls and return results."""
        try:
            if tool_name == "record_and_notify":
                return self.notification_system.record_and_notify(
                    tool_input.get("applicant_id"),
                    tool_input.get("applicant_data"),
                    tool_input.get("decision_data"),
                    tool_input.get("action_type", "decision_notification")
                )
            elif tool_name == "get_case_information":
                return self.notification_system.get_case_information(
                    tool_input.get("case_id")
                )
            elif tool_name == "check_notification_status":
                return self.notification_system.check_notification_status(
                    tool_input.get("case_id")
                )
            elif tool_name == "get_compliance_report":
                return self.notification_system.get_compliance_report(
                    tool_input.get("case_id")
                )
            elif tool_name == "resend_notification":
                return self.notification_system.resend_notification(
                    tool_input.get("case_id"),
                    tool_input.get("stakeholder_type")
                )
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

    def orchestrate_action(
        self,
        applicant_id: str,
        applicant_data: dict,
        decision_data: dict
    ) -> dict:
        """Orchestrate compliance and notification actions."""
        print(f"\n{'='*80}")
        print(f"  COMPLIANCE & ACTION ORCHESTRATOR - Processing {applicant_id}")
        print(f"{'='*80}\n")

        messages = [
            {
                "role": "user",
                "content": f"""You are recording a loan decision and orchestrating notifications for applicant {applicant_id}.

APPLICANT PROFILE:
{json.dumps(applicant_data, indent=2)}

DECISION FROM AGENT3:
{json.dumps(decision_data, indent=2)[:2000]}...

Please:
1. Record the decision in the compliance system
2. Verify all compliance requirements are met
3. Generate case ID and tracking information
4. Send appropriate notifications to all stakeholders
5. Create compliance documentation
6. Provide case management details and next steps

Return your action orchestration as valid JSON with all required fields."""
            }
        ]

        iteration = 0
        max_iterations = 10

        while iteration < max_iterations:
            iteration += 1
            print(f"\n>>> Agent Iteration {iteration}")

            # Call Claude with tools
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=self.define_tools(),
                messages=messages
            )

            print(f"Stop Reason: {response.stop_reason}")

            # Process response content
            if response.stop_reason == "tool_use":
                # Find tool use blocks
                tool_results = []

                for block in response.content:
                    if hasattr(block, "type") and block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_use_id = block.id

                        print(f"Tool Called: {tool_name}")
                        print(f"Input Keys: {list(tool_input.keys())}")

                        # Process the tool call
                        result = self.process_tool_call(tool_name, tool_input)
                        print(f"Result Status: {result.get('status', 'unknown')}")

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result)
                        })

                # Add assistant message and tool results to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

            elif response.stop_reason == "end_turn":
                # Extract final response
                final_response = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_response += block.text

                print(f"\n>>> Action Orchestration Complete")
                print(f"\nFinal Response Length: {len(final_response)} chars")

                # Parse JSON from response
                try:
                    json_start = final_response.find("{")
                    json_end = final_response.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = final_response[json_start:json_end]
                        action_result = json.loads(json_str)
                        return {
                            "status": "success",
                            "result": action_result,
                            "raw_response": final_response
                        }
                except json.JSONDecodeError:
                    pass

                return {
                    "status": "success",
                    "raw_response": final_response
                }
            else:
                print(f"Unexpected stop reason: {response.stop_reason}")
                break

        return {
            "status": "error",
            "message": f"Agent did not complete orchestration within {max_iterations} iterations"
        }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function to run the agent."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║   COMPLIANCE & ACTION ORCHESTRATOR (Agent4) - Anthropic Agent SDK with Claude  ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    # Initialize agent
    agent = ComplianceActionAgent()

    # Sample test case with Agent3 decision output
    test_case = {
        "applicant_id": "APP001",
        "applicant_data": {
            "name": "John Strong",
            "age": 45,
            "email": "john.strong@example.com",
            "phone": "+1-555-0100",
            "annual_income": 150000,
            "existing_monthly_debt": 1000,
            "credit_score": 760,
            "delinquencies": 0,
            "years_at_current_job": 8
        },
        # Agent3 Decision Output
        "decision_data": {
            "applicant_id": "APP001",
            "analysis_timestamp": "2026-05-25T10:30:00",
            "decision": {
                "classification": "APPROVE",
                "risk_score": 1.8,
                "confidence_level": "Very High",
                "confidence_percentage": 92,
                "reasoning": "Strong financial profile with excellent credit, very low employment risk, and manageable DTI."
            },
            "key_factors": [
                {
                    "category": "Income Stability",
                    "impact": "Positive",
                    "description": "8 years at current job",
                    "score": 85
                },
                {
                    "category": "Credit Profile",
                    "impact": "Positive",
                    "description": "Excellent credit score of 760",
                    "score": 95
                }
            ],
            "risk_summary": {
                "strengths": [
                    "Strong income stability",
                    "Excellent credit score",
                    "Very low employment risk"
                ],
                "concerns": [],
                "mitigating_factors": [],
                "critical_factors": []
            },
            "compliance_notes": {
                "fair_lending_compliant": True,
                "documentation_complete": True,
                "audit_trail_created": True
            }
        }
    }

    try:
        result = agent.orchestrate_action(
            test_case["applicant_id"],
            test_case["applicant_data"],
            test_case["decision_data"]
        )

        if result.get("status") == "success":
            if "result" in result:
                action = result["result"]
                print(f"\n✅ Action Orchestration Complete for {test_case['applicant_id']}")
                print(f"\n📋 Case ID: {action.get('case_id', 'N/A')}")
                print(f"📋 Action Status: {action.get('case_management', {}).get('status', 'N/A')}")
                print(f"📋 Notifications Sent: {action.get('notifications', {}).get('total_notifications', 0)}")
                print(f"📋 Compliance Verified: {action.get('compliance_certification', {}).get('fair_lending_compliant', False)}")
                print(f"📋 Action Summary: {action.get('action_summary', 'N/A')[:200]}...")

        else:
            print(f"❌ Error: {result.get('message', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("  1. NotificationSystem server is running: python mcp/notificationsystem/server.py")
        print("  2. ANTHROPIC_API_KEY is set")
        print("  3. All dependencies are installed")
        import traceback
        traceback.print_exc()
        return 1

    print(f"\n{'='*80}")
    print("Action orchestration complete.")
    print(f"{'='*80}\n")

    return 0


if __name__ == "__main__":
    exit(main())
