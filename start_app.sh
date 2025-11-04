#!/bin/bash
# Startup script for Rideshare Flask application
# Sets MySQL password to empty (since MySQL was installed without password)

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Set MySQL password to empty (for MySQL installed without password)
export MYSQL_PASSWORD=""

# Start Flask app
echo "Starting Rideshare Web Application..."
echo "Access at: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python web_app.py

