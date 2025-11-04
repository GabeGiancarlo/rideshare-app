#!/usr/bin/env python3
"""
CPSC 408 Assignment 05 - Helper Functions
Helper functions module for the rideshare application.

Author: [Your Name]
Date: [Current Date]
"""

from typing import List, Dict, Optional
from datetime import datetime


class Helper:
    """Helper class containing utility functions for the rideshare application."""
    
    def __init__(self):
        """Initialize the helper class."""
        pass
    
    def display_header(self, title: str):
        """Display a formatted header."""
        print("\n" + "="*70)
        print(f"{title:^70}")
        print("="*70)
    
    def display_section(self, title: str):
        """Display a section header."""
        print("\n" + "-"*70)
        print(f"  {title}")
        print("-"*70)
    
    def display_user_info(self, user: Dict):
        """Display user information in a formatted way."""
        if not user:
            print("No user information available.")
            return
        
        print(f"\nUser ID: {user['user_id']}")
        print(f"Username: {user['username']}")
        print(f"Full Name: {user['full_name']}")
        print(f"Email: {user['email']}")
        if user.get('phone_number'):
            print(f"Phone: {user['phone_number']}")
    
    def display_driver_info(self, driver: Dict):
        """Display driver information."""
        if not driver:
            print("No driver information available.")
            return
        
        print(f"\nDriver ID: {driver['driver_id']}")
        print(f"License Number: {driver['license_number']}")
        if driver.get('vehicle_make') and driver.get('vehicle_model'):
            print(f"Vehicle: {driver['vehicle_year']} {driver['vehicle_make']} {driver['vehicle_model']}")
        if driver.get('vehicle_color'):
            print(f"Color: {driver['vehicle_color']}")
        if driver.get('license_plate'):
            print(f"License Plate: {driver['license_plate']}")
        print(f"Driver Mode: {driver['driver_mode'].upper()}")
    
    def display_ride_details(self, ride: Dict):
        """Display ride details in a formatted way."""
        if not ride:
            print("No ride information available.")
            return
        
        print(f"\nRide ID: {ride['ride_id']}")
        print(f"Status: {ride['ride_status'].upper()}")
        print(f"\nPickup Location: {ride['pickup_location']}")
        if ride.get('pickup_address'):
            print(f"Pickup Address: {ride['pickup_address']}")
        print(f"\nDropoff Location: {ride['dropoff_location']}")
        if ride.get('dropoff_address'):
            print(f"Dropoff Address: {ride['dropoff_address']}")
        
        if ride.get('driver_name'):
            print(f"\nDriver: {ride['driver_name']}")
        if ride.get('rider_name'):
            print(f"Rider: {ride['rider_name']}")
        
        if ride.get('vehicle_make') and ride.get('vehicle_model'):
            print(f"Vehicle: {ride['vehicle_make']} {ride['vehicle_model']}")
        
        if ride.get('pickup_time'):
            pickup_time = ride['pickup_time']
            if isinstance(pickup_time, datetime):
                print(f"Pickup Time: {pickup_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"Pickup Time: {pickup_time}")
        
        if ride.get('dropoff_time'):
            dropoff_time = ride['dropoff_time']
            if isinstance(dropoff_time, datetime):
                print(f"Dropoff Time: {dropoff_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"Dropoff Time: {dropoff_time}")
        
        if ride.get('fare_amount'):
            print(f"Fare: ${ride['fare_amount']:.2f}")
        
        if ride.get('rating'):
            print(f"\nRating: {ride['rating']}/5")
            if ride.get('rating_comment'):
                print(f"Comment: {ride['rating_comment']}")
    
    def display_rides_table(self, rides: List[Dict]):
        """Display a formatted table of rides."""
        if not rides:
            print("No rides found.")
            return
        
        # Table headers
        headers = ["Ride ID", "Status", "Pickup", "Dropoff", "Fare", "Rating"]
        col_widths = [10, 12, 25, 25, 10, 8]
        
        # Print header
        header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print("\n" + header_row)
        print("-" * len(header_row))
        
        # Print rides
        for ride in rides:
            ride_id = str(ride.get('ride_id', 'N/A'))
            status = ride.get('ride_status', 'N/A').upper()
            pickup = self.truncate_text(ride.get('pickup_location', 'N/A'), 23)
            dropoff = self.truncate_text(ride.get('dropoff_location', 'N/A'), 23)
            fare = f"${ride.get('fare_amount', 0):.2f}" if ride.get('fare_amount') else "N/A"
            rating = f"{ride.get('rating', 'N/A')}/5" if ride.get('rating') else "N/A"
            
            row = [
                ride_id.ljust(col_widths[0]),
                status.ljust(col_widths[1]),
                pickup.ljust(col_widths[2]),
                dropoff.ljust(col_widths[3]),
                fare.ljust(col_widths[4]),
                rating.ljust(col_widths[5])
            ]
            print(" | ".join(row))
    
    def display_driver_rating(self, rating: Optional[float]):
        """Display driver rating."""
        if rating is None:
            print("\nNo ratings available yet.")
        else:
            print(f"\nAverage Rating: {rating:.2f}/5.0")
            stars = int(rating)
            print("Stars: " + "★" * stars + "☆" * (5 - stars))
    
    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        if not email or '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        if '.' not in parts[1]:
            return False
        return True
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format (basic check)."""
        if not phone:
            return True  # Phone is optional
        # Remove common formatting characters
        digits_only = ''.join(filter(str.isdigit, phone))
        return len(digits_only) >= 10
    
    def validate_rating(self, rating: str) -> Optional[int]:
        """Validate and convert rating input."""
        try:
            rating_int = int(rating)
            if 1 <= rating_int <= 5:
                return rating_int
            return None
        except ValueError:
            return None
    
    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input to prevent SQL injection (though we use parameterized queries)."""
        if not user_input:
            return ""
        # Remove potentially harmful characters
        sanitized = user_input.strip()
        return sanitized
    
    def truncate_text(self, text: str, max_length: int = 50) -> str:
        """Truncate text to specified length with ellipsis."""
        if not text:
            return ""
        if len(str(text)) <= max_length:
            return str(text)
        return str(text)[:max_length-3] + "..."
    
    def get_user_confirmation(self, message: str) -> bool:
        """Get user confirmation for an action."""
        while True:
            response = input(f"\n{message} (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'.")
    
    def format_datetime(self, dt) -> str:
        """Format datetime object to string."""
        if dt is None:
            return "N/A"
        if isinstance(dt, datetime):
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        return str(dt)
    
    def format_currency(self, amount: Optional[float]) -> str:
        """Format amount as currency."""
        if amount is None:
            return "N/A"
        return f"${amount:.2f}"

