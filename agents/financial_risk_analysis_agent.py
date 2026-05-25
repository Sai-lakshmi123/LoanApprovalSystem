"""
Financial Risk Analysis Agent (Agent2)
Uses Anthropic Agent SDK with Claude Sonnet 4.6 to analyze loan financial risk.
Connects to RiskRulesDB MCP Server and returns structured risk analysis.

Run the RiskRulesDB server first:
    python mcp/riskrulesdb/server.py

Then run this agent:
    python agents/financial_risk_analysis_agent.py
"""

import anthropic
import json
import httpx
from typing import Any
from datetime import datetime

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are an expert financial risk analyst specializing in loan underwriting. Your role is to comprehensively evaluate the financial risk of loan applications using the RiskRulesDB system.

## Your Responsibilities:

1. **Financial Assessment**: Analyze debt-to-income ratios, loan amounts, and financial capacity
2. **Risk Evaluation**: Assess credit risk with adjustments for delinquencies and inquiries
3. **Loan Metrics**: Evaluate loan-to-income and loan-to-value ratios
4. **Anomaly Detection**: Identify unusual patterns and red flags
5. **Comprehensive Analysis**: Synthesize all metrics into overall risk assessment
6. **Fair Lending**: Ensure objective, compliant analysis throughout

## Analysis Framework:

### Debt-to-Income (DTI) Ratio Analysis (0-100%)
- Calculate total monthly debt vs. monthly income
- Categories:
  - < 20%: Very Low Risk ✅
  - 20-36%: Low Risk ✅
  - 36-43%: Medium Risk ⚠️
  - 43-50%: High Risk ❌
  - > 50%: Very High Risk ❌❌

### Credit Score Risk Assessment
- Adjust credit score risk based on delinquencies and inquiries
- Categories:
  - Excellent (750+): Very Low Risk ✅
  - Good (700-749): Low Risk ✅
  - Fair (650-699): Medium Risk ⚠️
  - Poor (600-649): High Risk ❌
  - Very Poor (<600): Very High Risk ❌❌
- Apply penalties for negative factors

### Loan Amount Risk (LTI & LTV Analysis)
- Loan-to-Income (LTI): Loan amount vs. annual income
  - < 3%: Very Low ✅
  - 3-5%: Low ✅
  - 5-8%: Medium ⚠️
  - 8-12%: High ❌
  - > 12%: Very High ❌❌
- Loan-to-Value (LTV): Loan amount vs. property value
  - < 60%: Excellent ✅
  - 60-80%: Good ✅
  - 80-95%: Acceptable ⚠️
  - > 95%: High Risk ❌

### Anomaly Detection (9 Types)
Identify and classify unusual patterns:
- **Critical (Severity 100)**: High DTI (>50%), Recent delinquency (<6 months)
- **High (Severity 80)**: Low credit (<620), Unusual loan request (LTI >10%)
- **Medium (Severity 60)**: Excessive inquiries (>5 in 6mo), High utilization (>80%), Short tenure (<6mo)
- **Low (Severity 40)**: Income inconsistency, Age-employment mismatch

### Aggregate Risk Score (0-5 Scale)
Combine all dimensions:
- 0-1.5: Very Low Risk ✅ (APPROVE)
- 1.5-2.5: Low Risk ✅ (APPROVE with conditions)
- 2.5-3.5: Medium Risk ⚠️ (REVIEW)
- 3.5-4.5: High Risk ❌ (MANUAL UNDERWRITING)
- 4.5-5: Very High Risk ❌❌ (REJECT)

## Output Format:

