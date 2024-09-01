from celery import Celery
from PIL import Image
import requests
from io import BytesIO
import os
from app import db
from app.models.request import ProcessingRequest
from app.config import Config
import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Celery instance
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
celery.conf.update(
    result_backend=Config.CELERY_RESULT_BACKEND,
    broker_url=Config.CELERY_BROKER_URL,
)

@celery.task
def process_images(request_id):
    try:
        request = ProcessingRequest.query.filter_by(request_id=request_id).first()
        if not request:
            logger.error(f"Request with ID {request_id} not found.")
            return
        
        logger.info(f"Processing request with ID {request_id}")
        input_urls = request.input_urls.split(',')
        output_urls = []
        
        for url in input_urls:
            try:
                response = requests.get(url.strip())
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                output_path = os.path.join(Config.PROCESSED_FOLDER, os.path.basename(url.strip()))
                
                if not os.path.exists(Config.PROCESSED_FOLDER):
                    os.makedirs(Config.PROCESSED_FOLDER)
                
                img.save(output_path, quality=50)
                output_urls.append(output_path)
            except Exception as e:
                logger.error(f"Error processing image {url}: {e}", exc_info=True)
        
        request.output_urls = ','.join(output_urls)
        request.status = 'Completed'
        db.session.commit()

        # Call the webhook endpoint
        webhook_url = 'https://thundering-artist-39.webhook.cool'   
        payload = {
            'request_id': request_id,
            'status': 'Completed',
            'output_urls': request.output_urls
        }
        requests.post(webhook_url, json=payload)
        
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {e}", exc_info=True)
