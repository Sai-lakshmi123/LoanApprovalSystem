# Python Development Environment Setup

## Prerequisites

Ensure you have Python 3.10 or higher installed:

```bash
python3 --version
# Should output Python 3.10+ or Python 3.11+
```

If you need to install Python:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# macOS (using Homebrew)
brew install python@3.11
```

---

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to project directory
cd /path/to/LoanApprovalSystem

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal after activation.

### 2. Upgrade pip and setuptools

```bash
pip install --upgrade pip setuptools wheel
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The installation will include:
- **FastAPI** - Modern web framework for building APIs
- **Streamlit** - UI framework for data apps
- **LangChain** - Framework for developing apps with language models
- **LangGraph** - Tool for building stateful, multi-actor applications
- **Anthropic SDK** - Official SDK for Claude API
- **FastMCP** - FastAPI integration for Model Context Protocol
- **Uvicorn** - ASGI server for running FastAPI apps
- Supporting libraries (numpy, pandas, requests, etc.)

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following variables:

```
# Anthropic API
ANTHROPIC_API_KEY=your_api_key_here

# FastAPI
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Streamlit
STREAMLIT_LOGGER_LEVEL=info

# Development
ENVIRONMENT=development
DEBUG=True
```

**Important**: Get your API key from [console.anthropic.com](https://console.anthropic.com)

### 5. Verify Installation

Run the verification script to check all components are installed:

```bash
python3 -c "
import sys
print(f'Python: {sys.version}')
print('Checking packages...')

packages = ['fastapi', 'streamlit', 'langchain', 'langgraph', 'anthropic', 'mcp', 'fastmcp']
for pkg in packages:
    try:
        __import__(pkg.replace('-', '_'))
        print(f'✓ {pkg}')
    except ImportError:
        print(f'✗ {pkg} - NOT INSTALLED')
"
```

---

## Project Structure

Recommended directory layout:

```
LoanApprovalSystem/
├── venv/                      # Virtual environment
├── src/
│   ├── agents/               # Multi-agent definitions
│   │   ├── __init__.py
│   │   ├── loan_agent.py    # Agent for loan processing
│   │   ├── approval_agent.py # Agent for approval logic
│   │   └── supervisor.py     # Supervisor/coordinator agent
│   ├── tools/                # LangChain tools
│   │   ├── __init__.py
│   │   └── mcp_tools.py
│   ├── api/                  # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes.py
│   ├── ui/                   # Streamlit application
│   │   ├── __init__.py
│   │   └── app.py
│   └── config.py            # Configuration management
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_api.py
├── .env                      # Environment variables (DO NOT commit)
├── .env.example              # Template for .env
├── requirements.txt          # Python dependencies
├── SETUP.md                  # This file
└── README.md                 # Project documentation
```

---

## Quick Start

### Run FastAPI Server

```bash
# From project root with venv activated
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

### Run Streamlit App

```bash
# From project root with venv activated
streamlit run src/ui/app.py
```

Visit `http://localhost:8501` in your browser.

### Run LangGraph Agent

```python
from src.agents.supervisor import create_agent_network
from langgraph.graph import StateGraph

# Create and run agent network
graph = create_agent_network()
result = graph.invoke({"messages": "Process loan application"})
```

---

## Example: Simple Multi-Agent System

Create `src/agents/supervisor.py`:

```python
from langchain.chat_models import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from typing import Annotated
import operator

class AgentState:
    messages: Annotated[list, operator.add]

def create_agent_network():
    model = ChatAnthropic(model="claude-opus-4-1-20250805")
    
    def loan_processor(state):
        response = model.invoke([{"role": "user", "content": "Process loan application"}])
        return {"messages": [response]}
    
    def approval_agent(state):
        response = model.invoke([{"role": "user", "content": "Approve or reject based on criteria"}])
        return {"messages": [response]}
    
    graph = StateGraph(AgentState)
    graph.add_node("loan_processor", loan_processor)
    graph.add_node("approval_agent", approval_agent)
    graph.add_edge(START, "loan_processor")
    graph.add_edge("loan_processor", "approval_agent")
    graph.add_edge("approval_agent", END)
    
    return graph.compile()
```

---

## Troubleshooting

### "ModuleNotFoundError" for installed packages
- Ensure virtual environment is activated: `source venv/bin/activate`
- Reinstall with: `pip install -r requirements.txt --force-reinstall`

### API Key Issues
- Verify ANTHROPIC_API_KEY is set: `echo $ANTHROPIC_API_KEY`
- If empty, update `.env` file and reload shell

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn src.api.main:app --port 8001
```

### Dependency Conflicts
- Update all packages: `pip install --upgrade -r requirements.txt`
- Or use specific versions from requirements.txt lock file

---

## Development Tips

1. **Use Python 3.11+** for better performance
2. **Enable code reloading** with `uvicorn --reload` for development
3. **Use debugger**: Add `import ipdb; ipdb.set_trace()` in code
4. **Check API docs**: FastAPI auto-generates OpenAPI docs at `/docs`
5. **Monitor logs**: Use `python-json-logger` for structured logging
6. **Test agents**: Write unit tests in `tests/` before deploying

---

## Updating Dependencies

To check for outdated packages:

```bash
pip list --outdated
```

To update a specific package:

```bash
pip install --upgrade package_name
```

To regenerate requirements.txt:

```bash
pip freeze > requirements.txt
```

---

## Deactivating Virtual Environment

When done working:

```bash
deactivate
```

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Anthropic SDK Documentation](https://github.com/anthropics/anthropic-sdk-python)
- [MCP Documentation](https://modelcontextprotocol.io/)
