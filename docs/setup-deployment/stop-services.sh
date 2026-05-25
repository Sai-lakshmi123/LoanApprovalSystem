#!/bin/bash

# ============================================================================
# Loan Approval System - Service Shutdown Script
# ============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}============================================================================${NC}"
echo -e "${YELLOW}  LOAN APPROVAL SYSTEM - Stopping Services${NC}"
echo -e "${YELLOW}============================================================================${NC}"

echo -e "\n${RED}[1/2]${NC} Stopping FastAPI server..."
pkill -f "python3 src/api" 2>/dev/null || echo "  (not running)"
sleep 1
echo -e "${GREEN}✓ FastAPI stopped${NC}"

echo -e "\n${RED}[2/2]${NC} Stopping Streamlit UI..."
pkill -f "streamlit" 2>/dev/null || echo "  (not running)"
sleep 1
echo -e "${GREEN}✓ Streamlit stopped${NC}"

echo -e "\n${YELLOW}============================================================================${NC}"
echo -e "${GREEN}✓ All services stopped${NC}"
echo -e "${YELLOW}============================================================================${NC}"

echo -e "\n${GREEN}To start services again:${NC}"
echo -e "  bash START_SERVICES.sh"
echo ""
