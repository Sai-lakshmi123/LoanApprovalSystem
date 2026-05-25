# Multi-Agent Loan Approval System - Architecture Documentation

## 📐 System Architecture Overview

This document provides comprehensive details about the multi-agent loan approval system architecture, including component interactions, data flows, and design patterns.

---

## 🏗️ Architecture Layers

### Layer 1: Presentation Layer (Streamlit)
**Location**: `presentation/`
**Responsibility**: User interface and interaction

```
┌─────────────────────────────────────┐
│   Streamlit Presentation Layer      │
├─────────────────────────────────────┤
│  Pages:                             │
│  • Dashboard - KPIs & analytics     │
│  • Loan Application - Form input    │
│  • Application Status - Tracking    │
│  • Analytics - Reports              │
│  • Settings - User preferences      │
├─────────────────────────────────────┤
│  Components:                        │
│  • Forms, Cards, Charts             │
│  • Status Indicators, Navigation    │
├─────────────────────────────────────┤
│  Utils:                             │
│  • API Client (HTTP calls)          │
│  • Session State Management         │
│  • Data Formatters & Validators     │
└─────────────────────────────────────┘
```

**Key Files**:
- `app.py` - Main entry point, page routing
- `pages/` - Individual page implementations
- `components/` - Reusable UI components
- `utils/api_client.py` - Communicates with FastAPI

---

### Layer 2: Microservices Layer (FastAPI)
**Location**: `microservices/`
**Responsibility**: RESTful API and business logic orchestration

```
┌─────────────────────────────────────┐
│   FastAPI Microservices Layer       │
├─────────────────────────────────────┤
│  API Routes:                        │
│  • /loans - CRUD operations         │
│  • /status - Application tracking   │
│  • /analytics - Reporting           │
│  • /health - Health checks          │
├─────────────────────────────────────┤
│  Data Validation:                   │
│  • Pydantic Schemas                 │
│  • Request/Response models          │
├─────────────────────────────────────┤
│  Database:                          │
│  • SQLAlchemy ORM models            │
│  • CRUD operations                  │
├─────────────────────────────────────┤
│  Middleware:                        │
│  • Authentication & Authorization   │
│  • Request/Response Logging         │
│  • Error Handling                   │
│  • CORS Configuration               │
├─────────────────────────────────────┤
│  Dependency Injection:              │
│  • Database sessions                │
│  • LangGraph orchestrator           │
│  • MCP clients                      │
│  • Authentication context           │
└─────────────────────────────────────┘
```

**Key Files**:
- `main.py` - FastAPI initialization
- `api/` - Route definitions
- `schemas/` - Pydantic validation models
- `models/` - SQLAlchemy ORM models
- `crud/` - Database operations
- `dependencies/` - Dependency injection setup
- `middleware/` - Request processing

---

### Layer 3: Orchestration Layer (LangGraph)
**Location**: `orchestration/`
**Responsibility**: Workflow graph definition and state management

```
┌─────────────────────────────────────┐
│   LangGraph Orchestration Layer     │
├─────────────────────────────────────┤
│  Graph Builder:                     │
│  • StateGraph definition            │
│  • Node definitions (agents)        │
│  • Edge definitions (transitions)   │
│  • Conditional routing              │
├─────────────────────────────────────┤
│  State Management:                  │
│  • Application state                │
│  • Conversation history             │
│  • Workflow progress                │
│  • Context preservation             │
├─────────────────────────────────────┤
│  Workflows:                         │
│  • Loan Approval Workflow           │
│  • Parallel Processing              │
│  • Callback/Async Workflows         │
└─────────────────────────────────────┘
```

**Workflow Graph**:
```
START
  ↓
┌─────────────────────────┐
│ Node 1: Loan Processor  │ (Extracts & validates application)
└────────────┬────────────┘
             ↓
┌─────────────────────────────┐
│ Node 2: Credit Analyzer     │ (Analyzes credit history)
└────────────┬────────────────┘
             ↓
┌──────────────────────────────┐
│ Node 3: Risk Assessor        │ (Evaluates financial risk)
└────────────┬─────────────────┘
             ↓
┌──────────────────────────────┐
│ Node 4: Decision Maker       │ (Makes approval decision)
└────────────┬─────────────────┘
             ↓
          END
```

**Key Files**:
- `graph.py` - Builds the workflow graph
- `state.py` - Defines state schema
- `router.py` - Conditional routing logic
- `workflows/` - Workflow implementations

---

### Layer 4: Agent Layer (4 Specialized Agents)
**Location**: `agents/`
**Responsibility**: AI-powered decision making using LLMs

#### **Agent 1: Loan Processor**
```
Input: Raw loan application data
Process:
  • Extract key information
  • Validate data completeness
  • Check for required fields
  • Standardize formats
Output: Processed application data
```

