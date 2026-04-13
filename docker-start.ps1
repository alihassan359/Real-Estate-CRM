# Docker Quick Start Script for Real Estate CRM
# 
# This script automates Docker setup and startup
# Usage: .\docker-start.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Real Estate CRM - Docker Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "✓ Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found! Please install Docker Desktop" -ForegroundColor Red
    exit 1
}

# Check if .env file exists
Write-Host "✓ Checking .env configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠ .env file not found. Creating from .env.docker..." -ForegroundColor Yellow
    if (Test-Path ".env.docker") {
        Copy-Item ".env.docker" ".env"
        Write-Host "✓ .env created. Please update with your Google OAuth credentials!" -ForegroundColor Yellow
        Write-Host "  Edit .env and add:" -ForegroundColor Yellow
        Write-Host "  - GOOGLE_CLIENT_ID" -ForegroundColor Yellow
        Write-Host "  - GOOGLE_CLIENT_SECRET" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow
    } else {
        Write-Host "✗ .env.docker template not found!" -ForegroundColor Red
        exit 1
    }
}

# Prompt to update .env if needed
Write-Host ""
Write-Host "Do you want to:" -ForegroundColor Cyan
Write-Host "1. Start Docker (proceed with current .env)" -ForegroundColor Cyan
Write-Host "2. Edit .env file first" -ForegroundColor Cyan
Write-Host "3. Exit" -ForegroundColor Cyan
$choice = Read-Host "Enter choice (1-3)"

if ($choice -eq "2") {
    Write-Host "Opening .env in Notepad..." -ForegroundColor Yellow
    notepad ".env"
    Write-Host ""
} elseif ($choice -eq "3") {
    Write-Host "Exiting..." -ForegroundColor Yellow
    exit 0
}

# Stop existing containers (optional)
Write-Host ""
Write-Host "Checking for existing containers..." -ForegroundColor Yellow
$existingContainers = docker-compose ps -q
if ($existingContainers) {
    Write-Host "Found existing containers. Stopping..." -ForegroundColor Yellow
    docker-compose stop
    Write-Host "✓ Existing containers stopped" -ForegroundColor Green
}

# Build Docker image
Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker-compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Docker build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Docker image built successfully" -ForegroundColor Green

# Start services
Write-Host ""
Write-Host "Starting services (PostgreSQL, Redis, FastAPI)..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start Docker services!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Docker services started" -ForegroundColor Green

# Wait for services to be healthy
Write-Host ""
Write-Host "Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test PostgreSQL
Write-Host "Testing PostgreSQL..." -ForegroundColor Yellow
$pgTest = docker-compose exec -T postgres pg_isready -U postgres
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PostgreSQL is healthy" -ForegroundColor Green
} else {
    Write-Host "⚠ PostgreSQL test inconclusive (may still be starting)" -ForegroundColor Yellow
}

# Test Redis
Write-Host "Testing Redis..." -ForegroundColor Yellow
$redisTest = docker-compose exec -T redis redis-cli ping
if ($redisTest -eq "PONG") {
    Write-Host "✓ Redis is healthy" -ForegroundColor Green
} else {
    Write-Host "⚠ Redis test inconclusive (may still be starting)" -ForegroundColor Yellow
}

# Test API
Write-Host ""
Write-Host "Testing FastAPI health endpoint..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ FastAPI API is healthy!" -ForegroundColor Green
        Write-Host ""
        Write-Host "API Response:" -ForegroundColor Cyan
        Write-Host $response.Content -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ API health check failed (may still be starting)" -ForegroundColor Yellow
    Write-Host "Check logs with: docker-compose logs api" -ForegroundColor Yellow
}

# Run migrations
Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Yellow
docker-compose exec -T api alembic upgrade head
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database migrations completed" -ForegroundColor Green
} else {
    Write-Host "⚠ Migrations may have had issues (check logs)" -ForegroundColor Yellow
}

# Display summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Docker Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services running:" -ForegroundColor Cyan
Write-Host "✓ PostgreSQL      - localhost:5432" -ForegroundColor Green
Write-Host "✓ Redis           - localhost:6379" -ForegroundColor Green
Write-Host "✓ FastAPI API     - http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Quick Test Commands:" -ForegroundColor Cyan
Write-Host "  curl http://localhost:8000/api/auth/health" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f api" -ForegroundColor Yellow
Write-Host "  docker-compose ps" -ForegroundColor Yellow
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  Stop all:     docker-compose stop" -ForegroundColor Yellow
Write-Host "  Start all:    docker-compose up -d" -ForegroundColor Yellow
Write-Host "  View logs:    docker-compose logs -f" -ForegroundColor Yellow
Write-Host "  DB shell:     docker-compose exec postgres psql -U postgres" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update .env with Google OAuth credentials:" -ForegroundColor Yellow
Write-Host "   - GOOGLE_CLIENT_ID" -ForegroundColor Yellow
Write-Host "   - GOOGLE_CLIENT_SECRET" -ForegroundColor Yellow
Write-Host "2. Then restart API: docker-compose restart api" -ForegroundColor Yellow
Write-Host "3. Set up frontend at http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ready to test! 🚀" -ForegroundColor Green
