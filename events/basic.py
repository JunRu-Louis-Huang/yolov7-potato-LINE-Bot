import os

import subprocess

from line_bot_api import *

import cv2
import numpy as np
import torch
from PIL import Image

from models.experimental import attempt_load
from utils.general import non_max_suppression

WEIGHTS = "best_potato_20230201.pt"
DEVICE = "cuda"
IMAGE_SIZE = 640

CLASSES = ['potato', 'sprout', 'green', 'scab', 'black', 'hole', 'deformation', 'mold']

# Load YOLOv7
model = attempt_load(WEIGHTS, map_location=DEVICE)

def detect_event(event):
    # 開啟相機功能
    camera_button = QuickReplyButton(
            action = CameraAction(label="開啟相機", text="以相機拍照")
        )
    # 開啟圖庫功能
    Camera_roll_button = QuickReplyButton(
            action=CameraRollAction(label="從相簿上傳")
        )
    
    quick_reply = QuickReply(items=[camera_button, Camera_roll_button])

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="好的，您可以使用相機拍照，或者上傳照片", quick_reply=quick_reply)
    )

# 下載APP
def download_RealTime(event):
    f = open("./events/downloadAPP.json", "r", encoding="utf-8")
    contents_json = json.load(f)  # 載入自製的 FlexSendMessage 的 JSON 
    flex_message = FlexSendMessage(alt_text='下載APP', contents=contents_json)
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)


# image message type 
def save_img(event):
    global filename 
    message_content = line_bot_api.get_message_content(event.message.id)
    print(f"Message type: {event.message.type}\tMessage id: {event.message.id}")

    if not os.path.exists("./Images"):
        os.mkdir("./Images")

    filename = f"./Images/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
    
    with open(filename, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text='照片上傳成功，開始辨識，請稍候......'))

## yolo detector
# def yolo_detect(event):
#     command = ("python detect_2.py --weights ./runs/train/yolov7-potato/weights/best.pt --source {0}".format(filename)) 
#     subprocess.call(command, shell=True)


# Predict by YOLO
def yolo_predict(image, image_size=640):
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

# # Load image
# image = Image.open(filename)

# # Predict
# pred = yolo_predict(image)

# # Visualize the result 
# image = cv2.imread(filename)  # queryImage
# for x1, y1, x2, y2, conf, class_id in pred:
#     text = f"{CLASSES[int(class_id)]}  {conf:.2f}"
#     # print(x1, y1, x2,  y2, conf, class_id) 
#     x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#     # print(x1, y1, x2, y2)
#     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
#     cv2.putText(image, text, (x1, y1), 2, 1, (30,250,255), 2)
#     # print(f"{CLASSES[int(class_id)]}  {conf:.2f}")

# # cv2.imshow('Predict', image)
# cv2.imwrite(filename, image)

# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# # cv2.waitKey(1)


    
