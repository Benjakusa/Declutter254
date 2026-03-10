import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for sessions - in production, always use environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - using SQLite for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///declutter.db'
    
    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False