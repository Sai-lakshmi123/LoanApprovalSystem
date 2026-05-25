"""
Loan Decision Agent (Agent3)
Uses Anthropic Agent SDK with Claude Sonnet 4.6 to synthesize final loan decisions.
Connects to DecisionSynthesis MCP Server and integrates Agent1 + Agent2 outputs.

Run the DecisionSynthesis server first:
    python mcp/decisionsynthesis/server.py

Then run this agent:
    python agents/loan_decision_agent.py
"""

import anthropic
import json
import httpx
from typing import Any
from datetime import datetime

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are an expert loan decision analyst responsible for making final lending decisions. Your role is to synthesize outputs from applicant profile analysis and financial risk analysis to produce a comprehensive, well-reasoned loan decision.

## Your Responsibilities:

1. **Decision Synthesis**: Combine multiple data sources into coherent decision
2. **Risk Evaluation**: Assess overall financial risk profile
3. **Confidence Assessment**: Determine decision confidence based on data quality
4. **Condition Generation**: Identify specific conditions for conditional approvals
5. **Reasoning**: Provide clear, documented reasoning for all decisions
6. **Compliance**: Ensure fair lending and regulatory compliance
7. **Documentation**: Create audit trail for every decision

## Analysis Framework:

### Decision Classification
- **APPROVE**: Application approved for full loan amount
  - Risk score < 1.5 and no critical violations
  - Strong financial profile across all dimensions
  - Clear path to repayment

- **CONDITIONAL_APPROVE**: Approved with specific conditions
  - Risk score 1.5-2.5 with minor concerns
  - Conditions address specific issues
  - High likelihood of success with conditions

- **REVIEW**: Requires manual underwriting review
  - Risk score 2.5-3.5 with mixed signals
  - Concerns that may be resolvable
  - Senior underwriter input recommended

- **REJECT**: Does not meet lending criteria
  - Risk score > 3.5 or critical violations
  - Multiple high-risk factors identified
  - Insufficient mitigating factors

### Confidence Level Assessment (0-100%)
- **Very High (85-100%)**: Complete data, strong agreement across metrics
- **High (70-84%)**: Good data quality, minor inconsistencies
- **Moderate (55-69%)**: Acceptable data, some concerns
- **Low (40-54%)**: Limited data or conflicting signals
- **Very Low (<40%)**: Incomplete data, major inconsistencies

### Key Decision Factors
Evaluate:
1. Income stability and employment security
2. Debt-to-income and debt management capacity
3. Credit history and payment discipline
4. Loan amount relative to financial capacity
5. Collateral value and equity protection
6. Unusual patterns or red flags
7. Compensating factors and mitigating circumstances

### Risk Score Integration
Synthesize from:
- Agent1: Income stability (0-100), Employment risk (0-100), Credit score, Completeness (0-100%)
- Agent2: DTI risk (0-100%), Credit risk (0-100), Loan risk, Anomalies, Aggregate risk (0-5)
- Derive: Overall risk score (0-5 scale) and final recommendation

## Output Format:

Always structure your final decision as valid JSON with these exact fields:
{
    "applicant_id": "string",
    "analysis_timestamp": "ISO format datetime",
    "decision": {
        "classification": "string (APPROVE/CONDITIONAL_APPROVE/REVIEW/REJECT)",
        "risk_score": number (0-5),
        "confidence_level": "string (Very High/High/Moderate/Low/Very Low)",
        "confidence_percentage": number (0-100),
        "reasoning": "string - detailed explanation of decision",
        "conditions": ["string array - only for CONDITIONAL_APPROVE"],
        "appeal_process": "string - information if applicable"
    },
    "key_factors": [
        {
            "category": "string",
            "impact": "string (Positive/Neutral/Concern/Critical)",
            "description": "string",
            "score": number
        }
    ],
    "risk_summary": {
        "strengths": ["string array"],
        "concerns": ["string array"],
        "mitigating_factors": ["string array"],
        "critical_factors": ["string array"]
    },
    "metrics_integration": {
        "income_stability_score": number,
        "employment_risk_level": "string",
        "credit_score": number,
        "dti_percentage": number,
        "loan_amount_risk": "string",
        "anomaly_count": number,
        "application_completeness": number
    },
    "recommendation_rationale": "string - executive summary of reasoning",
    "next_steps": ["string array"],
    "compliance_notes": {
        "fair_lending_compliant": boolean,
        "documentation_complete": boolean,
        "audit_trail_created": boolean
    }
}

## Guidelines:

- Integrate both Agent1 and Agent2 outputs into cohesive analysis
- Provide clear reasoning for all decisions
- Balance risk mitigation with fair lending principles
- Consider the complete applicant profile, not isolated factors
- Flag any inconsistencies between analyses
- Identify specific, actionable conditions
- Ensure compliance with lending regulations
- Create documented decision trail

## Tools Available:

- synthesize_loan_decision: Combine analyses and make final decision
- evaluate_multiple_scenarios: Compare outcomes across strategies
- explain_decision: Get detailed decision explanation
- compare_applicants: Assess relative risk profiles

