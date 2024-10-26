from locust import HttpUser, task, between
import os

class ImageUploadUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def classify_image(self):
        # Path to the sample image
        image_path = "~/<Path to the sample image>"

        # Read the image file as binary
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            self.client.post("/classify", files=files)
