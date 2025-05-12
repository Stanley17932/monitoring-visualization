import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://your-connection-string')
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'