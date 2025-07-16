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
from components.GrayZeynep.src.utils.response import build_response
from components.GrayZeynep.src.models.PackageModel import PackageModel


class GrayZeynepExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.rotation_degree = self.request.get_param("Degree")
        self.keep_side = self.request.get_param("KeepSide")
        self.image = self.request.get_param("inputImageOne")

        # Dependent dropdown parametreleri
        self.gray_method = self.request.get_param("grayMethod")
        self.load_gray_parameters()

    def load_gray_parameters(self):
        """Seçilen gray method'a göre parametreleri yükle"""
        if self.gray_method == "Normal":
            self.alpha = self.request.get_param("alpha")
            self.beta = self.request.get_param("beta")
        elif self.gray_method == "Weighted":
            self.red_weight = self.request.get_param("red_weight")
            self.green_weight = self.request.get_param("green_weight")
            self.blue_weight = self.request.get_param("blue_weight")
            self.blur_kernel = self.request.get_param("blur_kernel")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def gray(self, img):
        """
        Convert image to grayscale based on selected method.
        """
        if self.gray_method == "Normal":
            # Normal grayscale conversion with alpha and beta adjustments
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_img = cv2.convertScaleAbs(gray_img, alpha=self.alpha, beta=self.beta)
            return gray_img

        elif self.gray_method == "Weighted":
            # Weighted grayscale conversion
            b, g, r = cv2.split(img)
            gray_img = (self.red_weight * r + self.green_weight * g + self.blue_weight * b).astype(np.uint8)

            # Apply blur if kernel size > 1
            if self.blur_kernel > 1:
                gray_img = cv2.blur(gray_img, (self.blur_kernel, self.blur_kernel))

            return gray_img

        else:
            # Default grayscale conversion
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)




    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.gray(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)

        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()