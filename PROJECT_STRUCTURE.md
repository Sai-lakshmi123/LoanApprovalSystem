# Multi-Agent Loan Approval System - Project Structure

## 📁 Complete Folder Tree

```
LoanApprovalSystem/
│
├── 📂 presentation/                    # Streamlit Presentation Layer
│   ├── __init__.py
│   ├── app.py                          # Main Streamlit app entry point
│   ├── config.py                       # Streamlit configuration
│   │
│   ├── 📂 pages/                       # Multi-page app pages
│   │   ├── __init__.py
│   │   ├── 01_dashboard.py            # Main dashboard
│   │   ├── 02_loan_application.py     # Loan application form
│   │   ├── 03_application_status.py   # Check status of applications
│   │   ├── 04_analytics.py            # Analytics and reports
│   │   └── 05_settings.py             # User settings and preferences
│   │
│   ├── 📂 components/                  # Reusable Streamlit components
│   │   ├── __init__.py
│   │   ├── forms.py                    # Form components
│   │   ├── cards.py                    # Card/widget components
│   │   ├── charts.py                   # Chart and visualization components
│   │   ├── status_indicators.py        # Status badges and indicators
│   │   └── navigation.py               # Navigation menus
│   │
│   ├── 📂 utils/                       # Presentation utilities
│   │   ├── __init__.py
│   │   ├── api_client.py              # HTTP client to call FastAPI
│   │   ├── formatters.py              # Data formatting/display utilities
│   │   ├── validators.py              # Input validation
│   │   └── session_state.py           # Streamlit session state management
│   │
│   └── 📂 assets/                      # Static assets
│       ├── styles.css
│       ├── images/
│       └── icons/
│
├── 📂 microservices/                   # FastAPI Microservices Layer
│   ├── __init__.py
│   ├── main.py                         # FastAPI app initialization
│   │
│   ├── 📂 api/                         # API route handlers
│   │   ├── __init__.py
│   │   ├── routes.py                   # Main router definitions
│   │   ├── loan_routes.py              # Loan application endpoints
│   │   ├── status_routes.py            # Status checking endpoints
│   │   ├── analytics_routes.py         # Analytics endpoints
│   │   └── health.py                   # Health check endpoint
│   │
│   ├── 📂 schemas/                     # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── loan.py                     # Loan-related schemas
│   │   ├── applicant.py                # Applicant-related schemas
│   │   ├── decision.py                 # Decision-related schemas
│   │   └── responses.py                # Common response schemas
│   │
│   ├── 📂 models/                      # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── loan_application.py         # LoanApplication model
│   │   ├── applicant.py                # Applicant model
│   │   ├── decision.py                 # Decision model
│   │   └── audit_log.py                # Audit trail model
│   │
│   ├── 📂 middleware/                  # Middleware components
│   │   ├── __init__.py
│   │   ├── auth.py                     # Authentication middleware
│   │   ├── logging.py                  # Request logging middleware
│   │   ├── error_handling.py           # Error handling middleware
│   │   └── cors.py                     # CORS configuration
│   │
│   ├── 📂 dependencies/                # Dependency injection
│   │   ├── __init__.py
│   │   ├── database.py                 # Database session management
│   │   ├── auth.py                     # Authentication dependencies
│   │   ├── orchestrator.py             # LangGraph orchestrator dependency
│   │   └── mcp.py                      # MCP client dependency
│   │
│   └── 📂 crud/                        # Database CRUD operations
│       ├── __init__.py
│       ├── loan.py                     # Loan CRUD operations
│       ├── applicant.py                # Applicant CRUD operations
│       └── decision.py                 # Decision CRUD operations
│
├── 📂 orchestration/                   # LangGraph Orchestration Layer
│   ├── __init__.py
│   ├── graph.py                        # Main LangGraph graph builder
│   ├── state.py                        # Graph state definition
│   ├── router.py                       # Conditional routing logic
│   │
│   ├── 📂 workflows/                   # Workflow definitions
│   │   ├── __init__.py
│   │   ├── loan_approval_workflow.py   # Main approval workflow
│   │   ├── parallel_workflow.py        # Parallel processing workflow
│   │   └── callback_workflow.py        # Callback/async workflow
│   │
│   ├── 📂 state_managers/              # State management
│   │   ├── __init__.py
│   │   ├── conversation_state.py       # Conversation state tracker
│   │   ├── workflow_state.py           # Workflow progress tracker
│   │   └── context_manager.py          # Context preservation
│   │
│   └── 📂 validators/                  # Orchestration validators
│       ├── __init__.py
│       ├── state_validator.py          # Validate state transitions
│       └── workflow_validator.py       # Validate workflow rules
│
├── 📂 agents/                          # Agent Layer (4 Specialized Agents)
│   ├── __init__.py
│   ├── base_agent.py                   # Base agent class
│   │
│   ├── 📂 loan_processor/              # Agent 1: Loan Processor
│   │   ├── __init__.py
│   │   ├── agent.py                    # Loan processor agent logic
│   │   ├── prompts.py                  # System prompts for agent
│   │   ├── tools.py                    # Tools available to agent
│   │   └── validators.py               # Input validation
│   │
│   ├── 📂 credit_analyzer/             # Agent 2: Credit Analyzer
│   │   ├── __init__.py
│   │   ├── agent.py                    # Credit analysis agent logic
│   │   ├── prompts.py                  # System prompts for agent
│   │   ├── tools.py                    # Tools available to agent
│   │   └── validators.py               # Input validation
│   │
│   ├── 📂 risk_assessor/               # Agent 3: Risk Assessor
│   │   ├── __init__.py
│   │   ├── agent.py                    # Risk assessment agent logic
│   │   ├── prompts.py                  # System prompts for agent
│   │   ├── tools.py                    # Tools available to agent
│   │   └── validators.py               # Input validation
│   │
│   ├── 📂 decision_maker/              # Agent 4: Decision Maker
│   │   ├── __init__.py
│   │   ├── agent.py                    # Decision making agent logic
│   │   ├── prompts.py                  # System prompts for agent
│   │   ├── tools.py                    # Tools available to agent
│   │   └── validators.py               # Input validation
│   │
│   └── 📂 shared/                      # Shared agent utilities
│       ├── __init__.py
│       ├── common_tools.py             # Common tools all agents use
│       ├── memory.py                   # Agent memory/context
│       └── response_formatter.py       # Response formatting
│
├── 📂 mcp/                             # Model Context Protocol Integration
│   ├── __init__.py
│   ├── server.py                       # MCP server initialization
│   │
│   ├── 📂 clients/                     # MCP clients
│   │   ├── __init__.py
│   │   ├── mcp_client.py              # Generic MCP client
│   │   └── tool_client.py             # Tool-specific MCP client
│   │
│   ├── 📂 tools/                       # MCP tool definitions
│   │   ├── __init__.py
│   │   ├── database_tools.py           # Database access tools
│   │   ├── external_api_tools.py       # External API integration tools
│   │   ├── calculation_tools.py        # Calculation and analysis tools
│   │   └── document_tools.py           # Document processing tools
│   │
│   ├── 📂 resources/                   # MCP resources (read-only data)
│   │   ├── __init__.py
│   │   ├── credit_rules.py             # Credit scoring rules
│   │   ├── compliance_rules.py         # Compliance rules
│   │   └── reference_data.py           # Reference data resources
│   │
│   └── 📂 handlers/                    # MCP request handlers
│       ├── __init__.py
│       ├── call_tool_handler.py        # Tool call handling
│       ├── read_resource_handler.py    # Resource reading
│       └── list_handler.py             # List tools/resources
│
├── 📂 shared/                          # Shared utilities across layers
│   ├── __init__.py
│   ├── config.py                       # Global configuration
│   ├── logger.py                       # Centralized logging
│   ├── constants.py                    # Application constants
│   ├── enums.py                        # Enumerations
│   │
│   ├── 📂 database/                    # Database utilities
│   │   ├── __init__.py
│   │   ├── connection.py               # Database connections
│   │   ├── session.py                  # Session management
│   │   └── migrations.py               # Database migrations
│   │
│   ├── 📂 exceptions/                  # Custom exceptions
│   │   ├── __init__.py
│   │   ├── loan_exceptions.py          # Loan-related exceptions
│   │   ├── agent_exceptions.py         # Agent-related exceptions
│   │   └── mcp_exceptions.py           # MCP-related exceptions
│   │
│   └── 📂 utils/                       # Utility functions
│       ├── __init__.py
│       ├── validators.py               # Data validation
│       ├── formatters.py               # Data formatting
│       ├── calculators.py              # Calculation helpers
│       └── helpers.py                  # General utilities
│
├── 📂 tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py                     # Pytest configuration
│   │
│   ├── 📂 unit/                        # Unit tests
│   │   ├── test_agents.py
│   │   ├── test_microservices.py
│   │   └── test_orchestration.py
│   │
│   ├── 📂 integration/                 # Integration tests
│   │   ├── test_workflow.py
│   │   ├── test_api.py
│   │   └── test_mcp_integration.py
│   │
│   └── 📂 fixtures/                    # Test fixtures and mocks
│       ├── loan_fixtures.py
│       ├── agent_fixtures.py
│       └── mcp_fixtures.py
│
├── 📂 config/                          # Configuration files
│   ├── __init__.py
│   ├── settings.py                     # Environment-based settings
│   ├── database.py                     # Database configuration
│   ├── logging.py                      # Logging configuration
│   ├── mcp.py                          # MCP configuration
│   └── agents.py                       # Agent configuration
│
├── 📂 scripts/                         # Utility scripts
│   ├── __init__.py
│   ├── setup_db.py                     # Database initialization
│   ├── seed_data.py                    # Seed test data
│   ├── run_migration.py                # Run database migrations
│   └── cleanup.py                      # Cleanup utilities
│
├── 📂 docs/                            # Documentation
│   ├── architecture.md                 # Architecture documentation
│   ├── api.md                          # API documentation
│   ├── agents.md                       # Agent documentation
│   ├── workflows.md                    # Workflow documentation
│   ├── mcp.md                          # MCP integration guide
│   └── deployment.md                   # Deployment guide
│
├── .env                                # Environment variables
├── .env.example                        # Environment template
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Python dependencies
├── setup.sh                            # Setup script
├── docker-compose.yml                  # Docker Compose configuration
├── Dockerfile                          # Docker image definition
├── main.py                             # Application entry point
├── README.md                           # Project README
└── PROJECT_STRUCTURE.md               # This file
```

