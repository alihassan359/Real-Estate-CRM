#!/usr/bin/env python3
"""
Standalone Database Reset Script - No project dependencies needed
Connects directly to database and resets it
"""

import sys
import os

def reset_database():
    """Reset the database"""
    try:
        import psycopg2
        from psycopg2 import sql
    except ImportError:
        print("ERROR: psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    
    # Database connection details
    DB_HOST = "aws-1-ap-northeast-2.pooler.supabase.com"
    DB_PORT = 5432
    DB_USER = "postgres.shnbijxwgcfdwikzmigv"
    DB_PASSWORD = "u24yVpQRWwEX2167"
    DB_NAME = "postgres"
    
    print("=" * 60)
    print("DATABASE RESET SCRIPT (Direct Connection)")
    print("=" * 60)
    print(f"\nDatabase: {DB_HOST}")
    print(f"Database: {DB_NAME}")
    print("")
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        print("✓ Connected to database successfully\n")
        
        # Get all tables
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"Dropping {len(tables)} tables...")
            for (table,) in tables:
                cursor.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(
                    sql.Identifier(table)
                ))
                print(f"  ✓ Dropped table: {table}")
        
        # Get all ENUM types
        cursor.execute("""
            SELECT t.typname
            FROM pg_type t
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            WHERE (t.typrelid = 0 OR (SELECT c.relkind = 'c' FROM pg_catalog.pg_class c WHERE c.oid = t.typrelid))
            AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_type el WHERE el.oid = t.typelem)
            AND n.nspname NOT IN ('pg_catalog', 'information_schema')
            AND t.typtype = 'e'
        """)
        enums = cursor.fetchall()
        
        if enums:
            print(f"\nDropping {len(enums)} ENUM types...")
            for (enum,) in enums:
                cursor.execute(sql.SQL("DROP TYPE IF EXISTS {} CASCADE").format(
                    sql.Identifier(enum)
                ))
                print(f"  ✓ Dropped ENUM type: {enum}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✓ Database cleared successfully!")
        print("=" * 60)
        print("Now run: python scripts/reset_db.py (or use Django migrations)")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False


if __name__ == "__main__":
    confirm = input("⚠️  This will DELETE ALL DATA in the database! Continue? (yes/no): ")
    if confirm.lower() == "yes":
        success = reset_database()
        sys.exit(0 if success else 1)
    else:
        print("Reset cancelled.")
        sys.exit(0)
