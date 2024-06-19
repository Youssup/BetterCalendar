import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = json.loads(os.getenv('SECRET_KEY'))

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}
