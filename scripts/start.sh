#!/usr/bin/env bash
# Real Estate CRM - Docker Startup Script (Linux/Mac)

set -e

echo "🚀 Real Estate CRM - Docker Setup"
echo "=================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose found${NC}"

# Create .env if not exists
if [ ! -f .env.development ]; then
    echo -e "${YELLOW}⚠️  .env.development not found, copying from .env.example${NC}"
    cp .env.example .env.development
fi

# Create logs directory
mkdir -p logs

# Pull latest images
echo -e "${YELLOW}📥 Pulling latest images...${NC}"
docker-compose pull

# Build images
echo -e "${YELLOW}🔨 Building images...${NC}"
docker-compose build

# Start services
echo -e "${YELLOW}🚀 Starting services...${NC}"
docker-compose up -d

# Wait for services to be healthy
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 5

# Check health
echo -e "\n${GREEN}✅ Services started!${NC}\n"

# Check API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API is running${NC}"
    echo "   📍 API: http://localhost:8000"
    echo "   📍 Docs: http://localhost:8000/docs"
else
    echo -e "${RED}❌ API is not responding${NC}"
fi

# Check Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
    echo "   📍 Frontend: http://localhost:3000"
else
    echo -e "${RED}❌ Frontend is not responding${NC}"
fi

echo -e "\n${GREEN}=================================="
echo "📊 Real Estate CRM is ready!"
echo "🌐 Open http://localhost:3000 in your browser"
echo "==================================${NC}\n"

# Show logs
echo -e "${YELLOW}Showing logs (Ctrl+C to exit):${NC}"
docker-compose logs -f
