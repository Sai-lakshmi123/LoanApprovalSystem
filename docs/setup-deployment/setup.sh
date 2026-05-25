#!/bin/bash
# Multi-Agent AI System Setup Script

set -e  # Exit on error

echo "=========================================="
echo "Multi-Agent AI System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python installation..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Extract major and minor version
major=$(echo $python_version | cut -d. -f1)
minor=$(echo $python_version | cut -d. -f2)

if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 10 ]); then
    echo "   ✗ Python 3.10+ required"
    exit 1
fi
echo "   ✓ Python version is compatible"
echo ""

# Create virtual environment
echo "2. Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo "   ℹ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "3. Activating virtual environment..."
source venv/bin/activate
echo "   ✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "4. Upgrading pip and setuptools..."
pip install --quiet --upgrade pip setuptools wheel
echo "   ✓ pip and setuptools updated"
echo ""

# Install requirements
echo "5. Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "   ✓ All dependencies installed"
echo ""

# Create .env file if it doesn't exist
echo "6. Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "   ✓ Created .env file from .env.example"
    echo "   ⚠ Please edit .env and add your ANTHROPIC_API_KEY"
else
    echo "   ℹ .env file already exists"
fi
echo ""

# Create project directories
echo "7. Creating project structure..."
mkdir -p src/agents src/tools src/api src/ui tests
touch src/__init__.py
touch src/agents/__init__.py
touch src/tools/__init__.py
touch src/api/__init__.py
touch src/ui/__init__.py
echo "   ✓ Project directories created"
echo ""

# Verify installation
echo "8. Verifying installation..."
python3 << 'EOF'
import sys
failed = False

packages = {
    'fastapi': 'FastAPI',
    'streamlit': 'Streamlit',
    'langchain': 'LangChain',
    'langgraph': 'LangGraph',
    'anthropic': 'Anthropic SDK',
    'mcp': 'MCP',
}

for import_name, display_name in packages.items():
    try:
        __import__(import_name.replace('-', '_'))
        print(f"   ✓ {display_name}")
    except ImportError as e:
        print(f"   ✗ {display_name}: {e}")
        failed = True

if failed:
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo "   ✓ All packages verified"
else
    echo "   ✗ Some packages failed verification"
    exit 1
fi
echo ""

echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY:"
echo "   nano .env"
echo ""
echo "2. Start FastAPI server:"
echo "   uvicorn src.api.main:app --reload"
echo ""
echo "3. Or run Streamlit app (in another terminal):"
echo "   streamlit run src/ui/app.py"
echo ""
echo "For more information, see SETUP.md"
echo ""
