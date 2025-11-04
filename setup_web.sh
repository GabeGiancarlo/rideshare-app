#!/bin/bash
# Setup script for Rideshare Web Application

echo "Setting up Rideshare Web Application..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Flask..."
pip install Flask mysql-connector-python

echo ""
echo "Setup complete! To run the web application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the app: python3 web_app.py"
echo "3. Open your browser to: http://localhost:8080"

