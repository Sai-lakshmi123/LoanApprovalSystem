# Application DB MCP Server - Usage Guide

## Overview

The Application DB is a FastMCP server that simulates a database of applicant profiles and provides tools for analyzing applicant data. It includes:

- **4 Applicants** with realistic financial profiles (APP001-APP004)
- **7 MCP Tools** for fetching and analyzing applicant data
- **3 MCP Resources** for access to reference data (credit rules, employment factors, regulatory requirements)

---

## Getting Started

### 1. Install FastMCP

```bash
pip install fastmcp
```

### 2. Start the MCP Server

```bash
python mcp/server.py
```

Or with uvicorn directly:

```bash
uvicorn mcp.server:app --host 0.0.0.0 --port 3000 --reload
```

The server will start on `http://localhost:3000`

### 3. Verify the Server is Running

```bash
curl http://localhost:3000/health
```

---

## Available Applicants

| ID | Name | Age | Income | Credit Score | Employment |
|----|----|-----|--------|--------------|------------|
| APP001 | John Smith | 35 | $85,000 | 750 | Full-time Engineer |
| APP002 | Sarah Johnson | 28 | $55,000 | 680 | Full-time Marketing |
| APP003 | Michael Chen | 45 | $120,000 | 720 | Self-employed |
| APP004 | Emma Wilson | 32 | $72,000 | 620 | Part-time Sales |

---

## MCP Tools

### Tool 1: `get_applicant_profile`

Fetch complete applicant profile data.

**Parameters:**
- `applicant_id` (string): Applicant ID (e.g., "APP001")

**Returns:**
- Full applicant profile including demographics, income, employment, and credit data

**Example Usage (Sync):**
```python
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()
profile = client.get_applicant_profile("APP001")
print(profile)
```

**Example Usage (Async):**
```python
import asyncio
from mcp.clients.mcp_client import MCPClient

async def main():
    client = MCPClient()
    profile = await client.get_applicant_profile("APP001")
    print(profile)

asyncio.run(main())
```

**Sample Response:**
```json
{
  "status": "success",
  "data": {
    "id": "APP001",
    "name": "John Smith",
    "age": 35,
    "annual_income": 85000,
    "employment_type": "full_time",
    "credit_score": 750,
    "credit_history": {...}
  }
}
```

---

### Tool 2: `get_income_stability_score`

Calculate income stability score based on employment type and tenure.

**Score Range:** 0-100 (higher = more stable)

**Factors Considered:**
- Employment type (full-time, self-employed, part-time, contract)
- Years at current job
- Age (25-55 is optimal)

**Example Usage:**
```python
client = SyncMCPClient()
stability = client.get_income_stability_score("APP001")
print(f"Score: {stability['analysis']['score']}")
print(f"Category: {stability['analysis']['stability_category']}")
```

**Sample Response:**
```json
{
  "status": "success",
  "applicant_id": "APP001",
  "analysis": {
    "score": 89,
    "employment_type": "full_time",
    "years_at_job": 4,
    "age": 35,
    "stability_category": "Very High"
  }
}
```

---

### Tool 3: `get_employment_risk`

Calculate employment risk score based on employment type and job tenure.

**Score Range:** 0-100 (higher = more risky)

**Factors Considered:**
- Employment type stability
- Tenure at current position
- Recent job changes

**Example Usage:**
```python
client = SyncMCPClient()
risk = client.get_employment_risk("APP001")
print(f"Risk Score: {risk['analysis']['risk_score']}")
print(f"Risk Level: {risk['analysis']['risk_level']}")
print(f"Tenure Risk: {risk['analysis']['tenure_risk']}")
```

**Sample Response:**
```json
{
  "status": "success",
  "applicant_id": "APP001",
  "analysis": {
    "risk_score": 15,
    "risk_level": "Low",
    "employment_type": "full_time",
    "tenure_risk": "Stable"
  }
}
```

---

### Tool 4: `get_credit_history_summary`

Get comprehensive credit history analysis.

**Metrics Provided:**
- Credit score and category
- Delinquency status
- Payment history trend
- Credit utilization ratio
- Account information
- Summary text

**Example Usage:**
```python
client = SyncMCPClient()
credit = client.get_credit_history_summary("APP001")
print(f"Score: {credit['analysis']['credit_score']}")
print(f"Category: {credit['analysis']['score_category']}")
print(f"Summary: {credit['analysis']['summary']}")
```

