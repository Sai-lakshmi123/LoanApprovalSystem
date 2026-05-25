# 📡 MCP Servers Documentation

Four Model Context Protocol servers that provide data and tool integration for the AI agents.

## 📖 What are MCP Servers?

MCP (Model Context Protocol) servers are standalone services that:
- Provide tools and resources to AI agents
- Return structured data for decision-making
- Simulate real database/system interactions
- Run on separate ports (3001-3004)

## 🛠️ The Four MCP Servers

### 1️⃣ [Application DB](application-db/)
**Purpose:** Fetch and manage applicant profile data

**Port:** 3001

**Data Provided:**
- Applicant age, employment type, duration
- Annual income and monthly expenses
- Credit score and history
- Application completeness flags
- Income stability score
- Employment risk assessment

**Files:**
- [Implementation Guide](application-db/implementation.md)
- [Quick Reference](application-db/quick-reference.md)
- [Summary](application-db/summary.txt)

---

### 2️⃣ [Risk Rules DB](risk-rules-db/)
**Purpose:** Evaluate financial risk metrics

**Port:** 3002

**Data Provided:**
- Debt-to-Income (DTI) Ratio calculation
- Loan-to-Value (LTV) Ratio
- Credit score risk level
- Loan amount risk assessment
- Anomaly detection (unusual patterns)
- Risk reasoning and explanations

**Files:**
- [Implementation Guide](risk-rules-db/implementation.md)
- [Quick Reference](risk-rules-db/quick-reference.md)
- [Summary](risk-rules-db/summary.txt)

---

### 3️⃣ [Decision Synthesis](decision-synthesis/)
**Purpose:** Compile decision classification and factors

**Port:** 3003

**Data Provided:**
- Decision classification (APPROVE/REJECT/REVIEW)
- Risk score (1-5 scale)
- Confidence level (0-100%)
- Key decision factors
- Detailed explanation

**Files:**
- [Implementation Guide](decision-synthesis/implementation.md)
- [Quick Reference](decision-synthesis/quick-reference.md)
- [Summary](decision-synthesis/summary.txt)

---

### 4️⃣ [Notification System](notification-system/)
**Purpose:** Record decisions and compliance actions

**Port:** 3004

**Data Provided:**
- Action recorded (decision type)
- Case ID generation (unique tracking)
- Timestamp recording
- Notification sent confirmation
- Summary of action

**Files:**
- [Implementation Guide](notification-system/implementation.md)
- [Quick Reference](notification-system/quick-reference.md)
- [Summary](notification-system/summary.txt)

---

## 🔄 How Agents Use MCP Servers

```
┌─────────────┐
│  Agent 1    │
└──────┬──────┘
       │ queries
       ↓
┌──────────────────────────┐
│ Application DB (Port 3001)│  ← Returns applicant profile
└──────────────────────────┘

┌─────────────┐
│  Agent 2    │
└──────┬──────┘
       │ queries
       ↓
┌──────────────────────────┐
│ Risk Rules DB (Port 3002) │  ← Returns risk metrics
└──────────────────────────┘

┌─────────────┐
│  Agent 3    │
└──────┬──────┘
       │ queries
       ↓
┌────────────────────────────┐
│ Decision Synthesis (Port 3003)│ ← Returns decision
└────────────────────────────┘

┌─────────────┐
│  Agent 4    │
└──────┬──────┘
       │ queries
       ↓
┌──────────────────────────────┐
│ Notification System (Port 3004)│ ← Records decision
└──────────────────────────────┘
```

## 🚀 Quick Start

### 1. Start All MCP Servers
```bash
bash START_SERVICES.sh
```

### 2. Verify They're Running
```bash
# Check all ports are listening
netstat -tuln | grep 300
```

Expected output:
```
LISTEN  3001  (Application DB)
LISTEN  3002  (Risk Rules DB)
LISTEN  3003  (Decision Synthesis)
LISTEN  3004  (Notification System)
```

### 3. Test an MCP Server
```bash
# Example: Test Application DB
curl -X POST http://localhost:3001/get_applicant_profile \
  -H "Content-Type: application/json" \
  -d '{"applicant_id": "TEST_001"}'
```

## 📚 Detailed Documentation

- **Overview & Concepts:** [overview.md](overview.md)
- **MCP Framework Guide:** [mcp-framework-guide.md](mcp-framework-guide.md)
- **Quick Start Guide:** [quick-start.md](quick-start.md)
- **Usage Guide:** [usage-guide.md](usage-guide.md)
- **Files Index:** [files-index.txt](files-index.txt)

## 🔧 Technology Stack

- **Framework:** FastMCP (Python)
- **Protocol:** Model Context Protocol (MCP)
- **Server Type:** Standalone HTTP services
- **Data Format:** JSON
- **Ports:** 3001, 3002, 3003, 3004

## 📊 Data Flow Example

**Request Flow for a Loan Application:**

```
1. User submits loan via Streamlit UI
   ↓
2. FastAPI receives POST /evaluate-loan
   ↓
3. LangGraph starts orchestration
   ↓
4. Agent 1 calls Application DB (3001)
   → Gets applicant profile
   ↓
5. Agent 2 calls Risk Rules DB (3002)
   → Gets risk metrics
   ↓
6. Agent 3 calls Decision Synthesis (3003)
   → Gets decision factors
   ↓
7. Agent 4 calls Notification System (3004)
   → Records case ID
   ↓
8. Final decision returned to user
```

## ⚙️ Configuration

Each MCP server can be configured:
- **Port:** Change in config or environment variables
- **Database:** Point to real/mock data sources
- **Timeout:** Set response time limits
- **Retry Logic:** Enable/disable automatic retries

See individual implementation guides for configuration details.

## 🔗 Related Documentation

- **Architecture:** [System Design](../architecture/system-design.md)
- **Agents:** [Agent Documentation](../agents/) (how agents use these servers)
- **API:** [FastAPI Guide](../fastapi/) (how requests reach agents)
- **Testing:** [Testing Guide](../testing/) (test MCP servers)

## 🐛 Troubleshooting

**MCP server not starting?**
- Check port availability: `lsof -i :3001`
- Check logs: See startup output
- See [Error Handling Guide](../api-integration/error-handling-guide.md)

**Data not returning?**
- Verify server is running: `curl http://localhost:3001/health`
- Check request format matches specification
- Review MCP server logs

**Performance issues?**
- Check response times in logs
- Verify no concurrent agent calls overwhelming single server
- Consider load balancing multiple instances

---

**Next Steps:** 
1. Choose a specific MCP server above
2. Read its Implementation guide
3. Test with cURL or the UI
4. See it in action with test scenarios

Ready to dive deeper? 🚀
