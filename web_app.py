#!/usr/bin/env python3
"""
CPSC 408 Assignment 05 - Rideshare Web Application
Flask web application for the rideshare management system.

Authors:
- Gabe Giancarlo (2405449) - giancarlo@chapman.edu
- Gustavo de Moraes (002427902) - demoraes@chapman.edu
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from db_operations import DatabaseOperations
from helper import Helper
import os
import getpass
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'rideshare-secret-key-change-in-production')

# Global database connection (will be initialized on first request)
db_ops = None
helper = Helper()


def init_db():
    """Initialize database connection."""
    global db_ops
    if db_ops is None:
        try:
            db_ops = DatabaseOperations()
            if not db_ops.connect():
                print("Warning: Database connection failed")
                db_ops = None
                return None
            # Verify cursor is initialized
            if db_ops.cursor is None:
                print("Warning: Database cursor is None")
                db_ops = None
                return None
        except Exception as e:
            print(f"Database connection error: {e}")
            db_ops = None
            return None
    
    # Double-check cursor is still valid
    if db_ops is not None and db_ops.cursor is None:
        print("Warning: Database cursor became None, reconnecting...")
        try:
            if db_ops.connect():
                return db_ops
            else:
                db_ops = None
                return None
        except Exception as e:
            print(f"Reconnection failed: {e}")
            db_ops = None
            return None
    
    return db_ops


@app.before_request
def before_request():
    """Initialize database before each request."""
    logger.debug(f"before_request() - db_ops is None: {db_ops is None}")
    # Skip database init for static files or if already connected
    # Only initialize if not already connected
    if db_ops is None:
        logger.debug("db_ops is None, calling init_db()")
        try:
            result = init_db()
            logger.debug(f"init_db() returned: {result is not None}")
            if result is None:
                logger.warning("Database initialization failed in before_request")
        except Exception as e:
            # Don't block requests if DB connection fails
            logger.exception(f"Exception in before_request during DB init: {e}")
            pass
    else:
        logger.debug(f"db_ops already exists, cursor status: {db_ops.cursor is not None if hasattr(db_ops, 'cursor') else 'N/A'}")


@app.teardown_appcontext
def close_db(error):
    """Close database connection after each request."""
    pass


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Main page - redirects to login/home."""
    # Check database connection
    if db_ops is None:
        init_db()
        if db_ops is None:
            flash('Database connection failed. Please ensure MySQL is running and the database is created.', 'error')
    
    if 'user_id' in session:
        user_type = session.get('user_type')
        if user_type == 'driver':
            return redirect(url_for('driver_dashboard'))
        elif user_type == 'rider':
            return redirect(url_for('rider_dashboard'))
    return render_template('index.html')


@app.route('/login/rider', methods=['GET', 'POST'])
def rider_login():
    """Rider login page."""
    if request.method == 'POST':
        if db_ops is None:
            flash('Database connection failed. Please ensure MySQL is running.', 'error')
            return render_template('rider_login.html')
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('rider_login.html')
        
        user = db_ops.authenticate_user(username, password)
        if not user:
            flash('Invalid username or password.', 'error')
            return render_template('rider_login.html')
        
        rider = db_ops.get_rider_by_user_id(user['user_id'])
        if not rider:
            flash('No rider profile found for this user.', 'error')
            return render_template('rider_login.html')
        
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        session['user_type'] = 'rider'
        session['profile_id'] = rider['rider_id']
        
        return redirect(url_for('rider_dashboard'))
    
    return render_template('rider_login.html')


