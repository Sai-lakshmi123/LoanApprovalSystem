# Layer Implementation Guide - File Purposes & Examples

This guide explains what should be implemented in each file across all layers.

---

## 📂 LAYER 1: PRESENTATION LAYER

### `presentation/app.py`
**Purpose**: Main Streamlit application entry point
```python
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Loan Approval System", layout="wide")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Dashboard", "Apply for Loan", "Check Status", "Analytics"]
    )

# Route to pages
if selected == "Dashboard":
    exec(open("presentation/pages/01_dashboard.py").read())
elif selected == "Apply for Loan":
    exec(open("presentation/pages/02_loan_application.py").read())
# ... etc
```

### `presentation/pages/01_dashboard.py`
**Purpose**: Main dashboard with KPIs and metrics
```python
import streamlit as st
import pandas as pd
from presentation.utils.api_client import APIClient

client = APIClient()

st.title("📊 Dashboard")

# Fetch metrics
metrics = client.get("/analytics/metrics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Applications", metrics["total_apps"])
with col2:
    st.metric("Approval Rate", f"{metrics['approval_rate']}%")
with col3:
    st.metric("Avg Processing Time", f"{metrics['avg_time']}h")
with col4:
    st.metric("Pending Applications", metrics["pending"])
```

### `presentation/pages/02_loan_application.py`
**Purpose**: Loan application form submission
```python
import streamlit as st
from presentation.components.forms import loan_application_form
from presentation.utils.api_client import APIClient

st.title("📝 New Loan Application")

form_data = loan_application_form()

if st.button("Submit Application"):
    client = APIClient()
    response = client.post("/loans", data=form_data)
    st.success(f"Application submitted! ID: {response['id']}")
```

### `presentation/components/forms.py`
**Purpose**: Reusable form components
```python
import streamlit as st

def loan_application_form():
    """Return loan application form data"""
    with st.form("loan_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name")
            email = st.email_input("Email")
            
        with col2:
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone")
        
        loan_amount = st.number_input("Loan Amount ($)", min_value=1000)
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home", "Car", "Education", "Business", "Other"]
        )
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            return {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "loan_amount": loan_amount,
                "loan_purpose": loan_purpose
            }
```

### `presentation/utils/api_client.py`
**Purpose**: HTTP client for API communication
```python
import requests
from config.settings import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.API_URL
        self.timeout = 30
    
    def get(self, endpoint: str):
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: dict):
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
```

### `presentation/utils/session_state.py`
**Purpose**: Manage Streamlit session state
```python
import streamlit as st

def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'authenticated': False,
        'user_id': None,
        'current_app_id': None,
        'page': 'dashboard'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_session(key: str):
    """Get session value"""
    return st.session_state.get(key)

def set_session(key: str, value):
    """Set session value"""
    st.session_state[key] = value
```

---

## 🔧 LAYER 2: MICROSERVICES LAYER

### `microservices/main.py`
**Purpose**: FastAPI application initialization
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from microservices.api.routes import router
from microservices.middleware.auth import AuthMiddleware
from microservices.middleware.logging import LoggingMiddleware

load_dotenv()

app = FastAPI(
    title="Loan Approval System API",
    version="1.0.0"
)

# Add middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)

# Include routes
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### `microservices/api/loan_routes.py`
**Purpose**: Loan application endpoints
```python
from fastapi import APIRouter, Depends, HTTPException
from microservices.schemas.loan import LoanApplicationRequest, LoanApplicationResponse
from microservices.crud.loan import create_loan, get_loan, list_loans
from microservices.dependencies.database import get_db
from microservices.dependencies.orchestrator import get_orchestrator

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("", response_model=LoanApplicationResponse)
async def submit_loan_application(
    request: LoanApplicationRequest,
    db = Depends(get_db),
    orchestrator = Depends(get_orchestrator)
):
    """Submit a new loan application"""
    # Create application in DB
    application = create_loan(db, request)
    
    # Start orchestration workflow
    result = orchestrator.invoke({
        "messages": [{"role": "user", "content": f"Process loan: {application.id}"}],
        "application_id": application.id
    })
    
    return LoanApplicationResponse.from_orm(application)

@router.get("/{application_id}", response_model=LoanApplicationResponse)
async def get_application(application_id: str, db = Depends(get_db)):
    """Get loan application details"""
    application = get_loan(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.get("", response_model=list[LoanApplicationResponse])
async def list_applications(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    """List all loan applications"""
    return list_loans(db, skip, limit)
```

