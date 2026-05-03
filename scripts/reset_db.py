#!/usr/bin/env python3
"""
Database Reset Script
Completely clears the database and reinitializes all tables
"""

import os
import sys
from pathlib import Path

# Add src to path - handle running from different directories
script_dir = Path(__file__).parent
project_root = script_dir.parent
src_dir = project_root / "src"

# Ensure src is in the path
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Change to project root
os.chdir(project_root)

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.tenant import Tenant
from models.user import User
from models.user_mfa import UserMFA
from models.refresh_token import RefreshToken
import models  # noqa: F401 - Import all models to register them

# Database URL from environment or provided as argument
DB_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres.shnbijxwgcfdwikzmigv:u24yVpQRWwEX2167@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres'
)

# Convert async URL to sync if needed
if 'asyncpg' in DB_URL:
    DB_URL = DB_URL.replace('postgresql+asyncpg://', 'postgresql://')


def drop_all_tables_and_types(engine):
    """Drop all tables and custom types"""
    with engine.connect() as conn:
        # Get all table names
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"Found {len(tables)} tables to drop")
        
        # Drop all tables with CASCADE to handle foreign keys
        for table in tables:
            print(f"Dropping table: {table}")
            conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
        
        # Drop all custom ENUM types
        result = conn.execute(
            text("""
            SELECT t.typname
            FROM pg_type t
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            WHERE (t.typrelid = 0 OR (SELECT c.relkind = 'c' FROM pg_catalog.pg_class c WHERE c.oid = t.typrelid))
            AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_type el WHERE el.oid = t.typelem)
            AND n.nspname NOT IN ('pg_catalog', 'information_schema')
            AND t.typtype = 'e'
            """)
        )
        
        enum_types = [row[0] for row in result]
        print(f"Found {len(enum_types)} ENUM types to drop")
        
        for enum_type in enum_types:
            print(f"Dropping ENUM type: {enum_type}")
            conn.execute(text(f"DROP TYPE IF EXISTS {enum_type} CASCADE"))
        
        conn.commit()
    
    print("✓ All tables and types dropped successfully")


def create_all_tables(engine):
    """Create all tables using SQLAlchemy metadata"""
    print("\nCreating tables...")
    Base.metadata.create_all(
        bind=engine,
        tables=[Tenant.__table__, User.__table__, UserMFA.__table__, RefreshToken.__table__],
        checkfirst=False
    )
    print("✓ All tables created successfully")


def main():
    """Main function"""
    print("=" * 60)
    print("DATABASE RESET SCRIPT")
    print("=" * 60)
    print(f"\nDatabase URL: {DB_URL[:50]}...")
    
    try:
        # Create engine
        engine = create_engine(DB_URL, echo=False)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Connected to database successfully\n")
        
        # Drop all tables and types
        drop_all_tables_and_types(engine)
        
        # Create all tables
        create_all_tables(engine)
        
        print("\n" + "=" * 60)
        print("✓ DATABASE RESET COMPLETE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