---

## 🎯 Layer-by-Layer Explanation

### 1️⃣ **Presentation Layer** (`presentation/`)
**Purpose**: User-facing Streamlit interface

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit entry point, sets up page routing |
| `pages/01_dashboard.py` | Analytics dashboard with KPIs and charts |
| `pages/02_loan_application.py` | Form for submitting new loan applications |
| `pages/03_application_status.py` | Check and track application status |
| `pages/04_analytics.py` | Reports and analytics views |
| `pages/05_settings.py` | User preferences and settings |
| `components/forms.py` | Reusable form input components |
| `components/cards.py` | Card/widget display components |
| `components/charts.py` | Visualization and chart components |
| `utils/api_client.py` | HTTP client to communicate with FastAPI |
| `utils/session_state.py` | Manages Streamlit session state |

---

### 2️⃣ **Microservices Layer** (`microservices/`)
**Purpose**: RESTful API backend using FastAPI

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization, middleware setup |
| `api/loan_routes.py` | Endpoints for loan operations (create, read, update) |
| `api/status_routes.py` | Endpoints for checking application status |
| `api/analytics_routes.py` | Endpoints for analytics and reporting |
| `schemas/loan.py` | Pydantic models for loan data validation |
| `schemas/applicant.py` | Pydantic models for applicant data |
| `models/loan_application.py` | SQLAlchemy ORM model for database |
| `models/applicant.py` | SQLAlchemy ORM model for applicants |
| `crud/loan.py` | Database operations: Create, Read, Update, Delete |
| `dependencies/orchestrator.py` | Provides LangGraph orchestrator instance |
| `dependencies/database.py` | Provides database session |
| `middleware/auth.py` | Authentication and authorization |
| `middleware/logging.py` | Request/response logging |

