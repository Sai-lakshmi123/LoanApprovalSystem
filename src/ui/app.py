"""
Streamlit UI for multi-agent AI system
"""
import streamlit as st
import requests
import json
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_endpoint = st.text_input(
        "API Endpoint",
        value="http://localhost:8000",
        help="FastAPI server endpoint"
    )
    agent_type = st.selectbox(
        "Select Agent Type",
        ["default", "loan_processor", "approval_agent", "supervisor"]
    )

# Main title
st.title("🤖 Multi-Agent AI System")
st.subheader("Intelligent Multi-Agent Processing Interface")

# Tabs
tab1, tab2, tab3 = st.tabs(["Process", "Agent Status", "Documentation"])

# Tab 1: Processing
with tab1:
    st.header("Process Input")

    col1, col2 = st.columns([2, 1])

    with col1:
        user_input = st.text_area(
            "Enter input for processing:",
            placeholder="Enter your request here...",
            height=150,
            key="user_input"
        )

    with col2:
        st.write("### Advanced Options")
        include_metadata = st.checkbox("Include metadata", value=True)

        if include_metadata:
            metadata_input = st.text_area(
                "Metadata (JSON):",
                value='{"source": "UI", "timestamp": "now"}',
                height=100
            )
        else:
            metadata_input = None

    if st.button("Process Request", type="primary", use_container_width=True):
        if not user_input.strip():
            st.error("Please enter input to process")
        else:
            try:
                # Parse metadata if provided
                metadata = None
                if metadata_input:
                    try:
                        metadata = json.loads(metadata_input)
                    except json.JSONDecodeError:
                        st.warning("Invalid JSON in metadata, skipping...")

                # Make API request
                with st.spinner("Processing..."):
                    response = requests.post(
                        f"{api_endpoint}/process",
                        json={
                            "input_data": user_input,
                            "agent_type": agent_type,
                            "metadata": metadata
                        },
                        timeout=30
                    )

                if response.status_code == 200:
                    result = response.json()
                    st.success("Processing completed!")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("### Result")
                        st.write(result.get("result", "No result"))

                    with col2:
                        if result.get("metadata"):
                            st.write("### Metadata")
                            st.json(result["metadata"])

                else:
                    st.error(f"API Error: {response.status_code}")
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to API at {api_endpoint}")
                st.info("Make sure the FastAPI server is running:")
                st.code("uvicorn src.api.main:app --reload")
            except requests.exceptions.Timeout:
                st.error("Request timeout. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tab 2: Agent Status
with tab2:
    st.header("Agent Status")

    if st.button("Refresh Status", use_container_width=True):
        try:
            with st.spinner("Fetching agent status..."):
                response = requests.get(
                    f"{api_endpoint}/agents",
                    timeout=10
                )

            if response.status_code == 200:
                agents_data = response.json()
                st.success("Agents available!")

                # Create columns for agents
                cols = st.columns(len(agents_data.get("agents", [])))

                for idx, agent in enumerate(agents_data.get("agents", [])):
                    with cols[idx]:
                        status_color = "🟢" if agent.get("status") == "active" else "🔴"
                        st.metric(
                            f"**{status_color} {agent['name']}**",
                            agent.get("status", "unknown").upper()
                        )
            else:
                st.error(f"Error fetching agent status: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to API at {api_endpoint}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Health check
    st.write("### System Health")
    if st.button("Check System Health", use_container_width=True):
        try:
            response = requests.get(f"{api_endpoint}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                st.success(f"✓ System Status: {health.get('status', 'unknown')}")
            else:
                st.error("System health check failed")
        except Exception as e:
            st.error(f"Health check failed: {str(e)}")

# Tab 3: Documentation
with tab3:
    st.header("Documentation")

    st.write("""
    ### About This System

    This is a multi-agent AI system built with:
    - **FastAPI** - High-performance API framework
    - **Streamlit** - Interactive UI
    - **LangChain & LangGraph** - Agent orchestration
    - **Anthropic Claude** - Language model backbone

    ### Features

    - 🤖 Multi-agent processing
    - 📊 Real-time status monitoring
    - 🔗 API integration
    - 📝 Metadata support
    - 🎨 User-friendly interface

    ### Quick Start

    1. **Start the API Server:**
       ```bash
       source venv/bin/activate
       uvicorn src.api.main:app --reload
       ```

    2. **Run the Streamlit App:**
       ```bash
       streamlit run src/ui/app.py
       ```

    3. **Use the Interface:**
       - Enter your input in the Process tab
       - View agent status in the Agent Status tab
       - Configure API endpoint in the sidebar

    ### API Endpoints

    - `GET /health` - System health check
    - `GET /agents` - List available agents
    - `POST /process` - Process input through agents
    - `GET /docs` - Interactive API documentation

    ### Configuration

    Edit `.env` file to configure:
    - `ANTHROPIC_API_KEY` - Your Claude API key
    - `FASTAPI_HOST` - API host (default: 0.0.0.0)
    - `FASTAPI_PORT` - API port (default: 8000)

    ### Support

    For issues or questions, see `SETUP.md` for detailed documentation.
    """)

    st.divider()
    st.info("💡 Tip: Check the API documentation at http://localhost:8000/docs")