**Location**: `agents/loan_processor/`
- `agent.py` - Core agent logic
- `prompts.py` - System prompts
- `tools.py` - Available tools
- `validators.py` - Input validation

---

#### **Agent 2: Credit Analyzer**
```
Input: Applicant information + credit requirements
Process:
  • Query credit bureau via MCP tools
  • Analyze credit history
  • Calculate credit score
  • Assess payment history
  • Identify risk factors
Output: Credit analysis report
```

**Location**: `agents/credit_analyzer/`
- Integrates with MCP to access external credit data
- Uses financial calculation tools
- Maintains conversation context

---

#### **Agent 3: Risk Assessor**
```
Input: Application data + credit analysis
Process:
  • Calculate debt-to-income ratio
  • Evaluate employment stability
  • Assess loan-to-value ratio
  • Calculate risk metrics
  • Compare to risk thresholds
Output: Risk assessment score
```

**Location**: `agents/risk_assessor/`
- Uses MCP calculation tools
- Applies compliance rules (via MCP resources)
- Generates risk metrics

---

#### **Agent 4: Decision Maker**
```
Input: All previous analyses
Process:
  • Review all supporting data
  • Apply approval decision rules
  • Check compliance requirements
  • Make APPROVED/REJECTED decision
  • Generate justification
Output: Final decision + reasoning
```

**Location**: `agents/decision_maker/`
- Synthesizes all agent outputs
- Applies business rules
- Makes final determination
- Generates documentation

---

### Layer 5: MCP Integration Layer
**Location**: `mcp/`
**Responsibility**: Model Context Protocol for tools and resources

```
┌─────────────────────────────────────┐
│   MCP Integration Layer             │
├─────────────────────────────────────┤
│  Tools (Agent-callable functions):  │
│  ┌─────────────────────────────────┐│
│  │ Database Tools                   ││
│  │ • Query applicant history        ││
│  │ • Fetch credit bureau data       ││
│  │ • Update decision records        ││
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ External API Tools               ││
│  │ • Call credit bureau APIs        ││
│  │ • Verify employment              ││
│  │ • Check fraud databases          ││
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ Calculation Tools                ││
│  │ • Compute risk scores            ││
│  │ • Calculate ratios               ││
│  │ • Generate recommendations       ││
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ Document Tools                   ││
│  │ • Generate reports               ││
│  │ • Create documents               ││
│  │ • Extract information            ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  Resources (Read-only reference):   │
│  • Credit scoring rules             │
│  • Compliance requirements          │
│  • Reference data (rates, limits)   │
└─────────────────────────────────────┘
```

**Communication Pattern**:
```
Agent invokes tool
    ↓
MCP Client (in agents/)
    ↓
MCP Server (in mcp/server.py)
    ↓
Tool Handler (mcp/handlers/)
    ↓
Execute Tool (mcp/tools/)
    ↓
Return result
    ↓
Agent receives response
```

---

### Layer 6: Shared Utilities
**Location**: `shared/`
**Responsibility**: Cross-cutting concerns

```
┌─────────────────────────────────────┐
│   Shared Layer                      │
├─────────────────────────────────────┤
│  Configuration:                     │
│  • Global settings                  │
│  • Environment variables            │
│  • Feature flags                    │
├─────────────────────────────────────┤
│  Logging & Monitoring:              │
│  • Centralized logging              │
│  • Request tracing                  │
│  • Performance metrics              │
├─────────────────────────────────────┤
│  Database Management:               │
│  • Connection pooling               │
│  • Session management               │
│  • Migration utilities              │
├─────────────────────────────────────┤
│  Error Handling:                    │
│  • Custom exceptions                │
│  • Error recovery                   │
│  • Error reporting                  │
├─────────────────────────────────────┤
│  Utilities:                         │
│  • Data validators                  │
│  • Formatters                       │
│  • Calculators                      │
│  • Helper functions                 │
└─────────────────────────────────────┘
```

---

## 🔄 Complete Data Flow

### User Submits Loan Application

