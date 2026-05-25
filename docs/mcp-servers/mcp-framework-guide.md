# MCP Application DB Server

## Overview

The **Application DB** is a FastMCP server that simulates a database of loan applicants and provides tools and resources for analyzing applicant data. It's designed to integrate with LangChain agents and FastAPI services to support intelligent loan approval decisions.

## 🎯 Key Features

### Tools (7 Available)
1. **`get_applicant_profile`** - Fetch full applicant demographics, income, employment, credit data
2. **`get_income_stability_score`** - Calculate income stability (0-100 score)
3. **`get_employment_risk`** - Calculate employment risk (0-100 score, higher = riskier)
4. **`get_credit_history_summary`** - Get comprehensive credit analysis
5. **`check_application_completeness_tool`** - Verify all required fields are present
6. **`get_complete_applicant_analysis`** - Get all metrics in one call (most useful)
7. **`list_all_applicants`** - List all available applicants

### Resources (3 Available)
1. **`applicant://credit/scoring_rules`** - Credit scoring thresholds and categories
2. **`applicant://employment/stability_factors`** - Employment risk assessment criteria
3. **`applicant://compliance/regulatory_requirements`** - Regulatory compliance rules

### Sample Applicants
- **APP001**: John Smith, 35, $85k, Full-time, Credit 750 (Excellent)
- **APP002**: Sarah Johnson, 28, $55k, Full-time, Credit 680 (Fair)
- **APP003**: Michael Chen, 45, $120k, Self-employed, Credit 720 (Good)
- **APP004**: Emma Wilson, 32, $72k, Part-time, Credit 620 (Poor)

---

## 📋 Quick Start

### 1. Install Dependencies
```bash
pip install fastmcp httpx uvicorn
```

### 2. Start the MCP Server
```bash
python mcp/server.py
```

Server will run on `http://localhost:3000`

### 3. Use in Your Code

**Synchronous (Recommended for most use cases):**
```python
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()
analysis = client.get_complete_analysis("APP001")
print(analysis)
```

**Asynchronous:**
```python
import asyncio
from mcp.clients.mcp_client import MCPClient

async def main():
    client = MCPClient()
    analysis = await client.get_complete_analysis("APP001")
    print(analysis)

asyncio.run(main())
```

---

## 📚 Usage Examples

### Get Complete Applicant Analysis

```python
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()

# Get comprehensive analysis
analysis = client.get_complete_analysis("APP001")

# Extract metrics
income_stability = analysis['analysis']['income_stability']['score']
employment_risk = analysis['analysis']['employment_risk']['risk_score']
credit_score = analysis['analysis']['credit_history']['credit_score']
is_complete = analysis['analysis']['application_completeness']['is_complete']

print(f"Income Stability: {income_stability}/100")
print(f"Employment Risk: {employment_risk}/100")
print(f"Credit Score: {credit_score}")
print(f"Application Complete: {is_complete}")
```

### Use in LangChain Agent

```python
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()
model = ChatAnthropic(model="claude-opus-4-1-20250805")

# Get MCP data
analysis = client.get_complete_analysis("APP001")

# Create context for LLM
context = f"""
Applicant: {analysis['name']}
Income Stability: {analysis['analysis']['income_stability']['score']}/100
Employment Risk: {analysis['analysis']['employment_risk']['risk_score']}/100
Credit Score: {analysis['analysis']['credit_history']['credit_score']}
"""

# Get LLM analysis
response = model.invoke([
    HumanMessage(content=f"Analyze this applicant and recommend approval: {context}")
])

print(response.content)
```

### Integration with FastAPI

```python
from fastapi import FastAPI
from mcp.clients.mcp_client import SyncMCPClient

app = FastAPI()
mcp_client = SyncMCPClient()

@app.get("/applicants/{applicant_id}/analysis")
async def get_analysis(applicant_id: str):
    """Get applicant analysis from MCP server."""
    analysis = mcp_client.get_complete_analysis(applicant_id)
    return analysis

@app.post("/loans", dependencies=[Depends(get_db)])
async def submit_loan(request: LoanRequest, orchestrator=Depends(get_orchestrator)):
    """Submit loan application and start workflow."""
    # Get applicant analysis from MCP
    analysis = mcp_client.get_complete_analysis(request.applicant_id)
    
    # Pass to orchestrator/agents
    result = orchestrator.invoke({"analysis": analysis})
    
    return result
```

