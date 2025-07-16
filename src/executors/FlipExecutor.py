"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayZeynep.src.utils.response import build_response_flip
from components.GrayZeynep.src.models.PackageModel import PackageModel


class FlipExecutor(Component):
    def __init__(self, request, bootstrap):


        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))


        self.flip_code = self.request.get_param("flipCode")
        self.brightness = self.request.get_param("Brightness")

        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

        # Dependent dropdown parametreleri
        self.flip_process_type = self.request.get_param("flipProcessType")
        self.load_flip_parameters()

    def load_flip_parameters(self):
        """Seçilen flip process type'a göre parametreleri yükle"""
        if self.flip_process_type == "Simple":
            self.contrast = self.request.get_param("contrast")
        elif self.flip_process_type == "Advanced":
            self.gamma = self.request.get_param("gamma")
            self.noise_level = self.request.get_param("noise_level")
            self.blur_strength = self.request.get_param("blur_strength")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def add_noise(self, img, noise_level):
        """Add gaussian noise to image"""
        if noise_level > 0:
            noise = np.random.normal(0, noise_level, img.shape).astype(np.uint8)
            return cv2.add(img, noise)
        return img

    def apply_gamma_correction(self, img, gamma):
        """Apply gamma correction to image"""
        if gamma != 1.0:
            inv_gamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            return cv2.LUT(img, table)
        return img

    def flip(self, img):
        """
        Flip image based on selected process type.
        """
        # Basic flip operation
        flipped = cv2.flip(img, self.flip_code)

        # Apply brightness adjustment
        if self.brightness != 0:
            flipped = cv2.convertScaleAbs(flipped, alpha=1, beta=self.brightness)

        # Apply process type specific operations
        if self.flip_process_type == "Simple":
            # Simple mode: only contrast adjustment
            if self.contrast != 1.0:
                flipped = cv2.convertScaleAbs(flipped, alpha=self.contrast, beta=0)

        elif self.flip_process_type == "Advanced":
            # Advanced mode: gamma correction, noise, and blur
            flipped = self.apply_gamma_correction(flipped, self.gamma)
            flipped = self.add_noise(flipped, self.noise_level)

            if self.blur_strength > 0:
                kernel_size = self.blur_strength * 2 + 1
                flipped = cv2.GaussianBlur(flipped, (kernel_size, kernel_size), 0)

        return flipped


    def run(self):

        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        img1.value = self.flip(img1.value)
        img2.value = self.flip(img2.value)

        self.imageOne = Image.set_frame(
            img=img1,
            package_uID=self.uID,
            redis_db=self.redis_db,
        )

        self.imageTwo = Image.set_frame(
            img=img2,
            package_uID=self.uID,
            redis_db=self.redis_db,
        )



        packageModel = build_response_flip(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
