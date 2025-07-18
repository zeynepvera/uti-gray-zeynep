import os
from ultralytics import YOLO

# Model path
MODEL_PATH = "/storage/best.pt"

def load_model():
    if os.path.isfile(MODEL_PATH):
        model = YOLO(MODEL_PATH)
        print("Model loads successfully.")
    else:
        raise FileNotFoundError(f"Model files couldnt found: {MODEL_PATH}")

    return model
