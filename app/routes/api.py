import pandas as pd
from io import StringIO
from flask import Blueprint, request, jsonify
from uuid import uuid4
from app import db
from app.models.request import ProcessingRequest
from app.services.image_processing import process_images
import logging

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@api_bp.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    try:
        csv_data = file.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))

        if 'Product Name' not in df.columns or 'Input Image Urls' not in df.columns:
            return jsonify({'error': 'CSV file must contain "Product Name" and "Input Image Urls" columns'}), 400

        request_ids = []
        for index, row in df.iterrows():
            request_id = str(uuid4())
            product_name = row['Product Name']
            input_urls = row['Input Image Urls'].split(', ')  # Split URLs by comma and space

            if pd.isna(product_name) or not input_urls:
                logger.error(f"Missing product name or input image URLs at row {index}")
                return jsonify({'error': f'Missing product name or input image URLs at row {index}'}), 400

            new_request = ProcessingRequest(
                request_id=request_id,
                product_name=product_name,
                input_urls=', '.join(input_urls)
            )
            db.session.add(new_request)
            request_ids.append(request_id)
        
        db.session.commit()
        logger.info(f"Requests created with IDs: {request_ids}")

        for request_id in request_ids:
            process_images.delay(request_id)

        return jsonify({'request_id': request_ids[0]}), 202

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        logger.error(f"Error uploading CSV: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500




@api_bp.route('/status/<request_id>', methods=['GET'])
def check_status(request_id):
    request = ProcessingRequest.query.filter_by(request_id=request_id).first()
    if not request:
        return jsonify({'error': 'Request not found'}), 404
    
    return jsonify({
        'request_id': request_id,
        'status': request.status,
        'output_urls': request.output_urls
    })
