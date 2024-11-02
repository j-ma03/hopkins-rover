import torch
from PIL import Image

import matplotlib.pyplot as plt

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/Users/jaydenma/Documents/mars rover/hopkins-rover/hammer_bottle detection/best.pt')

# Function to detect objects in an image
def detect_objects(image_path):
    # Load the image
    img = Image.open(image_path)
    
    # Perform inference
    results = model(img)
    
    # Print results
    results.print()
    
    # Show results
    results.show()

# Example usage
image_path = '/Users/jaydenma/Documents/mars rover/hopkins-rover/hammer_bottle detection/training images outside malone/IMG_2878.JPG'
detect_objects(image_path)