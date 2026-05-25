# Application Profile Agent (Agent1) - Quick Reference

## 🚀 30-Second Setup

```bash
# 1. Make sure Application DB server is running (separate terminal)
python mcp/server.py

# 2. Run Agent1
python agents/application_profile_agent.py
```

---

## 📊 What Agent1 Does

Agent1 is an intelligent loan analyst powered by Claude Sonnet 4.6. It:
- Connects to Application DB MCP Server
- Analyzes loan applicant data comprehensively
- Returns structured analysis with key metrics
- Provides detailed reasoning and assessments

**LLM Model:** Claude Sonnet 4.6 (claude-sonnet-4-6-20250514)
**Framework:** Anthropic Agent SDK
**Port:** Connects to Application DB on port 3000

---

## 📋 Structured Output

Agent1 returns analysis with these exact fields:

```json
{
    "applicant_id": "APP001",
    "applicant_name": "John Strong",
    "analysis_timestamp": "2026-05-24T10:30:00",
    "income_stability": {
        "score": 85,
        "stability_category": "Very Stable",
        "analysis": "Detailed explanation..."
    },
    "employment_risk": {
        "risk_score": 15,
        "risk_level": "Very Low",
        "employment_type": "W-2 Employee",
        "tenure_years": 8,
        "analysis": "Detailed explanation..."
    },
    "credit_history": {
        "credit_score": 760,
        "score_category": "Excellent",
        "delinquencies": 0,
        "default_count": 0,
        "credit_utilization": 30,
        "summary": "Comprehensive summary..."
    },
    "application_completeness": {
        "is_complete": true,
        "completeness_percentage": 100,
        "missing_items": [],
        "flags": []
    },
    "overall_assessment": "Executive summary...",
    "key_strengths": ["Strong income...", "Low employment risk..."],
    "key_concerns": [],
    "recommended_next_steps": ["Proceed to risk evaluation..."]
}
```

---

## 🛠️ 6 Tools Agent Has Access To

| Tool | Purpose |
|------|---------|
| `get_applicant_profile` | Fetch complete applicant data |
| `get_income_stability_score` | Analyze income stability (0-100) |
| `get_employment_risk` | Assess employment risk level |
| `get_credit_history_summary` | Review credit profile |
| `check_application_completeness` | Verify all required fields |
| `get_complete_applicant_analysis` | Get all metrics in one call |

---

## 💡 How Agent1 Works

```
User Input: "Analyze applicant APP001"
    ↓
Agent1 receives request with system prompt
    ↓
Agent uses tools to gather data from Application DB
    ↓
Claude Sonnet 4.6 analyzes all metrics
    ↓
Agent synthesizes findings into structured JSON
    ↓
Returns comprehensive analysis with all required fields
```

---

## 📚 System Prompt Highlights

Agent1 operates with a detailed system prompt that instructs Claude to:

1. **Gather Data**: Use all available tools systematically
2. **Analyze Thoroughly**: Evaluate financial and employment stability
3. **Score Metrics**:
   - Income Stability: 0-100 (0=Very Unstable, 100=Very Stable)
   - Employment Risk: 0-100 (0=Very Low, 100=Very High)
4. **Check Completeness**: Identify any missing documentation
5. **Provide Structure**: Always return valid JSON with exact fields
6. **Fair Lending**: Consider all factors objectively
7. **Executive Summary**: Provide actionable insights

---

## 🔧 Configuration

### Default Settings
```python
Model: claude-sonnet-4-6-20250514  # Latest Claude Sonnet 4.6
Port: http://localhost:3000        # Application DB
Timeout: 30 seconds
Max Iterations: 10                  # Safety limit for tool use loops
```

### Change Model (if needed)
Edit `agents/application_profile_agent.py`:
```python
self.model = "claude-opus-4-7-20250805"  # Or another model
```

### Change Application DB URL
```python
self.app_db = ApplicationDBClient(
    base_url="http://localhost:3001"  # Different port
)
```

---

## 📈 Income Stability Score Interpretation

| Score Range | Category | Meaning |
|---|---|---|
| 0-30 | Very Unstable | Highly variable/unreliable income |
| 31-50 | Unstable | Significant income variability |
| 51-70 | Stable | Generally consistent income |
| 71-100 | Very Stable | Strong, reliable income |

