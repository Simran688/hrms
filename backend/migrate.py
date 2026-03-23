#!/usr/bin/env python3
"""
Database migration script for Render deployment
Creates all tables required for HRMS Lite application
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.models import User, Employee, Attendance

def create_tables():
    """Create all database tables"""
    print(f"Connecting to database: {SQLALCHEMY_DATABASE_URL}")
    
    try:
        # Create engine
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        print("✅ Database engine created")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        
        # Verify tables exist
        inspector = engine.inspect(engine)
        tables = inspector.get_table_names()
        print(f"✅ Tables in database: {tables}")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 Starting database migration...")
    
    if create_tables():
        print("✅ Migration completed successfully!")
        sys.exit(0)
    else:
        print("❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
