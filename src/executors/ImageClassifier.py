"""
Image classification component using PyTorch pre-trained models.
"""

import os
import cv2
import sys
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import json
from PIL import Image as PILImage
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayZeynep.src.utils.response import build_response_classifier
from components.GrayZeynep.src.models.PackageModel import PackageModel


class ImageClassifier(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.model = bootstrap['model']
        self.transform = bootstrap['transform']
        self.device = bootstrap['device']
        self.class_labels = bootstrap['class_labels']

        self.confidence_threshold = self.request.get_param("confidenceThreshold")
        self.top_k = self.request.get_param("topK")

        self.image = self.request.get_param("inputImageOne")

    @staticmethod
    def bootstrap(config: dict) -> dict:

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        base_path = os.path.dirname(os.path.abspath(__file__))
        models_path = os.path.join(base_path, "../../../storage/models")

        model_path = os.path.join(models_path, "resnet18-5c106cde.pth")

        if os.path.exists(model_path):
            print(f" Loading local model from: {model_path}")
            model = models.resnet18(pretrained=False)
            model.load_state_dict(torch.load(model_path, map_location=device))
        else:
            print(" Loading pretrained ResNet18 from torchvision")
            model = models.resnet18(pretrained=True)

        model.eval()
        model = model.to(device)

        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

        json_path = os.path.join(models_path, 'imagenet_classes.json')

        try:
            with open(json_path, 'r') as f:
                class_labels = json.load(f)
            print(f" ImageNet sınıfları yüklendi: {len(class_labels)} sınıf")
        except FileNotFoundError:
            print(f" JSON dosyası bulunamadı: {json_path}")
            class_labels = {}

        print(f" Model loaded on device: {device}")
        print(f"  Loaded {len(class_labels)} classes")

        return {
            'model': model,
            'transform': transform,
            'device': device,
            'class_labels': class_labels
        }

    def preprocess_image(self, cv_image):

        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        pil_image = PILImage.fromarray(rgb_image)

        tensor = self.transform(pil_image).unsqueeze(0)  # Batch dimension ekle

        return tensor.to(self.device)

    def predict(self, img):
        """Image classification prediction"""

        input_tensor = self.preprocess_image(img)

        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

        top_probabilities, top_indices = torch.topk(probabilities, self.top_k)

        predictions = []
        for i in range(self.top_k):
            class_idx = top_indices[i].item()
            confidence = top_probabilities[i].item()

            if confidence >= self.confidence_threshold:
                class_name = self.class_labels.get(str(class_idx), f"class_{class_idx}")
                predictions.append({
                    'class_name': class_name,
                    'confidence': round(confidence * 100, 2),
                    'class_id': class_idx
                })

        return predictions

    def run(self):

        print(" ImageClassifier başlatılıyor...")

        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        print(f" Image shape: {img.value.shape}")

        # Prediction yap
        predictions = self.predict(img.value)
        print(f" {len(predictions)} prediction yapıldı")

        img.metadata = {
            'predictions': predictions,
            'model_type': 'image_classification',
            'top_k': self.top_k,
            'confidence_threshold': self.confidence_threshold
        }

        self.image = Image.set_frame(
            img=img,
            package_uID=self.uID,
            redis_db=self.redis_db,
        )

        self.predictions = predictions

        for pred in predictions:
            print(f"   {pred['class_name']}: {pred['confidence']}%")

        packageModel = build_response_classifier(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()