#!/usr/bin/env python3
"""
CPSC 408 Assignment 05 - Rideshare Application
Main application file for the rideshare management system.

Authors:
- Gabe Giancarlo (2405449) - giancarlo@chapman.edu
- Gustavo de Moraes (002427902) - demoraes@chapman.edu
"""

import sys
from db_operations import DatabaseOperations
from helper import Helper


class RideshareApp:
    """Main application class for the rideshare management system."""
    
    def __init__(self):
        """Initialize the application with database connection."""
        self.db_ops = DatabaseOperations()
        self.helper = Helper()
        
        if not self.db_ops.connect():
            print("Failed to connect to database. Exiting.")
            sys.exit(1)
        
        self.current_user = None
        self.current_user_type = None  # 'driver' or 'rider'
        self.current_profile = None  # driver or rider profile
    
    def display_main_menu(self):
        """Display the main authentication menu."""
        self.helper.display_header("RIDESHARE APPLICATION")
        print("1. New Account")
        print("2. Existing Rider Login")
        print("3. Existing Driver Login")
        print("4. Exit")
    
    def handle_new_account(self):
        """Handle new account creation."""
        self.helper.display_section("Create New Account")
        
        print("\nChoose account type:")
        print("1. Rider Account")
        print("2. Driver Account")
        print("3. Cancel")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "3":
            return
        
        if choice not in ["1", "2"]:
            print("Invalid choice.")
            return
        
        # Get user information
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        
        # Check if username exists
        if self.db_ops.get_user_by_username(username):
            print("Username already exists. Please choose another.")
            return
        
        password = input("Enter password: ").strip()
        if not password:
            print("Password cannot be empty.")
            return
        
        email = input("Enter email: ").strip()
        if not self.helper.validate_email(email):
            print("Invalid email format.")
            return
        
        full_name = input("Enter full name: ").strip()
        if not full_name:
            print("Full name cannot be empty.")
            return
        
        phone_number = input("Enter phone number (optional): ").strip()
        if phone_number and not self.helper.validate_phone(phone_number):
            print("Invalid phone number format.")
            return
        
        # Create user account
        user_id = self.db_ops.create_user(username, password, email, phone_number, full_name)
        
        if not user_id:
            print("Failed to create user account.")
            return
        
        print("\nUser account created successfully!")
        
        # Create rider or driver profile
        if choice == "1":
            self.create_rider_profile(user_id)
        else:
            self.create_driver_profile(user_id)
    
    def create_rider_profile(self, user_id: int):
        """Create a rider profile for a new user."""
        print("\nCreating rider profile...")
        
        payment_info = input("Enter payment information (optional): ").strip() or None
        preferred_payment = input("Enter preferred payment method (optional): ").strip() or None
        credit_card_last4 = input("Enter last 4 digits of credit card (optional): ").strip() or None
        default_location = input("Enter default location (optional): ").strip() or None
        
        rider_id = self.db_ops.create_rider(user_id, payment_info, preferred_payment,
                                           credit_card_last4, default_location)
        
        if rider_id:
            print("Rider profile created successfully!")
            print("\nYou can now log in as a rider.")
        else:
            print("Failed to create rider profile.")
    
    def create_driver_profile(self, user_id: int):
        """Create a driver profile for a new user."""
        print("\nCreating driver profile...")
        
        license_number = input("Enter license number: ").strip()
        if not license_number:
            print("License number is required.")
            return
        
        license_expiry = input("Enter license expiry date (YYYY-MM-DD, optional): ").strip() or None
        vehicle_make = input("Enter vehicle make (optional): ").strip() or None
        vehicle_model = input("Enter vehicle model (optional): ").strip() or None
        
        vehicle_year = None
        vehicle_year_input = input("Enter vehicle year (optional): ").strip()
        if vehicle_year_input:
            try:
                vehicle_year = int(vehicle_year_input)
            except ValueError:
                print("Invalid year format.")
                return
        
        vehicle_color = input("Enter vehicle color (optional): ").strip() or None
        license_plate = input("Enter license plate (optional): ").strip() or None
        insurance_number = input("Enter insurance number (optional): ").strip() or None
        
        driver_id = self.db_ops.create_driver(user_id, license_number, license_expiry,
                                             vehicle_make, vehicle_model, vehicle_year,
                                             vehicle_color, license_plate, insurance_number)
        
        if driver_id:
            print("Driver profile created successfully!")
            print("\nYou can now log in as a driver.")
        else:
            print("Failed to create driver profile.")
    
    def handle_rider_login(self):
        """Handle rider login."""
        self.helper.display_section("Rider Login")
        
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        user = self.db_ops.authenticate_user(username, password)
        if not user:
            print("Invalid username or password.")
            return
        
        rider = self.db_ops.get_rider_by_user_id(user['user_id'])
        if not rider:
            print("No rider profile found for this user.")
            return
        
        self.current_user = user
        self.current_user_type = 'rider'
        self.current_profile = rider
        
        print("\nLogin successful!")
        self.helper.display_user_info(user)
        
        self.rider_menu()
    
    def handle_driver_login(self):
        """Handle driver login."""
        self.helper.display_section("Driver Login")
        
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        user = self.db_ops.authenticate_user(username, password)
        if not user:
            print("Invalid username or password.")
            return
        
        driver = self.db_ops.get_driver_by_user_id(user['user_id'])
        if not driver:
            print("No driver profile found for this user.")
            return
        
        self.current_user = user
        self.current_user_type = 'driver'
        self.current_profile = driver
        
        print("\nLogin successful!")
        self.helper.display_user_info(user)
        self.helper.display_driver_info(driver)
        
        self.driver_menu()
    
    def driver_menu(self):
        """Display and handle driver menu options."""
        while True:
            self.helper.display_header("DRIVER MENU")
            print("1. View Rating")
            print("2. View Rides")
            print("3. Activate/Deactivate Driver Mode")
            print("4. Logout")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.driver_view_rating()
            elif choice == "2":
                self.driver_view_rides()
            elif choice == "3":
                self.driver_toggle_mode()
            elif choice == "4":
                self.logout()
                break
            else:
                print("Invalid choice. Please enter 1-4.")
            
            input("\nPress Enter to continue...")
    
    def driver_view_rating(self):
        """Display driver's average rating."""
        self.helper.display_section("Driver Rating")
        
        rating = self.db_ops.get_driver_rating(self.current_profile['driver_id'])
        self.helper.display_driver_rating(rating)
    
    def driver_view_rides(self):
        """Display all rides for the driver."""
        self.helper.display_section("My Rides")
        
        rides = self.db_ops.get_driver_rides(self.current_profile['driver_id'])
        
        if not rides:
            print("No rides found.")
            return
        
        print(f"\nTotal rides: {len(rides)}")
        self.helper.display_rides_table(rides)
        
        # Option to view details
        if rides:
            ride_id_input = input("\nEnter ride ID to view details (or press Enter to skip): ").strip()
            if ride_id_input:
                try:
                    ride_id = int(ride_id_input)
                    ride = next((r for r in rides if r['ride_id'] == ride_id), None)
                    if ride:
                        self.helper.display_section("Ride Details")
                        self.helper.display_ride_details(ride)
                    else:
                        print("Ride not found.")
                except ValueError:
                    print("Invalid ride ID.")
    
    def driver_toggle_mode(self):
        """Toggle driver mode between active and inactive."""
        self.helper.display_section("Driver Mode")
        
        current_mode = self.current_profile['driver_mode']
        print(f"Current mode: {current_mode.upper()}")
        
        new_mode = 'active' if current_mode == 'inactive' else 'inactive'
        
        if self.helper.get_user_confirmation(f"Switch to {new_mode.upper()} mode?"):
            if self.db_ops.toggle_driver_mode(self.current_profile['driver_id']):
                print(f"\nDriver mode changed to {new_mode.upper()}.")
                # Refresh driver profile
                self.current_profile = self.db_ops.get_driver_by_id(self.current_profile['driver_id'])
            else:
                print("Failed to update driver mode.")
        else:
            print("Mode change cancelled.")
    
    def rider_menu(self):
        """Display and handle rider menu options."""
        while True:
            self.helper.display_header("RIDER MENU")
            print("1. View Rides")
            print("2. Find a Driver")
            print("3. Rate My Driver")
            print("4. Logout")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.rider_view_rides()
            elif choice == "2":
                self.rider_find_driver()
            elif choice == "3":
                self.rider_rate_driver()
            elif choice == "4":
                self.logout()
                break
            else:
                print("Invalid choice. Please enter 1-4.")
            
            input("\nPress Enter to continue...")
    
    def rider_view_rides(self):
        """Display all rides for the rider."""
        self.helper.display_section("My Rides")
        
        rides = self.db_ops.get_rider_rides(self.current_profile['rider_id'])
        
        if not rides:
            print("No rides found.")
            return
        
        print(f"\nTotal rides: {len(rides)}")
        self.helper.display_rides_table(rides)
        
        # Option to view details
        if rides:
            ride_id_input = input("\nEnter ride ID to view details (or press Enter to skip): ").strip()
            if ride_id_input:
                try:
                    ride_id = int(ride_id_input)
                    ride = next((r for r in rides if r['ride_id'] == ride_id), None)
                    if ride:
                        self.helper.display_section("Ride Details")
                        self.helper.display_ride_details(ride)
                    else:
                        print("Ride not found.")
                except ValueError:
                    print("Invalid ride ID.")
    
    def rider_find_driver(self):
        """Find an available driver and create a ride."""
        self.helper.display_section("Find a Driver")
        
        # Find an active driver
        driver = self.db_ops.get_active_driver()
        
        if not driver:
            print("No active drivers available at the moment.")
            print("Please try again later.")
            return
        
        print(f"\nFound driver: {driver.get('vehicle_make', 'N/A')} {driver.get('vehicle_model', 'N/A')}")
        
        # Get pickup and dropoff locations
        pickup_location = input("\nEnter pickup location: ").strip()
        if not pickup_location:
            print("Pickup location is required.")
            return
        
        pickup_address = input("Enter pickup address (optional): ").strip() or None
        
        dropoff_location = input("Enter dropoff location: ").strip()
        if not dropoff_location:
            print("Dropoff location is required.")
            return
        
        dropoff_address = input("Enter dropoff address (optional): ").strip() or None
        
        fare_input = input("Enter fare amount (optional): ").strip()
        fare_amount = None
        if fare_input:
            try:
                fare_amount = float(fare_input)
            except ValueError:
                print("Invalid fare amount. Proceeding without fare.")
        
        # Create ride
        ride_id = self.db_ops.create_ride(
            driver['driver_id'],
            self.current_profile['rider_id'],
            pickup_location,
            dropoff_location,
            pickup_address,
            dropoff_address,
            fare_amount
        )
        
        if ride_id:
            print("\nRide created successfully!")
            ride = self.db_ops.get_ride_by_id(ride_id)
            if ride:
                self.helper.display_ride_details(ride)
        else:
            print("Failed to create ride.")
    
    def rider_rate_driver(self):
        """Allow rider to rate their driver for a ride."""
        self.helper.display_section("Rate My Driver")
        
        # Get most recent ride
        most_recent_ride = self.db_ops.get_rider_most_recent_ride(self.current_profile['rider_id'])
        
        if not most_recent_ride:
            print("No rides found. You need to take a ride before you can rate.")
            return
        
        # Display most recent ride
        print("\nMost recent ride:")
        self.helper.display_ride_details(most_recent_ride)
        
        # Check if already rated
        already_rated = most_recent_ride.get('rating') is not None
        if already_rated:
            print(f"\nThis ride has already been rated: {most_recent_ride['rating']}/5")
            if not self.helper.get_user_confirmation("Rate a different ride?"):
                return
            # User wants to rate a different ride, skip to getting new ride ID
            use_most_recent = False
        else:
            # Confirm this is the ride to rate
            use_most_recent = self.helper.get_user_confirmation("\nIs this the ride you want to rate?")
        
        if use_most_recent:
            # Use the most recent ride
            ride_id = most_recent_ride['ride_id']
        else:
            # Get ride ID from user
            ride_id_input = input("Enter the ride ID you want to rate: ").strip()
            try:
                ride_id = int(ride_id_input)
            except ValueError:
                print("Invalid ride ID.")
                return
            
            # Verify ride belongs to rider
            ride = self.db_ops.get_ride_by_id(ride_id, self.current_profile['rider_id'])
            if not ride:
                print("Ride not found or does not belong to you.")
                return
            
            print("\nRide information:")
            self.helper.display_ride_details(ride)
            
            if ride.get('rating'):
                print(f"\nThis ride has already been rated: {ride['rating']}/5")
                if not self.helper.get_user_confirmation("Update the rating?"):
                    return
        
        # Get rating
        while True:
            rating_input = input("\nEnter rating (1-5): ").strip()
            rating = self.helper.validate_rating(rating_input)
            if rating:
                break
            print("Invalid rating. Please enter a number between 1 and 5.")
        
        rating_comment = input("Enter rating comment (optional): ").strip() or None
        
        # Update ride rating
        if self.db_ops.update_ride_rating(ride_id, self.current_profile['rider_id'], rating, rating_comment):
            print("\nRating submitted successfully!")
        else:
            print("Failed to submit rating.")
    
    def logout(self):
        """Log out current user."""
        self.current_user = None
        self.current_user_type = None
        self.current_profile = None
        print("\nLogged out successfully.")
    
    def run(self):
        """Main application loop."""
        print("\nWelcome to the Rideshare Application!")
        
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.handle_new_account()
            elif choice == "2":
                self.handle_rider_login()
            elif choice == "3":
                self.handle_driver_login()
            elif choice == "4":
                print("\nThank you for using the Rideshare Application!")
                break
            else:
                print("Invalid choice. Please enter 1-4.")
            
            input("\nPress Enter to continue...")
    
    def __del__(self):
        """Cleanup on exit."""
        if self.db_ops:
            self.db_ops.disconnect()


def main():
    """Main entry point of the application."""
    try:
        app = RideshareApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()

