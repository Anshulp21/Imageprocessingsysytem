from flask import Blueprint, request, jsonify

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('', methods=['POST'])
def webhook():
    data = request.json
    # Handle the webhook payload here
    print("Received webhook payload:", data)
    return jsonify({'status': 'received'}), 200
