"""
Example multi-agent setup using LangGraph and LangChain
"""
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
import operator
import os
from dotenv import load_dotenv

load_dotenv()

# Define agent state
class AgentState(TypedDict):
    """State object passed between agents"""
    messages: Annotated[list[BaseMessage], operator.add]
    current_agent: str
    step_count: int

# Initialize Claude model
def get_model():
    """Get Claude model from Anthropic"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")
    return ChatAnthropic(
        model="claude-opus-4-1-20250805",
        temperature=0.7,
        api_key=api_key
    )

# Define individual agent nodes
def loan_processor_node(state: AgentState) -> AgentState:
    """
    Agent that processes loan applications
    """
    model = get_model()

    user_message = state["messages"][-1].content if state["messages"] else ""

    response = model.invoke([
        HumanMessage(content=f"""You are a loan processing agent.
Your job is to extract key information from loan applications.

User input: {user_message}

Respond with:
1. Loan amount
2. Applicant income
3. Loan purpose
4. Any red flags""")
    ])

    return {
        "messages": state["messages"] + [response],
        "current_agent": "loan_processor",
        "step_count": state.get("step_count", 0) + 1
    }

def risk_analyzer_node(state: AgentState) -> AgentState:
    """
    Agent that analyzes risk factors
    """
    model = get_model()

    conversation = "\n".join([
        f"{msg.type}: {msg.content}" for msg in state["messages"]
    ])

    response = model.invoke([
        HumanMessage(content=f"""You are a risk analysis agent.
Analyze the loan application for risk factors.

Conversation so far:
{conversation}

Provide a risk assessment (LOW, MEDIUM, HIGH) and explain your reasoning.""")
    ])

    return {
        "messages": state["messages"] + [response],
        "current_agent": "risk_analyzer",
        "step_count": state.get("step_count", 0) + 1
    }

def approval_agent_node(state: AgentState) -> AgentState:
    """
    Agent that makes approval decisions
    """
    model = get_model()

    conversation = "\n".join([
        f"{msg.type}: {msg.content}" for msg in state["messages"]
    ])

    response = model.invoke([
        HumanMessage(content=f"""You are an approval decision agent.
Based on the analysis, make a final approval decision.

Conversation so far:
{conversation}

Respond with:
- APPROVED / REJECTED / PENDING
- Reasoning
- Any conditions (if approved)""")
    ])

    return {
        "messages": state["messages"] + [response],
        "current_agent": "approval_agent",
        "step_count": state.get("step_count", 0) + 1
    }

# Define routing logic
def should_analyze_risk(state: AgentState) -> str:
    """Route to risk analyzer after loan processing"""
    if state["current_agent"] == "loan_processor":
        return "risk_analyzer"
    return END

def should_approve(state: AgentState) -> str:
    """Route to approval agent after risk analysis"""
    if state["current_agent"] == "risk_analyzer":
        return "approval_agent"
    return END

# Build the graph
def create_loan_approval_graph():
    """
    Create a LangGraph workflow for loan approval
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("loan_processor", loan_processor_node)
    graph.add_node("risk_analyzer", risk_analyzer_node)
    graph.add_node("approval_agent", approval_agent_node)

    # Add edges with routing
    graph.add_edge(START, "loan_processor")
    graph.add_conditional_edges(
        "loan_processor",
        should_analyze_risk,
        {"risk_analyzer": "risk_analyzer", END: END}
    )
    graph.add_conditional_edges(
        "risk_analyzer",
        should_approve,
        {"approval_agent": "approval_agent", END: END}
    )
    graph.add_edge("approval_agent", END)

    return graph.compile()

# Example usage
if __name__ == "__main__":
    # Create graph
    graph = create_loan_approval_graph()

    # Example input
    initial_state = {
        "messages": [HumanMessage(content="I need a $50,000 loan for a car")],
        "current_agent": "start",
        "step_count": 0
    }

    # Run the graph
    print("Starting loan approval workflow...\n")

    result = graph.invoke(initial_state)

    print("\n=== Workflow Complete ===")
    print(f"Total steps: {result['step_count']}")
    print("\nFinal conversation:")
    for i, msg in enumerate(result["messages"]):
        print(f"\n[{i}] {msg.__class__.__name__}:")
        print(msg.content[:200] + "..." if len(msg.content) > 200 else msg.content)