### `microservices/schemas/loan.py`
**Purpose**: Pydantic request/response models
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class LoanPurpose(str, Enum):
    HOME = "home"
    AUTO = "auto"
    EDUCATION = "education"
    BUSINESS = "business"
    PERSONAL = "personal"

class LoanApplicationRequest(BaseModel):
    """Request model for new loan application"""
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    loan_amount: float
    loan_purpose: LoanPurpose
    employment_status: str
    annual_income: float

class LoanApplicationResponse(BaseModel):
    """Response model for loan application"""
    id: str
    first_name: str
    last_name: str
    loan_amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### `microservices/models/loan_application.py`
**Purpose**: SQLAlchemy ORM model
```python
from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class LoanApplication(Base):
    """Loan application database model"""
    __tablename__ = "loan_applications"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    applicant_id = Column(String(36), nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_purpose = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### `microservices/crud/loan.py`
**Purpose**: Database CRUD operations
```python
from sqlalchemy.orm import Session
from microservices.models.loan_application import LoanApplication
from microservices.schemas.loan import LoanApplicationRequest

def create_loan(db: Session, request: LoanApplicationRequest) -> LoanApplication:
    """Create new loan application"""
    application = LoanApplication(**request.dict())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

def get_loan(db: Session, application_id: str) -> LoanApplication:
    """Get loan application by ID"""
    return db.query(LoanApplication).filter(
        LoanApplication.id == application_id
    ).first()

def list_loans(db: Session, skip: int = 0, limit: int = 10):
    """List loan applications"""
    return db.query(LoanApplication).offset(skip).limit(limit).all()

def update_loan_status(db: Session, application_id: str, status: str):
    """Update loan application status"""
    application = get_loan(db, application_id)
    if application:
        application.status = status
        db.commit()
        db.refresh(application)
    return application
```

### `microservices/dependencies/orchestrator.py`
**Purpose**: Provide LangGraph orchestrator instance
```python
from orchestration.graph import create_loan_approval_graph

_orchestrator = None

