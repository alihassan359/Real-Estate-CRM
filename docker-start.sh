#!/bin/bash

# Docker Quick Start Script for Real Estate CRM (Linux/Mac)
# Usage: bash docker-start.sh

echo "========================================"
echo "Real Estate CRM - Docker Quick Start"
echo "========================================"
echo ""

# Check if Docker is installed
echo "✓ Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found! Please install Docker Desktop"
    exit 1
fi

DOCKER_VERSION=$(docker --version)
echo "✓ Docker found: $DOCKER_VERSION"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker Compose not found! Please install Docker Compose"
    exit 1
fi

# Check if .env file exists
echo "✓ Checking .env configuration..."
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "⚠ .env file not found. Creating from .env.docker..."
    if [ -f ".env.docker" ]; then
        cp ".env.docker" ".env"
        echo "✓ .env created. Please update with your Google OAuth credentials!"
        echo "  Edit .env and add:"
        echo "  - GOOGLE_CLIENT_ID"
        echo "  - GOOGLE_CLIENT_SECRET"
        echo ""
    else
        echo "✗ .env.docker template not found!"
        exit 1
    fi
fi

# Prompt to update .env if needed
echo ""
echo "Do you want to:"
echo "1. Start Docker (proceed with current .env)"
echo "2. Edit .env file first"
echo "3. Exit"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        ;;
    2)
        echo "Opening .env in editor..."
        ${EDITOR:-nano} ".env"
        echo ""
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

# Stop existing containers (optional)
echo ""
echo "Checking for existing containers..."
if docker-compose ps -q | grep -q .; then
    echo "Found existing containers. Stopping..."
    docker-compose stop
    echo "✓ Existing containers stopped"
fi

# Build Docker image
echo ""
echo "Building Docker image..."
docker-compose build
if [ $? -ne 0 ]; then
    echo "✗ Docker build failed!"
    exit 1
fi
echo "✓ Docker image built successfully"

# Start services
echo ""
echo "Starting services (PostgreSQL, Redis, FastAPI)..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "✗ Failed to start Docker services!"
    exit 1
fi
echo "✓ Docker services started"

# Wait for services to be healthy
echo ""
echo "Waiting for services to be healthy..."
sleep 5

# Test PostgreSQL
echo "Testing PostgreSQL..."
if docker-compose exec -T postgres pg_isready -U postgres &> /dev/null; then
    echo "✓ PostgreSQL is healthy"
else
    echo "⚠ PostgreSQL test inconclusive (may still be starting)"
fi

# Test Redis
echo "Testing Redis..."
REDIS_TEST=$(docker-compose exec -T redis redis-cli ping)
if [ "$REDIS_TEST" = "PONG" ]; then
    echo "✓ Redis is healthy"
else
    echo "⚠ Redis test inconclusive (may still be starting)"
fi

# Test API
echo ""
echo "Testing FastAPI health endpoint..."
sleep 3
if command -v curl &> /dev/null; then
    RESPONSE=$(curl -s http://localhost:8000/api/auth/health)
    if echo "$RESPONSE" | grep -q "healthy"; then
        echo "✓ FastAPI API is healthy!"
        echo ""
        echo "API Response:"
        echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
    else
        echo "⚠ API health check failed (may still be starting)"
        echo "Check logs with: docker-compose logs api"
    fi
else
    echo "⚠ curl not found, skipping health check"
fi

# Run migrations
echo ""
echo "Running database migrations..."
docker-compose exec -T api alembic upgrade head
if [ $? -eq 0 ]; then
    echo "✓ Database migrations completed"
else
    echo "⚠ Migrations may have had issues (check logs)"
fi

# Display summary
echo ""
echo "========================================"
echo "Docker Setup Complete!"
echo "========================================"
echo ""
echo "Services running:"
echo "✓ PostgreSQL      - localhost:5432"
echo "✓ Redis           - localhost:6379"
echo "✓ FastAPI API     - http://localhost:8000"
echo ""
echo "Quick Test Commands:"
echo "  curl http://localhost:8000/api/auth/health"
echo "  docker-compose logs -f api"
echo "  docker-compose ps"
echo ""
echo "Useful Commands:"
echo "  Stop all:     docker-compose stop"
echo "  Start all:    docker-compose up -d"
echo "  View logs:    docker-compose logs -f"
echo "  DB shell:     docker-compose exec postgres psql -U postgres"
echo ""
echo "Next Steps:"
echo "1. Update .env with Google OAuth credentials:"
echo "   - GOOGLE_CLIENT_ID"
echo "   - GOOGLE_CLIENT_SECRET"
echo "2. Then restart API: docker-compose restart api"
echo "3. Set up frontend at http://localhost:3000"
echo ""
echo "Ready to test! 🚀"
