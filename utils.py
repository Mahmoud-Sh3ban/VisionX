from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf
from PIL import Image
import cv2
from collections import Counter

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="efficientnet_b0.tflite")
interpreter.allocate_tensors()

def preprocess_image(image):
    """Preprocesses the input image for the TensorFlow Lite EfficientNetB0 model."""
    image = image.convert('RGB')  # Convert image to RGB
    image = image.resize((224, 224))  # EfficientNetB0 input size
    image_array = np.array(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

def classify_image(image):
    """Classifies an image using the TensorFlow Lite model with decoded predictions."""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Preprocess the image and set the input tensor
    image_array = preprocess_image(image)
    interpreter.set_tensor(input_details[0]['index'], image_array)

    # Run inference
    interpreter.invoke()

    # Get the output tensor and reshape it for decode_predictions
    output_data = interpreter.get_tensor(output_details[0]['index'])
    decoded_predictions = tf.keras.applications.efficientnet.decode_predictions(np.expand_dims(output_data[0], axis=0), top=1)

    # Extract the label and confidence
    prediction_label = decoded_predictions[0][0][1]  # Get human-readable label
    confidence = float(decoded_predictions[0][0][2])  # Get confidence as a float
    return prediction_label, confidence

def secure_file_path(file, folder):
    """Saves the uploaded file securely in the specified folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = secure_filename(file.filename)
    filepath = os.path.join(folder, filename)
    file.save(filepath)
    return filepath

def process_video_frames(filepath):
    """Processes video frames and returns classification result for the most common prediction."""
    video_capture = cv2.VideoCapture(filepath)
    frame_count = 0
    predictions = []

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert frame to PIL Image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)

        # Classify the frame
        label, confidence = classify_image(frame_image)
        predictions.append((label, confidence))
        frame_count += 1

    video_capture.release()

    # Aggregate the predictions from all frames
    if predictions:
        most_common_prediction = Counter([pred[0] for pred in predictions]).most_common(1)[0][0]
        avg_confidence = np.mean([pred[1] for pred in predictions])
        return {"prediction": most_common_prediction, "confidence": avg_confidence, "frame_count": frame_count}
    else:
        raise ValueError("No frames could be processed from the video.")
