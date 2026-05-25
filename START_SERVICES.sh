#!/bin/bash

# ============================================================================
# Loan Approval System - Service Startup Script
# ============================================================================

set -e

PROJECT_DIR="/home/ubuntu/Desktop/LoanApprovalSystem/LoanApprovalSystem"
cd "$PROJECT_DIR"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}============================================================================${NC}"
echo -e "${YELLOW}  LOAN APPROVAL SYSTEM - Starting Services${NC}"
echo -e "${YELLOW}============================================================================${NC}"

# Activate virtual environment
echo -e "\n${GREEN}[1/4]${NC} Activating Python virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Stop any existing processes
echo -e "\n${GREEN}[2/4]${NC} Stopping any existing services..."
pkill -f "python3 src/api" 2>/dev/null || true
pkill -f "streamlit" 2>/dev/null || true
sleep 2
echo -e "${GREEN}✓ Existing services stopped${NC}"

# Start FastAPI
echo -e "\n${GREEN}[3/4]${NC} Starting FastAPI server on port 8000..."
nohup python3 src/api/main.py > /tmp/fastapi_server.log 2>&1 &
API_PID=$!
echo -e "${GREEN}✓ FastAPI starting (PID: $API_PID)${NC}"

# Wait for API to be ready
echo -e "\n${YELLOW}   Waiting for API to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API is ready!${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Verify API
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${RED}✗ API failed to start!${NC}"
    echo "Check logs: tail -50 /tmp/fastapi_server.log"
    exit 1
fi

# Start Streamlit
echo -e "\n${GREEN}[4/4]${NC} Starting Streamlit UI on port 8501..."
nohup streamlit run src/ui/streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --client.showErrorDetails=true \
    > /tmp/streamlit_server.log 2>&1 &
STREAMLIT_PID=$!
echo -e "${GREEN}✓ Streamlit starting (PID: $STREAMLIT_PID)${NC}"

sleep 3

# Final verification
echo -e "\n${YELLOW}============================================================================${NC}"
echo -e "${YELLOW}  SERVICE STATUS${NC}"
echo -e "${YELLOW}============================================================================${NC}"

echo -e "\n${GREEN}FastAPI API Server:${NC}"
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "  ✅ Status: RUNNING"
    echo -e "  📍 URL: http://localhost:8000"
    echo -e "  📋 Docs: http://localhost:8000/docs"
else
    echo -e "  ❌ Status: NOT RESPONDING"
fi

echo -e "\n${GREEN}Streamlit UI:${NC}"
if curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo -e "  ✅ Status: RUNNING"
    echo -e "  🌐 URL: http://localhost:8501"
else
    echo -e "  ⏳ Status: STARTING (wait a moment)"
    echo -e "  🌐 URL: http://localhost:8501"
fi

echo -e "\n${YELLOW}============================================================================${NC}"
echo -e "${GREEN}✓ All services started successfully!${NC}"
echo -e "${YELLOW}============================================================================${NC}"

echo -e "\n${GREEN}📝 Log Files:${NC}"
echo -e "  FastAPI:  tail -f /tmp/fastapi_server.log"
echo -e "  Streamlit: tail -f /tmp/streamlit_server.log"

echo -e "\n${GREEN}🌐 Open in Browser:${NC}"
echo -e "  http://localhost:8501  (Loan Application UI)"
echo -e "  http://localhost:8000/docs  (API Documentation)"

echo -e "\n${GREEN}⏹️  To Stop Services:${NC}"
echo -e "  bash STOP_SERVICES.sh"
echo ""
