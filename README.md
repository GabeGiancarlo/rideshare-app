# CPSC 408 Assignment 05 - Rideshare Application

## Author
[Your Name]

## Description
A comprehensive rideshare management system built with Python and MySQL that allows users to manage driver and rider accounts, create rides, and rate experiences. The application implements a complete database schema with proper normalization and referential integrity.

## Features Implemented

### Core Requirements

1. **ER Diagram**
   - Complete entity-relationship diagram documenting all relationships
   - Four main entities: USER, DRIVER, RIDER, RIDE
   - Properly defined cardinalities and relationships

2. **Database Schema**
   - MySQL database schema with all tables and attributes
   - Normalized to 3rd Normal Form (3NF)
   - Proper foreign key constraints and referential integrity
   - All relationships correctly implemented

3. **Database on MySQL**
   - Local MySQL database implementation
   - Proper indexing for performance
   - Transaction support with rollback on errors

4. **Sample Data**
   - Script to populate database with test data
   - Includes users, drivers, riders, and rides
   - Sample ratings for testing

5. **Interactive Python Program**
   - Clean, professional command-line interface
   - Full feature implementation for all requirements

### Application Specifications

#### User Authentication & Account Management

- New account creation (rider or driver)
- Existing user login (rider or driver)
- Username-based authentication
- Secure account management

#### Driver Features

1. **View Rating**
   - Displays average rating from all completed rides
   - Shows star rating visualization
   - Handles drivers with no ratings yet

2. **View Rides**
   - Lists all rides provided by the driver
   - Shows ride details including pickup/dropoff locations
   - Displays fare amounts and ratings
   - Option to view detailed information for specific rides

3. **Activate/Deactivate Driver Mode**
   - Toggle between active and inactive status
   - Active drivers are available for ride requests
   - Confirmation prompt before mode change

#### Rider Features

1. **View Rides**
   - Lists all rides taken by the rider
   - Shows ride details including driver information
   - Displays fare amounts and ratings
   - Option to view detailed information for specific rides

2. **Find a Driver**
   - Matches rider with an available active driver
   - Rider provides pickup and dropoff locations
   - Automatically creates ride record
   - Returns rider to menu after ride creation

3. **Rate My Driver**
   - Displays rider's most recent ride by default
   - Allows rider to confirm or select different ride
   - Accepts rating (1-5) and optional comment
   - Updates ride record with rating information

## File Structure
```
assignment5/
├── app.py                 # Main CLI application file
├── web_app.py             # Flask web application
├── db_operations.py       # Database operations module
├── helper.py              # Helper functions module
├── schema.sql             # MySQL database schema
├── sample_data.py         # Sample data insertion script
├── templates/            # HTML templates for web app
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── register*.html    # Registration pages
│   ├── *login.html       # Login pages
│   └── *.html            # Other pages
├── README.md              # This file
├── requirements.md        # Assignment requirements
├── plan.txt               # ER diagram and design plan
├── IMG_6914.HEIC          # ER diagram image 1
└── IMG_6915.HEIC          # ER diagram image 2
```

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- MySQL Server (local installation)
- mysql-connector-python package

### Installation Steps

1. **Install MySQL Connector**
   ```bash
   pip install mysql-connector-python
   ```

2. **Create Database Schema**
   ```bash
   mysql -u root -p < schema.sql
   ```
   Or connect to MySQL and run the schema.sql file manually.

3. **Populate Sample Data (Optional)**
   ```bash
   python sample_data.py
   ```

### Running the Application

#### Command-Line Interface (CLI)

1. Navigate to the assignment5 directory
2. Run the main application:
   ```bash
   python app.py
   ```
3. Enter MySQL password when prompted (default user: root)

#### Web Application (Browser)

1. Install Flask (if not already installed):
   ```bash
   pip install Flask
   ```

2. Navigate to the assignment5 directory

