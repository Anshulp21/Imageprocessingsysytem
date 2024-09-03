pip install -r requiremnts.txt


flask --app app.main run  


celery -A app.services.image_processing.celery worker --loglevel=info


.\venv\Scripts\Activate
       
