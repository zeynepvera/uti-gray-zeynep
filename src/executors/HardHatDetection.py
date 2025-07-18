import os
import sys
from ultralytics import YOLO

# PYTHONPATH ayarı
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from sdks.novavision.src.helper.executor import Executor

from components.GrayZeynep.src.utils.yolo_utils import load_model
from components.GrayZeynep.src.models.PackageModel import PackageModel


class HardHatDetection(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        # input image
        self.image = self.request.get_param("inputImageOne")
        self.model = self.bootstrap["model"]

    @staticmethod
    def bootstrap(config: dict) -> dict:
        """
        Model loads.
        """
        model = load_model()
        return {"model": model}

    def run(self):
        """
        Making predict with model and returns th result.
        """
        img_frame = Image.get_frame(img=self.image, redis_db=self.redis_db)
        results = self.model(img_frame)  # model prediction

        print(results)

        annotated_img = results[0].plot()

        output_image = Image.set_frame(img=annotated_img, package_uID=self.uID, redis_db=self.redis_db)

        self.request.model.outputs.outputImageOne.value = output_image

        return self.request.model


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
