# FastMCP Application DB - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install FastMCP (30 seconds)
```bash
pip install fastmcp httpx uvicorn
```

### Step 2: Start MCP Server (10 seconds)
```bash
python mcp/server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:3000
```

### Step 3: Run Demo (2 minutes)
In another terminal:
```bash
python examples/mcp_demo.py
```

You'll see complete demonstrations of all tools and resources.

### Step 4: Use in Your Code (2 minutes)
```python
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()
result = client.get_complete_analysis("APP001")
print(result)
```

**Done!** 🎉

---

## 📚 What's Available

### Tools (What You Can Do)
```python
# Fetch applicant data
client.get_applicant_profile("APP001")

# Calculate income stability (0-100, higher=better)
client.get_income_stability_score("APP001")

# Calculate employment risk (0-100, higher=worse)
client.get_employment_risk("APP001")

# Get credit analysis
client.get_credit_history_summary("APP001")

# Check if application is complete
client.check_application_completeness("APP001")

# Get ALL metrics in one call (recommended!)
client.get_complete_analysis("APP001")

# List all available applicants
client.list_all_applicants()
```

### Resources (Reference Data)
```python
# Credit scoring rules
client.get_credit_scoring_rules()

# Employment stability factors
client.get_employment_stability_factors()

# Regulatory requirements
client.get_regulatory_requirements()
```

---

## 🧑‍💼 Sample Applicants

Use these IDs:
- `APP001` - John Smith (35, $85k, Full-time, Score 750)
- `APP002` - Sarah Johnson (28, $55k, Full-time, Score 680)
- `APP003` - Michael Chen (45, $120k, Self-employed, Score 720)
- `APP004` - Emma Wilson (32, $72k, Part-time, Score 620)

---

## 💡 Common Use Cases

### Use Case 1: Analyze Single Applicant
```python
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()

# Get complete analysis
analysis = client.get_complete_analysis("APP001")

print(f"Income Stability: {analysis['analysis']['income_stability']['score']}/100")
print(f"Employment Risk: {analysis['analysis']['employment_risk']['risk_score']}/100")
print(f"Credit Score: {analysis['analysis']['credit_history']['credit_score']}")
print(f"Application Complete: {analysis['analysis']['application_completeness']['is_complete']}")
```

### Use Case 2: Use in LangChain Agent
```python
from mcp.clients.mcp_client import SyncMCPClient
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

client = SyncMCPClient()
model = ChatAnthropic()

# Get MCP data
analysis = client.get_complete_analysis("APP001")

# Get LLM recommendation
response = model.invoke([
    HumanMessage(content=f"""
    Recommend loan approval or rejection for:
    - Income Stability: {analysis['analysis']['income_stability']['score']}/100
    - Employment Risk: {analysis['analysis']['employment_risk']['risk_score']}/100
    - Credit Score: {analysis['analysis']['credit_history']['credit_score']}
    - Complete: {analysis['analysis']['application_completeness']['is_complete']}
    """)
])

print(response.content)
```

### Use Case 3: Use in FastAPI
```python
from fastapi import FastAPI, Depends
from mcp.clients.mcp_client import SyncMCPClient

app = FastAPI()

def get_mcp():
    return SyncMCPClient()

@app.get("/analyze/{app_id}")
async def analyze_applicant(app_id: str, mcp=Depends(get_mcp)):
    return mcp.get_complete_analysis(app_id)
```

### Use Case 4: Compare Multiple Applicants
```python
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()
applicants = ["APP001", "APP002", "APP003", "APP004"]

print("Applicant Comparison:")
print(f"{'ID':<8} {'Name':<20} {'Stability':<12} {'Risk':<12} {'Credit':<8}")
print("-" * 60)

for app_id in applicants:
    analysis = client.get_complete_analysis(app_id)
    stability = analysis['analysis']['income_stability']['score']
    risk = analysis['analysis']['employment_risk']['risk_score']
    credit = analysis['analysis']['credit_history']['credit_score']
    
    print(f"{app_id:<8} {analysis['name']:<20} {stability:<12} {risk:<12} {credit:<8}")
```

---

## 🔍 Understanding the Metrics

### Income Stability Score (0-100)
- **90+**: Very stable (full-time, 5+ years)
- **70+**: High stability (full-time, 3+ years)
- **50+**: Medium stability (self-employed, 1+ years)
- **<50**: Low stability (part-time, new job)

### Employment Risk Score (0-100)
- **<30**: Low risk (stable employment)
- **30-60**: Medium risk (some instability)
- **60-75**: High risk (unstable employment)
- **75+**: Very high risk (risky employment)

### Credit Score Categories
- **750+**: Excellent
- **700-749**: Good
- **650-699**: Fair
- **<650**: Poor

### Debt-to-Income Ratio
- **<36%**: Excellent
- **36-43%**: Acceptable
- **43%+**: High risk

---

