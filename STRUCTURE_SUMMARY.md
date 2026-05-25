# Multi-Agent Loan Approval System - Structure Summary

## 📋 Quick Overview

This is a **5-layer architecture** for a loan approval system using AI agents:

```
┌─────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (Streamlit)                         │
│  └─ User Interface & Forms                              │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────────────┐
│  MICROSERVICES LAYER (FastAPI)                          │
│  └─ REST API, Database, Validation                      │
└────────────────────┬────────────────────────────────────┘
                     │ Invoke
┌────────────────────▼────────────────────────────────────┐
│  ORCHESTRATION LAYER (LangGraph)                        │
│  └─ Workflow Graph, State Management                    │
└────────────────────┬────────────────────────────────────┘
                     │ Execute
         ┌───────────┴───────────┬───────────┬───────────┐
         │                       │           │           │
┌────────▼──────────┐ ┌─────────▼──────┐ ┌─▼──────────┐ ┌▼───────────────┐
│ Agent 1: Loan     │ │ Agent 2:       │ │ Agent 3:   │ │ Agent 4:       │
│ Processor         │ │ Credit         │ │ Risk       │ │ Decision       │
│                   │ │ Analyzer       │ │ Assessor   │ │ Maker          │
└───────┬──────────┘ └────────┬──────┘ └─┬──────────┘ └┬───────────────┘
        │ Use MCP Tools       │          │             │
        └───────────┬─────────┴──────────┴─────────────┘
                    │
         ┌──────────▼────────────┐
         │  MCP LAYER            │
         │  └─ Tools & Resources │
         └───────────────────────┘
```

---

## 📂 Folder Structure (5 Layers + Shared)

### **LAYER 1: PRESENTATION** (`presentation/`)
**What**: Streamlit UI interface  
**Files**:
- `app.py` - Main entry point
- `pages/` - Multi-page interface (Dashboard, Application Form, Status, Analytics)
- `components/` - Reusable UI components (Forms, Cards, Charts)
- `utils/` - Helper utilities (API client, formatters, validators)

**Purpose**: Users interact with the system here

---

### **LAYER 2: MICROSERVICES** (`microservices/`)
**What**: FastAPI REST API  
**Files**:
- `main.py` - FastAPI initialization
- `api/` - Route handlers (loan_routes.py, status_routes.py, analytics_routes.py)
- `schemas/` - Pydantic validation models (loan, applicant, decision, responses)
- `models/` - SQLAlchemy ORM models (database tables)
- `crud/` - Database operations (Create, Read, Update, Delete)
- `dependencies/` - Dependency injection (database, orchestrator, MCP, auth)
- `middleware/` - Request processing (authentication, logging, error handling)

**Purpose**: Receives requests, validates data, saves to database, triggers workflows

---

### **LAYER 3: ORCHESTRATION** (`orchestration/`)
**What**: LangGraph workflow graph  
**Files**:
- `graph.py` - Builds the workflow graph
- `state.py` - Defines state schema (data passed between agents)
- `router.py` - Conditional routing logic
- `workflows/` - Workflow implementations
- `state_managers/` - State tracking utilities
- `validators/` - Workflow validators

**Purpose**: Coordinates the flow between agents, manages state, handles routing

---

### **LAYER 4: AGENTS** (`agents/`)
**What**: Four specialized AI agents  
**Agents**:

1. **Loan Processor** (`agents/loan_processor/`)
   - Extracts & validates application info
   - Files: agent.py, prompts.py, tools.py, validators.py

2. **Credit Analyzer** (`agents/credit_analyzer/`)
   - Analyzes credit history
   - Files: agent.py, prompts.py, tools.py, validators.py

3. **Risk Assessor** (`agents/risk_assessor/`)
   - Evaluates financial risk
   - Files: agent.py, prompts.py, tools.py, validators.py

4. **Decision Maker** (`agents/decision_maker/`)
   - Makes final approval decision
   - Files: agent.py, prompts.py, tools.py, validators.py

**Purpose**: AI-powered analysis at each stage

---

### **LAYER 5: MCP INTEGRATION** (`mcp/`)
**What**: Model Context Protocol for tools & resources  
**Files**:
- `server.py` - MCP server
- `clients/` - MCP client implementation
- `tools/` - Tool definitions
  - `database_tools.py` - Query databases
  - `external_api_tools.py` - Call external APIs
  - `calculation_tools.py` - Financial calculations
  - `document_tools.py` - Document processing
- `resources/` - Read-only reference data
  - `credit_rules.py` - Credit scoring rules
  - `compliance_rules.py` - Compliance requirements
  - `reference_data.py` - Lookup tables
- `handlers/` - Tool/resource request handlers

**Purpose**: Provides data access and calculation tools for agents

---

### **SHARED UTILITIES** (`shared/`)
**What**: Cross-layer utilities  
**Files**:
- `config.py` - Global configuration
- `logger.py` - Logging setup
- `constants.py` - Application constants
- `enums.py` - Enumerations
- `database/` - Database utilities
- `exceptions/` - Custom exceptions
- `utils/` - Validators, formatters, calculators

