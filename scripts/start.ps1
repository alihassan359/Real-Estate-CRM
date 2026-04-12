# Real Estate CRM - Docker Startup Script (Windows PowerShell)

Write-Host "🚀 Real Estate CRM - Docker Setup" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check Docker
Write-Host "`n📦 Checking Docker installation..." -ForegroundColor Yellow
$dockerCheck = docker --version 2>&1
$composeCheck = docker-compose --version 2>&1

if ($dockerCheck -like "*error*" -or $null -eq $dockerCheck) {
    Write-Host "❌ Docker is not installed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker found: $dockerCheck" -ForegroundColor Green
Write-Host "✅ Docker Compose found: $composeCheck" -ForegroundColor Green

# Create .env if not exists
if (-not (Test-Path ".env.development")) {
    Write-Host "`n⚠️  .env.development not found, copying from .env.example" -ForegroundColor Yellow
    Copy-Item ".env.example" ".env.development"
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Build and start services
Write-Host "`n🔨 Building and starting services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "`n⏳ Waiting 10 seconds for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check API health
Write-Host "`n🔍 Checking service status..." -ForegroundColor Yellow

try {
    $apiHealth = Invoke-RestMethod -Uri "http://localhost:8000/health" -ErrorAction Stop
    Write-Host "✅ API is running at http://localhost:8000" -ForegroundColor Green
    Write-Host "   📖 API Documentation: http://localhost:8000/docs" -ForegroundColor Green
} catch {
    Write-Host "⚠️  API is starting... please wait a moment" -ForegroundColor Yellow
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -ErrorAction Stop
    Write-Host "✅ Frontend is running at http://localhost:3000" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend is starting... please wait a moment" -ForegroundColor Yellow
}

# Display services
Write-Host "`n==================================" -ForegroundColor Green
Write-Host "📊 Services Started!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔌 API:       http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 Docs:      http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "💾 Database:  localhost:5432" -ForegroundColor Cyan
Write-Host "⚡ Redis:     localhost:6379" -ForegroundColor Cyan
Write-Host ""

# Show containers
Write-Host "📦 Running Containers:" -ForegroundColor Yellow
docker-compose ps

Write-Host "`n💡 Useful Commands:" -ForegroundColor Yellow
Write-Host "  View logs:        docker-compose logs -f" -ForegroundColor Gray
Write-Host "  View API logs:    docker-compose logs -f api" -ForegroundColor Gray
Write-Host "  Stop services:    docker-compose down" -ForegroundColor Gray
Write-Host "  Restart services: docker-compose restart" -ForegroundColor Gray
Write-Host ""
Write-Host "✨ Ready! Open http://localhost:3000 in your browser" -ForegroundColor Green