**Sample Response:**
```json
{
  "status": "success",
  "applicant_id": "APP001",
  "analysis": {
    "credit_score": 750,
    "score_category": "Excellent",
    "delinquencies": 0,
    "delinquency_status": "No delinquencies",
    "accounts_open": 5,
    "total_accounts": 8,
    "credit_utilization_ratio": 35.0,
    "utilization_status": "Excellent",
    "payment_trend": "Improving",
    "summary": "Credit score of 750 (Excellent). No delinquencies. Payment history is Improving. Credit utilization is Excellent."
  }
}
```

---

### Tool 5: `check_application_completeness_tool`

Check if application has all required information.

**Checks:**
- All required fields present
- Credit history fully populated
- Completeness percentage
- Missing fields and flags

**Example Usage:**
```python
client = SyncMCPClient()
completeness = client.check_application_completeness("APP001")
print(f"Complete: {completeness['analysis']['is_complete']}")
print(f"Completeness: {completeness['analysis']['completeness_percentage']}%")
print(f"Flags: {completeness['analysis']['flags']}")
```

**Sample Response:**
```json
{
  "status": "success",
  "applicant_id": "APP001",
  "analysis": {
    "is_complete": true,
    "completeness_percentage": 100.0,
    "missing_fields": [],
    "incomplete_sections": [],
    "flags": ["COMPLETE"]
  }
}
```

---

### Tool 6: `get_complete_applicant_analysis`

Get all analyses in one call (most useful).

**Includes:**
- Income stability score
- Employment risk assessment
- Credit history summary
- Application completeness

**Example Usage:**
```python
client = SyncMCPClient()
full_analysis = client.get_complete_analysis("APP001")
print(f"Name: {full_analysis['name']}")
print(f"Stability Score: {full_analysis['analysis']['income_stability']['score']}")
print(f"Risk Level: {full_analysis['analysis']['employment_risk']['risk_level']}")
print(f"Credit Score: {full_analysis['analysis']['credit_history']['credit_score']}")
print(f"Completeness: {full_analysis['analysis']['application_completeness']['completeness_percentage']}%")
```

**Sample Response:**
```json
{
  "status": "success",
  "applicant_id": "APP001",
  "name": "John Smith",
  "analysis": {
    "income_stability": {
      "score": 89,
      "stability_category": "Very High"
    },
    "employment_risk": {
      "risk_score": 15,
      "risk_level": "Low"
    },
    "credit_history": {
      "credit_score": 750,
      "score_category": "Excellent"
    },
    "application_completeness": {
      "is_complete": true,
      "completeness_percentage": 100.0
    }
  },
  "timestamp": "2024-05-21T10:30:00"
}
```

---

### Tool 7: `list_all_applicants`

List all available applicants in the system.

**Example Usage:**
```python
client = SyncMCPClient()
applicants = client.list_all_applicants()
for app in applicants['applicants']:
    print(f"{app['id']}: {app['name']} (Score: {app['credit_score']})")
```

**Sample Response:**
```json
{
  "status": "success",
  "count": 4,
  "applicants": [
    {
      "id": "APP001",
      "name": "John Smith",
      "age": 35,
      "credit_score": 750
    },
    ...
  ]
}
```

---

## MCP Resources

### Resource 1: `applicant://credit/scoring_rules`

Credit scoring rules and thresholds.

**Example Usage:**
```python
client = SyncMCPClient()
rules = client.get_credit_scoring_rules()
print(f"Min Score: {rules['minimum_credit_score']}")
print(f"Recommended Min: {rules['recommended_minimum']}")
```

**Contains:**
- Score categories (Excellent, Good, Fair, Poor)
- Credit utilization thresholds
- Delinquency impact scores
- Minimum acceptable thresholds

---

### Resource 2: `applicant://employment/stability_factors`

Employment stability factors and risk criteria.

**Example Usage:**
```python
client = SyncMCPClient()
factors = client.get_employment_stability_factors()
for emp_type, info in factors['employment_types'].items():
    print(f"{emp_type}: {info['risk_level']}")
```

**Contains:**
- Employment type classifications
- Base stability scores by type
- Tenure adjustment factors
- Minimum acceptable stability scores

---

### Resource 3: `applicant://compliance/regulatory_requirements`

Regulatory compliance requirements.

**Example Usage:**
```python
client = SyncMCPClient()
reqs = client.get_regulatory_requirements()
print(f"Min Age: {reqs['minimum_requirements']['minimum_age']}")
print(f"Min Score: {reqs['minimum_requirements']['minimum_credit_score']}")
```

