"""
Application Profile Agent
Uses Anthropic Agent SDK with Claude Sonnet 4.6 to analyze loan applicant data.
Connects to Application DB MCP Server and returns structured applicant analysis.

Run the Application DB server first:
    python mcp/server.py

Then run this agent:
    python agents/application_profile_agent.py
"""

import anthropic
import json
import httpx
from typing import Any

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are an expert loan application profile analyst. Your role is to thoroughly analyze loan applicant data from our Application Database and provide comprehensive, structured analysis.

## Your Responsibilities:

1. **Data Gathering**: Use the available tools to fetch complete applicant profiles from the Application DB MCP Server
2. **Detailed Analysis**: Analyze all aspects of the applicant's financial and employment history
3. **Structured Output**: Return well-organized analysis with specific metrics and scores
4. **Risk Assessment**: Identify key risk factors and stability indicators
5. **Compliance**: Ensure fair lending by considering all relevant factors objectively

## Analysis Framework:

### Income Stability Score (0-100)
- Analyze income sources and consistency
- Consider employment length and tenure
- Evaluate income growth trends
- Check for income variability
- Return score where: 0-30 = Very Unstable, 31-50 = Unstable, 51-70 = Stable, 71-100 = Very Stable

### Employment Risk Assessment
- Evaluate employment type and security
- Consider industry trends
- Assess employment tenure
- Return risk level: Very Low (0-20), Low (21-40), Medium (41-60), High (61-80), Very High (81-100)

### Credit History Summary
- Review credit score category
- Identify any delinquencies or defaults
- Note credit utilization patterns
- Consider credit age and mix
- Return comprehensive summary with score category

### Application Completeness Flags
- Check all required fields are present
- Identify missing documentation
- Flag incomplete sections
- Return completion percentage and specific missing items

## Output Format:

Always structure your final analysis as valid JSON with these exact fields:
{
    "applicant_id": "string",
    "applicant_name": "string",
    "analysis_timestamp": "ISO format datetime",
    "income_stability": {
        "score": number (0-100),
        "stability_category": "string (Very Unstable/Unstable/Stable/Very Stable)",
        "analysis": "string - detailed explanation"
    },
    "employment_risk": {
        "risk_score": number (0-100),
        "risk_level": "string (Very Low/Low/Medium/High/Very High)",
        "employment_type": "string",
        "tenure_years": number,
        "analysis": "string - detailed explanation"
    },
    "credit_history": {
        "credit_score": number,
        "score_category": "string",
        "delinquencies": number,
        "default_count": number,
        "credit_utilization": number (0-100),
        "summary": "string - comprehensive summary"
    },
    "application_completeness": {
        "is_complete": boolean,
        "completeness_percentage": number (0-100),
        "missing_items": ["string array of missing fields"],
        "flags": ["string array of completion flags"]
    },
    "overall_assessment": "string - executive summary",
    "key_strengths": ["string array"],
    "key_concerns": ["string array"],
    "recommended_next_steps": ["string array"]
}

## Guidelines:

- Be thorough and objective in your analysis
- Provide clear reasoning for all scores and assessments
- Flag any discrepancies or concerns
- Highlight strengths and mitigating factors
- Consider the applicant's overall profile, not isolated factors
- Ensure all analysis is fair and compliant with lending regulations
- Use the actual data from the database, not assumptions

## Tools Available:

You have access to the following tools:
- get_applicant_profile: Retrieve complete applicant profile data
- get_income_stability_score: Get income stability analysis
- get_employment_risk: Get employment risk assessment
- get_credit_history_summary: Get credit history analysis
- check_application_completeness: Check application completeness
- get_complete_applicant_analysis: Get all analyses in one call