@app.route('/login/driver', methods=['GET', 'POST'])
def driver_login():
    """Driver login page."""
    if request.method == 'POST':
        if db_ops is None or db_ops.cursor is None:
            flash('Database connection failed. Please ensure MySQL is running and the database is created.', 'error')
            return render_template('driver_login.html')
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('driver_login.html')
        
        user = db_ops.authenticate_user(username, password)
        if not user:
            flash('Invalid username or password.', 'error')
            return render_template('driver_login.html')
        
        driver = db_ops.get_driver_by_user_id(user['user_id'])
        if not driver:
            flash('No driver profile found for this user.', 'error')
            return render_template('driver_login.html')
        
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        session['user_type'] = 'driver'
        session['profile_id'] = driver['driver_id']
        
        return redirect(url_for('driver_dashboard'))
    
    return render_template('driver_login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        
        if account_type == 'rider':
            return redirect(url_for('register_rider'))
        elif account_type == 'driver':
            return redirect(url_for('register_driver'))
    
    return render_template('register.html')


@app.route('/register/rider', methods=['GET', 'POST'])
def register_rider():
    """Rider registration page."""
    if request.method == 'POST':
        if db_ops is None or db_ops.cursor is None:
            flash('Database connection failed. Please ensure MySQL is running and the database is created.', 'error')
            return render_template('register_rider.html')
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_info = request.form.get('payment_info', '').strip()
        preferred_payment = request.form.get('preferred_payment', '').strip()
        credit_card_last4 = request.form.get('credit_card_last4', '').strip()
        default_location = request.form.get('default_location', '').strip()
        
        # Validation
        if not username or not password or not email or not full_name:
            flash('Please fill in all required fields.', 'error')
            return render_template('register_rider.html')
        
        if not helper.validate_email(email):
            flash('Invalid email format.', 'error')
            return render_template('register_rider.html')
        
        if phone_number and not helper.validate_phone(phone_number):
            flash('Invalid phone number format.', 'error')
            return render_template('register_rider.html')
        
        # Check if username exists
        try:
            if db_ops.get_user_by_username(username):
                flash('Username already exists. Please choose another.', 'error')
                return render_template('register_rider.html')
        except AttributeError:
            flash('Database connection error. Please try again.', 'error')
            return render_template('register_rider.html')
        
        # Create user
        user_id = db_ops.create_user(username, password, email, phone_number or None, full_name)
        if not user_id:
            flash('Failed to create user account.', 'error')
            return render_template('register_rider.html')
        
        # Create rider profile
        rider_id = db_ops.create_rider(
            user_id,
            payment_info or None,
            preferred_payment or None,
            credit_card_last4 or None,
            default_location or None
        )
        
        if rider_id:
            flash('Rider account created successfully! You can now log in.', 'success')
            return redirect(url_for('rider_login'))
        else:
            flash('Failed to create rider profile.', 'error')
            return render_template('register_rider.html')
    
    return render_template('register_rider.html')


@app.route('/register/driver', methods=['GET', 'POST'])
def register_driver():
    """Driver registration page."""
    logger.debug(f"register_driver() - method: {request.method}")
    logger.debug(f"db_ops is None: {db_ops is None}")
    logger.debug(f"db_ops.cursor is None: {db_ops.cursor is None if db_ops else 'N/A'}")
    
    if request.method == 'POST':
        if db_ops is None:
            logger.error("POST /register/driver - db_ops is None")
            flash('Database connection failed. Please ensure MySQL is running and the database is created.', 'error')
            return render_template('register_driver.html')
        
        if not hasattr(db_ops, 'cursor') or db_ops.cursor is None:
            logger.error("POST /register/driver - db_ops.cursor is None")
            logger.error(f"db_ops object: {db_ops}")
            logger.error(f"db_ops.connection: {db_ops.connection if hasattr(db_ops, 'connection') else 'N/A'}")
            flash('Database connection failed. Please ensure MySQL is running and the database is created.', 'error')
            return render_template('register_driver.html')
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        license_number = request.form.get('license_number', '').strip()
        license_expiry = request.form.get('license_expiry', '').strip()
        vehicle_make = request.form.get('vehicle_make', '').strip()
        vehicle_model = request.form.get('vehicle_model', '').strip()
        vehicle_year = request.form.get('vehicle_year', '').strip()
        vehicle_color = request.form.get('vehicle_color', '').strip()
        license_plate = request.form.get('license_plate', '').strip()
        insurance_number = request.form.get('insurance_number', '').strip()
        
        # Validation
        if not username or not password or not email or not full_name or not license_number:
            flash('Please fill in all required fields.', 'error')
            return render_template('register_driver.html')
        
        if not helper.validate_email(email):
            flash('Invalid email format.', 'error')
            return render_template('register_driver.html')
        
        # Check if username exists
        logger.debug(f"Checking if username '{username}' exists")
        try:
            existing_user = db_ops.get_user_by_username(username)
            logger.debug(f"get_user_by_username() returned: {existing_user}")
            if existing_user:
                logger.info(f"Username '{username}' already exists")
                flash('Username already exists. Please choose another.', 'error')
                return render_template('register_driver.html')
        except AttributeError as e:
            logger.exception(f"AttributeError when checking username: {e}")
            logger.error(f"db_ops state - connection: {db_ops.connection if hasattr(db_ops, 'connection') else 'N/A'}, cursor: {db_ops.cursor if hasattr(db_ops, 'cursor') else 'N/A'}")
            flash('Database connection error. Please try again.', 'error')
            return render_template('register_driver.html')
        except Exception as e:
            logger.exception(f"Exception when checking username: {e}")
            flash('Database error occurred. Please try again.', 'error')
            return render_template('register_driver.html')
        
        # Create user
        logger.debug(f"Creating user: {username}, {email}, {full_name}")
        try:
            user_id = db_ops.create_user(username, password, email, phone_number or None, full_name)
            logger.debug(f"create_user() returned: {user_id}")
            if not user_id:
                logger.error("create_user() returned None")
                flash('Failed to create user account.', 'error')
                return render_template('register_driver.html')
        except Exception as e:
            logger.exception(f"Exception when creating user: {e}")
            flash('Failed to create user account. Please try again.', 'error')
            return render_template('register_driver.html')
        
        # Convert vehicle year
        vehicle_year_int = None
        if vehicle_year:
            try:
                vehicle_year_int = int(vehicle_year)
            except ValueError:
                pass
        
        # Create driver profile
        driver_id = db_ops.create_driver(
            user_id,
            license_number,
            license_expiry or None,
            vehicle_make or None,
            vehicle_model or None,
            vehicle_year_int,
            vehicle_color or None,
            license_plate or None,
            insurance_number or None
        )
        
        if driver_id:
            flash('Driver account created successfully! You can now log in.', 'success')
            return redirect(url_for('driver_login'))
        else:
            flash('Failed to create driver profile.', 'error')
            return render_template('register_driver.html')
    
    return render_template('register_driver.html')


@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))