**Purpose**: Reusable code used by all layers

---

### **CONFIGURATION** (`config/`)
**Files**:
- `settings.py` - Environment-based settings
- `database.py` - Database config
- `logging.py` - Logging config
- `mcp.py` - MCP config
- `agents.py` - Agent config

---

### **TESTS** (`tests/`)
**Files**:
- `unit/` - Unit tests for components
- `integration/` - Integration tests
- `fixtures/` - Test data and mocks

---

### **DOCUMENTATION** (`docs/`)
**Files**:
- `ARCHITECTURE.md` - Detailed architecture
- `api.md` - API documentation
- `agents.md` - Agent specifications
- `workflows.md` - Workflow details
- `mcp.md` - MCP integration guide
- `deployment.md` - Deployment instructions

---

## 🔄 Complete Request Flow

```
1. USER (Streamlit UI)
   └─ Fills loan application form
   
2. PRESENTATION LAYER
   └─ Validates input, sends HTTP POST to API
   
3. MICROSERVICES LAYER
   ├─ Receives /loans request
   ├─ Validates with Pydantic schema
   ├─ Saves to database (SQLAlchemy)
   └─ Invokes orchestrator
   
4. ORCHESTRATION LAYER
   ├─ Creates workflow state
   ├─ Initializes graph
   └─ Starts agent execution
   
5. AGENT LAYER (Sequential)
   
   ├─ AGENT 1: LOAN PROCESSOR
   │  ├─ Receives: Raw application
   │  ├─ Does: Extract & validate
   │  └─ Outputs: Processed data
   │
   ├─ AGENT 2: CREDIT ANALYZER
   │  ├─ Receives: Processed data
   │  ├─ Does: Analyze credit (uses MCP tools)
   │  └─ Outputs: Credit report
   │
   ├─ AGENT 3: RISK ASSESSOR
   │  ├─ Receives: Credit report
   │  ├─ Does: Calculate risk (uses MCP tools)
   │  └─ Outputs: Risk assessment
   │
   └─ AGENT 4: DECISION MAKER
      ├─ Receives: All previous analyses
      ├─ Does: Make decision (uses MCP resources)
      └─ Outputs: APPROVED/REJECTED
   
6. MCP LAYER (Tools & Resources)
   ├─ Agents call tools (database queries, calculations, APIs)
   ├─ Agents access resources (rules, compliance, reference data)
   └─ Returns results
   
7. BACK TO MICROSERVICES LAYER
   ├─ Receives final decision
   ├─ Updates database
   ├─ Creates audit log
   └─ Returns response
   
8. PRESENTATION LAYER
   └─ Displays decision to user
```

---

## 📊 File Count by Layer

| Layer | Directories | Python Files | Total |
|-------|-------------|--------------|-------|
| Presentation | 4 | 15 | 19 |
| Microservices | 6 | 25 | 31 |
| Orchestration | 3 | 10 | 13 |
| Agents | 5 | 20 | 25 |
| MCP | 4 | 12 | 16 |
| Shared | 3 | 12 | 15 |
| Config | - | 5 | 5 |
| Scripts | - | 4 | 4 |
| Tests | 3 | 9 | 12 |
| Docs | - | 6 | 6 |
| **TOTAL** | **28** | **118** | **146** |

---

## 🎯 Key Design Principles

1. **Separation of Concerns**
   - Each layer has ONE responsibility
   - Layers communicate through defined interfaces

2. **Loose Coupling**
   - Layers don't directly depend on each other's internals
   - Use dependency injection

3. **High Cohesion**
   - Related code is grouped together
   - Easy to find and modify

4. **Scalability**
   - Each service can be scaled independently
   - Agents can be parallelized

5. **Testability**
   - Each component can be unit tested
   - Integration tests verify workflows

6. **Maintainability**
   - Clear structure is easy to navigate
   - Self-documenting code

---

## 🚀 Getting Started Checklist

