#!/usr/bin/env python3
"""
Database Connection Test Script for Supabase PostgreSQL
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test the database connection to Supabase"""
    try:
        # Get database URL from environment
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return False
            
        print("🔄 Testing Supabase PostgreSQL connection...")
        
        # Connect to the database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        
        print(f"✅ Database connection successful!")
        print(f"📊 PostgreSQL Version: {db_version}")
        
        # Close connections
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🎬 Movie Recommendation App - Database Connection Test")
    print("=" * 50)
    
    success = test_database_connection()
    
    if success:
        print("\n🎉 Your Supabase database is ready for Django!")
        print("\nNext steps:")
        print("1. Replace [YOUR-PASSWORD] in .env with your actual Supabase password")
        print("2. Initialize Django project")
        print("3. Configure Django settings for database")
    else:
        print("\n🔧 Please check your database credentials and try again")