---

### 3️⃣ **Orchestration Layer** (`orchestration/`)
**Purpose**: LangGraph workflow orchestration

| File | Purpose |
|------|---------|
| `graph.py` | Builds the LangGraph workflow graph |
| `state.py` | Defines the state object passed between agents |
| `router.py` | Conditional routing logic (if/else flows) |
| `workflows/loan_approval_workflow.py` | Main 4-agent approval workflow |
| `workflows/parallel_workflow.py` | Parallel processing for independent tasks |
| `state_managers/conversation_state.py` | Tracks conversation history |
| `state_managers/workflow_state.py` | Tracks workflow progress and decisions |

**Flow Example**:
```
START → Loan Processor → Credit Analyzer → Risk Assessor → Decision Maker → END
```

---

### 4️⃣ **Agent Layer** (`agents/`)
**Purpose**: Four specialized LLM agents

#### **Agent 1: Loan Processor**
- Extracts and validates loan application information
- Files: `loan_processor/agent.py`, `prompts.py`, `tools.py`

#### **Agent 2: Credit Analyzer**
- Analyzes credit history and creditworthiness
- Files: `credit_analyzer/agent.py`, `prompts.py`, `tools.py`

#### **Agent 3: Risk Assessor**
- Evaluates financial risk factors
- Files: `risk_assessor/agent.py`, `prompts.py`, `tools.py`

