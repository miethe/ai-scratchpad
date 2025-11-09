#!/bin/bash
# Development server startup script for Knit-Wit API

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Knit-Wit API Development Server${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    uv venv
    echo ""
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/installed" ]; then
    echo -e "${GREEN}Installing dependencies...${NC}"
    uv pip install -e ".[dev]"
    touch .venv/installed
    echo ""
fi

# Create .env from .env.example if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${GREEN}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo ""
fi

# Start the server with hot-reload
echo -e "${GREEN}Starting FastAPI server with hot-reload...${NC}"
echo -e "${BLUE}API Documentation: http://localhost:8000/docs${NC}"
echo -e "${BLUE}Health Check: http://localhost:8000/health${NC}"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