- [ ] Run `python create_structure.py` to generate all folders
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env` and fill in API keys
- [ ] Implement models in `microservices/models/`
- [ ] Implement schemas in `microservices/schemas/`
- [ ] Implement CRUD in `microservices/crud/`
- [ ] Implement routes in `microservices/api/`
- [ ] Implement agents in `agents/*/`
- [ ] Implement MCP tools in `mcp/tools/`
- [ ] Implement MCP resources in `mcp/resources/`
- [ ] Build orchestration graph in `orchestration/graph.py`
- [ ] Create Streamlit pages in `presentation/pages/`
- [ ] Write tests in `tests/`
- [ ] Run FastAPI: `uvicorn microservices.main:app --reload`
- [ ] Run Streamlit: `streamlit run presentation/app.py`

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and quick start |
| `SETUP.md` | Detailed setup instructions |
| `PROJECT_STRUCTURE.md` | Structure explanation with data flows |
| `FOLDER_TREE.txt` | ASCII folder tree visualization |
| `ARCHITECTURE.md` | Detailed architecture documentation |
| `LAYER_IMPLEMENTATION_GUIDE.md` | Code examples for each file |
| `STRUCTURE_SUMMARY.md` | This file |

---

## 🔗 Layer Dependencies

```
Presentation Layer
    ↓ (HTTP calls)
Microservices Layer
    ↓ (Invoke)
Orchestration Layer
    ↓ (Execute nodes)
Agent Layer (4 agents)
    ↓ (Call tools via MCP)
MCP Layer
    ↓ (Access data/tools)
Database & External Systems

All layers may use:
    ← Shared Utilities Layer
```

---

## 💡 Example: Extending the System

### To Add a New Agent:
1. Create `agents/new_agent/` directory
2. Create `agent.py`, `prompts.py`, `tools.py`
3. Add node to `orchestration/graph.py`
4. Connect edges in workflow

### To Add a New API Endpoint:
1. Create route in `microservices/api/`
2. Create schema in `microservices/schemas/`
3. Create CRUD in `microservices/crud/`
4. Update `microservices/api/routes.py`
5. Add Streamlit page in `presentation/pages/`

### To Add a New MCP Tool:
1. Create tool in `mcp/tools/`
2. Register in `mcp/server.py`
3. Add to agent's tool list
4. Document tool interface

---

## 🔐 Security Considerations

- **Authentication**: Middleware in `microservices/middleware/auth.py`
- **Input Validation**: Pydantic schemas in `microservices/schemas/`
- **Database Security**: SQLAlchemy ORM prevents SQL injection
- **Error Handling**: Custom exceptions with sanitized messages
- **Audit Logging**: All actions logged for compliance

---

## 📊 Performance Optimization

- **Caching**: Redis integration in shared utilities
- **Database Pooling**: Configured in `shared/database/`
- **Async Processing**: FastAPI async endpoints
- **Parallel Agents**: LangGraph supports parallel execution
- **Load Balancing**: Multiple API workers via Gunicorn

---

## 🧪 Testing Strategy

```
Unit Tests (tests/unit/)
├─ Agent logic
├─ API routes
└─ Orchestration

Integration Tests (tests/integration/)
├─ Full workflows
├─ API + Database
└─ MCP integration

Test Fixtures (tests/fixtures/)
├─ Sample data
├─ Mock agents
└─ Mock MCP
```

---

## 📱 Deployment Architecture

```
Docker Containers:
├─ API Container (FastAPI)
├─ UI Container (Streamlit)
├─ Database Container (PostgreSQL)
├─ Cache Container (Redis)
└─ MCP Server Container

Kubernetes:
├─ API Deployment (3 replicas)
├─ UI Deployment (2 replicas)
├─ Database StatefulSet
└─ MCP Service
```

---

## 🎓 Architecture Patterns Used

1. **Layered Architecture** - Clean separation
2. **MVC Pattern** - Presentation/Model/Controller
3. **Service Layer** - Business logic isolation
4. **Repository Pattern** - Data access abstraction
5. **Dependency Injection** - Loose coupling
6. **Factory Pattern** - Object creation
7. **Observer Pattern** - Event handling
8. **Chain of Responsibility** - Agent workflow
9. **Strategy Pattern** - Different decision strategies
10. **Template Method** - Agent base class

---

## 📞 Support & Documentation

For detailed information, see:
- **Architecture Details**: `docs/ARCHITECTURE.md`
- **Implementation Examples**: `LAYER_IMPLEMENTATION_GUIDE.md`
- **API Reference**: `docs/api.md`
- **Agent Specifications**: `docs/agents.md`
- **Workflow Details**: `docs/workflows.md`
- **MCP Integration**: `docs/mcp.md`
- **Setup Instructions**: `SETUP.md`

---

## ✅ Verification Checklist

After setup, verify:
- [ ] All folders created successfully
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Database initialized
- [ ] Environment variables set in `.env`
- [ ] API server starts: `uvicorn microservices.main:app --reload`
- [ ] API docs accessible at `http://localhost:8000/docs`
- [ ] Streamlit app starts: `streamlit run presentation/app.py`
- [ ] Can submit a loan application
- [ ] Workflow executes without errors
- [ ] Decision is saved to database
- [ ] Result displays in Streamlit UI

---

## 🎯 Next Steps

1. **Generate Structure**: Run `python create_structure.py`
2. **Review Architecture**: Read `docs/ARCHITECTURE.md`
3. **Implement Layer by Layer**:
   - Start with Shared utilities
   - Then Database models
   - Then API routes
   - Then Orchestration
   - Then Agents
   - Finally Presentation
4. **Test Incrementally**: Write tests as you go
5. **Deploy**: Use Docker and Kubernetes configs

---

## 📈 Project Status

- ✅ Architecture designed
- ✅ Folder structure documented
- ✅ Layer responsibilities defined
- ✅ Data flows documented
- ⏳ Ready for implementation

---

**Created**: May 21, 2026  
**Version**: 1.0  
**Status**: Ready for Development