#### **Agent 4: Decision Maker**
- Makes final approval/rejection decisions
- Files: `decision_maker/agent.py`, `prompts.py`, `tools.py`

Each agent has:
- `agent.py` - Core agent logic
- `prompts.py` - System prompts and instructions
- `tools.py` - Tools the agent can use
- `validators.py` - Input/output validation

---

### 5️⃣ **MCP Integration Layer** (`mcp/`)
**Purpose**: Model Context Protocol for tool and resource access

| File | Purpose |
|------|---------|
| `server.py` | MCP server setup and initialization |
| `clients/mcp_client.py` | MCP client for agents to access tools |
| `tools/database_tools.py` | Tools for database queries |
| `tools/external_api_tools.py` | Tools for calling external APIs |
| `tools/calculation_tools.py` | Tools for complex calculations |
| `resources/credit_rules.py` | Credit scoring rules (read-only resource) |
| `resources/compliance_rules.py` | Compliance rules (read-only resource) |
| `handlers/call_tool_handler.py` | Handles tool invocations from agents |

---

### 6️⃣ **Shared Utilities** (`shared/`)
**Purpose**: Cross-cutting concerns

| File | Purpose |
|------|---------|
| `config.py` | Global configuration and settings |
| `logger.py` | Centralized logging setup |
| `constants.py` | Application-wide constants |
| `database/connection.py` | Database connection pooling |
| `exceptions/` | Custom exception classes |
| `utils/validators.py` | Reusable validation functions |
| `utils/calculators.py` | Financial calculation utilities |

---

### 7️⃣ **Configuration** (`config/`)
**Purpose**: Environment-based configuration

| File | Purpose |
|------|---------|
| `settings.py` | Loads from .env, defines all settings |
| `database.py` | Database connection strings and options |
| `mcp.py` | MCP server configuration |
| `agents.py` | Agent model selection and parameters |

---

### 8️⃣ **Tests** (`tests/`)
**Purpose**: Comprehensive test coverage

| Directory | Purpose |
|-----------|---------|
| `unit/` | Unit tests for individual components |
| `integration/` | Integration tests for workflows |
| `fixtures/` | Mock data and test fixtures |

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (Streamlit)                             │
│  ├─ User fills loan application form                        │
│  └─ Submits via API client                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP POST /loans
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  MICROSERVICES LAYER (FastAPI)                              │
│  ├─ Validates request (Pydantic schema)                     │
│  ├─ Saves to database (SQLAlchemy)                          │
│  └─ Calls orchestrator                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │ Invokes workflow
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER (LangGraph)                            │
│  ├─ Creates workflow state                                  │
│  ├─ Routes through agent nodes                              │
│  └─ Manages decisions and branching                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┬──────────────┬──────────────┐
        │                             │              │              │
        ▼                             ▼              ▼              ▼
   ┌─────────────┐            ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │ Agent 1:    │            │ Agent 2:    │  │ Agent 3:    │  │ Agent 4:    │
   │ Loan        │            │ Credit      │  │ Risk        │  │ Decision    │
   │ Processor   │            │ Analyzer    │  │ Assessor    │  │ Maker       │
   └─────────────┘            └─────────────┘  └─────────────┘  └─────────────┘
        │                             │              │              │
        └──────────────┬──────────────┴──────────────┴──────────────┘
                       │ Uses MCP tools
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  MCP LAYER (Model Context Protocol)                         │
│  ├─ Database tools (query credit info)                      │
│  ├─ External API tools (credit bureau)                      │
│  ├─ Calculation tools (risk score)                          │
│  └─ Resource access (compliance rules)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ Result flows back
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  BACK TO MICROSERVICES LAYER                                │
│  ├─ Updates decision in database                            │
│  ├─ Returns status to API                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │ JSON response
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                         │
│  └─ Displays decision and status to user                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Agent Interaction Flow

