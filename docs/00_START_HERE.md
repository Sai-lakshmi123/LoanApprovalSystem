# 📚 Loan Approval System - Documentation Hub

Welcome! This folder contains complete documentation for the multi-agent Loan Approval System. Choose your starting point below:

---

## 🚀 **Quick Start (5 minutes)**

**New to the project?** Start here:
1. Read [Installation Guide](setup-deployment/installation-guide.md)
2. Run `bash START_SERVICES.sh`
3. Open Streamlit UI at `http://localhost:8501`

---

## 📑 **Documentation By Category**

### 🏗️ **[Architecture](architecture/)** - Understand the System Design
- [System Overview](architecture/system-index.md) - High-level architecture
- [Layer Architecture](architecture/layer-architecture.md) - Presentation, Microservices, Orchestration, Agents
- [System Design](architecture/system-design.md) - Detailed design patterns
- [LangGraph Orchestration](architecture/langgraph-orchestration.md) - Workflow coordination
- [Project Structure](architecture/project-structure.md) - Folder organization
- [Folder Tree](architecture/folder-tree.txt) - Visual directory structure

### ⚙️ **[Setup & Deployment](setup-deployment/)** - Install & Configure
- [Installation Guide](setup-deployment/installation-guide.md) - Step-by-step setup
- [Environment Setup](setup-deployment/.env.example) - Configuration template
- [Security Best Practices](setup-deployment/security-best-practices.md) - Keep your API keys safe
- [Security Checklist](setup-deployment/security-checklist.md) - Pre-deployment checklist
- [Deployment Guide](setup-deployment/start-services.sh) - Start all services

### 🤖 **[Agents](agents/)** - AI Decision Makers
Four intelligent agents work together to evaluate loan applications:

1. **[Agent 1: Profile Analysis](agents/agent-1-profile/)**
   - Analyzes applicant profile and financial stability
   - [Implementation](agents/agent-1-profile/implementation.md)
   - [System Prompt](agents/agent-1-profile/prompt.md)
   - [Quick Reference](agents/agent-1-profile/quick-reference.md)

2. **[Agent 2: Risk Analysis](agents/agent-2-risk/)**
   - Evaluates financial risk and credit metrics
   - [Implementation](agents/agent-2-risk/implementation.md)
   - [System Prompt](agents/agent-2-risk/prompt.md)
   - [Quick Reference](agents/agent-2-risk/quick-reference.md)

3. **[Agent 3: Decision Synthesis](agents/agent-3-decision/)**
   - Makes final approval/rejection decision
   - [Implementation](agents/agent-3-decision/implementation.md)
   - [System Prompt](agents/agent-3-decision/prompt.md)
   - [Quick Reference](agents/agent-3-decision/quick-reference.md)

4. **[Agent 4: Compliance](agents/agent-4-compliance/)**
   - Ensures regulatory compliance (TILA, FCRA, ECOA)
   - [Implementation](agents/agent-4-compliance/implementation.md)
   - [System Prompt](agents/agent-4-compliance/prompt.md)
   - [Quick Reference](agents/agent-4-compliance/quick-reference.md)

**All Agents Overview:** [System Prompts](agents/system-prompts.md) | [Summary](agents/prompts-summary.md)

### 📡 **[MCP Servers](mcp-servers/)** - Data & Tool Integration
Four Model Context Protocol servers provide data and tools:

1. **[Application DB](mcp-servers/application-db/)**
   - Fetches applicant profiles and financial data
   - [Implementation](mcp-servers/application-db/implementation.md)
   - [Quick Reference](mcp-servers/application-db/quick-reference.md)

2. **[Risk Rules DB](mcp-servers/risk-rules-db/)**
   - Evaluates debt-to-income, credit risk, loan amount risk
   - [Implementation](mcp-servers/risk-rules-db/implementation.md) | [Summary](mcp-servers/risk-rules-db/summary.txt)

3. **[Decision Synthesis](mcp-servers/decision-synthesis/)**
   - Compiles decision classification and factors
   - [Implementation](mcp-servers/decision-synthesis/implementation.md) | [Summary](mcp-servers/decision-synthesis/summary.txt)

4. **[Notification System](mcp-servers/notification-system/)**
   - Records compliance actions and case tracking
   - [Implementation](mcp-servers/notification-system/implementation.md) | [Summary](mcp-servers/notification-system/summary.txt)

**MCP Overview:** [Overview](mcp-servers/overview.md) | [Quick Start](mcp-servers/quick-start.md) | [Usage Guide](mcp-servers/usage-guide.md)

### 🔌 **[FastAPI](fastapi/)** - REST API Server
RESTful API for loan evaluation:

