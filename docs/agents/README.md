# 🤖 Agents Documentation

Four intelligent AI agents that collaborate to evaluate loan applications.

## 📖 Overview

The system uses **Claude Sonnet 4.6** (via Anthropic Agent SDK) to power four specialized agents:

1. **Agent 1: Application Profile Analysis**
   - Evaluates applicant profile and financial stability
   - Scores income stability and credit quality
   
2. **Agent 2: Financial Risk Analysis**
   - Calculates debt-to-income ratio, loan-to-value ratio
   - Identifies financial anomalies and risk factors
   
3. **Agent 3: Loan Decision Synthesis**
   - Synthesizes findings from Agent 1 & 2
   - Makes APPROVE/REJECT/REVIEW decision
   
4. **Agent 4: Compliance & Notification**
   - Ensures Fair Lending Act, TILA, FCRA, ECOA compliance
   - Records case ID and sends notifications

## 📊 Agent Details

### [Agent 1: Profile Analysis](agent-1-profile/)
- [Implementation Guide](agent-1-profile/implementation.md)
- [System Prompt](agent-1-profile/prompt.md) - How it's instructed
- [Quick Reference](agent-1-profile/quick-reference.md)
- [Summary](agent-1-profile/summary.txt)

**Role:** Analyzes applicant information and financial stability  
**Input:** Age, income, employment, credit history  
**Output:** Profile strength (1-5), employment risk, credit summary

---

### [Agent 2: Risk Analysis](agent-2-risk/)
- [Implementation Guide](agent-2-risk/implementation.md)
- [System Prompt](agent-2-risk/prompt.md)
- [Quick Reference](agent-2-risk/quick-reference.md)
- [Summary](agent-2-risk/summary.txt)

**Role:** Evaluates financial risk and identifies concerns  
**Input:** Income, expenses, liabilities, loan amount  
**Output:** Risk score (1-5), DTI ratio, anomalies detected

---

### [Agent 3: Decision Synthesis](agent-3-decision/)
- [Implementation Guide](agent-3-decision/implementation.md)
- [System Prompt](agent-3-decision/prompt.md)
- [Quick Reference](agent-3-decision/quick-reference.md)
- [Summary](agent-3-decision/summary.txt)

**Role:** Makes final loan approval decision  
**Input:** Profile analysis + Risk analysis  
**Output:** Decision (APPROVE/REJECT/REVIEW), confidence level, reasoning

---

### [Agent 4: Compliance & Notification](agent-4-compliance/)
- [Implementation Guide](agent-4-compliance/implementation.md)
- [System Prompt](agent-4-compliance/prompt.md)
- [Quick Reference](agent-4-compliance/quick-reference.md)
- [Summary](agent-4-compliance/summary.txt)

**Role:** Ensures regulatory compliance and records decision  
**Input:** Loan decision + Applicant data  
**Output:** Case ID, compliance status, notifications sent

---

## 🎯 Decision Flow

```
┌──────────────────────────┐
│   Loan Application       │
│   (Applicant Data)       │
└────────────┬─────────────┘
             │
┌────────────┴─────────────┐
│ Agent 1: Profile         │
│ Analysis                 │
│ → Profile Strength       │
│ → Employment Risk        │
└────────────┬─────────────┘
             │
┌────────────┴─────────────┐
│ Agent 2: Risk Analysis   │
│ → DTI Calculation        │
│ → Risk Score             │
└────────────┬─────────────┘
             │
┌────────────┴─────────────┐
│ Agent 3: Decision        │
│ → APPROVE/REJECT/REVIEW  │
│ → Confidence Level       │
└────────────┬─────────────┘
             │
┌────────────┴─────────────┐
│ Agent 4: Compliance      │
│ → Verify Fair Lending    │
│ → Record Case ID         │
└────────────┬─────────────┘
             │
        ┌────┴────┐
        │ FINAL   │
        │ DECISION│
        └─────────┘
```

## 📋 System Prompts

All agent prompts are detailed here:
- [All System Prompts](system-prompts.md) - Complete prompt text
- [Prompts Summary](prompts-summary.md) - Quick summary of each

## 🔧 Technology Stack

- **LLM:** Claude Sonnet 4.6
- **SDK:** Anthropic Agent SDK
- **Orchestration:** LangGraph (see [architecture docs](../architecture/langgraph-orchestration.md))
- **Data Source:** MCP Servers (see [mcp-servers docs](../mcp-servers/))

## 📈 Key Metrics

| Metric | Description |
|--------|-------------|
| **Profile Strength** | 1-5 scale (income stability + credit quality) |
| **Risk Score** | 1-5 scale (financial risk assessment) |
| **DTI Ratio** | Debt-to-Income (target: < 0.43) |
| **LTV Ratio** | Loan-to-Value (property value consideration) |
| **Confidence** | 0-100% (decision certainty) |

## ⚙️ Agent Collaboration

Agents work in **sequence** (not parallel):

1. **Agent 1** gathers and analyzes profile data
2. **Agent 2** analyzes financial risk based on Agent 1's output
3. **Agent 3** synthesizes findings and makes decision
4. **Agent 4** verifies compliance and records case

If any agent encounters an issue → System routes to **manual review**

## 🔗 Related Documentation

- **Orchestration:** See [LangGraph Guide](../architecture/langgraph-orchestration.md)
- **MCP Servers:** See [MCP Documentation](../mcp-servers/) (data sources)
- **API:** See [FastAPI Guide](../fastapi/) (how requests are received)
- **Testing:** See [Testing Guide](../testing/) (how to test agents)

## 🚀 Getting Started

1. **Understand the overall architecture:** [Architecture Overview](../architecture/)
2. **Read Agent 1 implementation:** [Agent 1 Guide](agent-1-profile/implementation.md)
3. **Review system prompts:** [System Prompts](system-prompts.md)
4. **See agents in action:** [Testing Guide](../testing/test-scenarios.md)

---

**Next:** Explore individual agent folders above! 🤖📖
