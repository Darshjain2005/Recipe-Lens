import sys
import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# ---------------- CONFIG ----------------
MODEL_PATH = "vegetable_model.pth"
CLASS_PATH = "vegetable_classes.json"
IMG_SIZE = 224

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- LOAD CLASSES ----------------
with open(CLASS_PATH, "r") as f:
    classes = json.load(f)

# ---------------- MODEL ----------------
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, len(classes))
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()
model.to(DEVICE)

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor()
])

# ---------------- PREDICT ----------------
def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    return classes[predicted.item()]

# ---------------- MAIN ----------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict_vegetable.py image.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    result = predict(image_path)

    print("\n🥕 Predicted Vegetable:")
    print("-", result)
