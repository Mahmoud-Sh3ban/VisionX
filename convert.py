import tensorflow as tf

# Load the pre-trained EfficientNetB0 model with ImageNet weights
model = tf.keras.applications.EfficientNetB0(weights="imagenet")

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the converted model as efficientnet_b0.tflite
with open("efficientnet_b0.tflite", "wb") as f:
    f.write(tflite_model)

print("Model has been successfully converted and saved as efficientnet_b0.tflite.")