Always structure your final analysis as valid JSON with these exact fields:
{
    "applicant_id": "string",
    "analysis_timestamp": "ISO format datetime",
    "dti_analysis": {
        "current_dti_percentage": number,
        "dti_with_new_loan_percentage": number,
        "dti_risk_level": "string",
        "analysis": "string - detailed explanation"
    },
    "credit_risk": {
        "credit_score": number,
        "base_risk_level": "string",
        "adjusted_risk_level": "string",
        "delinquencies": number,
        "inquiry_count": number,
        "analysis": "string - detailed explanation"
    },
    "loan_amount_risk": {
        "loan_amount": number,
        "annual_income": number,
        "property_value": number,
        "lti_percentage": number,
        "ltv_percentage": number,
        "overall_loan_risk": "string",
        "analysis": "string - detailed explanation"
    },
    "anomaly_detection": {
        "anomaly_count": number,
        "has_critical_anomalies": boolean,
        "anomalies": [
            {
                "type": "string",
                "severity": "string (Critical/High/Medium/Low)",
                "description": "string",
                "impact": "string"
            }
        ],
        "overall_anomaly_score": number,
        "analysis": "string"
    },
    "aggregate_risk_assessment": {
        "overall_risk_score": number (0-5),
        "overall_risk_level": "string (Very Low/Low/Medium/High/Very High)",
        "primary_risk_factors": ["string array"],
        "mitigating_factors": ["string array"],
        "recommendation": "string (APPROVE/CONDITIONAL/REVIEW/DECLINE)"
    },
    "financial_summary": "string - executive summary of financial risk",
    "key_findings": ["string array"],
    "recommended_conditions": ["string array"],
    "next_steps": ["string array"]
}

## Guidelines:

- Use actual RiskRulesDB data, not assumptions
- Be systematic in gathering all risk metrics
- Provide clear reasoning for all risk assessments
- Flag critical risk factors prominently
- Consider compensating factors
- Maintain fair lending compliance
- Provide actionable insights
- Balance conservatism with fairness

## Tools Available:

- evaluate_dti_ratio: Analyze debt-to-income metrics
- evaluate_credit_risk: Assess credit score risk
- evaluate_loan_amount_risk: Evaluate loan size relative to income/property
- detect_risk_anomalies: Identify unusual patterns and red flags
- generate_risk_report: Get comprehensive risk assessment
- evaluate_with_scenario_analysis: Test alternative loan amounts