def get_orchestrator():
    """Get or create orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = create_loan_approval_graph()
    return _orchestrator
```

---

## 🔀 LAYER 3: ORCHESTRATION LAYER

### `orchestration/state.py`
**Purpose**: Define workflow state schema
```python
from typing import Annotated, List
from langchain_core.messages import BaseMessage
import operator

class WorkflowState:
    """State passed between orchestration nodes"""
    
    messages: Annotated[List[BaseMessage], operator.add]
    application_id: str
    current_stage: str
    loan_data: dict
    credit_data: dict
    risk_data: dict
    decision: str
    decision_reason: str
```

### `orchestration/graph.py`
**Purpose**: Build LangGraph workflow
```python
from langgraph.graph import StateGraph, START, END
from orchestration.state import WorkflowState
from agents.loan_processor.agent import loan_processor_agent
from agents.credit_analyzer.agent import credit_analyzer_agent
from agents.risk_assessor.agent import risk_assessor_agent
from agents.decision_maker.agent import decision_maker_agent

def create_loan_approval_graph():
    """Create the loan approval workflow graph"""
    
    graph = StateGraph(WorkflowState)
    
    # Add nodes for each agent
    graph.add_node("loan_processor", loan_processor_agent)
    graph.add_node("credit_analyzer", credit_analyzer_agent)
    graph.add_node("risk_assessor", risk_assessor_agent)
    graph.add_node("decision_maker", decision_maker_agent)
    
    # Define edges (workflow flow)
    graph.add_edge(START, "loan_processor")
    graph.add_edge("loan_processor", "credit_analyzer")
    graph.add_edge("credit_analyzer", "risk_assessor")
    graph.add_edge("risk_assessor", "decision_maker")
    graph.add_edge("decision_maker", END)
    
    return graph.compile()
```

### `orchestration/workflows/loan_approval_workflow.py`
**Purpose**: Loan approval workflow implementation
```python
from orchestration.graph import create_loan_approval_graph
from langchain_core.messages import HumanMessage

def execute_loan_approval_workflow(application_data: dict):
    """Execute the complete loan approval workflow"""
    
    graph = create_loan_approval_graph()
    
    # Initial state
    initial_state = {
        "messages": [
            HumanMessage(content=f"Process loan application: {application_data['id']}")
        ],
        "application_id": application_data["id"],
        "current_stage": "loan_processor",
        "loan_data": application_data,
        "credit_data": {},
        "risk_data": {},
        "decision": None,
        "decision_reason": None
    }
    
    # Execute workflow
    result = graph.invoke(initial_state)
    
    return result
```

---

## 🤖 LAYER 4: AGENT LAYER

### `agents/base_agent.py`
**Purpose**: Base class for all agents
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, model_name: str = "claude-opus-4-1-20250805"):
        from langchain_anthropic import ChatAnthropic
        self.model = ChatAnthropic(model=model_name)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return system prompt for agent"""
        pass
    
    @abstractmethod
    def get_tools(self) -> list:
        """Return tools available to agent"""
        pass
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke agent with given state"""
        # Implementation in subclasses
        pass
```

### `agents/loan_processor/agent.py`
**Purpose**: Loan processor agent implementation
```python
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from agents.base_agent import BaseAgent
from agents.loan_processor.prompts import LOAN_PROCESSOR_PROMPT
from agents.loan_processor.tools import get_validation_tools

class LoanProcessorAgent(BaseAgent):
    """Agent that processes and validates loan applications"""
    
    def get_system_prompt(self) -> str:
        return LOAN_PROCESSOR_PROMPT
    
    def get_tools(self) -> list:
        return get_validation_tools()
    
    def invoke(self, state):
        """Process loan application"""
        system_prompt = self.get_system_prompt()
        
        # Format application data for processing
        application = state.get("loan_data", {})
        user_message = f"""
        Please process and validate this loan application:
        
        Applicant: {application.get('first_name')} {application.get('last_name')}
        Loan Amount: ${application.get('loan_amount')}
        Purpose: {application.get('loan_purpose')}
        Income: ${application.get('annual_income')}
        
        Validate all required fields and extract key information.
        """
        
        # Call model
        response = self.model.invoke([
            {"role": "system", "content": system_prompt},
            HumanMessage(content=user_message)
        ])
        
        # Update state
        state["messages"].append(response)
        state["current_stage"] = "credit_analyzer"
        
        return state
```

### `agents/loan_processor/prompts.py`
**Purpose**: System prompts for agents
```python
LOAN_PROCESSOR_PROMPT = """
You are a Loan Processor Agent responsible for initial loan application validation.

Your tasks:
1. Extract all required information from the application
2. Validate data completeness and format
3. Check for obvious errors or inconsistencies
4. Flag any missing or incorrect information
5. Summarize key application details

Be thorough but fair. Look for genuine issues, not nitpicky formatting problems.
Generate a structured summary of the application and validation results.

Output format:
- Status: (VALID / INVALID)
- Summary: Brief overview
- Issues: Any problems found (if any)
- Next Steps: Recommended next action
"""

CREDIT_ANALYZER_PROMPT = """
You are a Credit Analyzer Agent responsible for assessing creditworthiness.

Your tasks:
1. Analyze the applicant's credit history and score
2. Assess payment history patterns
3. Evaluate debt-to-income ratio implications
4. Identify credit risk factors
5. Generate a credit risk assessment

Be analytical and fact-based. Consider both positive and negative factors.

