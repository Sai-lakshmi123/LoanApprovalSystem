"""
FastAPI application for multi-agent AI system with loan evaluation
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import logging
from dotenv import load_dotenv
import os
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from orchestration.fast_orchestration import get_fast_orchestrator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Loan Approval System API",
    description="API for multi-agent loan approval system with orchestration",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Request/Response Models ====================

class ProcessingRequest(BaseModel):
    """Request model for agent processing"""
    input_data: str
    agent_type: Optional[str] = "default"
    metadata: Optional[dict] = None

class ProcessingResponse(BaseModel):
    """Response model for agent processing"""
    status: str
    result: str
    metadata: Optional[dict] = None

# Loan Evaluation Request Model
class LoanEvaluationRequest(BaseModel):
    """Request model for loan evaluation"""
    applicant_id: str = Field(..., min_length=1, description="Unique applicant identifier")
    age: int = Field(..., ge=18, le=100, description="Applicant age")
    annual_income: float = Field(..., gt=0, description="Annual income in dollars")
    employment_type: str = Field(..., description="Type of employment (e.g., employed, self-employed, retired)")
    credit_score: int = Field(..., ge=300, le=850, description="Credit score (300-850)")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount in dollars")
    tenure_months: int = Field(..., ge=12, le=360, description="Loan tenure in months")
    existing_liabilities: float = Field(default=0, ge=0, description="Existing monthly debt obligations")
    location: str = Field(..., min_length=2, description="Geographic location/state")
    monthly_expenses: Optional[float] = Field(default=None, description="Monthly expenses (optional, derived if not provided)")
    delinquencies: Optional[int] = Field(default=0, ge=0, description="Number of delinquencies")
    inquiries_last_6_months: Optional[int] = Field(default=0, ge=0, description="Credit inquiries in last 6 months")
    credit_utilization: Optional[float] = Field(default=0.5, ge=0, le=1, description="Credit utilization ratio")
    years_at_current_job: Optional[int] = Field(default=1, ge=0, description="Years at current job")
    existing_loans: Optional[int] = Field(default=0, ge=0, description="Number of existing loans")
    property_value: Optional[float] = Field(default=None, description="Property value for mortgage")
    email: Optional[str] = Field(default=None, description="Applicant email")
    phone: Optional[str] = Field(default=None, description="Applicant phone")
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat(), description="Request timestamp")

    @validator('employment_type')
    def validate_employment_type(cls, v):
        valid_types = ['employed', 'self-employed', 'retired', 'student', 'unemployed']
        if v.lower() not in valid_types:
            raise ValueError(f'Employment type must be one of {valid_types}')
        return v.lower()

    @validator('monthly_expenses', pre=True, always=True)
    def calculate_monthly_expenses(cls, v, values):
        if v is not None:
            return v
        if 'existing_liabilities' in values:
            return values['existing_liabilities'] * 2
        return 5000

# Decision Details Model
class DecisionDetails(BaseModel):
    """Loan decision details"""
    classification: str = Field(..., description="Decision classification (APPROVE/REJECT/REVIEW)")
    risk_score: float = Field(..., description="Risk score (0-5)")
    confidence_level: str = Field(..., description="Confidence level (Very High/High/Medium/Low/Very Low)")
    confidence_percentage: int = Field(..., ge=0, le=100, description="Confidence percentage")
    reasoning: str = Field(..., description="Decision reasoning")
    key_factors: Optional[List[str]] = Field(default=None, description="Key decision factors")

# Error Handling Details Model
class ErrorHandlingInfo(BaseModel):
    """Error handling and retry information"""
    critical_errors: Optional[List[Dict[str, Any]]] = Field(default=None, description="List of critical errors encountered")
    error_count: int = Field(default=0, description="Total number of errors")
    error_escalation: bool = Field(default=False, description="Whether escalated to manual review")
    retry_statistics: Optional[Dict[str, int]] = Field(default=None, description="Retry attempt statistics")

# Loan Evaluation Response Model
class LoanEvaluationResponse(BaseModel):
    """Response model for loan evaluation"""
    success: bool = Field(..., description="Whether evaluation was successful")
    applicant_id: str = Field(..., description="Applicant ID from request")
    decision: DecisionDetails = Field(..., description="Loan decision details")
    risk_score: float = Field(..., description="Overall risk score")
    risk_level: str = Field(..., description="Risk level (Low/Medium/High)")
    next_steps: List[str] = Field(..., description="Recommended next steps")
    case_id: str = Field(..., description="Generated case ID for tracking")
    error_handling: Optional[ErrorHandlingInfo] = Field(default=None, description="Error handling information")
    workflow_status: str = Field(..., description="Overall workflow status")
    execution_path: List[str] = Field(..., description="Execution path through agents")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Response timestamp")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")

# ==================== Endpoints ====================

# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint"""
    return {
        "message": "Loan Approval System API",
        "docs": "/docs",
        "version": "2.0.0",
        "endpoints": {
            "health": "/health",
            "evaluate_loan": "/evaluate-loan",
            "agents": "/agents"
        }
    }

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Loan Approval System API",
        "timestamp": datetime.now().isoformat()
    }