**Contains:**
- Minimum requirements (age, income, credit score, debt-to-income)
- Preferred thresholds
- Required documentation
- Fair lending compliance checks

---

## Integration with LangChain Agents

### Example: Using in an Agent

```python
from langchain.tools import tool
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()

@tool
def analyze_applicant(applicant_id: str) -> dict:
    """Get complete applicant analysis from Application DB."""
    return client.get_complete_analysis(applicant_id)

@tool
def check_compliance(applicant_id: str) -> dict:
    """Check if applicant meets regulatory requirements."""
    analysis = client.get_complete_analysis(applicant_id)
    rules = client.get_regulatory_requirements()
    
    is_compliant = (
        analysis['analysis']['credit_history']['credit_score'] >= 
        rules['minimum_requirements']['minimum_credit_score']
    )
    
    return {
        "compliant": is_compliant,
        "credit_score": analysis['analysis']['credit_history']['credit_score'],
        "minimum_required": rules['minimum_requirements']['minimum_credit_score']
    }
```

---

## Integration with LangGraph Workflows

### Example: Agent Using MCP Tools

```python
from langgraph.graph import StateGraph
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()

def credit_analyzer_agent(state):
    """Analyze applicant credit using MCP tools."""
    app_id = state['application_id']
    
    # Get credit history from MCP
    credit = client.get_credit_history_summary(app_id)
    
    # Get rules from MCP resource
    rules = client.get_credit_scoring_rules()
    
    # Analyze
    score = credit['analysis']['credit_score']
    min_required = rules['minimum_credit_score']
    
    state['credit_analysis'] = {
        'score': score,
        'meets_minimum': score >= min_required,
        'category': credit['analysis']['score_category']
    }
    
    return state

# Use in workflow
graph = StateGraph(WorkflowState)
graph.add_node("credit_analyzer", credit_analyzer_agent)
```

---

## Async/Await Pattern

### Example with Asyncio

```python
import asyncio
from mcp.clients.mcp_client import MCPClient

async def analyze_multiple_applicants():
    client = MCPClient()
    applicant_ids = ["APP001", "APP002", "APP003", "APP004"]
    
    # Fetch all in parallel
    tasks = [client.get_complete_analysis(app_id) for app_id in applicant_ids]
    results = await asyncio.gather(*tasks)
    
    return results

# Run
results = asyncio.run(analyze_multiple_applicants())
for result in results:
    print(f"{result['name']}: Credit {result['analysis']['credit_history']['credit_score']}")
```

---

## Error Handling

### Handle Missing Applicant

```python
client = SyncMCPClient()
result = client.get_applicant_profile("INVALID_ID")

if result.get('status') == 'error':
    print(f"Error: {result['message']}")
    print(f"Available: {result.get('available_applicants', [])}")
else:
    print(f"Found: {result['data']['name']}")
```

---

## Complete Example Script

See [examples/mcp_demo.py](examples/mcp_demo.py) for a complete working example.

To run:
```bash
python examples/mcp_demo.py
```

---

## Configuration

### Server Configuration

Edit `mcp/server.py` to:
- Add more applicants to `APPLICANTS_DB`
- Modify scoring algorithms
- Change port (currently 3000)

### Client Configuration

```python
# Use different server URL
client = SyncMCPClient(base_url="http://localhost:3001")

# Adjust timeout
client.timeout = 60
```

---

## Troubleshooting

### Server not responding
```
Error: Connection refused
Solution: Make sure server is running: python mcp/server.py
```

### Applicant not found
```
Error: Applicant APP999 not found
Solution: Use one of: APP001, APP002, APP003, APP004
Use list_all_applicants() to see available applicants
```

### Tool call timeout
```
Error: Request timeout
Solution: Increase client timeout:
client.timeout = 60
```

---

## Performance

- **Tool call latency**: < 100ms (local)
- **Resource read latency**: < 50ms (local)
- **Concurrent requests**: Supports 100+ concurrent calls
- **Memory footprint**: < 50MB

---

## Next Steps

1. **Add to agents**: Use MCP tools in LangChain agents
2. **Extend resources**: Add more reference data resources
3. **Add tools**: Create additional analysis tools
4. **Integrate with FastAPI**: Use MCP client in API endpoints
5. **Deploy**: Run in production with proper error handling

