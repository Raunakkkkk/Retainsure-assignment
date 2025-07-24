#!/usr/bin/env python3
"""
Simple script to run the URL Shortener application.
Usage: python run.py
"""

import sys
import os

# Add the current directory to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == '__main__':
    print("Server will be running at: http://localhost:5000")
    print("API Documentation:")
    print("   - POST /api/shorten - Shorten a URL")
    print("   - GET /<short_code> - Redirect to original URL") 
    print("   - GET /api/stats/<short_code> - Get analytics")
    print("   - GET /api/health - Health check")
    print("\n" + "="*50)
    
    app.run(host='0.0.0.0', port=5000, debug=True) 