Output format:
- Credit Score: [score if available]
- Credit History Summary: [overview]
- Risk Assessment: (LOW / MEDIUM / HIGH)
- Key Factors: List of important considerations
- Recommendation: Suggested next action
"""

# ... Similar prompts for other agents
```

### `agents/loan_processor/tools.py`
**Purpose**: Tools available to agents
```python
from mcp.clients import MCPClient

def get_validation_tools():
    """Return validation tools for loan processor"""
    return [
        {
            "name": "validate_email",
            "description": "Validate email format",
            "parameters": {"email": "string"}
        },
        {
            "name": "validate_phone",
            "description": "Validate phone number format",
            "parameters": {"phone": "string"}
        },
        {
            "name": "check_application_completeness",
            "description": "Check if all required fields are present",
            "parameters": {"application": "dict"}
        }
    ]

def get_credit_analysis_tools():
    """Return tools for credit analyzer"""
    client = MCPClient()
    return client.list_tools("credit_*")
```

---

## 🔌 LAYER 5: MCP INTEGRATION LAYER

### `mcp/server.py`
**Purpose**: MCP server initialization
```python
from mcp.tools import database_tools, external_api_tools, calculation_tools
from mcp.resources import credit_rules, compliance_rules

class MCPServer:
    """Model Context Protocol Server"""
    
    def __init__(self):
        self.tools = []
        self.resources = []
        self._register_tools()
        self._register_resources()
    
    def _register_tools(self):
        """Register all available tools"""
        self.tools.extend(database_tools.get_tools())
        self.tools.extend(external_api_tools.get_tools())
        self.tools.extend(calculation_tools.get_tools())
    
    def _register_resources(self):
        """Register all available resources"""
        self.resources.append(credit_rules.get_resource())
        self.resources.append(compliance_rules.get_resource())
    
    def handle_tool_call(self, tool_name: str, arguments: dict):
        """Handle tool invocation"""
        for tool in self.tools:
            if tool['name'] == tool_name:
                return tool['execute'](arguments)
        
        raise ValueError(f"Tool {tool_name} not found")
```

### `mcp/tools/database_tools.py`
**Purpose**: Database access tools
```python
from shared.database.session import get_db

def query_credit_history(applicant_id: str):
    """Query applicant credit history from database"""
    db = get_db()
    # Implementation
    return {
        "applicant_id": applicant_id,
        "credit_score": 750,
        "accounts": [...],
        "payment_history": [...]
    }

def query_employment_history(applicant_id: str):
    """Query applicant employment history"""
    db = get_db()
    # Implementation
    return {
        "applicant_id": applicant_id,
        "current_employer": "...",
        "employment_history": [...]
    }

def get_tools():
    """Return all database tools"""
    return [
        {
            "name": "query_credit_history",
            "description": "Get applicant credit history",
            "execute": query_credit_history
        },
        {
            "name": "query_employment_history",
            "description": "Get applicant employment history",
            "execute": query_employment_history
        }
    ]
```

### `mcp/tools/calculation_tools.py`
**Purpose**: Financial calculation tools
```python
def calculate_dti_ratio(monthly_income: float, monthly_debt: float) -> float:
    """Calculate debt-to-income ratio"""
    if monthly_income == 0:
        return float('inf')
    return (monthly_debt / monthly_income) * 100

def calculate_loan_to_value(loan_amount: float, property_value: float) -> float:
    """Calculate loan-to-value ratio"""
    if property_value == 0:
        return float('inf')
    return (loan_amount / property_value) * 100

def calculate_risk_score(factors: dict) -> float:
    """Calculate overall risk score based on multiple factors"""
    credit_weight = 0.4
    dti_weight = 0.3
    ltv_weight = 0.2
    history_weight = 0.1
    
    score = (
        factors.get('credit_score', 650) * credit_weight +
        (100 - factors.get('dti_ratio', 50)) * dti_weight +
        (100 - factors.get('ltv_ratio', 80)) * ltv_weight +
        factors.get('history_score', 70) * history_weight
    )
    
    return min(max(score, 300), 850)  # Cap between 300-850

def get_tools():
    """Return all calculation tools"""
    return [
        {"name": "calculate_dti_ratio", "execute": calculate_dti_ratio},
        {"name": "calculate_loan_to_value", "execute": calculate_loan_to_value},
        {"name": "calculate_risk_score", "execute": calculate_risk_score},
    ]
```

### `mcp/resources/credit_rules.py`
**Purpose**: Credit scoring rules (read-only resource)
```python
CREDIT_RULES = {
    "min_credit_score": 650,
    "excellent_credit": 750,
    "good_credit": 700,
    "fair_credit": 650,
    "poor_credit": 600,
    "score_weights": {
        "payment_history": 0.35,
        "credit_utilization": 0.30,
        "length_of_history": 0.15,
        "credit_mix": 0.10,
        "new_inquiries": 0.10
    }
}

def get_resource():
    """Return credit rules resource"""
    return {
        "uri": "resource://credit/scoring_rules",
        "description": "Credit scoring rules and thresholds",
        "content": CREDIT_RULES
    }
```

---

## ⚙️ LAYER 6: SHARED UTILITIES

### `shared/config.py`
**Purpose**: Global configuration
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./loan_system.db"
    
    # Anthropic
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str = "claude-opus-4-1-20250805"
    
    # MCP
    MCP_SERVER_HOST: str = "localhost"
    MCP_SERVER_PORT: int = 3000
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### `shared/logger.py`
**Purpose**: Centralized logging
```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    """Setup logger for a module"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=10485760, backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