---

## 🔧 Configuration

### Server Configuration
Edit `mcp/server.py`:

```python
# Change port
if __name__ == "__main__":
    uvicorn.run(
        "mcp.server:app",
        host="0.0.0.0",
        port=3001,  # Change port here
        reload=True
    )

# Add more applicants
APPLICANTS_DB["APP005"] = {
    "id": "APP005",
    "name": "New Applicant",
    # ... rest of profile
}

# Modify scoring algorithms
def calculate_income_stability_score(applicant):
    # Adjust logic as needed
    ...
```

### Client Configuration
```python
from mcp.clients.mcp_client import SyncMCPClient

# Use different server
client = SyncMCPClient(base_url="http://prod-mcp.example.com:3000")

# Adjust timeout
client.timeout = 60

# List available tools
tools = client.list_tools()

# List available resources
resources = client.list_resources()
```

---

## 📊 Data Models

### Applicant Profile
```json
{
  "id": "APP001",
  "name": "John Smith",
  "age": 35,
  "email": "john@example.com",
  "phone": "555-0101",
  "annual_income": 85000,
  "monthly_expenses": 3200,
  "employment_type": "full_time",
  "employer": "Tech Corp",
  "job_title": "Senior Engineer",
  "years_at_current_job": 4,
  "credit_score": 750,
  "credit_history": {
    "accounts": 5,
    "delinquencies": 0,
    "payment_history": [...],
    "credit_utilization": 0.35
  }
}
```

### Income Stability Analysis
```json
{
  "score": 89,
  "stability_category": "Very High",
  "employment_type": "full_time",
  "years_at_job": 4,
  "age": 35
}
```

### Employment Risk Analysis
```json
{
  "risk_score": 15,
  "risk_level": "Low",
  "employment_type": "full_time",
  "tenure_risk": "Stable"
}
```

### Credit History Summary
```json
{
  "credit_score": 750,
  "score_category": "Excellent",
  "delinquencies": 0,
  "accounts_open": 5,
  "credit_utilization_ratio": 35.0,
  "payment_trend": "Improving",
  "summary": "Credit score of 750 (Excellent)..."
}
```

### Application Completeness
```json
{
  "is_complete": true,
  "completeness_percentage": 100.0,
  "missing_fields": [],
  "flags": ["COMPLETE"]
}
```

---

## 🧪 Testing

### Run Demo Script
```bash
python examples/mcp_demo.py
```

Demonstrates:
- Listing applicants
- Getting profiles
- Income stability analysis
- Employment risk assessment
- Credit history analysis
- Application completeness
- Complete analysis
- Resource access
- Applicant comparison

### Run Agent Integration Example
```bash
python examples/agent_with_mcp.py
```

Demonstrates:
- Credit analyzer agent
- Employment risk agent
- Completeness checker
- Comprehensive loan assessor

---

## 📈 Scoring Formulas

### Income Stability Score (0-100)
```
base_score = employment_type_base (40-75)
+ tenure_adjustment (-10 to +25)
+ age_adjustment (-10 to +5)
= total (0-100)
```

Employment Type Base Scores:
- Full-time: 75
- Self-employed: 50
- Contract: 45
- Part-time: 40

Tenure Adjustments:
- < 1 year: -10
- 1-3 years: +5
- 3-5 years: +10
- 5+ years: +15

### Employment Risk Score (0-100)
```
risk_score = employment_type_risk (20-80)
+ tenure_risk (-25 to +15)
= total (0-100)
(higher = more risky)
```

### Credit History Summary
Based on:
- Credit score (primary)
- Delinquencies (significant impact)
- Payment history trend
- Credit utilization ratio
- Account history

---

## 🔐 Security

### Authentication
Currently no authentication. In production, add:

