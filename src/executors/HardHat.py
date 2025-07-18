import cv2
import torch
import numpy as np
from PIL import Image as PILImage
from pathlib import Path
from typing import List, Dict, Any
from sdks.novavision.src.base.model import Image, Inputs, Configs, Outputs, Response, Request
from ..models.PackageModel import HardHatRequest, HardHatResponse
from ..utils.hardhat_util import HardHatDetector


class HardHat:
    def __init__(self):
        self.detector = HardHatDetector()

    def execute(self, request: HardHatRequest) -> HardHatResponse:
        """Execute hard hat detection on input image"""
        try:
            # Get input image
            input_image = request.inputs.inputImageOne.value

            # Convert to numpy array if needed
            if isinstance(input_image, Image):
                img_array = self._image_to_numpy(input_image)
            else:
                raise ValueError("Input must be an Image object")

            # Get detection parameters
            confidence_threshold = request.configs.hardHatDetectionType.value.confidenceThreshold.value
            iou_threshold = request.configs.hardHatDetectionType.value.iouThreshold.value

            # Perform detection
            results = self.detector.detect(
                img_array,
                confidence_threshold=confidence_threshold,
                iou_threshold=iou_threshold
            )

            # Draw bounding boxes on image
            output_image = self._draw_detections(img_array, results)

            # Convert back to Image object
            output_image_obj = self._numpy_to_image(output_image)

            # Create response
            response = HardHatResponse(
                outputs={
                    "outputImageOne": {
                        "name": "outputImageOne",
                        "value": output_image_obj,
                        "type": "object"
                    }
                }
            )

            return response

        except Exception as e:
            raise Exception(f"Hard hat detection failed: {str(e)}")

    def _image_to_numpy(self, image: Image) -> np.ndarray:
        """Convert Image object to numpy array"""
        # Assuming Image object has image data - adjust based on your Image class structure
        if hasattr(image, 'data'):
            return np.array(image.data)
        elif hasattr(image, 'path'):
            return cv2.imread(image.path)
        else:
            raise ValueError("Cannot convert Image to numpy array")

    def _numpy_to_image(self, img_array: np.ndarray) -> Image:
        """Convert numpy array back to Image object"""
        # Adjust based on your Image class structure
        return Image(data=img_array)

    def _draw_detections(self, img: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """Draw bounding boxes and labels on image"""
        output_img = img.copy()

        for detection in detections:
            bbox = detection['bbox']  # [x1, y1, x2, y2]
            confidence = detection['confidence']
            class_name = detection['class']

            # Draw bounding box
            cv2.rectangle(output_img,
                          (int(bbox[0]), int(bbox[1])),
                          (int(bbox[2]), int(bbox[3])),
                          (0, 255, 0), 2)

            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(output_img, label,
                        (int(bbox[0]), int(bbox[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return output_img