from app.services.image_processing import celery

if __name__ == '__main__':
    celery.start()
