from flask import Flask
from flask_cors import CORS
from config import config

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS for frontend communication
    CORS(app)
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    return app
