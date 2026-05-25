# Multi-Agent Agentic AI System

A comprehensive Python development environment for building multi-agent AI systems using FastAPI, Streamlit, LangChain, LangGraph, and the Anthropic Claude API.

## 🎯 Overview

This project provides a production-ready setup for developing intelligent multi-agent systems with:

- **FastAPI** - Modern, fast web framework for building APIs
- **Streamlit** - Interactive UI framework for AI applications
- **LangChain** - Framework for developing language model applications
- **LangGraph** - Tool for building stateful, multi-actor applications
- **Anthropic Claude** - Powerful language model backbone
- **FastMCP** - Model Context Protocol integration for FastAPI

## 📋 What's Included

### Files

- **`requirements.txt`** - All Python dependencies with pinned versions
- **`SETUP.md`** - Comprehensive setup and installation guide
- **`.env.example`** - Environment variable template
- **`setup.sh`** - Automated setup script (Linux/macOS)
- **`src/api/main.py`** - FastAPI application template
- **`src/ui/app.py`** - Streamlit UI template
- **`src/agents/example_agent.py`** - Multi-agent workflow example

### Package Versions

All packages are pre-configured with stable, tested versions:

```
FastAPI==0.109.2
Streamlit==1.31.1
LangChain==0.1.14
LangGraph==0.0.30
Anthropic==0.25.8
FastMCP==0.0.11
```

## 🚀 Quick Start

### Option 1: Automated Setup (Linux/macOS)

```bash
cd /path/to/LoanApprovalSystem
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## ⚙️ Configuration

### Environment Variables

Required:
```env
ANTHROPIC_API_KEY=sk_...  # Get from console.anthropic.com
```

Optional:
```env
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
STREAMLIT_SERVER_PORT=8501
ENVIRONMENT=development
DEBUG=True
```

## 🏃 Running the System

### Start FastAPI Server

```bash
source venv/bin/activate
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs (Interactive API docs)

### Start Streamlit UI (in another terminal)

```bash
source venv/bin/activate
streamlit run src/ui/app.py
```

Visit: http://localhost:8501

### Run Example Agent

```bash
python3 src/agents/example_agent.py
```

## 📁 Project Structure

```
├── venv/                      # Virtual environment
├── src/
│   ├── agents/               # Multi-agent definitions
│   │   ├── example_agent.py  # Example loan approval workflow
│   │   └── __init__.py
│   ├── api/                  # FastAPI application
│   │   ├── main.py           # Main API server
│   │   └── __init__.py
│   ├── ui/                   # Streamlit application
│   │   ├── app.py            # Main UI
│   │   └── __init__.py
│   └── tools/                # Custom tools and utilities
│       └── __init__.py
├── tests/                    # Unit tests
├── .env                      # Environment variables (DO NOT commit)
├── .env.example              # Template
├── requirements.txt          # Dependencies
├── setup.sh                  # Setup script
├── SETUP.md                  # Detailed setup guide
└── README.md                 # This file
```

## 🔌 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### List Agents
```bash
curl http://localhost:8000/agents
```

### Process Request
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "Process my loan application",
    "agent_type": "loan_processor",
    "metadata": {"source": "api"}
  }'
```

## 💡 Example: Creating an Agent

```python
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

model = ChatAnthropic(model="claude-opus-4-1-20250805")

def my_agent(state):
    response = model.invoke([
        HumanMessage(content="Your prompt here")
    ])
    return {"messages": state["messages"] + [response]}

graph = StateGraph(AgentState)
graph.add_node("my_agent", my_agent)
graph.add_edge(START, "my_agent")
graph.add_edge("my_agent", END)

compiled = graph.compile()
result = compiled.invoke(initial_state)
```

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# With coverage
python -m pytest tests/ --cov=src
```

## 🔧 Troubleshooting

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### "ANTHROPIC_API_KEY not found"
```bash
# Check .env file
cat .env

# Or set inline
export ANTHROPIC_API_KEY=sk_...
```

### Port Already in Use
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn src.api.main:app --port 8001
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 📋 Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] .env file created with ANTHROPIC_API_KEY
- [ ] FastAPI server running (`uvicorn src.api.main:app --reload`)
- [ ] Streamlit app running (`streamlit run src/ui/app.py`)
- [ ] Tested basic endpoints

## 🤝 Next Steps

1. **Customize Agents** - Modify `src/agents/example_agent.py` for your use case
2. **Add API Routes** - Extend `src/api/main.py` with custom endpoints
3. **Enhance UI** - Customize `src/ui/app.py` with your branding
4. **Integrate Tools** - Add custom tools in `src/tools/`
5. **Add Tests** - Create tests in `tests/`
6. **Deploy** - Use Docker or your preferred hosting platform

## 📝 Notes

- Always use Python 3.10+
- Keep virtual environment activated during development
- Update dependencies regularly: `pip install --upgrade -r requirements.txt`
- Store secrets in .env, never commit to version control
- Use `ANTHROPIC_API_KEY` from [console.anthropic.com](https://console.anthropic.com)

## ✅ Verification

Run this to verify all packages are installed:

```bash
python3 -c "
packages = ['fastapi', 'streamlit', 'langchain', 'langgraph', 'anthropic', 'mcp']
for pkg in packages:
    try:
        __import__(pkg.replace('-', '_'))
        print(f'✓ {pkg}')
    except ImportError:
        print(f'✗ {pkg} - NOT INSTALLED')
"
```

## 📞 Support

For detailed setup instructions, see [SETUP.md](SETUP.md)

For issues or questions about this project, check the troubleshooting section or review the included documentation.

---

**Created**: 2026-05-21  
**Status**: Ready for Development  
**Python**: 3.10+  
**Framework**: FastAPI + Streamlit + LangChain + Anthropic Claude
