#!/usr/bin/env python3
"""
Test script to verify if the Flask application is working correctly
"""

import requests
import time
import sys

def test_flask_app():
    """Tests if the Flask application is running"""
    try:
        # Test if server is responding
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Flask server is running at http://localhost:5000")
            print("🌐 Access the web interface in your browser")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server")
        print("💡 Make sure the server is running with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def test_imports():
    """Tests if all dependencies are installed"""
    try:
        import flask
        import requests
        import bs4
        import openai
        import google.generativeai as genai
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    print("🔍 Testing Market Insight Crawler...")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Test server
    if not test_flask_app():
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 All tests passed!")
    print("🚀 The application is ready to use!") 