Start by gathering all risk data, then synthesize into comprehensive analysis."""


# ============================================================================
# RISKRULESDB CLIENT
# ============================================================================

class RiskRulesDBClient:
    """Client for RiskRulesDB MCP Server."""

    def __init__(self, base_url: str = "http://localhost:3001", timeout: float = 30.0):
        """Initialize client."""
        self.base_url = base_url
        self.timeout = timeout

    def evaluate_dti_ratio(self, monthly_income: float, monthly_debt: float) -> dict:
        """Evaluate debt-to-income ratio."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/evaluate_dti_ratio/execute",
                json={"monthly_income": monthly_income, "monthly_debt": monthly_debt}
            )
            response.raise_for_status()
            return response.json()

    def evaluate_credit_risk(self, credit_score: int, delinquencies: int, inquiries: int) -> dict:
        """Evaluate credit score risk."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/evaluate_credit_risk/execute",
                json={
                    "credit_score": credit_score,
                    "delinquencies": delinquencies,
                    "inquiries_last_6_months": inquiries
                }
            )
            response.raise_for_status()
            return response.json()

    def evaluate_loan_amount_risk(
        self,
        loan_amount: float,
        annual_income: float,
        property_value: float,
        existing_loans: int,
        credit_score: int
    ) -> dict:
        """Evaluate loan amount risk."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/evaluate_loan_amount_risk/execute",
                json={
                    "loan_amount": loan_amount,
                    "annual_income": annual_income,
                    "property_value": property_value,
                    "existing_loans": existing_loans,
                    "credit_score": credit_score
                }
            )
            response.raise_for_status()
            return response.json()

    def detect_risk_anomalies(self, applicant: dict, loan: dict) -> dict:
        """Detect risk anomalies."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/detect_risk_anomalies/execute",
                json={"applicant": applicant, "loan": loan}
            )
            response.raise_for_status()
            return response.json()

    def generate_risk_report(self, applicant_id: str, applicant: dict, loan: dict) -> dict:
        """Generate comprehensive risk report."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/generate_risk_report/execute",
                json={"applicant_id": applicant_id, "applicant_data": applicant, "loan_request": loan}
            )
            response.raise_for_status()
            return response.json()

    def evaluate_with_scenario_analysis(
        self,
        applicant_id: str,
        applicant: dict,
        loan: dict,
        scenarios: list
    ) -> dict:
        """Evaluate with scenario analysis."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/evaluate_with_scenario_analysis/execute",
                json={
                    "applicant_id": applicant_id,
                    "applicant_data": applicant,
                    "base_loan_request": loan,
                    "scenarios": scenarios
                }
            )
            response.raise_for_status()
            return response.json()


# ============================================================================
# FINANCIAL RISK ANALYSIS AGENT
# ============================================================================

class FinancialRiskAnalysisAgent:
    """Agent for analyzing financial risk of loan applications."""

    def __init__(self, api_key: str = None):
        """Initialize agent with Anthropic client."""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"
        self.risk_db = RiskRulesDBClient()

    def define_tools(self) -> list:
        """Define tools for the agent."""
        return [
            {
                "name": "evaluate_dti_ratio",
                "description": "Evaluate debt-to-income ratio with risk assessment",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "monthly_income": {
                            "type": "number",
                            "description": "Monthly income in dollars"
                        },
                        "monthly_debt": {
                            "type": "number",
                            "description": "Total monthly debt obligations in dollars"
                        }
                    },
                    "required": ["monthly_income", "monthly_debt"]
                }
            },
            {
                "name": "evaluate_credit_risk",
                "description": "Evaluate credit score risk with adjustments",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "credit_score": {
                            "type": "integer",
                            "description": "Credit score (300-850)"
                        },
                        "delinquencies": {
                            "type": "integer",
                            "description": "Number of delinquencies"
                        },
                        "inquiries": {
                            "type": "integer",
                            "description": "Number of hard inquiries in last 6 months"
                        }
                    },
                    "required": ["credit_score", "delinquencies", "inquiries"]
                }
            },
            {
                "name": "evaluate_loan_amount_risk",
                "description": "Evaluate loan amount risk relative to income and property value",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "loan_amount": {
                            "type": "number",
                            "description": "Loan amount in dollars"
                        },
                        "annual_income": {
                            "type": "number",
                            "description": "Annual income in dollars"
                        },
                        "property_value": {
                            "type": "number",
                            "description": "Property value in dollars"
                        },
                        "existing_loans": {
                            "type": "integer",
                            "description": "Number of existing loans"
                        },
                        "credit_score": {
                            "type": "integer",
                            "description": "Credit score"
                        }
                    },
                    "required": ["loan_amount", "annual_income", "property_value", "existing_loans", "credit_score"]
                }
            },
            {
                "name": "detect_risk_anomalies",
                "description": "Detect unusual patterns and risk anomalies",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant": {
                            "type": "object",
                            "description": "Applicant profile data"
                        },
                        "loan": {
                            "type": "object",
                            "description": "Loan request data"
                        }
                    },
                    "required": ["applicant", "loan"]
                }
            },
            {
                "name": "generate_risk_report",
                "description": "Generate comprehensive financial risk assessment report",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        },
                        "applicant": {
                            "type": "object",
                            "description": "Complete applicant profile"
                        },
                        "loan": {
                            "type": "object",
                            "description": "Loan request details"
                        }
                    },
                    "required": ["applicant_id", "applicant", "loan"]
                }
            },
            {
                "name": "evaluate_with_scenario_analysis",
                "description": "Evaluate financial risk across multiple loan amount scenarios",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        },
                        "applicant": {
                            "type": "object",
                            "description": "Applicant profile"
                        },
                        "loan": {
                            "type": "object",
                            "description": "Base loan request"
                        },
                        "scenarios": {
                            "type": "array",
                            "description": "List of scenario dicts with 'name' and 'loan_amount' keys"
                        }
                    },
                    "required": ["applicant_id", "applicant", "loan", "scenarios"]
                }
            }
        ]

    def process_tool_call(self, tool_name: str, tool_input: dict) -> dict:
        """Process tool calls and return results."""
        try:
            if tool_name == "evaluate_dti_ratio":
                return self.risk_db.evaluate_dti_ratio(
                    tool_input.get("monthly_income"),
                    tool_input.get("monthly_debt")
                )
            elif tool_name == "evaluate_credit_risk":
                return self.risk_db.evaluate_credit_risk(
                    tool_input.get("credit_score"),
                    tool_input.get("delinquencies"),
                    tool_input.get("inquiries")
                )
            elif tool_name == "evaluate_loan_amount_risk":
                return self.risk_db.evaluate_loan_amount_risk(
                    tool_input.get("loan_amount"),
                    tool_input.get("annual_income"),
                    tool_input.get("property_value"),
                    tool_input.get("existing_loans"),
                    tool_input.get("credit_score")
                )
            elif tool_name == "detect_risk_anomalies":
                return self.risk_db.detect_risk_anomalies(
                    tool_input.get("applicant"),
                    tool_input.get("loan")
                )
            elif tool_name == "generate_risk_report":
                return self.risk_db.generate_risk_report(
                    tool_input.get("applicant_id"),
                    tool_input.get("applicant"),
                    tool_input.get("loan")
                )
            elif tool_name == "evaluate_with_scenario_analysis":
                return self.risk_db.evaluate_with_scenario_analysis(
                    tool_input.get("applicant_id"),
                    tool_input.get("applicant"),
                    tool_input.get("loan"),
                    tool_input.get("scenarios", [])
                )
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

    def analyze_financial_risk(
        self,
        applicant_id: str,
        applicant_data: dict,
        loan_request: dict
    ) -> dict:
        """Analyze financial risk and return structured analysis."""
        print(f"\n{'='*80}")
        print(f"  FINANCIAL RISK ANALYSIS AGENT - Analyzing {applicant_id}")
        print(f"{'='*80}\n")

        messages = [
            {
                "role": "user",
                "content": f"""Please analyze the financial risk for loan applicant {applicant_id}.

