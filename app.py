from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

# Initialize extensions (but don't connect them to app yet)
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_class=Config):
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object(config_class)
    
    # Initialize extensions with this app instance
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Simple test route to verify API is working
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Declutter254 API is running!',
            'status': 'success',
            'version': '1.0'
        })
    
    # Another test route to check database connection later
    @app.route('/health')
    def health_check():
        try:
            # Try to query the database
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            db_status = 'error'
        
        return jsonify({
            'api': 'running',
            'database': db_status,
            'environment': 'development'
        })
    
    return app

# This runs when you execute the file directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)  # debug=True auto-reloads on code changes