- [Overview](fastapi/overview.md) - API introduction
- [API Reference](fastapi/api-reference.md) - All endpoints
- [Quick Start](fastapi/quick-start.md) - Get API running
- [Implementation Summary](fastapi/implementation-summary.md) - Service details

**Key Endpoint:** `POST /evaluate-loan` - Submit loan application

### 🎨 **[Streamlit UI](streamlit-ui/)** - Web Interface
Interactive web application for loan submission:

- [Quick Start](streamlit-ui/quick-start.md) - Launch UI
- [UI Guide](streamlit-ui/ui-guide.md) - Feature walkthrough
- [Implementation Summary](streamlit-ui/implementation-summary.md) - Technical details

**Features:** Application form | Real-time results | History tracking | Analytics

### 🧪 **[Testing](testing/)** - Validation & Quality
Test suites and example scenarios:

- [Test Scenarios](testing/test-scenarios.md) - 3 sample loan applications
- [Implementation Guide](testing/implementation-guide.md) - Running tests
- [cURL Examples](testing/curl-examples.sh) - Direct API testing

### ⚠️ **[API Integration](api-integration/)** - Error Handling & Recovery
Handle errors gracefully:

- [Error Handling Guide](api-integration/error-handling-guide.md) - Error types & recovery
- [Error Reference](api-integration/error-handling-reference.md) - Quick lookup
- [Error Summary](api-integration/error-summary.txt) - Overview

---

## 🔑 **Key Concepts**

### Decision Flow
```
Applicant Info 
  ↓
Agent 1: Profile Analysis
  ↓
Agent 2: Risk Analysis
  ↓
Agent 3: Decision Synthesis
  ↓
Agent 4: Compliance Check
  ↓
APPROVE / REJECT / REVIEW
```

### Technology Stack
- **LLM:** Claude Sonnet 4.6 (Anthropic Agent SDK)
- **Orchestration:** LangGraph StateGraph
- **APIs:** FastAPI (Python)
- **UI:** Streamlit
- **Data Integration:** MCP (Model Context Protocol)
- **Tools:** FastMCP framework for MCP servers

### Key Files
- `src/api/main.py` - FastAPI service
- `src/ui/streamlit_app.py` - Streamlit web UI
- `agents/*.py` - Four intelligent agents
- `mcp/*.py` - Four MCP data servers
- `orchestration/*.py` - LangGraph workflow

---

## 📦 **Project Structure at a Glance**

```
LoanApprovalSystem/
├── docs/                          ← You are here
├── src/
│   ├── api/                       ← FastAPI service
│   └── ui/                        ← Streamlit UI
├── agents/                        ← 4 AI agents
├── mcp/                           ← 4 MCP servers
├── orchestration/                 ← LangGraph workflow
├── utils/                         ← Helper functions
├── tests/                         ← Test suite
├── requirements.txt               ← Dependencies
└── README.md                      ← Main README
```

---

## 🎯 **For Different Roles**

### 👨‍💻 **Developers**
Start with: [Architecture](architecture/) → [FastAPI](fastapi/) → [Agents](agents/)

### 🔧 **DevOps/Operations**
Start with: [Setup & Deployment](setup-deployment/) → [Security Best Practices](setup-deployment/security-best-practices.md)

### 📊 **Business Analysts**
Start with: [System Overview](architecture/system-index.md) → [Agents](agents/) (understand decision logic)

### 🧪 **QA/Testers**
Start with: [Testing](testing/) → [API Integration](api-integration/)

### 🔒 **Security Team**
Start with: [Security Best Practices](setup-deployment/security-best-practices.md) → [Security Checklist](setup-deployment/security-checklist.md)

---

## ❓ **Common Questions**

**Q: How do I start the system?**  
A: See [Installation Guide](setup-deployment/installation-guide.md)

**Q: How do agents make decisions?**  
A: See [Agents Overview](agents/) - each agent has a detailed guide

**Q: How do I call the API?**  
A: See [API Reference](fastapi/api-reference.md)

**Q: What's the architecture?**  
A: See [System Overview](architecture/system-index.md)

**Q: How do I handle errors?**  
A: See [Error Handling Guide](api-integration/error-handling-guide.md)

---

## 📞 **Support Resources**

- **Main README:** See [project root README](../README.md)
- **API Documentation:** [FastAPI Guide](fastapi/api-reference.md)
- **Security Issues:** [Security Best Practices](setup-deployment/security-best-practices.md)
- **Errors:** [Error Handling Guide](api-integration/error-handling-guide.md)

---

**Last Updated:** May 25, 2026  
**Version:** 2.0.0

Start reading → Pick a category above → Explore → Build amazing things! 🚀
