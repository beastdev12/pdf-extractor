from flask import Blueprint, request, jsonify, send_from_directory, config
from flask_cors import CORS, cross_origin
import os
from app.utils import process_pdf
import logging

logging.basicConfig(level=logging.INFO)  # or INFO
logger = logging.getLogger(__name__)
main = Blueprint('app', __name__)

cors = CORS(main)


@main.route('/upload', methods=['POST'])
def upload_file():
    print("request Recieved")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = os.path.join('uploads', file.filename)
        file.save(filename)
        excel_path = process_pdf(filename)
        return jsonify({'downloadUrl': f'/download/{os.path.basename(excel_path)}'})

    return jsonify({'error': 'File processing failed'}), 500

@main.route('/download/<path:filename>', methods=['GET'])
@cross_origin()
def download_file(filename):
    # Construct the full file path
    file_path = os.path.join('uploads', filename)
    logger.info("Request recieved")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    # If the file exists, send it as an attachment
    return send_from_directory(os.path.join('..', 'uploads'), filename)