## 📊 Understanding Responses

All responses follow this format:

**Success**:
```json
{
  "status": "success",
  "applicant_id": "APP001",
  "analysis": {
    // Requested data here
  }
}
```

**Error**:
```json
{
  "status": "error",
  "message": "Applicant APP999 not found",
  "available_applicants": ["APP001", "APP002", ...]
}
```

---

## 🐛 Troubleshooting

### "Connection refused"
**Problem**: MCP server not running
**Solution**: 
```bash
python mcp/server.py
```

### "Applicant APP999 not found"
**Problem**: Using invalid applicant ID
**Solution**: Use valid IDs: APP001, APP002, APP003, APP004

### "Request timeout"
**Problem**: Server too slow
**Solution**: 
```python
client.timeout = 60  # Increase timeout
```

### "Module not found: fastmcp"
**Problem**: Dependency not installed
**Solution**:
```bash
pip install fastmcp
```

---

## 🎓 Learning Path

1. **Start here** (5 min)
   - Read this guide
   - Start the server
   - Run the demo

2. **Explore tools** (10 min)
   - Use `get_complete_analysis()` for each applicant
   - Try other individual tools
   - Check resources with `get_credit_scoring_rules()`

3. **Integrate with agents** (20 min)
   - See `examples/agent_with_mcp.py`
   - Create your own agent
   - Use MCP data in decision logic

4. **Deploy** (advanced)
   - Run in Docker
   - Deploy to cloud
   - Scale horizontally

---

## 📁 File Guide

| File | Purpose |
|------|---------|
| `mcp/server.py` | Main MCP server (start this) |
| `mcp/clients/mcp_client.py` | Client library (use this) |
| `examples/mcp_demo.py` | Full demo (run this first) |
| `examples/agent_with_mcp.py` | Agent examples (learn from this) |
| `mcp/README.md` | Full documentation |
| `mcp/USAGE_GUIDE.md` | Detailed API reference |

---

## ⚡ Common Commands

```bash
# Start server
python mcp/server.py

# Run demo
python examples/mcp_demo.py

# Run agent example
python examples/agent_with_mcp.py

# Start with custom port
python -c "import uvicorn; uvicorn.run('mcp.server:app', port=3001)"

# Debug mode
python mcp/server.py --log-level DEBUG
```

---

## 🧪 Test It Now

Open Python and try:

```python
from mcp.clients.mcp_client import SyncMCPClient

client = SyncMCPClient()

# List applicants
print("Available Applicants:")
applicants = client.list_all_applicants()
for app in applicants['applicants']:
    print(f"  {app['id']}: {app['name']} (Credit: {app['credit_score']})")

# Get analysis
print("\nAnalyzing APP001...")
analysis = client.get_complete_analysis("APP001")
print(f"Name: {analysis['name']}")
print(f"Stability: {analysis['analysis']['income_stability']['score']}")
print(f"Risk: {analysis['analysis']['employment_risk']['risk_score']}")
print(f"Credit: {analysis['analysis']['credit_history']['credit_score']}")
```

Expected output:
```
Available Applicants:
  APP001: John Smith (Credit: 750)
  APP002: Sarah Johnson (Credit: 680)
  APP003: Michael Chen (Credit: 720)
  APP004: Emma Wilson (Credit: 620)

Analyzing APP001...
Name: John Smith
Stability: 89
Risk: 15
Credit: 750
```

---

## 🎯 Next Steps

1. ✅ Run demo: `python examples/mcp_demo.py`
2. ✅ Try in Python: Use code samples above
3. ✅ Integrate with agents: See `examples/agent_with_mcp.py`
4. ✅ Add to FastAPI: Use in API routes
5. ✅ Deploy: Docker, Kubernetes, or cloud provider

---

## 💬 Quick Reference

**Get everything about an applicant**:
```python
analysis = client.get_complete_analysis("APP001")
```

**Get just one metric**:
```python
stability = client.get_income_stability_score("APP001")
risk = client.get_employment_risk("APP001")
credit = client.get_credit_history_summary("APP001")
complete = client.check_application_completeness("APP001")
```

**Get reference rules**:
```python
credit_rules = client.get_credit_scoring_rules()
employment_factors = client.get_employment_stability_factors()
compliance_reqs = client.get_regulatory_requirements()
```

---

## 🆘 Help

- **Not working?** Check troubleshooting above
- **Need details?** See `mcp/USAGE_GUIDE.md`
- **Want examples?** See `examples/agent_with_mcp.py`
- **Full docs?** See `mcp/README.md`

---

## 🎉 You're Ready!

The MCP server is production-ready and can:
- ✅ Fetch applicant profiles
- ✅ Calculate financial stability
- ✅ Assess employment risk
- ✅ Analyze credit history
- ✅ Verify application completeness
- ✅ Provide compliance rules
- ✅ Scale to thousands of applicants

Start using it in your agents and services now!

