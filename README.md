
# VisionX: Real-Time Image and Video Classifier

VisionX is a simple web-based computer vision app that enables users to classify images, videos, and live webcam feeds in real-time using a pre-trained **EfficientNetB0** model.

---

## Overview

VisionX aims to simplify the computer vision pipeline by providing a user-friendly interface for real-time image and video classification tasks.

---

## Key Features

- **Image Classification:** Upload images to get predictions and confidence scores.
- **Video Classification:** Classify video frames with overall prediction and average confidence.
- **Webcam Classification:** Real-time prediction using webcam feed.
- **Cloud-Ready:** Designed for cloud deployment using Docker and Kubernetes.

---

## Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/VisionX
   cd VisionX
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the model conversion script:
   ```bash
   python convert.py
   ```
   This script converts the pre-trained EfficientNetB0 model to TensorFlow Lite format.

4. Start the application:
   ```bash
   python app.py
   ```

---

## Usage

1. **Run the Flask app**:
   ```bash
   python app.py
   ```
2. **Open the app** in a browser at:
   `http://127.0.0.1:5000/`
3. **Classify images, videos, or webcam feeds** using the provided interface.

---

## Deployment

### Docker
1. Build the Docker image:
   ```bash
   docker build -t visionx:v1 .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 visionx:v1
   ```

### Kubernetes
1. Push your Docker image to a registry:
   ```bash
   docker push <your-dockerhub-username>/visionx:v1
   ```
2. Deploy on Kubernetes using the provided YAML configuration:
   ```bash
   kubectl apply -f deployment.yaml
   ```
3. Verify deployment and access the app using the provided external IP or URL.

### Updating the Deployment Configuration
Before deploying, update `deployment.yml` with the appropriate values:
   - Replace `<your-docker-image>` and `<version-tag>` with your Docker image URL and tag.
   - Specify `<your-domain>` and `TLS secret` in the Ingress section if you are using HTTPS.

---

## License

This project is licensed under the MIT License.