# ==================== DRIVER ROUTES ====================

@app.route('/driver/dashboard')
def driver_dashboard():
    """Driver dashboard."""
    if 'user_id' not in session or session.get('user_type') != 'driver':
        flash('Please log in as a driver to access this page.', 'error')
        return redirect(url_for('driver_login'))
    
    driver_id = session['profile_id']
    driver = db_ops.get_driver_by_id(driver_id)
    user = db_ops.get_user_by_id(session['user_id'])
    
    return render_template('driver_dashboard.html', driver=driver, user=user)


@app.route('/driver/rating')
def driver_rating():
    """View driver rating."""
    if 'user_id' not in session or session.get('user_type') != 'driver':
        flash('Please log in as a driver to access this page.', 'error')
        return redirect(url_for('driver_login'))
    
    driver_id = session['profile_id']
    rating = db_ops.get_driver_rating(driver_id)
    
    return render_template('driver_rating.html', rating=rating)


@app.route('/driver/rides')
def driver_rides():
    """View driver rides."""
    if 'user_id' not in session or session.get('user_type') != 'driver':
        flash('Please log in as a driver to access this page.', 'error')
        return redirect(url_for('driver_login'))
    
    driver_id = session['profile_id']
    rides = db_ops.get_driver_rides(driver_id)
    
    return render_template('driver_rides.html', rides=rides)


@app.route('/driver/rides/<int:ride_id>')
def driver_ride_detail(ride_id):
    """View specific ride details."""
    if 'user_id' not in session or session.get('user_type') != 'driver':
        flash('Please log in as a driver to access this page.', 'error')
        return redirect(url_for('driver_login'))
    
    driver_id = session['profile_id']
    rides = db_ops.get_driver_rides(driver_id)
    ride = next((r for r in rides if r['ride_id'] == ride_id), None)
    
    if not ride:
        flash('Ride not found.', 'error')
        return redirect(url_for('driver_rides'))
    
    return render_template('ride_detail.html', ride=ride, user_type='driver')


