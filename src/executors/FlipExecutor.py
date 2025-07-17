"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import cv2
import sys
##
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

        self.operation_type = self.request.get_param("flipOperationType")

        if self.operation_type == "SimpleFlip":
            self.flip_code = self.request.get_param("flipCode")
        elif self.operation_type == "AdvancedFlip":

            self.brightness = self.request.get_param("brightness")
            self.rotation_angle = self.request.get_param("rotationAngle")
            self.quality = self.request.get_param("quality")

        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def flip(self, img):
        if self.operation_type == "SimpleFlip":
            flipped = cv2.flip(img, self.flip_code)
        elif self.operation_type == "AdvancedFlip":
            flipped = img.copy()

            if hasattr(self, 'rotation_angle') and self.rotation_angle != 0:
                height, width = flipped.shape[:2]
                center = (width // 2, height // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, self.rotation_angle, 1.0)
                flipped = cv2.warpAffine(flipped, rotation_matrix, (width, height))

            if hasattr(self, 'brightness') and self.brightness != 0:
                flipped = cv2.convertScaleAbs(flipped, alpha=1, beta=self.brightness)

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