Start by synthesizing all available data, then provide your comprehensive decision."""


# ============================================================================
# DECISIONSYNTHESIS CLIENT
# ============================================================================

class DecisionSynthesisClient:
    """Client for DecisionSynthesis MCP Server."""

    def __init__(self, base_url: str = "http://localhost:3002", timeout: float = 30.0):
        """Initialize client."""
        self.base_url = base_url
        self.timeout = timeout

    def synthesize_loan_decision(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        risk_assessment: dict,
        strategy: str = "Balanced"
    ) -> dict:
        """Synthesize loan decision from combined analyses."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/synthesize_loan_decision/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant_data,
                    "application_analysis": application_analysis,
                    "risk_assessment": risk_assessment,
                    "strategy": strategy
                }
            )
            response.raise_for_status()
            return response.json()

    def evaluate_multiple_scenarios(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        base_risk_assessment: dict,
        scenario_results: list
    ) -> dict:
        """Evaluate decisions across multiple scenarios."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/evaluate_multiple_scenarios/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant_data,
                    "application_analysis": application_analysis,
                    "base_risk_assessment": base_risk_assessment,
                    "scenario_results": scenario_results
                }
            )
            response.raise_for_status()
            return response.json()

    def explain_decision(
        self,
        applicant_id: str,
        applicant_data: dict,
        application_analysis: dict,
        risk_assessment: dict
    ) -> dict:
        """Get detailed explanation of decision."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/explain_decision/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant_data,
                    "application_analysis": application_analysis,
                    "risk_assessment": risk_assessment
                }
            )
            response.raise_for_status()
            return response.json()

    def compare_applicants(self, applicants: list) -> dict:
        """Compare multiple applicants."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/compare_applicants/execute",
                json={"applicants": applicants}
            )
            response.raise_for_status()
            return response.json()


# ============================================================================
# LOAN DECISION AGENT
# ============================================================================

class LoanDecisionAgent:
    """Agent for synthesizing final loan decisions."""

    def __init__(self, api_key: str = None):
        """Initialize agent with Anthropic client."""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"
        self.decision_db = DecisionSynthesisClient()

    def define_tools(self) -> list:
        """Define tools for the agent."""
        return [
            {
                "name": "synthesize_loan_decision",
                "description": "Synthesize final loan decision from applicant profile and risk analysis",
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
                        "application_analysis": {
                            "type": "object",
                            "description": "Analysis from Agent1"
                        },
                        "risk_assessment": {
                            "type": "object",
                            "description": "Analysis from Agent2"
                        },
                        "strategy": {
                            "type": "string",
                            "description": "Decision strategy (Conservative/Balanced/Aggressive)"
                        }
                    },
                    "required": ["applicant_id", "applicant_data", "application_analysis", "risk_assessment"]
                }
            },
            {
                "name": "evaluate_multiple_scenarios",
                "description": "Evaluate decision outcomes across multiple loan amount scenarios",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        },
                        "applicant_data": {
                            "type": "object",
                            "description": "Applicant profile"
                        },
                        "application_analysis": {
                            "type": "object",
                            "description": "Application analysis"
                        },
                        "base_risk_assessment": {
                            "type": "object",
                            "description": "Base risk assessment"
                        },
                        "scenario_results": {
                            "type": "array",
                            "description": "Scenario comparison results"
                        }
                    },
                    "required": ["applicant_id", "applicant_data", "application_analysis", "base_risk_assessment"]
                }
            },
            {
                "name": "explain_decision",
                "description": "Get detailed explanation of the decision with key factors",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        },
                        "applicant_data": {
                            "type": "object",
                            "description": "Applicant profile"
                        },
                        "application_analysis": {
                            "type": "object",
                            "description": "Application analysis"
                        },
                        "risk_assessment": {
                            "type": "object",
                            "description": "Risk assessment"
                        }
                    },
                    "required": ["applicant_id", "applicant_data", "application_analysis", "risk_assessment"]
                }
            },
            {
                "name": "compare_applicants",
                "description": "Compare decisions across multiple applicants",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicants": {
                            "type": "array",
                            "description": "List of applicants with their analyses"
                        }
                    },
                    "required": ["applicants"]
                }
            }
        ]

    def process_tool_call(self, tool_name: str, tool_input: dict) -> dict:
        """Process tool calls and return results."""
        try:
            if tool_name == "synthesize_loan_decision":
                return self.decision_db.synthesize_loan_decision(
                    tool_input.get("applicant_id"),
                    tool_input.get("applicant_data"),
                    tool_input.get("application_analysis"),
                    tool_input.get("risk_assessment"),
                    tool_input.get("strategy", "Balanced")
                )
            elif tool_name == "evaluate_multiple_scenarios":
                return self.decision_db.evaluate_multiple_scenarios(
                    tool_input.get("applicant_id"),
                    tool_input.get("applicant_data"),
                    tool_input.get("application_analysis"),
                    tool_input.get("base_risk_assessment"),
                    tool_input.get("scenario_results", [])
                )
            elif tool_name == "explain_decision":
                return self.decision_db.explain_decision(
                    tool_input.get("applicant_id"),
                    tool_input.get("applicant_data"),
                    tool_input.get("application_analysis"),
                    tool_input.get("risk_assessment")
                )
            elif tool_name == "compare_applicants":
                return self.decision_db.compare_applicants(
                    tool_input.get("applicants", [])
                )
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

    def make_decision(
        self,
        applicant_id: str,
        applicant_data: dict,
        applicant_analysis: dict,
        risk_analysis: dict,
        strategy: str = "Balanced"
    ) -> dict:
        """Synthesize final loan decision."""
        print(f"\n{'='*80}")
        print(f"  LOAN DECISION AGENT - Making Decision for {applicant_id}")
        print(f"{'='*80}\n")

        messages = [
            {
                "role": "user",
                "content": f"""You are making a final loan decision for applicant {applicant_id}.

