from flask import Flask, render_template, request, jsonify
from utils import classify_image, secure_file_path, process_video_frames
from PIL import Image
import numpy as np
import io
import os
import time
import logging
import concurrent.futures
import cv2
from collections import Counter

# Initialize Flask app and set static folder for serving static files
app = Flask(__name__, static_folder='static')

# Configure logging to output information to standard output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define route for the main index page
@app.route('/')
def index():
    logger.info("Serving the index page.")
    return render_template('index.html')

# Define route for live camera feed (camera.html)
@app.route('/camera.html')
def camera_page():
    return render_template('camera.html')

# Define route for image classification
@app.route('/image', methods=['POST'])
def classify_image_route():
    # Check if an image file is provided in the request
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('index.html', error="image: Please upload an image.")

    file = request.files['file']
    try:
        # Open the image and perform classification
        image = Image.open(file.stream)
        start_time = time.time()
        prediction, confidence = classify_image(image)  # Call to classification function
        inference_time = time.time() - start_time  # Calculate time taken for inference
        return render_template('index.html', prediction=prediction, confidence=confidence, inference_time=inference_time)
    except Exception as e:
        # Log any errors and return error message
        logger.error(f"Error processing image: {e}")
        return render_template('index.html', error=f"image: {str(e)}")

# Define route for video classification
@app.route('/video', methods=['POST'])
def classify_video_route():
    # Check if a video file is provided in the request
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('index.html', error="video: Please upload a video file.")

    file = request.files['file']
    filepath = secure_file_path(file, 'uploads')  # Securely store the file path

    try:
        # Process video frames asynchronously using thread pool
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(process_video_frames, filepath)
            result = future.result()
        return render_template('index.html', **result)
    except Exception as e:
        # Log any errors and return error message
        logger.error(f"Error processing video: {e}")
        return render_template('index.html', error=f"video: {str(e)}")

# Define route for webcam frame classification
@app.route('/camera', methods=['POST'])
def classify_webcam_frame():
    # Ensure a file is provided in the request
    if 'file' not in request.files:
        logger.error("No file provided in request")
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    try:
        # Open the image and classify it
        image = Image.open(file.stream)
        prediction, confidence = classify_image(image)  # Call to classification function

        # Log and return the classification result
        logger.info(f"Prediction: {prediction}, Confidence: {confidence}")
        return jsonify({"prediction": prediction, "confidence": float(confidence)})
    except Exception as e:
        # Log any errors and return error message as JSON
        logger.error(f"Error during classification: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app on the specified host and port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

