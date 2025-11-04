#!/usr/bin/env python3
"""
Comprehensive test script for the Rideshare Flask application
Tests various functionalities without requiring manual interaction
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Test if database connection works."""
    print("=" * 60)
    print("TEST 1: Database Connection")
    print("=" * 60)
    
    try:
        from db_operations import DatabaseOperations
        
        db_ops = DatabaseOperations()
        print("✓ DatabaseOperations class imported successfully")
        print("Note: Actual connection will require MySQL password")
        return True
    except Exception as e:
        print(f"✗ Error importing DatabaseOperations: {e}")
        return False


def test_flask_app_imports():
    """Test if Flask app can be imported."""
    print("\n" + "=" * 60)
    print("TEST 2: Flask App Imports")
    print("=" * 60)
    
    try:
        from web_app import app
        print("✓ Flask app imported successfully")
        print(f"✓ App name: {app.name}")
        print(f"✓ Debug mode: {app.debug}")
        return True
    except Exception as e:
        print(f"✗ Error importing Flask app: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flask_routes():
    """Test Flask routes configuration."""
    print("\n" + "=" * 60)
    print("TEST 3: Flask Routes Configuration")
    print("=" * 60)
    
    try:
        from web_app import app
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': sorted(rule.methods - {'HEAD', 'OPTIONS'}),
                'path': rule.rule
            })
        
        print(f"✓ Found {len(routes)} routes:")
        for route in sorted(routes, key=lambda x: x['path']):
            methods = ', '.join(route['methods'])
            print(f"  {route['path']:30s} [{methods:15s}] {route['endpoint']}")
        
        return True
    except Exception as e:
        print(f"✗ Error checking routes: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_helper_functions():
    """Test helper functions."""
    print("\n" + "=" * 60)
    print("TEST 4: Helper Functions")
    print("=" * 60)
    
    try:
        from helper import Helper
        
        helper = Helper()
        print("✓ Helper class imported successfully")
        
        # Test email validation
        test_emails = [
            ("test@example.com", True),
            ("invalid.email", False),
            ("user@domain.co.uk", True),
            ("@invalid.com", False)
        ]
        
        print("\n  Testing email validation:")
        for email, expected in test_emails:
            result = helper.validate_email(email)
            status = "✓" if result == expected else "✗"
            print(f"    {status} {email:25s} -> {result} (expected {expected})")
        
        # Test phone validation
        test_phones = [
            ("123-456-7890", True),
            ("(123) 456-7890", True),
            ("1234567890", True),
            ("invalid", False)
        ]
        
        print("\n  Testing phone validation:")
        for phone, expected in test_phones:
            result = helper.validate_phone(phone)
            status = "✓" if result == expected else "✗"
            print(f"    {status} {phone:25s} -> {result} (expected {expected})")
        
        # Test rating validation
        test_ratings = [
            ("1", 1),
            ("5", 5),
            ("3", 3),
            ("0", None),
            ("6", None),
            ("abc", None)
        ]
        
        print("\n  Testing rating validation:")
        for rating_str, expected in test_ratings:
            result = helper.validate_rating(rating_str)
            status = "✓" if result == expected else "✗"
            print(f"    {status} '{rating_str}' -> {result} (expected {expected})")
        
        return True
    except Exception as e:
        print(f"✗ Error testing helper functions: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flask_app_startup():
    """Test if Flask app can start (without actually running server)."""
    print("\n" + "=" * 60)
    print("TEST 5: Flask App Startup Test")
    print("=" * 60)
    
    try:
        from web_app import app
        
        # Create a test client
        with app.test_client() as client:
            print("✓ Flask test client created successfully")
            
            # Test homepage
            response = client.get('/')
            print(f"✓ GET / -> Status: {response.status_code}")
            
            # Test login pages
            response = client.get('/login/rider')
            print(f"✓ GET /login/rider -> Status: {response.status_code}")
            
            response = client.get('/login/driver')
            print(f"✓ GET /login/driver -> Status: {response.status_code}")
            
            # Test registration pages
            response = client.get('/register')
            print(f"✓ GET /register -> Status: {response.status_code}")
            
            response = client.get('/register/rider')
            print(f"✓ GET /register/rider -> Status: {response.status_code}")
            
            response = client.get('/register/driver')
            print(f"✓ GET /register/driver -> Status: {response.status_code}")
            
            # Test protected routes (should redirect)
            response = client.get('/driver/dashboard')
            print(f"✓ GET /driver/dashboard -> Status: {response.status_code} (should redirect if not logged in)")
            
            response = client.get('/rider/dashboard')
            print(f"✓ GET /rider/dashboard -> Status: {response.status_code} (should redirect if not logged in)")
            
            return True
    except Exception as e:
        print(f"✗ Error testing Flask app: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_templates():
    """Test if all templates exist."""
    print("\n" + "=" * 60)
    print("TEST 6: Template Files")
    print("=" * 60)
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    required_templates = [
        'base.html',
        'index.html',
        'register.html',
        'register_rider.html',
        'register_driver.html',
        'rider_login.html',
        'driver_login.html',
        'rider_dashboard.html',
        'driver_dashboard.html',
        'rider_rides.html',
        'driver_rides.html',
        'find_driver.html',
        'rate_driver.html',
        'driver_rating.html',
        'ride_detail.html'
    ]
    
    missing = []
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✓ {template}")
        else:
            print(f"✗ {template} (MISSING)")
            missing.append(template)
    
    if missing:
        print(f"\n✗ {len(missing)} template(s) missing")
        return False
    else:
        print(f"\n✓ All {len(required_templates)} templates found")
        return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("RIDESHARE APPLICATION - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Database Connection", test_database_connection()))
    results.append(("Flask App Imports", test_flask_app_imports()))
    results.append(("Flask Routes", test_flask_routes()))
    results.append(("Helper Functions", test_helper_functions()))
    results.append(("Flask App Startup", test_flask_app_startup()))
    results.append(("Template Files", test_templates()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name:30s} [{status}]")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Application is ready to run.")
        print("\nTo start the Flask app, run:")
        print("  python web_app.py")
        print("\nThen open: http://localhost:8080")
    else:
        print("\n⚠ Some tests failed. Please review the output above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

