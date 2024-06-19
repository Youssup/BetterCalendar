import os
import json
from shutil import copyfile
from dotenv import load_dotenv

load_dotenv()

credentials_folder = '.credentials'
if not os.path.exists(credentials_folder):
    os.makedirs(credentials_folder)

credentials_path = os.path.join(credentials_folder, 'credentials.json')

if not os.path.exists(credentials_path):
    source_credentials_path = os.getenv('CREDENTIALS_PATH')
    copyfile(source_credentials_path, credentials_path)

class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    CREDENTIALS_PATH = credentials_path
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = json.loads(os.getenv('SECRET_KEY'))

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}
