#!/usr/bin/env python
"""
Main entry point for the Algorithmic Trading Application
Run this file to start the Flask server
"""

import os
from app import create_app
from config import config

if __name__ == '__main__':
    # Get environment (development or production)
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create Flask app
    app = create_app(config_name=env)
    
    # Get port from environment or default to 5001 (5000 may be used by AirPlay on macOS)
    port = int(os.getenv('PORT', 5001))
    
    # Run the app
    debug = env == 'development'
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