3. Run the web application:
   ```bash
   python web_app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

5. Enter MySQL password when prompted (if using default settings)

The web application provides a modern, clean interface accessible through your browser with all the same functionality as the CLI version.

## Usage Instructions

### Main Menu

1. **New Account** - Create a new rider or driver account
2. **Existing Rider Login** - Log in as an existing rider
3. **Existing Driver Login** - Log in as an existing driver
4. **Exit** - Close the application

### Creating an Account

1. Select "New Account" from main menu
2. Choose account type (Rider or Driver)
3. Enter required information:
   - Username (must be unique)
   - Password
   - Email (must be unique)
   - Full name
   - Phone number (optional)
4. For drivers: Enter license and vehicle information
5. For riders: Enter payment preferences (optional)

### Driver Menu Options

1. **View Rating** - See average rating from all rides
2. **View Rides** - See all rides provided, with option to view details
3. **Activate/Deactivate Driver Mode** - Toggle availability for new rides
4. **Logout** - Return to main menu

### Rider Menu Options

1. **View Rides** - See all rides taken, with option to view details
2. **Find a Driver** - Request a ride with an available driver
3. **Rate My Driver** - Rate a driver for a completed ride
4. **Logout** - Return to main menu

## Database Schema

### Tables

#### USER
- Primary Key: `user_id`
- Stores authentication and basic user information
- Unique constraints on username and email

#### DRIVER
- Primary Key: `driver_id`
- Foreign Key: `user_id` → USER(user_id)
- Stores driver-specific information and vehicle details
- Driver mode: 'active' or 'inactive'

#### RIDER
- Primary Key: `rider_id`
- Foreign Key: `user_id` → USER(user_id)
- Stores rider-specific information and payment preferences

#### RIDE
- Primary Key: `ride_id`
- Foreign Key: `driver_id` → DRIVER(driver_id)
- Foreign Key: `rider_id` → RIDER(rider_id)
- Stores ride information, locations, status, and ratings

### Relationships

1. **USER → DRIVER (1:1, optional)**
   - One user can have one driver profile
   - Not all users are drivers

2. **USER → RIDER (1:1, optional)**
   - One user can have one rider profile
   - Not all users are riders

3. **DRIVER → RIDE (1:M)**
   - One driver can provide many rides
   - Each ride has exactly one driver

4. **RIDER → RIDE (1:M)**
   - One rider can take many rides
   - Each ride has exactly one rider

### Normalization

All tables are normalized to 3rd Normal Form (3NF):
- No repeating groups
- No partial dependencies
- No transitive dependencies
- Proper primary and foreign key relationships

## Technical Implementation

### Key Classes and Methods

#### DatabaseOperations Class
- `create_user()` - Create new user account
- `authenticate_user()` - Verify user credentials
- `create_driver()` - Create driver profile
- `create_rider()` - Create rider profile
- `get_active_driver()` - Find available driver
- `create_ride()` - Create new ride
- `get_driver_rating()` - Calculate average driver rating
- `update_ride_rating()` - Store rider rating
- `toggle_driver_mode()` - Change driver availability

#### Helper Class
- `display_header()` - Format section headers
- `display_user_info()` - Show user information
- `display_driver_info()` - Show driver information
- `display_ride_details()` - Show detailed ride information
- `display_rides_table()` - Format rides as table
- `display_driver_rating()` - Show rating with stars
- Validation functions for email, phone, rating

#### RideshareApp Class
- Main application controller
- Handles user authentication
- Manages driver and rider workflows
- Clean menu-driven interface

### Security Features
- SQL injection prevention through parameterized queries
- Input validation and sanitization
- Safe error handling with database rollback
- Password authentication (basic implementation)

## Testing

### Test Accounts

After running `sample_data.py`, you can use these test accounts:

**Drivers:**
- Username: `john_doe`, Password: `password123`
- Username: `jane_smith`, Password: `password123`
- Username: `mike_wilson`, Password: `password123`

**Riders:**
- Username: `sarah_jones`, Password: `password123`
- Username: `david_brown`, Password: `password123`
- Username: `emily_davis`, Password: `password123`

### Testing Checklist

- [x] Create new rider account
- [x] Create new driver account
- [x] Login as existing rider
- [x] Login as existing driver
- [x] Driver: View rating (with and without ratings)
- [x] Driver: View all rides
- [x] Driver: Toggle driver mode
- [x] Rider: View all rides
- [x] Rider: Find a driver (when driver is active)
- [x] Rider: Rate a driver
- [x] Error handling for invalid inputs
- [x] Database transaction rollback on errors

## Screenshots

### Application Interface
![Rideshare Application Screenshot](media/Screenshot%202025-11-03%20at%2010.08.14%20PM.png)

*Main application interface showing the rideshare web application*

## Error Handling

- Comprehensive exception handling for database operations
- Input validation for all user inputs
- Graceful error messages and recovery
- Database rollback on failed operations
- Connection error handling with clear messages

## Database Configuration

### Default Settings
- Host: `localhost`
- Database: `rideshare_db`
- User: `root`
- Password: Prompted at runtime

### Custom Configuration

To use different database settings, modify the `DatabaseOperations` initialization in `app.py`:

```python
self.db_ops = DatabaseOperations(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password"
)
```

## Design Decisions

1. **Separate USER, DRIVER, RIDER tables**: Allows users to potentially be both driver and rider, maintains data normalization
2. **ENUM for driver_mode**: Ensures only valid values ('active', 'inactive')
3. **ENUM for ride_status**: Standardizes ride states
4. **Rating CHECK constraint**: Ensures ratings are between 1-5
5. **CASCADE on USER deletion**: Automatically removes associated driver/rider profiles
6. **RESTRICT on RIDE deletion**: Prevents deletion of users with ride history
7. **Dictionary cursor**: Returns results as dictionaries for easier access
8. **Transaction management**: All operations use transactions with rollback on errors

## Known Limitations

1. Password storage: Passwords are stored in plain text (not recommended for production)
2. Authentication: Basic username/password only (no session management)
3. Driver matching: Simple first-available driver selection (no advanced matching)
4. No real-time updates: Driver availability not refreshed in real-time
5. No payment processing: Fare amounts are stored but not processed

## Future Enhancements

- Password hashing (bcrypt)
- Session management
- Advanced driver matching (proximity, rating)
- Real-time location tracking
- Payment integration
- Email notifications
- Mobile app interface

## References

- MySQL 8.0 Documentation
- mysql-connector-python Documentation
- CPSC 408 Course Materials
- Database Design Principles (3NF Normalization)

## Special Instructions

1. Ensure MySQL server is running before starting the application
2. Database schema must be created before running the application
3. Sample data script is optional but recommended for testing
4. All database operations are atomic (all succeed or all fail)
5. Application uses parameterized queries to prevent SQL injection

## Assignment Completion Summary

- [x] ER Diagram created (see IMG_6914.HEIC and IMG_6915.HEIC)
- [x] Database schema designed and implemented
- [x] MySQL database created locally
- [x] Sample data populated for testing
- [x] Interactive Python program with all required features
- [x] All relationships properly implemented
- [x] Database normalized to 3NF
- [x] Referential integrity maintained
- [x] Clean, professional user interface
- [x] Comprehensive error handling
- [x] Complete documentation