@app.route('/driver/toggle-mode', methods=['POST'])
def driver_toggle_mode():
    """Toggle driver mode."""
    if 'user_id' not in session or session.get('user_type') != 'driver':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    driver_id = session['profile_id']
    if db_ops.toggle_driver_mode(driver_id):
        driver = db_ops.get_driver_by_id(driver_id)
        return jsonify({
            'success': True,
            'mode': driver['driver_mode']
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to update mode'}), 500


# ==================== RIDER ROUTES ====================

@app.route('/rider/dashboard')
def rider_dashboard():
    """Rider dashboard."""
    if 'user_id' not in session or session.get('user_type') != 'rider':
        flash('Please log in as a rider to access this page.', 'error')
        return redirect(url_for('rider_login'))
    
    rider_id = session['profile_id']
    user = db_ops.get_user_by_id(session['user_id'])
    
    return render_template('rider_dashboard.html', user=user)


@app.route('/rider/rides')
def rider_rides():
    """View rider rides."""
    if 'user_id' not in session or session.get('user_type') != 'rider':
        flash('Please log in as a rider to access this page.', 'error')
        return redirect(url_for('rider_login'))
    
    rider_id = session['profile_id']
    rides = db_ops.get_rider_rides(rider_id)
    
    return render_template('rider_rides.html', rides=rides)


@app.route('/rider/rides/<int:ride_id>')
def rider_ride_detail(ride_id):
    """View specific ride details."""
    if 'user_id' not in session or session.get('user_type') != 'rider':
        flash('Please log in as a rider to access this page.', 'error')
        return redirect(url_for('rider_login'))
    
    rider_id = session['profile_id']
    ride = db_ops.get_ride_by_id(ride_id, rider_id)
    
    if not ride:
        flash('Ride not found.', 'error')
        return redirect(url_for('rider_rides'))
    
    return render_template('ride_detail.html', ride=ride, user_type='rider')


@app.route('/rider/find-driver', methods=['GET', 'POST'])
def rider_find_driver():
    """Find a driver and create ride."""
    if 'user_id' not in session or session.get('user_type') != 'rider':
        flash('Please log in as a rider to access this page.', 'error')
        return redirect(url_for('rider_login'))
    
    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '').strip()
        dropoff_location = request.form.get('dropoff_location', '').strip()
        pickup_address = request.form.get('pickup_address', '').strip()
        dropoff_address = request.form.get('dropoff_address', '').strip()
        fare_amount = request.form.get('fare_amount', '').strip()
        
        if not pickup_location or not dropoff_location:
            flash('Please provide both pickup and dropoff locations.', 'error')
            return render_template('find_driver.html')
        
        # Find active driver
        driver = db_ops.get_active_driver()
        if not driver:
            flash('No active drivers available at the moment. Please try again later.', 'error')
            return render_template('find_driver.html')
        
        # Convert fare
        fare = None
        if fare_amount:
            try:
                fare = float(fare_amount)
            except ValueError:
                pass
        
        # Create ride
        rider_id = session['profile_id']
        ride_id = db_ops.create_ride(
            driver['driver_id'],
            rider_id,
            pickup_location,
            dropoff_location,
            pickup_address or None,
            dropoff_address or None,
            fare
        )
        
        if ride_id:
            flash('Ride created successfully!', 'success')
            return redirect(url_for('rider_ride_detail', ride_id=ride_id))
        else:
            flash('Failed to create ride.', 'error')
            return render_template('find_driver.html')
    
    return render_template('find_driver.html')


@app.route('/rider/rate', methods=['GET', 'POST'])
def rider_rate():
    """Rate a driver for a ride."""
    if 'user_id' not in session or session.get('user_type') != 'rider':
        flash('Please log in as a rider to access this page.', 'error')
        return redirect(url_for('rider_login'))
    
    rider_id = session['profile_id']
    
    if request.method == 'POST':
        ride_id = request.form.get('ride_id', '').strip()
        rating = request.form.get('rating', '').strip()
        rating_comment = request.form.get('rating_comment', '').strip()
        
        if not ride_id or not rating:
            flash('Please select a ride and provide a rating.', 'error')
            return redirect(url_for('rider_rate'))
        
        rating_int = helper.validate_rating(rating)
        if not rating_int:
            flash('Invalid rating. Please enter a number between 1 and 5.', 'error')
            return redirect(url_for('rider_rate'))
        
        try:
            ride_id_int = int(ride_id)
        except ValueError:
            flash('Invalid ride ID.', 'error')
            return redirect(url_for('rider_rate'))
        
        if db_ops.update_ride_rating(ride_id_int, rider_id, rating_int, rating_comment or None):
            flash('Rating submitted successfully!', 'success')
            return redirect(url_for('rider_rides'))
        else:
            flash('Failed to submit rating.', 'error')
            return redirect(url_for('rider_rate'))
    
    # GET request - show form
    most_recent_ride = db_ops.get_rider_most_recent_ride(rider_id)
    all_rides = db_ops.get_rider_rides(rider_id)
    
    return render_template('rate_driver.html', most_recent_ride=most_recent_ride, all_rides=all_rides)


if __name__ == '__main__':
    try:
        port = 8080  # Use 8080 to avoid conflicts with AirPlay and other services
        print("Starting Rideshare Web Application...")
        print(f"Access the application at: http://localhost:{port}")
        app.run(debug=True, host='127.0.0.1', port=port)
    except Exception as e:
        print(f"Error starting server: {e}")

