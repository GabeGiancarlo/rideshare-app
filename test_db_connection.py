#!/usr/bin/env python3
"""
Test database connection script
Helps diagnose MySQL connection issues
"""

import mysql.connector
from mysql.connector import Error
import getpass

def test_connection():
    """Test MySQL connection with user input."""
    print("=" * 60)
    print("MySQL Database Connection Test")
    print("=" * 60)
    
    # Get connection details
    host = input("Enter MySQL host (default: localhost): ").strip() or "localhost"
    user = input("Enter MySQL user (default: root): ").strip() or "root"
    password = getpass.getpass(f"Enter MySQL password for {user}: ")
    
    try:
        print("\nAttempting to connect...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("✓ Successfully connected to MySQL server!")
            
            # Get server info
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL Server version: {version[0]}")
            
            # Check if database exists
            cursor.execute("SHOW DATABASES LIKE 'rideshare_db'")
            db_exists = cursor.fetchone()
            
            if db_exists:
                print("✓ Database 'rideshare_db' exists")
                
                # Try to use it
                cursor.execute("USE rideshare_db")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"✓ Database has {len(tables)} table(s)")
                if tables:
                    print("  Tables:", [t[0] for t in tables])
            else:
                print("✗ Database 'rideshare_db' does NOT exist")
                print("\nTo create it, run:")
                print("  mysql -u root -p < schema.sql")
            
            cursor.close()
            connection.close()
            print("\n✓ Connection test completed successfully!")
            return True
            
    except Error as e:
        print(f"\n✗ Error connecting to MySQL: {e}")
        print("\nPossible issues:")
        print("  1. MySQL server is not running")
        print("  2. Wrong username/password")
        print("  3. MySQL is not installed")
        print("\nTo install MySQL on macOS:")
        print("  brew install mysql")
        print("  brew services start mysql")
        return False

if __name__ == "__main__":
    test_connection()

