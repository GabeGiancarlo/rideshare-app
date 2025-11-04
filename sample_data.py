#!/usr/bin/env python3
"""
CPSC 408 Assignment 05 - Sample Data
Script to populate the rideshare database with sample data for testing.

Author: [Your Name]
Date: [Current Date]
"""

import mysql.connector
from mysql.connector import Error
import getpass
import sys


def connect_to_db(host="localhost", database="rideshare_db", user="root", password=None):
    """Connect to MySQL database."""
    try:
        if password is None:
            password = getpass.getpass(f"Enter MySQL password for {user}: ")
        
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def insert_sample_data(connection):
    """Insert sample data into the database."""
    cursor = connection.cursor()
    
    try:
        # Insert Users
        users = [
            ("john_doe", "password123", "john.doe@email.com", "555-0101", "John Doe"),
            ("jane_smith", "password123", "jane.smith@email.com", "555-0102", "Jane Smith"),
            ("mike_wilson", "password123", "mike.wilson@email.com", "555-0103", "Mike Wilson"),
            ("sarah_jones", "password123", "sarah.jones@email.com", "555-0104", "Sarah Jones"),
            ("david_brown", "password123", "david.brown@email.com", "555-0105", "David Brown"),
            ("emily_davis", "password123", "emily.davis@email.com", "555-0106", "Emily Davis"),
        ]
        
        user_ids = []
        print("Inserting users...")
        for username, password, email, phone, full_name in users:
            cursor.execute("""
                INSERT INTO USER (username, password, email, phone_number, full_name)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, email, phone, full_name))
            user_ids.append(cursor.lastrowid)
        
        # Insert Drivers
        drivers_data = [
            (user_ids[0], "DL123456", "2026-12-31", "Toyota", "Camry", 2020, "Silver", "ABC-1234", "INS001"),
            (user_ids[1], "DL234567", "2027-06-30", "Honda", "Accord", 2021, "Blue", "XYZ-5678", "INS002"),
            (user_ids[2], "DL345678", "2026-09-15", "Ford", "Fusion", 2019, "Black", "DEF-9012", "INS003"),
        ]
        
        driver_ids = []
        print("Inserting drivers...")
        for driver_data in drivers_data:
            cursor.execute("""
                INSERT INTO DRIVER (user_id, license_number, license_expiry, vehicle_make,
                                   vehicle_model, vehicle_year, vehicle_color, license_plate,
                                   insurance_number, driver_mode)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (*driver_data, 'active'))
            driver_ids.append(cursor.lastrowid)
        
        # Insert Riders
        riders_data = [
            (user_ids[3], "Credit Card", "Visa", "1234", "Downtown Plaza"),
            (user_ids[4], "Debit Card", "Mastercard", "5678", "University Campus"),
            (user_ids[5], "PayPal", "PayPal", None, "Airport Terminal"),
        ]
        
        rider_ids = []
        print("Inserting riders...")
        for rider_data in riders_data:
            cursor.execute("""
                INSERT INTO RIDER (user_id, payment_info, preferred_payment,
                                 credit_card_last4, default_location)
                VALUES (%s, %s, %s, %s, %s)
            """, rider_data)
            rider_ids.append(cursor.lastrowid)
        
        # Insert Rides
        rides_data = [
            (driver_ids[0], rider_ids[0], "123 Main St", "456 Oak Ave", 
             "123 Main Street, City", "456 Oak Avenue, City", 25.50),
            (driver_ids[1], rider_ids[1], "789 Pine Rd", "321 Elm Blvd",
             "789 Pine Road, City", "321 Elm Boulevard, City", 18.75),
            (driver_ids[0], rider_ids[2], "555 Park Ave", "777 Market St",
             "555 Park Avenue, City", "777 Market Street, City", 32.00),
            (driver_ids[2], rider_ids[0], "999 Beach Dr", "111 Hill Rd",
             "999 Beach Drive, City", "111 Hill Road, City", 28.50),
        ]
        
        ride_ids = []
        print("Inserting rides...")
        for ride_data in rides_data:
            cursor.execute("""
                INSERT INTO RIDE (driver_id, rider_id, pickup_location, dropoff_location,
                                pickup_address, dropoff_address, ride_status, fare_amount,
                                pickup_time, dropoff_time)
                VALUES (%s, %s, %s, %s, %s, %s, 'completed', %s, NOW(), NOW())
            """, ride_data)
            ride_ids.append(cursor.lastrowid)
        
        # Add ratings to some rides
        print("Adding ratings...")
        ratings = [
            (ride_ids[0], 5, "Excellent driver, very professional!"),
            (ride_ids[1], 4, "Good ride, arrived on time."),
            (ride_ids[2], 5, "Perfect service!"),
            (ride_ids[3], 3, "Driver was okay."),
        ]
        
        for ride_id, rating, comment in ratings:
            cursor.execute("""
                UPDATE RIDE
                SET rating = %s, rating_comment = %s
                WHERE ride_id = %s
            """, (rating, comment, ride_id))
        
        connection.commit()
        print("\nSample data inserted successfully!")
        
        print(f"\nCreated:")
        print(f"  - {len(user_ids)} users")
        print(f"  - {len(driver_ids)} drivers")
        print(f"  - {len(rider_ids)} riders")
        print(f"  - {len(ride_ids)} rides")
        
        print("\nTest Accounts:")
        print("  Drivers:")
        print("    - username: john_doe, password: password123")
        print("    - username: jane_smith, password: password123")
        print("    - username: mike_wilson, password: password123")
        print("  Riders:")
        print("    - username: sarah_jones, password: password123")
        print("    - username: david_brown, password: password123")
        print("    - username: emily_davis, password: password123")
        
    except Error as e:
        connection.rollback()
        print(f"Error inserting sample data: {e}")
        raise
    finally:
        cursor.close()


def main():
    """Main entry point."""
    print("Rideshare Database - Sample Data Insertion")
    print("=" * 50)
    
    connection = connect_to_db()
    if not connection:
        print("Failed to connect to database.")
        sys.exit(1)
    
    try:
        confirm = input("\nThis will insert sample data. Continue? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("Cancelled.")
            return
        
        insert_sample_data(connection)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()

