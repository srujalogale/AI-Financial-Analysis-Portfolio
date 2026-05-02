#!/bin/bash

# Define colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting AI Portfolio Navigator...${NC}"

# Start Backend
echo -e "${GREEN}Starting FastAPI backend on port 8000...${NC}"
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r ../requirements.txt > /dev/null 2>&1
uvicorn main:app --port 8000 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo -e "${GREEN}Starting Vite frontend...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install > /dev/null 2>&1
fi
npm run dev &
FRONTEND_PID=$!
cd ..

# Handle shutdown
trap "echo -e '\n${BLUE}Shutting down services...${NC}'; kill $BACKEND_PID; kill $FRONTEND_PID; exit" SIGINT SIGTERM

echo -e "${BLUE}Both services are running. Press Ctrl+C to stop.${NC}"

# Wait for background processes
wait