```python
# Add authentication middleware
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/tools/{tool_name}")
async def call_tool(tool_name: str, credentials = Depends(security)):
    # Validate credentials
    # Then execute tool
    ...
```

### Data Privacy
- No sensitive data stored in logs
- Applicant IDs are anonymized
- Credit scores are not logged
- PII should be masked in production

---

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "mcp/server.py"]
```

### Docker Compose
```yaml
services:
  mcp-server:
    build: .
    ports:
      - "3000:3000"
    environment:
      - LOG_LEVEL=info
    volumes:
      - ./mcp:/app/mcp
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: mcp-server:latest
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
```

---

## 📝 API Reference

### Tools

```
GET /tools
- List all available tools

GET /tools/{tool_name}
- Get tool details

POST /tools/{tool_name}/call
- Call a tool with arguments
```

### Resources

```
GET /resources
- List all available resources

POST /resources/read
- Read a resource by URI
```

---

## 🔗 Integration Points

### With FastAPI Services
```python
# In microservices/dependencies/mcp.py
from mcp.clients.mcp_client import SyncMCPClient

def get_mcp_client():
    return SyncMCPClient()

# Use in routes
@app.post("/loans")
async def submit_loan(request: LoanRequest, mcp=Depends(get_mcp_client)):
    analysis = mcp.get_complete_analysis(request.applicant_id)
    ...
```

### With LangChain Agents
```python
# In agents/credit_analyzer/agent.py
from mcp.clients.mcp_client import SyncMCPClient

class CreditAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.mcp = SyncMCPClient()
    
    def invoke(self, state):
        # Get data from MCP
        credit = self.mcp.get_credit_history_summary(state['applicant_id'])
        ...
```

### With LangGraph Orchestration
```python
# In orchestration/workflows/loan_approval_workflow.py
from mcp.clients.mcp_client import SyncMCPClient

def loan_processor_node(state):
    mcp = SyncMCPClient()
    analysis = mcp.get_complete_analysis(state['application_id'])
    state['applicant_analysis'] = analysis
    return state
```

---

## 🐛 Troubleshooting

### Connection Refused
```
Error: Connection refused
Solution: 
  1. Start server: python mcp/server.py
  2. Check port: http://localhost:3000/health
  3. Verify firewall isn't blocking port 3000
```

### Applicant Not Found
```
Error: Applicant APP999 not found
Solution:
  1. Use: APP001, APP002, APP003, or APP004
  2. List available: client.list_all_applicants()
  3. Add more applicants to APPLICANTS_DB in server.py
```

### Timeout Issues
```
Error: Request timeout
Solution:
  1. Increase timeout: client.timeout = 60
  2. Check server performance
  3. Check network latency
```

### Import Errors
```
Error: ModuleNotFoundError: No module named 'fastmcp'
Solution:
  1. Install: pip install fastmcp
  2. Check requirements.txt
  3. Use virtual environment
```

---

## 📚 Documentation

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Detailed usage examples
- [examples/mcp_demo.py](../examples/mcp_demo.py) - Complete demo script
- [examples/agent_with_mcp.py](../examples/agent_with_mcp.py) - Agent integration
- [mcp/clients/mcp_client.py](clients/mcp_client.py) - Client implementation

---

## 🤝 Contributing

To extend the MCP server:

1. **Add a Tool**
   ```python
   @app.tool()
   def new_tool(arg: str) -> dict:
       """Tool description"""
       # Implementation
       return result
   ```

2. **Add a Resource**
   ```python
   @app.resource("applicant://category/resource")
   def new_resource() -> dict:
       """Resource description"""
       return data
   ```

3. **Add Test Data**
   ```python
   APPLICANTS_DB["APP005"] = {
       # New applicant profile
   }
   ```

---

## 📄 License

Part of the Multi-Agent Loan Approval System

---

## 📞 Support

For issues or questions:
1. Check [USAGE_GUIDE.md](USAGE_GUIDE.md)
2. Run [examples/mcp_demo.py](../examples/mcp_demo.py)
3. Review [examples/agent_with_mcp.py](../examples/agent_with_mcp.py)
4. Check server logs: `python mcp/server.py --log-level DEBUG`

