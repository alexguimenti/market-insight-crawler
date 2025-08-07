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
from config import current_config

# Configure the app for production
app.config.from_object(current_config)

if __name__ == "__main__":
    app.run(
        host=current_config.HOST,
        port=current_config.PORT,
        debug=current_config.DEBUG,
        threaded=current_config.THREADED if hasattr(current_config, 'THREADED') else False
    )
