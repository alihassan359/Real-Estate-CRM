#!/usr/bin/env python
import asyncio
from models.base import Base
from database.session import engine

async def create_schema():
    """Create database schema"""
    async with engine.begin() as conn:
        # Drop all existing tables
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database schema created successfully!")

asyncio.run(create_schema())
