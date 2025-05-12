from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import mongo, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    
    # Import and register blueprints
    from routes.metrics import metrics
    from routes.alerts import alerts
    from routes.auth import auth
    
    app.register_blueprint(metrics, url_prefix='/api')
    app.register_blueprint(alerts, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/api/auth')
    
    @app.route('/health')
    def health_check():
        try:
            # Attempt to connect to MongoDB
            mongo.db.command('ping')
            return {"status": "healthy", "database": "connected"}
        except Exception as e:
            return {"status": "unhealthy", "database": str(e)}, 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
