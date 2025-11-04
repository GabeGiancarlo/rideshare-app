#!/usr/bin/env python3
"""
CPSC 408 Assignment 05 - Database Operations
Database operations module for the rideshare application using MySQL.

Author: [Your Name]
Date: [Current Date]
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Tuple, Optional, Dict
import getpass
import logging

logger = logging.getLogger(__name__)


class DatabaseOperations:
    """Handles all database operations for the rideshare application."""
    
    def __init__(self, host: str = "localhost", database: str = "rideshare_db",
                 user: str = "root", password: str = None):
        """Initialize database connection."""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection."""
        logger.debug(f"connect() called - host={self.host}, database={self.database}, user={self.user}")
        logger.debug(f"password is None: {self.password is None}")
        
        try:
            if self.password is None:
                # Check environment variable first
                import os
                env_password = os.environ.get('MYSQL_PASSWORD')
                if env_password is not None:
                    self.password = env_password
                    logger.info("Password obtained from MYSQL_PASSWORD environment variable")
                else:
                    logger.info("Password not set, prompting user...")
                    try:
                        self.password = getpass.getpass(f"Enter MySQL password for {self.user} (or press Enter for no password): ")
                        logger.debug("Password obtained (length hidden)")
                    except (EOFError, KeyboardInterrupt):
                        # If no input available (non-interactive), try empty password
                        self.password = ""
                        logger.info("No password input available, attempting connection with empty password")
            
            logger.info(f"Attempting to connect to MySQL at {self.host} as {self.user} to database {self.database}")
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                autocommit=False
            )
            
            logger.debug(f"mysql.connector.connect() returned: {self.connection}")
            
            if self.connection and self.connection.is_connected():
                logger.info("MySQL connection established successfully")
                logger.debug(f"Connection ID: {self.connection.connection_id}")
                
                self.cursor = self.connection.cursor(dictionary=True)
                logger.info("Database cursor created successfully")
                logger.debug(f"Cursor type: {type(self.cursor)}")
                
                return True
            else:
                logger.error("Connection object is None or not connected")
                logger.error(f"connection: {self.connection}")
                logger.error(f"is_connected: {self.connection.is_connected() if self.connection else 'N/A'}")
                return False
                
        except Error as e:
            logger.exception(f"MySQL Error connecting: {e}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error code: {e.errno if hasattr(e, 'errno') else 'N/A'}")
            logger.error(f"Error message: {e.msg if hasattr(e, 'msg') else 'N/A'}")
            print(f"Error connecting to MySQL: {e}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected exception during connection: {e}")
            logger.error(f"Exception type: {type(e)}")
            print(f"Unexpected error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username: str, password: str, email: str, 
                   phone_number: str, full_name: str) -> Optional[int]:
        """Create a new user account."""
        logger.debug(f"create_user() called - username: {username}, email: {email}, full_name: {full_name}")
        logger.debug(f"self.cursor is None: {self.cursor is None}")
        logger.debug(f"self.connection is None: {self.connection is None}")
        
        if self.cursor is None:
            logger.error("Cursor is None in create_user()")
            logger.error(f"Connection state: {self.connection}")
            raise AttributeError("Database cursor is not initialized. Connection failed.")
        
        query = """
        INSERT INTO USER (username, password, email, phone_number, full_name)
        VALUES (%s, %s, %s, %s, %s)
        """
        logger.debug(f"Executing INSERT query with params: ({username}, {email}, {full_name})")
        
        try:
            self.cursor.execute(query, (username, password, email, phone_number, full_name))
            logger.debug(f"INSERT executed, rowcount: {self.cursor.rowcount}")
            
            self.connection.commit()
            logger.info("Transaction committed successfully")
            
            user_id = self.cursor.lastrowid
            logger.info(f"User created with ID: {user_id}")
            return user_id
            
        except Error as e:
            logger.exception(f"MySQL Error creating user: {e}")
            logger.error(f"Error type: {type(e)}, Error code: {e.errno if hasattr(e, 'errno') else 'N/A'}")
            logger.error(f"Error message: {e.msg if hasattr(e, 'msg') else 'N/A'}")
            
            try:
                self.connection.rollback()
                logger.debug("Transaction rolled back")
            except Exception as rollback_error:
                logger.exception(f"Error during rollback: {rollback_error}")
            
            print(f"Error creating user: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected exception creating user: {e}")
            try:
                self.connection.rollback()
            except:
                pass
            print(f"Unexpected error creating user: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username."""
        logger.debug(f"get_user_by_username() called with username: {username}")
        logger.debug(f"self.cursor is None: {self.cursor is None}")
        logger.debug(f"self.connection is None: {self.connection is None}")
        
        if self.cursor is None:
            logger.error("Cursor is None in get_user_by_username()")
            logger.error(f"Connection state: {self.connection}")
            raise AttributeError("Database cursor is not initialized. Connection failed.")
        
        query = "SELECT * FROM USER WHERE username = %s"
        logger.debug(f"Executing query: {query} with params: ({username},)")
        
        try:
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            logger.debug(f"Query result: {result}")
            return result
        except Error as e:
            logger.exception(f"MySQL Error retrieving user: {e}")
            logger.error(f"Error type: {type(e)}, Error code: {e.errno if hasattr(e, 'errno') else 'N/A'}")
            print(f"Error retrieving user: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected exception retrieving user: {e}")
            print(f"Unexpected error retrieving user: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by user_id."""
        query = "SELECT * FROM USER WHERE user_id = %s"
        try:
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving user: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user by username and password."""
        user = self.get_user_by_username(username)
        if user and user['password'] == password:
            return user
        return None
    
    # ==================== DRIVER OPERATIONS ====================
    
    def create_driver(self, user_id: int, license_number: str, license_expiry: str = None,
                     vehicle_make: str = None, vehicle_model: str = None,
                     vehicle_year: int = None, vehicle_color: str = None,
                     license_plate: str = None, insurance_number: str = None) -> Optional[int]:
        """Create a new driver profile."""
        query = """
        INSERT INTO DRIVER (user_id, license_number, license_expiry, vehicle_make,
                           vehicle_model, vehicle_year, vehicle_color, license_plate,
                           insurance_number, driver_mode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'inactive')
        """
        try:
            self.cursor.execute(query, (user_id, license_number, license_expiry,
                                       vehicle_make, vehicle_model, vehicle_year,
                                       vehicle_color, license_plate, insurance_number))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"Error creating driver: {e}")
            return None
    
    def get_driver_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Get driver by user_id."""
        query = "SELECT * FROM DRIVER WHERE user_id = %s"
        try:
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving driver: {e}")
            return None
    
    def get_driver_by_id(self, driver_id: int) -> Optional[Dict]:
        """Get driver by driver_id."""
        query = "SELECT * FROM DRIVER WHERE driver_id = %s"
        try:
            self.cursor.execute(query, (driver_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving driver: {e}")
            return None
    
    def get_active_driver(self) -> Optional[Dict]:
        """Get an available active driver."""
        query = "SELECT * FROM DRIVER WHERE driver_mode = 'active' LIMIT 1"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving active driver: {e}")
            return None
    
    def toggle_driver_mode(self, driver_id: int) -> bool:
        """Toggle driver mode between active and inactive."""
        driver = self.get_driver_by_id(driver_id)
        if not driver:
            return False
        
        new_mode = 'active' if driver['driver_mode'] == 'inactive' else 'inactive'
        query = "UPDATE DRIVER SET driver_mode = %s WHERE driver_id = %s"
        try:
            self.cursor.execute(query, (new_mode, driver_id))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            print(f"Error updating driver mode: {e}")
            return False
    
    def get_driver_rating(self, driver_id: int) -> Optional[float]:
        """Get average rating for a driver."""
        query = """
        SELECT AVG(rating) as avg_rating
        FROM RIDE
        WHERE driver_id = %s AND rating IS NOT NULL
        """
        try:
            self.cursor.execute(query, (driver_id,))
            result = self.cursor.fetchone()
            return result['avg_rating'] if result and result['avg_rating'] else None
        except Error as e:
            print(f"Error retrieving driver rating: {e}")
            return None
    
    def get_driver_rides(self, driver_id: int) -> List[Dict]:
        """Get all rides for a driver."""
        query = """
        SELECT r.*, u.full_name as rider_name
        FROM RIDE r
        JOIN RIDER rd ON r.rider_id = rd.rider_id
        JOIN USER u ON rd.user_id = u.user_id
        WHERE r.driver_id = %s
        ORDER BY r.created_at DESC
        """
        try:
            self.cursor.execute(query, (driver_id,))
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"Error retrieving driver rides: {e}")
            return []
    
    # ==================== RIDER OPERATIONS ====================
    
    def create_rider(self, user_id: int, payment_info: str = None,
                    preferred_payment: str = None, credit_card_last4: str = None,
                    default_location: str = None) -> Optional[int]:
        """Create a new rider profile."""
        query = """
        INSERT INTO RIDER (user_id, payment_info, preferred_payment,
                          credit_card_last4, default_location)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (user_id, payment_info, preferred_payment,
                                       credit_card_last4, default_location))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"Error creating rider: {e}")
            return None
    
    def get_rider_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Get rider by user_id."""
        query = "SELECT * FROM RIDER WHERE user_id = %s"
        try:
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving rider: {e}")
            return None
    
    def get_rider_by_id(self, rider_id: int) -> Optional[Dict]:
        """Get rider by rider_id."""
        query = "SELECT * FROM RIDER WHERE rider_id = %s"
        try:
            self.cursor.execute(query, (rider_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving rider: {e}")
            return None
    
    def get_rider_rides(self, rider_id: int) -> List[Dict]:
        """Get all rides for a rider."""
        query = """
        SELECT r.*, d.vehicle_make, d.vehicle_model, u.full_name as driver_name
        FROM RIDE r
        JOIN DRIVER d ON r.driver_id = d.driver_id
        JOIN USER u ON d.user_id = u.user_id
        WHERE r.rider_id = %s
        ORDER BY r.created_at DESC
        """
        try:
            self.cursor.execute(query, (rider_id,))
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"Error retrieving rider rides: {e}")
            return []
    
    def get_rider_most_recent_ride(self, rider_id: int) -> Optional[Dict]:
        """Get the most recent ride for a rider."""
        query = """
        SELECT r.*, d.vehicle_make, d.vehicle_model, u.full_name as driver_name
        FROM RIDE r
        JOIN DRIVER d ON r.driver_id = d.driver_id
        JOIN USER u ON d.user_id = u.user_id
        WHERE r.rider_id = %s
        ORDER BY r.created_at DESC
        LIMIT 1
        """
        try:
            self.cursor.execute(query, (rider_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving most recent ride: {e}")
            return None
    
    # ==================== RIDE OPERATIONS ====================
    
    def create_ride(self, driver_id: int, rider_id: int, pickup_location: str,
                   dropoff_location: str, pickup_address: str = None,
                   dropoff_address: str = None, fare_amount: float = None) -> Optional[int]:
        """Create a new ride."""
        query = """
        INSERT INTO RIDE (driver_id, rider_id, pickup_location, dropoff_location,
                         pickup_address, dropoff_address, ride_status, fare_amount,
                         pickup_time)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending', %s, NOW())
        """
        try:
            self.cursor.execute(query, (driver_id, rider_id, pickup_location,
                                       dropoff_location, pickup_address,
                                       dropoff_address, fare_amount))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"Error creating ride: {e}")
            return None
    
    def get_ride_by_id(self, ride_id: int, rider_id: int = None) -> Optional[Dict]:
        """Get ride by ride_id, optionally verifying it belongs to a rider."""
        if rider_id:
            query = """
            SELECT r.*, d.vehicle_make, d.vehicle_model, u.full_name as driver_name
            FROM RIDE r
            JOIN DRIVER d ON r.driver_id = d.driver_id
            JOIN USER u ON d.user_id = u.user_id
            WHERE r.ride_id = %s AND r.rider_id = %s
            """
            try:
                self.cursor.execute(query, (ride_id, rider_id))
                result = self.cursor.fetchone()
                return result
            except Error as e:
                print(f"Error retrieving ride: {e}")
                return None
        else:
            query = "SELECT * FROM RIDE WHERE ride_id = %s"
            try:
                self.cursor.execute(query, (ride_id,))
                result = self.cursor.fetchone()
                return result
            except Error as e:
                print(f"Error retrieving ride: {e}")
                return None
    
    def update_ride_rating(self, ride_id: int, rider_id: int, rating: int,
                          rating_comment: str = None) -> bool:
        """Update ride rating and comment."""
        query = """
        UPDATE RIDE
        SET rating = %s, rating_comment = %s
        WHERE ride_id = %s AND rider_id = %s
        """
        try:
            self.cursor.execute(query, (rating, rating_comment, ride_id, rider_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            self.connection.rollback()
            print(f"Error updating ride rating: {e}")
            return False
    
    def __del__(self):
        """Destructor to ensure database connection is closed."""
        try:
            self.disconnect()
        except:
            pass

