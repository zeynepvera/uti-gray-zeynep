import torch
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
import os


class HardHatDetector:
    def __init__(self, model_path: str = None):
        """Initialize HardHat detector with YOLOv5 model"""
        if model_path is None:
            # Default path to your model in storage
            model_path = Path(__file__).parent.parent.parent.parent / "storage" / "best.pt"

        self.model_path = model_path
        self.model = None
        self.device = None
        self.class_names = ['hardhat', 'no-hardhat', 'person']  # Adjust based on your model's classes
        self._load_model()

    def _load_model(self):
        """Load YOLOv5 model"""
        try:
            # Check if CUDA is available
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

            # Load YOLOv5 model
            self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                        path=str(self.model_path),
                                        device=self.device)

            # Set model to evaluation mode
            self.model.eval()

            print(f"Model loaded successfully on {self.device}")

        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

    def detect(self,
               image: np.ndarray,
               confidence_threshold: float = 0.5,
               iou_threshold: float = 0.45) -> List[Dict[str, Any]]:
        """
        Detect hard hats in image

        Args:
            image: Input image as numpy array
            confidence_threshold: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS

        Returns:
            List of detection dictionaries with bbox, confidence, and class
        """
        try:
            # Set model parameters
            self.model.conf = confidence_threshold
            self.model.iou = iou_threshold

            # Convert BGR to RGB if needed (OpenCV uses BGR, YOLOv5 expects RGB)
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image

            # Run inference
            results = self.model(image_rgb)

            # Parse results
            detections = []

            # results.pandas().xyxy[0] gives pandas DataFrame with detections
            if len(results.pandas().xyxy[0]) > 0:
                for _, detection in results.pandas().xyxy[0].iterrows():
                    bbox = [detection['xmin'], detection['ymin'],
                            detection['xmax'], detection['ymax']]
                    confidence = detection['confidence']
                    class_id = int(detection['class'])
                    class_name = detection['name']

                    detections.append({
                        'bbox': bbox,
                        'confidence': confidence,
                        'class_id': class_id,
                        'class': class_name
                    })

            return detections

        except Exception as e:
            raise Exception(f"Detection failed: {str(e)}")

    def preprocess_image(self, image: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
        """
        Preprocess image for YOLOv5

        Args:
            image: Input image
            target_size: Target size for model input

        Returns:
            Preprocessed image
        """
        # Resize image while maintaining aspect ratio
        h, w = image.shape[:2]
        scale = min(target_size[0] / w, target_size[1] / h)
        new_w, new_h = int(w * scale), int(h * scale)

        # Resize
        resized = cv2.resize(image, (new_w, new_h))

        # Create padded image
        padded = np.full((target_size[1], target_size[0], 3), 114, dtype=np.uint8)

        # Calculate padding
        pad_x = (target_size[0] - new_w) // 2
        pad_y = (target_size[1] - new_h) // 2

        # Place resized image in center
        padded[pad_y:pad_y + new_h, pad_x:pad_x + new_w] = resized

        return padded

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            'model_path': str(self.model_path),
            'device': str(self.device),
            'class_names': self.class_names,
            'model_loaded': self.model is not None
        }