---

## ⚠️ Employment Risk Level Interpretation

| Risk Score | Level | Characteristics |
|---|---|---|
| 0-20 | Very Low | Stable job, long tenure, strong industry |
| 21-40 | Low | Secure employment, decent tenure |
| 41-60 | Medium | Some concerns but generally acceptable |
| 61-80 | High | Significant employment risks |
| 81-100 | Very High | Critical employment concerns |

---

## 🔍 Credit History Summary

Agent analyzes:
- **Credit Score**: Ranges from 300-850
- **Categories**: Excellent (750+), Good (700-749), Fair (650-699), Poor (600-649), Very Poor (<600)
- **Delinquencies**: 30, 60, 90+ day late payments
- **Defaults**: Account defaults or charge-offs
- **Utilization**: % of available credit being used (30% = healthy)

---

## ✅ Application Completeness Flags

Agent identifies:
- **Complete**: All required fields present (100%)
- **Missing Items**: Specific documentation needed
- **Incomplete Sections**: Partially filled forms
- **Outstanding Requests**: Items awaiting applicant submission

---

## 🔌 Integration with Other Agents

Agent1 provides foundational analysis for downstream agents:

```
Agent1 (Application Profile)
    ↓ (income, employment, credit data)
Agent2 (Risk Rules Agent) - To be created
    ↓ (risk assessment)
Agent3 (Decision Synthesis Agent) - To be created
    ↓ (final decision)
Agent4 (Notification Agent) - To be created
```

---

## 📊 Output Examples

### Strong Applicant
```
Income Stability: 85 (Very Stable)
Employment Risk: 15 (Very Low)
Credit Score: 760 (Excellent)
Completeness: 100%

✅ Recommended: Proceed to risk evaluation
```

### Acceptable with Concerns
```
Income Stability: 65 (Stable)
Employment Risk: 45 (Medium)
Credit Score: 680 (Fair)
Completeness: 85%

⚠️ Recommended: Review with conditions, verify missing documents
```

### High Risk Profile
```
Income Stability: 35 (Unstable)
Employment Risk: 75 (High)
Credit Score: 580 (Very Poor)
Completeness: 60%

❌ Recommended: Manual review required, request additional documentation
```

---

## 🚨 Troubleshooting

**Connection Refused**
```
Make sure Application DB server is running:
python mcp/server.py
```

**JSON Parse Error**
Agent response format invalid - check Claude's output formatting

**Tool Not Found**
Ensure Application DB has all 6 tools available

**Timeout**
Increase timeout: `ApplicationDBClient(timeout=60)`

---

## 📝 System Prompt Summary

The complete system prompt instructs the agent to:

1. **Role**: Expert loan application profile analyst
2. **Data Gathering**: Fetch complete applicant data using available tools
3. **Analysis**: Evaluate income, employment, credit, and completeness
4. **Scoring**: Apply standard scoring methodologies
5. **Output**: Structure results as valid JSON with exact fields
6. **Compliance**: Fair lending considerations throughout
7. **Context**: Provide reasoning for all assessments
8. **Guidelines**: Be thorough, objective, and evidence-based

---

## 🎯 Next Steps

1. ✅ Run Agent1: `python agents/application_profile_agent.py`
2. 📊 Review structured output for applicants
3. 🔗 Integrate output with downstream agents
4. 📈 Use as foundation for risk evaluation
5. 🎓 Build Agent2 for risk rules evaluation

---

## 📞 Files Reference

- **Agent Code**: `agents/application_profile_agent.py`
- **Documentation**: `agents/AGENT1_QUICKREF.md` (this file)
- **Full Guide**: `agents/AGENT1_IMPLEMENTATION.md` (coming soon)
- **System Prompt**: See agent file, lines 20-120
- **Tools**: Connected to `mcp/server.py` (Application DB)

---

## ✨ Key Features of Agent1

✅ Claude Sonnet 4.6 LLM for intelligent analysis
✅ Anthropic Agent SDK for structured tool use
✅ 6 specialized tools for data gathering
✅ Comprehensive system prompt with analysis framework
✅ Structured JSON output with exact required fields
✅ Fair lending compliance built-in
✅ Multi-iteration support for complex analysis
✅ Error handling and validation
✅ Production-ready implementation