```
Loan Application Input
        │
        ▼
┌──────────────────────────────────┐
│ Agent 1: LOAN PROCESSOR           │
│ ├─ Extract applicant info         │
│ ├─ Validate loan details          │
│ └─ Check completeness             │
└──────────────┬───────────────────┘
               │ (Pass/Fail)
               ▼
        ┌──────────────────────────────────┐
        │ Agent 2: CREDIT ANALYZER          │
        │ ├─ Query credit history via MCP   │
        │ ├─ Calculate credit score         │
        │ ├─ Assess payment history         │
        │ └─ Generate credit report         │
        └──────────────┬───────────────────┘
                       │
                       ▼
                ┌──────────────────────────────────┐
                │ Agent 3: RISK ASSESSOR            │
                │ ├─ Calculate risk metrics         │
                │ ├─ Check debt-to-income ratio     │
                │ ├─ Evaluate employment stability  │
                │ └─ Assess loan-to-value ratio     │
                └──────────────┬───────────────────┘
                               │
                               ▼
                        ┌──────────────────────────────────┐
                        │ Agent 4: DECISION MAKER           │
                        │ ├─ Review all inputs              │
                        │ ├─ Apply approval rules           │
                        │ ├─ Check compliance (MCP)         │
                        │ └─ Make APPROVE/REJECT decision   │
                        └──────────────┬───────────────────┘
                                       │
                                       ▼
                                Final Decision
```

---

## 🔧 Configuration Management

```
.env (environment variables)
  └─ loaded by config/settings.py
     ├─ Database URL
     ├─ API Key
     ├─ Agent Models
     ├─ MCP Configuration
     └─ Feature Flags
```

---

## 📦 Dependencies Between Layers

```
Presentation Layer
    └─ depends on → Microservices Layer
                    └─ depends on → Orchestration Layer
                                    └─ depends on → Agent Layer
                                                    └─ uses → MCP Layer
                                    
All layers may use → Shared Layer
```

---

## 🚀 Key Design Principles

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Loose Coupling**: Layers communicate through defined interfaces
3. **High Cohesion**: Related functionality is grouped together
4. **Reusability**: Shared utilities avoid duplication
5. **Testability**: Each component can be tested independently
6. **Scalability**: Microservices can be deployed separately
7. **Maintainability**: Clear structure makes code easy to navigate

---

## 💡 Example: Adding a New Feature

To add a new feature (e.g., "Employment Verification Agent"), you would:

1. **Agent Layer**: Create `agents/employment_verifier/agent.py`
2. **Orchestration**: Add node to workflow in `orchestration/workflows/`
3. **MCP**: Add tool in `mcp/tools/employment_tools.py`
4. **Microservices**: Add endpoint in `microservices/api/employment_routes.py`
5. **Presentation**: Add page in `presentation/pages/06_employment_status.py`

---

## 📋 File Creation Checklist

- [ ] Create all folders with `__init__.py` files
- [ ] Create base configuration files
- [ ] Create database models
- [ ] Create API schemas and routes
- [ ] Create agent base classes
- [ ] Create MCP tool definitions
- [ ] Create Streamlit pages
- [ ] Add logging configuration
- [ ] Add error handling
- [ ] Write tests for each layer

---

## 🔗 Related Files

- **Architecture details**: See `docs/architecture.md`
- **API documentation**: See `docs/api.md`
- **Agent prompts**: See `docs/agents.md`
- **Workflow details**: See `docs/workflows.md`