Applicant Profile:
{json.dumps(applicant_data, indent=2)}

Loan Request:
{json.dumps(loan_request, indent=2)}

Perform comprehensive financial risk analysis including:
1. Debt-to-Income (DTI) ratio assessment
2. Credit risk evaluation
3. Loan amount risk analysis (LTI and LTV)
4. Anomaly detection for red flags
5. Aggregate risk scoring

Return your complete analysis as valid JSON with all required fields."""
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

                print(f"\n>>> Agent Analysis Complete")
                print(f"\nFinal Response Length: {len(final_response)} chars")

                # Parse JSON from response
                try:
                    json_start = final_response.find("{")
                    json_end = final_response.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = final_response[json_start:json_end]
                        analysis = json.loads(json_str)
                        return {
                            "status": "success",
                            "analysis": analysis,
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
            "message": f"Agent did not complete analysis within {max_iterations} iterations"
        }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function to run the agent."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║   FINANCIAL RISK ANALYSIS AGENT (Agent2) - Anthropic Agent SDK with Claude    ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    # Initialize agent
    agent = FinancialRiskAnalysisAgent()

    # Sample applicant data and loan requests
    test_cases = [
        {
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
            "loan_request": {
                "loan_amount": 300000,
                "property_value": 500000,
                "loan_term_months": 360
            }
        },
        {
            "applicant_id": "APP002",
            "applicant_data": {
                "name": "Jane Moderate",
                "age": 35,
                "annual_income": 80000,
                "monthly_expenses": 2500,
                "existing_monthly_debt": 500,
                "credit_score": 700,
                "delinquencies": 0,
                "inquiries_last_6_months": 1,
                "credit_utilization": 0.45,
                "years_at_current_job": 3,
                "existing_loans": 1
            },
            "loan_request": {
                "loan_amount": 250000,
                "property_value": 400000,
                "loan_term_months": 360
            }
        }
    ]

    results = {}
    for test_case in test_cases:
        try:
            applicant_id = test_case["applicant_id"]
            result = agent.analyze_financial_risk(
                applicant_id,
                test_case["applicant_data"],
                test_case["loan_request"]
            )
            results[applicant_id] = result

            if result.get("status") == "success" and "analysis" in result:
                analysis = result["analysis"]
                print(f"\n✅ Analysis Complete for {applicant_id}")
                print(f"\n📊 DTI Risk: {analysis.get('dti_analysis', {}).get('dti_risk_level', 'N/A')}")
                print(f"📊 Credit Risk: {analysis.get('credit_risk', {}).get('adjusted_risk_level', 'N/A')}")
                print(f"📊 Loan Amount Risk: {analysis.get('loan_amount_risk', {}).get('overall_loan_risk', 'N/A')}")
                print(f"📊 Anomalies: {analysis.get('anomaly_detection', {}).get('anomaly_count', 0)}")
                print(f"📊 Overall Risk Score: {analysis.get('aggregate_risk_assessment', {}).get('overall_risk_score', 'N/A')}/5")
                print(f"📊 Recommendation: {analysis.get('aggregate_risk_assessment', {}).get('recommendation', 'N/A')}")

        except Exception as e:
            print(f"❌ Error analyzing {test_case['applicant_id']}: {e}")
            results[test_case["applicant_id"]] = {"status": "error", "message": str(e)}

    print(f"\n{'='*80}")
    print("All analyses complete.")
    print(f"{'='*80}\n")

    return results


if __name__ == "__main__":
    main()