# Loan Evaluation Endpoint
@app.post(
    "/evaluate-loan",
    response_model=LoanEvaluationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Loan Evaluation"],
    summary="Evaluate Loan Application",
    description="Submit a loan application for evaluation through the multi-agent orchestration system"
)
async def evaluate_loan(request: LoanEvaluationRequest):
    """
    Evaluate a loan application using the multi-agent orchestration system.

    This endpoint:
    1. Validates the incoming loan application data
    2. Passes it through Agent1 (Profile Analysis)
    3. Routes through Agent2 (Risk Analysis)
    4. Gets decision from Agent3 (Decision Synthesis)
    5. Records action with Agent4 (Compliance)
    6. Returns comprehensive evaluation result

    Args:
        request: LoanEvaluationRequest containing applicant and loan details

    Returns:
        LoanEvaluationResponse with decision, risk assessment, and next steps

    Raises:
        HTTPException: If validation fails or orchestration encounters fatal errors
    """
    start_time = datetime.now()

    try:
        logger.info(f"Evaluating loan application for applicant: {request.applicant_id}")

        # Initialize fast orchestrator
        orchestrator = get_fast_orchestrator()

        # Build applicant data dictionary
        applicant_data = {
            "name": request.applicant_id,
            "age": request.age,
            "annual_income": request.annual_income,
            "credit_score": request.credit_score,
            "delinquencies": request.delinquencies or 0,
            "existing_liabilities": request.existing_liabilities,
            "years_at_current_job": request.years_at_current_job or 1,
        }

        # Build loan request dictionary
        loan_request = {
            "loan_amount": request.loan_amount,
            "property_value": request.property_value or (request.loan_amount * 1.5),
            "loan_term_months": request.tenure_months
        }

        # Invoke fast evaluation
        logger.info(f"Invoking fast orchestration for {request.applicant_id}")
        result = orchestrator.evaluate_application(applicant_data, loan_request)

        # Extract decision information
        decision = result.get("decision", {})

        # Calculate processing time
        end_time = datetime.now()
        processing_time_ms = (end_time - start_time).total_seconds() * 1000

        # Build response
        response = LoanEvaluationResponse(
            success=result.get("success", True),
            applicant_id=request.applicant_id,
            decision=DecisionDetails(
                classification=decision.get("classification", "REVIEW"),
                risk_score=decision.get("risk_score", result.get("risk_score", 0.0)),
                confidence_level=decision.get("confidence_level", "Low"),
                confidence_percentage=decision.get("confidence_percentage", 0),
                reasoning=decision.get("reasoning", "Unable to determine decision"),
                key_factors=decision.get("key_factors", [])
            ),
            risk_score=result.get("risk_score", 0.0),
            risk_level=result.get("risk_level", "Unknown"),
            next_steps=result.get("next_steps", ["Contact applicant for additional information"]),
            case_id=result.get("case_id", f"CASE-{request.applicant_id}-{int(start_time.timestamp())}"),
            error_handling=None,
            workflow_status="success",
            execution_path=["Fast Evaluation"],
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time_ms
        )

        logger.info(f"✅ Evaluation complete for {request.applicant_id}: {response.decision.classification}")
        return response

    except Exception as e:
        logger.error(f"❌ Error evaluating loan for {request.applicant_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Loan evaluation failed",
                "applicant_id": request.applicant_id,
                "message": str(e)
            }
        )

# Processing endpoint (legacy)
@app.post("/process", response_model=ProcessingResponse, tags=["Legacy"])
async def process(request: ProcessingRequest):
    """Process input through the multi-agent system (legacy endpoint)"""
    try:
        logger.info(f"Processing request with agent_type: {request.agent_type}")
        return ProcessingResponse(
            status="success",
            result=f"Processed: {request.input_data}",
            metadata=request.metadata
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Agent status endpoint
@app.get("/agents", tags=["System"])
async def list_agents():
    """Get list of available agents"""
    return {
        "agents": [
            {
                "name": "Agent1",
                "type": "Profile Analysis",
                "status": "active",
                "description": "Analyzes applicant profile and financial stability"
            },
            {
                "name": "Agent2",
                "type": "Risk Analysis",
                "status": "active",
                "description": "Evaluates financial risk and metrics"
            },
            {
                "name": "Agent3",
                "type": "Decision Synthesis",
                "status": "active",
                "description": "Synthesizes decision based on profile and risk analysis"
            },
            {
                "name": "Agent4",
                "type": "Compliance Orchestration",
                "status": "active",
                "description": "Records decision and compliance information"
            }
        ],
        "orchestration_engine": "LangGraph",
        "llm_model": "Claude Sonnet 4.6"
    }

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 8000))

    print("\n" + "="*80)
    print("  LOAN APPROVAL SYSTEM API")
    print("="*80)
    print(f"  Starting FastAPI server...")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  API Docs: http://{host}:{port}/docs")
    print("="*80 + "\n")

    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
