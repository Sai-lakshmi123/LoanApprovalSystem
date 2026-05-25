# 🏗️ Architecture Documentation

Understand how the Loan Approval System is structured and designed.

## 📖 What's in This Folder

| File | Purpose |
|------|---------|
| [system-index.md](system-index.md) | Complete system index with all components |
| [system-design.md](system-design.md) | Detailed system design and patterns |
| [layer-architecture.md](layer-architecture.md) | 5-layer architecture (Presentation → Agent) |
| [langgraph-orchestration.md](langgraph-orchestration.md) | Agent orchestration workflow |
| [project-structure.md](project-structure.md) | High-level project structure |
| [structure-summary.md](structure-summary.md) | Structure summary notes |
| [folder-tree.txt](folder-tree.txt) | Visual file tree |
| [orchestration-summary.txt](orchestration-summary.txt) | Orchestration implementation notes |

## 🔍 Quick Navigation

### Understand the Overall Design
Start with → [system-index.md](system-index.md) (5 min read)

### Deep Dive: How It's Organized
Then read → [layer-architecture.md](layer-architecture.md) (10 min read)

### Deep Dive: How Agents Work Together
Then read → [langgraph-orchestration.md](langgraph-orchestration.md) (10 min read)

### Visual Reference
Check → [folder-tree.txt](folder-tree.txt) (2 min)

## 🎯 Key Architecture Principles

1. **Layered Architecture** - Clear separation of concerns
   - Presentation Layer (Streamlit UI)
   - Microservices Layer (FastAPI)
   - Orchestration Layer (LangGraph)
   - Agent Layer (4 intelligent agents)
   - Integration Layer (MCP servers)

2. **Agent-Based Decision Making** - Multiple agents with specialized roles
3. **Event-Driven Orchestration** - LangGraph manages agent coordination
4. **Tool Integration** - MCP servers provide data and capabilities
5. **Error Resilience** - Retry logic and fallback mechanisms

## 📊 System Overview

```
┌─────────────────────────────────────────────┐
│         Streamlit Web UI (Port 8501)        │
│  - Application form submission              │
│  - Real-time result display                 │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────┴──────────────────────────┐
│      FastAPI REST Service (Port 8000)       │
│  - /evaluate-loan endpoint                  │
│  - Request validation                       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────┴──────────────────────────┐
│    LangGraph Orchestration Engine           │
│  - Coordinates 4 agents                     │
│  - State management                         │
│  - Error handling & retries                 │
└──────────────────┬──────────────────────────┘
        │          │          │          │
┌───────┴──┐  ┌────┴───┐  ┌──┴────┐  ┌─┴──────┐
│ Agent 1  │  │Agent 2 │  │Agent 3│  │Agent 4 │
│ Profile  │  │ Risk   │  │Decisi-│  │Compli- │
│ Analysis │  │ Analysis  │on     │  │ance    │
└────┬─────┘  └────┬───┘  └───┬───┘  └──┬─────┘
     │             │          │         │
┌────┴──────────────┴──────────┴─────────┴────┐
│         MCP Servers (4 servers)             │
│  1. Application DB    (Port 3001)           │
│  2. Risk Rules DB     (Port 3002)           │
│  3. Decision Synthesis (Port 3003)          │
│  4. Notification System (Port 3004)         │
└──────────────────────────────────────────────┘
```

## 🔗 Related Documentation

- **Agents:** See [agents/](../agents/README.md) for individual agent details
- **MCP Servers:** See [mcp-servers/](../mcp-servers/) for data integration
- **API:** See [fastapi/](../fastapi/) for REST endpoints
- **UI:** See [streamlit-ui/](../streamlit-ui/) for web interface
- **Setup:** See [setup-deployment/](../setup-deployment/) for installation

---

**Next Step:** Start with [system-index.md](system-index.md) for a complete overview! 📖