Start by gathering the applicant data, then provide your structured analysis."""


# ============================================================================
# APPLICATION DB CLIENT
# ============================================================================

class ApplicationDBClient:
    """Client for Application DB MCP Server."""

    def __init__(self, base_url: str = "http://localhost:3000", timeout: float = 30.0):
        """Initialize client."""
        self.base_url = base_url
        self.timeout = timeout

    def get_applicant_profile(self, applicant_id: str) -> dict:
        """Get applicant profile from Application DB."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/get_applicant_profile/execute",
                json={"applicant_id": applicant_id}
            )
            response.raise_for_status()
            return response.json()

    def get_income_stability_score(self, applicant_id: str) -> dict:
        """Get income stability score."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/get_income_stability_score/execute",
                json={"applicant_id": applicant_id}
            )
            response.raise_for_status()
            return response.json()

    def get_employment_risk(self, applicant_id: str) -> dict:
        """Get employment risk assessment."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/get_employment_risk/execute",
                json={"applicant_id": applicant_id}
            )
            response.raise_for_status()
            return response.json()

    def get_credit_history_summary(self, applicant_id: str) -> dict:
        """Get credit history summary."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/get_credit_history_summary/execute",
                json={"applicant_id": applicant_id}
            )
            response.raise_for_status()
            return response.json()

    def check_application_completeness(self, applicant_id: str) -> dict:
        """Check application completeness."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/check_application_completeness_tool/execute",
                json={"applicant_id": applicant_id}
            )
            response.raise_for_status()
            return response.json()

    def get_complete_applicant_analysis(self, applicant_id: str) -> dict:
        """Get complete applicant analysis."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/tools/get_complete_applicant_analysis/execute",
                json={"applicant_id": applicant_id}
            )
            response.raise_for_status()
            return response.json()


# ============================================================================
# APPLICATION PROFILE AGENT
# ============================================================================

class ApplicationProfileAgent:
    """Agent for analyzing loan applicant profiles."""

    def __init__(self, api_key: str = None):
        """Initialize agent with Anthropic client."""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"
        self.app_db = ApplicationDBClient()

    def define_tools(self) -> list:
        """Define tools for the agent."""
        return [
            {
                "name": "get_applicant_profile",
                "description": "Retrieve complete applicant profile data including name, age, income, employment, and credit information",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier (e.g., APP001)"
                        }
                    },
                    "required": ["applicant_id"]
                }
            },
            {
                "name": "get_income_stability_score",
                "description": "Get income stability analysis with score (0-100) and stability category",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        }
                    },
                    "required": ["applicant_id"]
                }
            },
            {
                "name": "get_employment_risk",
                "description": "Get employment risk assessment with risk score and level",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        }
                    },
                    "required": ["applicant_id"]
                }
            },
            {
                "name": "get_credit_history_summary",
                "description": "Get credit history summary including credit score, delinquencies, and utilization",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        }
                    },
                    "required": ["applicant_id"]
                }
            },
            {
                "name": "check_application_completeness",
                "description": "Check application completeness percentage and identify missing items",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        }
                    },
                    "required": ["applicant_id"]
                }
            },
            {
                "name": "get_complete_applicant_analysis",
                "description": "Get complete analysis of applicant (all metrics in one call)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {
                            "type": "string",
                            "description": "Unique applicant identifier"
                        }
                    },
                    "required": ["applicant_id"]
                }
            }
        ]

    def process_tool_call(self, tool_name: str, tool_input: dict) -> dict:
        """Process tool calls and return results."""
        try:
            applicant_id = tool_input.get("applicant_id")

            if tool_name == "get_applicant_profile":
                return self.app_db.get_applicant_profile(applicant_id)
            elif tool_name == "get_income_stability_score":
                return self.app_db.get_income_stability_score(applicant_id)
            elif tool_name == "get_employment_risk":
                return self.app_db.get_employment_risk(applicant_id)
            elif tool_name == "get_credit_history_summary":
                return self.app_db.get_credit_history_summary(applicant_id)
            elif tool_name == "check_application_completeness":
                return self.app_db.check_application_completeness(applicant_id)
            elif tool_name == "get_complete_applicant_analysis":
                return self.app_db.get_complete_applicant_analysis(applicant_id)
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

    def analyze_applicant(self, applicant_id: str) -> dict:
        """Analyze an applicant and return structured analysis."""
        print(f"\n{'='*80}")
        print(f"  APPLICATION PROFILE AGENT - Analyzing {applicant_id}")
        print(f"{'='*80}\n")

        messages = [
            {
                "role": "user",
                "content": f"Please analyze the loan applicant with ID {applicant_id}. Gather all available data about this applicant and provide a comprehensive structured analysis including income stability score, employment risk, credit history summary, and application completeness flags. Return your analysis as valid JSON."
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
                        print(f"Input: {json.dumps(tool_input, indent=2)}")

                        # Process the tool call
                        result = self.process_tool_call(tool_name, tool_input)
                        print(f"Result: {json.dumps(result, indent=2)[:200]}...")

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
                print(f"\nFinal Response:\n{final_response[:500]}...")

                # Parse JSON from response
                try:
                    # Try to extract JSON from the response
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
    print("║        APPLICATION PROFILE AGENT - Anthropic Agent SDK with Claude Sonnet 4.6 ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")

    # Initialize agent
    agent = ApplicationProfileAgent()

    # Analyze applicants
    applicant_ids = ["APP001", "APP002", "APP003"]

    results = {}
    for applicant_id in applicant_ids:
        try:
            result = agent.analyze_applicant(applicant_id)
            results[applicant_id] = result

            if result.get("status") == "success":
                if "analysis" in result:
                    analysis = result["analysis"]
                    print(f"\n✅ Analysis Complete for {applicant_id}")
                    print(f"\n📊 Income Stability: {analysis.get('income_stability', {}).get('score')} ({analysis.get('income_stability', {}).get('stability_category')})")
                    print(f"📊 Employment Risk: {analysis.get('employment_risk', {}).get('risk_level')} ({analysis.get('employment_risk', {}).get('risk_score')})")
                    print(f"📊 Credit Score: {analysis.get('credit_history', {}).get('credit_score')} ({analysis.get('credit_history', {}).get('score_category')})")
                    print(f"📊 Application Completeness: {analysis.get('application_completeness', {}).get('completeness_percentage')}%")
                    print(f"\n📋 Overall Assessment:\n{analysis.get('overall_assessment', 'N/A')}")

        except Exception as e:
            print(f"❌ Error analyzing {applicant_id}: {e}")
            results[applicant_id] = {"status": "error", "message": str(e)}

    # Save results
    print(f"\n{'='*80}")
    print("All analyses complete. Results saved.")
    print(f"{'='*80}\n")

    return results


if __name__ == "__main__":
    main()
