# Image detector with a tiny PyTorch toy model wrapper.
# The code below is a starter: it expects torch to be installed when running.
import os
from PIL import Image
import numpy as np

# Attempt to import torch; if unavailable, we fallback to a deterministic stub
try:
    import torch
    import torch.nn as nn
    import torchvision.transforms as T
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False
    torch = None
    nn = None
    T = None

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'toy_model.pth')

class TinyNet:
    """Tiny CNN used only as an example. In production replace with a trained model."""
    def __init__(self):
        if not TORCH_AVAILABLE:
            self.stub = True
        else:
            self.stub = False
            # Define a very small model
            self.net = nn.Sequential(
                nn.Conv2d(3, 8, kernel_size=3, stride=1, padding=1),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d(1),
                nn.Flatten(),
                nn.Linear(8, 2),
                nn.Softmax(dim=1)
            )
            # Try to load weights if present
            try:
                self.net.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
            except Exception:
                pass

    def predict(self, pil_image):
        """Return fake probability between 0 and 1."""
        if self.stub:
            # deterministic stub based on image size
            w,h = pil_image.size
            score = (w % 100) / 100.0
            return float(score)
        else:
            transform = T.Compose([T.Resize((128,128)), T.ToTensor()])
            x = transform(pil_image).unsqueeze(0)  # 1x3xHxW
            with torch.no_grad():
                out = self.net(x)
                fake_prob = float(out[0,0].item())
                return fake_prob

_MODEL = TinyNet()

def heuristic_checks(image_path):
    checks = {}
    try:
        img = Image.open(image_path)
        checks['size'] = img.size
        checks['format'] = img.format
        exif = img.getexif()
        checks['has_exif'] = bool(exif)
    except Exception as e:
        checks['error'] = str(e)
    return checks

def analyze_image(image_path):
    result = {}
    result['file'] = os.path.basename(image_path)
    result['heuristics'] = heuristic_checks(image_path)
    try:
        img = Image.open(image_path).convert('RGB')
        fake_prob = _MODEL.predict(img)
    except Exception as e:
        fake_prob = 0.0
        result['error'] = str(e)

    result['model'] = {'fake_prob': fake_prob, 'real_prob': 1.0 - fake_prob}
    result['is_fake'] = fake_prob > 0.5
    result['confidence'] = fake_prob if result['is_fake'] else 1.0 - fake_prob
    return result
