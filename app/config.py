import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///image_processing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    UPLOAD_FOLDER = 'uploads/'
    PROCESSED_FOLDER = 'processed/'
    
    # Increase the SQLite timeout to handle potential locking issues
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 15  # Increase timeout to 15 seconds
        }
    }

config = Config()
