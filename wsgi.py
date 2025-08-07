#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Configure the app for production
app.config['DEBUG'] = False
app.config['TESTING'] = False

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=False,
        threaded=True
    )