```
1. PRESENTATION LAYER
   User fills form in Streamlit
   ↓
2. API CALL
   Streamlit sends HTTP POST to FastAPI
   POST /loans with LoanApplicationRequest
   ↓
3. MICROSERVICES LAYER
   ├─ Validate request (Pydantic schema)
   ├─ Save to database (SQLAlchemy)
   └─ Invoke orchestrator
   ↓
4. ORCHESTRATION LAYER
   ├─ Create workflow state
   ├─ Initialize context
   └─ Start graph execution
   ↓
5. AGENT LAYER - Agent 1: LOAN PROCESSOR
   ├─ Receive application data
   ├─ Extract key information
   ├─ Validate completeness
   ├─ Update state
   └─ Pass to next agent
   ↓
6. AGENT LAYER - Agent 2: CREDIT ANALYZER
   ├─ Receive processed data
   ├─ Call MCP tools (credit bureau)
   │  └─ Retrieve applicant credit history
   ├─ Analyze credit metrics
   ├─ Generate credit score
   ├─ Update state with analysis
   └─ Pass to next agent
   ↓
7. AGENT LAYER - Agent 3: RISK ASSESSOR
   ├─ Receive credit analysis
   ├─ Call MCP tools (calculations)
   │  ├─ Compute risk metrics
   │  └─ Access compliance rules (MCP resource)
   ├─ Assess financial risk
   ├─ Generate risk report
   ├─ Update state with risk assessment
   └─ Pass to next agent
   ↓
8. AGENT LAYER - Agent 4: DECISION MAKER
   ├─ Receive all previous analyses
   ├─ Call MCP resources (approval rules)
   ├─ Synthesize all information
   ├─ Make APPROVED/REJECTED/CONDITIONAL decision
   ├─ Generate decision justification
   └─ Return to orchestration
   ↓
9. ORCHESTRATION LAYER
   ├─ Receive final decision
   ├─ Complete workflow
   └─ Return result to FastAPI
   ↓
10. MICROSERVICES LAYER
    ├─ Save decision to database
    ├─ Update application status
    ├─ Create audit log entry
    └─ Return response to client
    ↓
11. PRESENTATION LAYER
    ├─ Receive response
    ├─ Display decision
    ├─ Show analysis results
    └─ Update UI with status
```

---

## 🔌 MCP Integration Pattern

### How Agents Use MCP Tools

```
Agent Code:
    from mcp.clients import MCPClient
    
    client = MCPClient()
    
    # Call a tool
    result = client.call_tool(
        name="query_credit_bureau",
        arguments={"applicant_id": "123"}
    )

MCP Flow:
    client.call_tool()
    ↓
    MCPClient.call_tool() → sends request
    ↓
    MCPServer.handle_call_tool()
    ↓
    tool_handler.call_tool()
    ↓
    tools.query_credit_bureau()
    ↓
    returns result
    ↓
    client receives response
```

### MCP Resources (Read-Only Reference Data)

```
Agent Code:
    rules = client.read_resource(
        uri="resource://compliance/approval_rules"
    )
    
    # Now use rules in decision logic
    if score >= rules.min_credit_score:
        approve()

Available Resources:
    • resource://credit/scoring_rules
    • resource://compliance/regulatory_requirements
    • resource://risk/risk_thresholds
    • resource://approval/decision_rules
```

---

## 🔐 Authentication & Authorization

### Flow

```
HTTP Request
    ↓
middleware/auth.py
    ├─ Extract token from header
    ├─ Validate token
    ├─ Extract user info
    ├─ Check permissions
    └─ Add to request context
    ↓
Route Handler
    ├─ Receives authenticated request
    ├─ Uses current_user dependency
    └─ Performs operation
```

---

## 💾 Database Schema

### Key Entities

```
APPLICANT
├─ id (PK)
├─ name
├─ email
├─ phone
├─ income
├─ employment_status
└─ created_at

LOAN_APPLICATION
├─ id (PK)
├─ applicant_id (FK → APPLICANT)
├─ loan_amount
├─ loan_purpose
├─ loan_term
├─ status
├─ created_at
└─ updated_at

DECISION
├─ id (PK)
├─ application_id (FK → LOAN_APPLICATION)
├─ decision (APPROVED/REJECTED/CONDITIONAL)
├─ decision_reason
├─ approved_amount
├─ approved_rate
├─ created_at
└─ created_by

CREDIT_REPORT
├─ id (PK)
├─ applicant_id (FK → APPLICANT)
├─ credit_score
├─ credit_history
├─ debt_history
├─ created_at

RISK_ASSESSMENT
├─ id (PK)
├─ application_id (FK → LOAN_APPLICATION)
├─ risk_score
├─ risk_category
├─ dti_ratio
├─ created_at

AUDIT_LOG
├─ id (PK)
├─ action
├─ resource_type
├─ resource_id
├─ user_id
├─ timestamp
└─ changes
```

---

## ⚙️ Configuration Management

### Configuration Hierarchy

```
1. Environment Variables (.env)
   ├─ ANTHROPIC_API_KEY
   ├─ DATABASE_URL
   ├─ MCP_SERVER_HOST
   └─ ...
   
2. config/settings.py
   ├─ Loads from .env
   ├─ Defines defaults
   └─ Validates values
   
3. Layer-specific config
   ├─ config/database.py
   ├─ config/logging.py
   ├─ config/mcp.py
   └─ config/agents.py
   
4. Runtime configuration
   ├─ API query parameters
   ├─ Request body options
   └─ Feature flags
```