### `shared/exceptions/loan_exceptions.py`
**Purpose**: Custom exceptions
```python
class LoanException(Exception):
    """Base loan exception"""
    pass

class InvalidApplicationException(LoanException):
    """Invalid loan application"""
    pass

class InsufficientCreditException(LoanException):
    """Applicant has insufficient credit"""
    pass

class HighRiskApplicationException(LoanException):
    """Application is high risk"""
    pass
```

---

## 📋 CONFIGURATION LAYER

### `config/settings.py`
**Purpose**: Environment-based settings (detailed)
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./loan_system.db"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20
    
    # Anthropic Configuration
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str = "claude-opus-4-1-20250805"
    ANTHROPIC_MAX_TOKENS: int = 2048
    
    # MCP Configuration
    MCP_SERVER_HOST: str = "localhost"
    MCP_SERVER_PORT: int = 3000
    
    # Streamlit Configuration
    STREAMLIT_SERVER_PORT: int = 8501
    
    # Application Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

---

## 🧪 TEST LAYER

### `tests/unit/test_agents.py`
**Purpose**: Agent unit tests
```python
import pytest
from agents.loan_processor.agent import LoanProcessorAgent

@pytest.fixture
def loan_processor():
    return LoanProcessorAgent()

def test_loan_processor_validates_application(loan_processor):
    """Test that loan processor validates applications"""
    
    application = {
        "id": "123",
        "first_name": "John",
        "last_name": "Doe",
        "loan_amount": 50000,
        "loan_purpose": "home",
        "annual_income": 100000
    }
    
    state = {
        "messages": [],
        "loan_data": application,
        "credit_data": {},
        "risk_data": {}
    }
    
    result = loan_processor.invoke(state)
    
    assert result["current_stage"] == "credit_analyzer"
    assert len(result["messages"]) > 0
```

---

## 📚 Documentation

### `docs/ARCHITECTURE.md`
See the comprehensive architecture documentation file for complete details.

---

## 🚀 Summary

Each layer has a specific responsibility:

| Layer | Location | Purpose |
|-------|----------|---------|
| **Presentation** | `presentation/` | User interface (Streamlit) |
| **Microservices** | `microservices/` | REST API & business logic |
| **Orchestration** | `orchestration/` | Workflow graph (LangGraph) |
| **Agents** | `agents/` | AI-powered decision making |
| **MCP** | `mcp/` | Tool & resource access |
| **Shared** | `shared/` | Cross-cutting utilities |

Follow these patterns when implementing files in each layer!

