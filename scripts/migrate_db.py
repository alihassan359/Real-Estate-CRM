"""
Database Migration Script - Create tables for authentication system
Run this script to initialize the database with required tables.
"""

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import settings
from models.base import Base
from models.user import User, UserRole, UserStatus
from models.tenant import Tenant, SubscriptionPlan, TenantStatus


async def create_tables():
    """Create all tables in the database"""
    
    # Create engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )
    
    async with engine.begin() as conn:
        # Create UUID extension if not exists
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        
        # Create PostgreSQL enum types for SQLAlchemy models
        await conn.execute(text('CREATE TYPE subscription_plan AS ENUM (\'FREE\', \'BASIC\', \'PRO\', \'ENTERPRISE\')'))
        await conn.execute(text('CREATE TYPE tenant_status AS ENUM (\'ACTIVE\', \'INACTIVE\', \'SUSPENDED\')'))
        await conn.execute(text('CREATE TYPE user_role AS ENUM (\'SUPER_ADMIN\', \'PLATFORM_ADMIN\', \'TENANT_OWNER\', \'MANAGER\', \'OPERATOR\', \'ACCOUNTANT\', \'SALESMAN\')'))
        await conn.execute(text('CREATE TYPE user_status AS ENUM (\'ACTIVE\', \'INACTIVE\', \'SUSPENDED\')'))
        
        # Create all tables from models
        await conn.run_sync(Base.metadata.create_all)
        
        print("✅ All tables created successfully!")
    
    await engine.dispose()


async def drop_tables():
    """Drop all tables from the database (use with caution!)"""
    
    # Create engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )
    
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        
        # Drop enum types
        await conn.execute(text('DROP TYPE IF EXISTS subscription_plan CASCADE'))
        await conn.execute(text('DROP TYPE IF EXISTS tenant_status CASCADE'))
        await conn.execute(text('DROP TYPE IF EXISTS user_role CASCADE'))
        await conn.execute(text('DROP TYPE IF EXISTS user_status CASCADE'))
        
        print("✅ All tables dropped successfully!")
    
    await engine.dispose()


async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Migration Tool")
    parser.add_argument(
        "action",
        choices=["create", "drop"],
        help="Action to perform: create tables or drop tables"
    )
    
    args = parser.parse_args()
    
    print(f"Database: {settings.DATABASE_URL}")
    print(f"Environment: {settings.ENVIRONMENT}\n")
    
    if args.action == "create":
        print("🔧 Creating tables...")
        await create_tables()
    elif args.action == "drop":
        confirm = input("⚠️  Are you sure? This will delete all data. Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            print("🔧 Dropping tables...")
            await drop_tables()
        else:
            print("❌ Cancelled")
    
    print("\n✅ Migration complete!")


if __name__ == "__main__":
    asyncio.run(main())
