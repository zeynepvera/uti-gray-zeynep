"""
    It is one of the preprocessing components in which the image is converted to grayscale.
"""

import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayZeynep.src.utils.response import build_response
from components.GrayZeynep.src.models.PackageModel import PackageModel


class Gray(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.processing_type = self.request.get_param("grayProcessingType")

        if self.processing_type == "BasicProcessing":
            self.blur_kernel = self.request.get_param("BlurKernel")
            self.morphology_enabled = self.request.get_param("MorphologyEnabled")
        elif self.processing_type == "AdvancedProcessing":
            self.gray_scale = self.request.get_param("GrayScale")
            self.gray_contrast = self.request.get_param("GrayContrast")

        self.image = self.request.get_param("inputImageOne")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_blur(self, img, kernel_size):
        """Apply Gaussian blur to the image."""
        if kernel_size > 1:
            return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
        return img

    def apply_morphology(self, img):
        """Apply morphological operations (opening) to clean up the image."""
        kernel = np.ones((3, 3), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    def adjust_brightness_contrast(self, img, brightness=0, contrast=1.0):
        """Adjust brightness and contrast of the image."""
        return cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

    def gray(self, img):
        """
        Convert image to grayscale with different processing methods.
        """
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if self.processing_type == "BasicProcessing":
            if hasattr(self, 'blur_kernel') and self.blur_kernel > 1:
                gray_img = self.apply_blur(gray_img, self.blur_kernel)

            if hasattr(self, 'morphology_enabled') and self.morphology_enabled:
                gray_img = self.apply_morphology(gray_img)

        elif self.processing_type == "AdvancedProcessing":
            if hasattr(self, 'gray_scale') and hasattr(self, 'gray_contrast'):
                brightness = int((self.gray_scale - 50) * 2)  # 0-100 -> -100 ile +100

                contrast = self.gray_contrast

                gray_img = self.adjust_brightness_contrast(gray_img, brightness, contrast)

        return gray_img

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.gray(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)

        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()