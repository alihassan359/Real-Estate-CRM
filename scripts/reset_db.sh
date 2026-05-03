#!/bin/bash
# Database Reset Script for Linux/Mac
# Clears and reinitializes the database

DATABASE_URL="postgresql://postgres.shnbijxwgcfdwikzmigv:u24yVpQRWwEX2167@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

echo "========================================"
echo "Database Reset Script"
echo "========================================"
echo ""
echo "⚠️  WARNING: This will DELETE ALL DATA in the database!"
echo "Database URL: ${DATABASE_URL:0:50}..."
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    echo "Proceeding with database reset..."
    echo ""
    
    # Set environment variable and run script
    export DATABASE_URL="$DATABASE_URL"
    
    # Run the Python reset script
    python scripts/reset_db.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "========================================"
        echo "✓ Database reset completed successfully!"
        echo "========================================"
    else
        echo "✗ Database reset failed!"
    fi
else
    echo "Reset cancelled."
fi
