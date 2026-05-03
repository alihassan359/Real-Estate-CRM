# Database Reset Script for Windows
# Clears and reinitializes the database

$DatabaseUrl = "postgresql://postgres.shnbijxwgcfdwikzmigv:u24yVpQRWwEX2167@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Database Reset Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "WARNING: This will DELETE ALL DATA in the database!" -ForegroundColor Red
Write-Host "Database URL: $($DatabaseUrl.Substring(0, 50))..." -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Are you sure you want to continue? (yes/no)"

if ($confirm -eq "yes") {
    Write-Host "Proceeding with database reset..." -ForegroundColor Green
    Write-Host ""
    
    # Set environment variable and run script
    $env:DATABASE_URL = $DatabaseUrl
    
    # Run the Python reset script
    python scripts/reset_db.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "✓ Database reset completed successfully!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
    } else {
        Write-Host "✗ Database reset failed!" -ForegroundColor Red
    }
} else {
    Write-Host "Reset cancelled." -ForegroundColor Yellow
}
