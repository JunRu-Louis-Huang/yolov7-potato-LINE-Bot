# Import libraries

import sys
# sys.path.append("/kaggle/input/yolov7-lib/yolov7-main")

import cv2
import numpy as np
import torch
from PIL import Image

from models.experimental import attempt_load
from utils.general import non_max_suppression

WEIGHTS = "./runs/train/yolov7-potato/weights/best.pt"
DEVICE = "cuda"
IMAGE_SIZE = 640

CLASSES = ['potato', 'sprout', 'green', 'scab', 'black', 'hole', 'disformation', 'mold']

# Load YOLOv7
model = attempt_load(WEIGHTS, map_location=DEVICE)


def predict(image, image_size=640):
    image = np.asarray(image)
    
    # Resize image to the inference size
    ori_h, ori_w = image.shape[:2]
    image = cv2.resize(image, (image_size, image_size))
    
    # Transform image from numpy to torch format
    image_pt = torch.from_numpy(image).permute(2, 0, 1).to(DEVICE)
    image_pt = image_pt.float() / 255.0
    
    # Infer
    with torch.no_grad():
        pred = model(image_pt[None], augment=False)[0]
    
    # NMS
    pred = non_max_suppression(pred)[0].cpu().numpy()
    
    # Resize boxes to the original image size
    pred[:, [0, 2]] *= ori_w / image_size
    pred[:, [1, 3]] *= ori_h / image_size
    
    return pred

# Load image
IMAGE_FILE = "<影像路徑>"
image = Image.open(IMAGE_FILE)


# Predict
pred = predict(image)

# Visualize the result 
image = cv2.imread(IMAGE_FILE)  # queryImage
for x1, y1, x2, y2, conf, class_id in pred:
    text = f"{CLASSES[int(class_id)]}  {conf:.2f}"
    # print(x1, y1, x2,  y2, conf, class_id) 
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    # print(x1, y1, x2, y2)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
    cv2.putText(image, text, (x1, y1), 2, 1, (30,250,255), 2)
    # print(f"{CLASSES[int(class_id)]}  {conf:.2f}")

# cv2.imshow('Predict', image)
cv2.imwrite('<檔案路徑>', image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)