---

## 🧪 Testing Strategy

### Test Pyramid

```
        △
       /|\
      / | \
     /  |  \ Integration Tests
    /   |   \ (API + Orchestration)
   /    |    \
  /____ | ____\
 |            | Unit Tests
 | (Components, Functions, Classes)
 |____________|
```

### Test Organization

```
tests/
├─ unit/
│  ├─ test_agents.py (Agent logic)
│  ├─ test_microservices.py (Routes, schemas)
│  └─ test_orchestration.py (Graph, state)
├─ integration/
│  ├─ test_workflow.py (Full workflow)
│  ├─ test_api.py (API + DB)
│  └─ test_mcp_integration.py (MCP tools)
└─ fixtures/
   ├─ loan_fixtures.py (Sample data)
   ├─ agent_fixtures.py (Mock agents)
   └─ mcp_fixtures.py (Mock MCP)
```

---

## 🚀 Deployment Architecture

### Docker Containerization

```
docker-compose.yml
├─ api-service (FastAPI)
├─ ui-service (Streamlit)
├─ postgres (Database)
├─ redis (Caching)
└─ mcp-server (MCP Server)
```

### Kubernetes Deployment

```
Namespace: loan-approval
├─ Deployment: API Service
├─ Deployment: Streamlit UI
├─ StatefulSet: Database
├─ Service: MCP Server
├─ ConfigMap: Configuration
└─ Secret: Credentials
```

---

## 🔄 Asynchronous Processing

### For Long-Running Workflows

```
1. Client submits request
   ↓
2. API returns immediately with job_id
   ↓
3. Workflow processes in background
   ├─ Agents process sequentially
   ├─ MCP tools called as needed
   └─ Results saved to database
   ↓
4. Client polls for status
   GET /jobs/{job_id}/status
   ↓
5. When complete, client fetches result
   GET /jobs/{job_id}/result
```

---

## 🔗 Inter-Layer Dependencies

```
Presentation ← → Microservices
    ↓              ↓
    └── calls ──→ API
                   ↓
            Orchestration
                   ↓
            Agents (4)
                   ↓
              MCP Layer
                   ↓
            Database & External APIs
                   
All layers may use Shared Layer
```

---

## 📊 Key Metrics & Monitoring

### Application Metrics

```
API Performance:
  • Request latency (p50, p95, p99)
  • Request throughput (requests/sec)
  • Error rate (errors/sec)
  • Response size

Agent Performance:
  • Agent execution time
  • Tool call count
  • Success rate
  • Token usage (Claude API)

Workflow Metrics:
  • Workflow completion time
  • Approval rate (%)
  • Rejection rate (%)
  • Average decision time

Database Metrics:
  • Query latency
  • Connection pool usage
  • Slow queries
  • Transaction rollbacks
```

---

## 🔐 Security Considerations

### Key Areas

1. **Authentication**
   - JWT tokens or session-based
   - Token expiration and refresh
   - Secure storage in Streamlit

2. **Authorization**
   - Role-based access control (RBAC)
   - Resource-level permissions
   - Audit logging of all actions

3. **Data Protection**
   - HTTPS only
   - Encryption at rest (database)
   - Encryption in transit (TLS)
   - PII masking in logs

4. **Input Validation**
   - Pydantic schema validation
   - SQL injection prevention (SQLAlchemy ORM)
   - XSS prevention (Streamlit auto-escaping)
   - Rate limiting on API endpoints

5. **MCP Security**
   - Authenticate MCP clients
   - Validate tool arguments
   - Audit all MCP calls
   - Limit tool access by role

---

## 🧩 Extensibility Patterns

### Adding a New Agent

1. Create directory: `agents/new_agent/`
2. Create files: `agent.py`, `prompts.py`, `tools.py`
3. Update `orchestration/graph.py` to add node
4. Add edges to connect to workflow

### Adding a New API Endpoint

1. Create route in `microservices/api/`
2. Create schema in `microservices/schemas/`
3. Create CRUD in `microservices/crud/`
4. Add to main router in `api/routes.py`
5. Create UI page in `presentation/pages/`

### Adding a New MCP Tool

1. Create tool in `mcp/tools/`
2. Register in MCP server
3. Add to agent's tool list
4. Document tool and arguments

---

## 📚 Document Cross-References

- **Quick Start**: See `README.md`
- **Setup Instructions**: See `SETUP.md`
- **Project Structure**: See `PROJECT_STRUCTURE.md`
- **API Documentation**: See `docs/api.md`
- **Agent Details**: See `docs/agents.md`
- **Workflow Details**: See `docs/workflows.md`
- **MCP Guide**: See `docs/mcp.md`
- **Deployment**: See `docs/deployment.md`