APPLICANT PROFILE:
{json.dumps(applicant_data, indent=2)}

AGENT1 - APPLICATION PROFILE ANALYSIS:
{json.dumps(applicant_analysis, indent=2)[:1500]}...

AGENT2 - FINANCIAL RISK ANALYSIS:
{json.dumps(risk_analysis, indent=2)[:1500]}...

Please synthesize these analyses and make a final loan decision using the {strategy} strategy.

Provide:
1. Final decision classification (APPROVE/CONDITIONAL_APPROVE/REVIEW/REJECT)
2. Risk score (0-5) based on all factors
3. Confidence level and percentage
4. Key decision factors with impacts
5. Complete reasoning
6. Any conditions or next steps
7. Compliance notes

Return your decision as valid JSON with all required fields."""
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

                print(f"\n>>> Decision Complete")
                print(f"\nFinal Response Length: {len(final_response)} chars")

                # Parse JSON from response
                try:
                    json_start = final_response.find("{")
                    json_end = final_response.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = final_response[json_start:json_end]
                        decision = json.loads(json_str)
                        return {
                            "status": "success",
                            "decision": decision,
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
            "message": f"Agent did not complete decision within {max_iterations} iterations"
        }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function to run the agent."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║         LOAN DECISION AGENT (Agent3) - Anthropic Agent SDK with Claude        ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    # Initialize agent
    agent = LoanDecisionAgent()

    # Sample test case with Agent1 and Agent2 outputs
    test_case = {
        "applicant_id": "APP001",
        "applicant_data": {
            "name": "John Strong",
            "age": 45,
            "annual_income": 150000,
            "monthly_expenses": 4000,
            "existing_monthly_debt": 1000,
            "credit_score": 760,
            "delinquencies": 0,
            "inquiries_last_6_months": 1,
            "credit_utilization": 0.30,
            "years_at_current_job": 8,
            "existing_loans": 1
        },
        # Agent1 Output (simplified)
        "applicant_analysis": {
            "income_stability": {
                "score": 85,
                "stability_category": "Very Stable"
            },
            "employment_risk": {
                "risk_score": 15,
                "risk_level": "Very Low"
            },
            "credit_history": {
                "credit_score": 760,
                "score_category": "Excellent"
            },
            "application_completeness": {
                "is_complete": True,
                "completeness_percentage": 100
            }
        },
        # Agent2 Output (simplified)
        "risk_analysis": {
            "dti_analysis": {
                "dti_with_new_loan_percentage": 35.5,
                "dti_risk_level": "Low"
            },
            "credit_risk": {
                "adjusted_risk_level": "Excellent",
                "credit_score": 760
            },
            "loan_amount_risk": {
                "overall_loan_risk": "Very Low",
                "lti_percentage": 2.0,
                "ltv_percentage": 60.0
            },
            "anomaly_detection": {
                "anomaly_count": 0,
                "has_critical_anomalies": False
            },
            "aggregate_risk_assessment": {
                "overall_risk_score": 1.8,
                "overall_risk_level": "Very Low"
            }
        }
    }

    try:
        result = agent.make_decision(
            test_case["applicant_id"],
            test_case["applicant_data"],
            test_case["applicant_analysis"],
            test_case["risk_analysis"],
            strategy="Balanced"
        )

        if result.get("status") == "success":
            if "decision" in result:
                decision = result["decision"]
                print(f"\n✅ Decision Complete for {test_case['applicant_id']}")
                print(f"\n📋 Decision Classification: {decision.get('decision', {}).get('classification', 'N/A')}")
                print(f"📋 Risk Score: {decision.get('decision', {}).get('risk_score', 'N/A')}/5")
                print(f"📋 Confidence: {decision.get('decision', {}).get('confidence_level', 'N/A')}")
                print(f"📋 Reasoning: {decision.get('decision', {}).get('reasoning', 'N/A')[:200]}...")

        else:
            print(f"❌ Error: {result.get('message', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("  1. DecisionSynthesis server is running: python mcp/decisionsynthesis/server.py")
        print("  2. ANTHROPIC_API_KEY is set")
        print("  3. All dependencies are installed")
        import traceback
        traceback.print_exc()
        return 1

    print(f"\n{'='*80}")
    print("Decision process complete.")
    print(f"{'='*80}\n")

    return 0


if __name__ == "__main__":
    exit(main())
