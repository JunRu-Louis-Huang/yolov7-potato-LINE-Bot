import os
import io

# import subprocess
from datetime import datetime

from line_bot_api import *

import cv2
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont

from models.experimental import attempt_load
from utils.general import non_max_suppression
from events.gcs import *

WEIGHTS = WEIGHTS
DEVICE = "cpu"
IMAGE_SIZE = 640

CLASSES = ['potato', 'sprout', 'green', 'scab', 'black', 'hole', 'deformation', 'mold']
CLASSES_zh = ["馬鈴薯", "發芽", "發綠", "瘡痂", "發黑", "洞", "畸形", "白絹病(發霉)"]
bucket_name = bucket_name

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

# 馬鈴薯小學堂
def introduction(event):
    template_message = TemplateSendMessage(
        alt_text='馬鈴薯小學堂',
        template=ButtonsTemplate(
                thumbnail_image_url='https://static.vecteezy.com/system/resources/thumbnails/002/044/760/small_2x/fresh-organic-potatoes-in-a-bowl-free-photo.jpg',
                title='馬鈴薯小學堂',
                text='了解更多馬鈴薯瑕疵介紹、品種介紹資訊......',
                actions=[
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='瑕疵導覽',  #按鈕文字
                        text='瑕疵導覽',  #顯示文字訊息
                        data='defect_introduction'  #Postback資料
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='品種介紹',  #按鈕文字
                        text='品種介紹',  #顯示文字訊息
                        data='variety_introduction'  #Postback資料
                    )
                ]
            )
    
    )
    line_bot_api.reply_message(
            event.reply_token,
            template_message)

def more_(event):
    template_message = TemplateSendMessage(
        alt_text='說明資訊',
        template=ButtonsTemplate(
                title='🥔說明   📰關於',
                text='歡迎點下方擊連結填寫問卷，幫助我們做得更好',
                actions=[
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='使用說明',  #按鈕文字
                        data='Manual'  #Postback資料
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='關於我們',  #按鈕文字
                        data='About'  #Postback資料
                    ),
                    MessageTemplateAction(  #文字按鈕
                        label='看 我是誰',  #按鈕文字
                        text='@我是誰'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='回饋問卷(可重複填寫)',
                        uri='https://liff.line.me/' + liffid
                    )
                ]
            )
    
    )
    line_bot_api.reply_message(
            event.reply_token,
            template_message)


# image message type 
def save_img(event):
    # global filename
    message_content = line_bot_api.get_message_content(event.message.id)
    filename = f"./Images/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
    print(f"Message type: {event.message.type}\tMessage id: {event.message.id}")

    if not os.path.exists("./Images"):
        os.mkdir("./Images")
    
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
def yolo_predict_text_save(event, image_size=640):
    message_content = line_bot_api.get_message_content(event.message.id)
    filename = f"./Images/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
    image = Image.open(filename)
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
    
    # return pred

    ## Visualize the result 
    image = cv2.imread(filename)  # queryImage
    result_text = "影像偵測到可能有：\n"
    i = 1
    pred_list = []  
    # potato_range_list = []
    # print(pred)
    
    for x1, y1, x2, y2, conf, class_id in pred:
        # if conf >= 0.4:
        text = f"{CLASSES_zh[int(class_id)]}  {conf:.2f}"
        # print(x1, y1, x2,  y2, conf, class_id) 
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # print(x1, y1, x2, y2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
        cv2.putText(image, text, (x1, y1), 2, 1, (30,250,255), 2)
        # print(f"{CLASSES_zh[int(class_id)]}  {conf:.2f}")
        if int(class_id) == 0:
            # coordinate = (x1, y1, x2, y2)
            # potato_range_list.append(coordinate)
            pred_list.append(int(class_id))

        else:
            # for j in potato_range_list:
            #     if ((j[0] <= x1 <= j[2]) and (j[1] <= y1 <= j[3])) or ((j[0] <= x2 <= j[2]) and (j[1] <= y2 <= j[3])) or ((j[0] <= x1 <= j[2]) and (j[1] <= y2 <= j[3])) or ((j[0] <= x2 <= j[2]) and (j[1] <= y1 <= j[3])):
                    pred_list.append(int(class_id))
                    result_text += f"{i}. {CLASSES_zh[int(class_id)]}  (Conf: {conf:.2f})\n"
                    i += 1           

        # pred_list.append(int(class_id))
    # print(potato_range_list)
    # print(result_text)
    # print(pred_list)

    # cv2.imshow('Predict', image)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()
    # # cv2.waitKey(1)
    if not os.path.exists("./static"):
        os.mkdir("./static")
    pred_img_file = f"./static/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
    cv2.imwrite(pred_img_file, image)

    if {0} == set(pred_list):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="辨識完成，AI目前沒有偵測到瑕疵"))
    elif {0} <= set(pred_list):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result_text))
    elif 0 not in pred_list:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="沒有偵測到馬鈴薯，請重新拍照"))

## 照片存本地、回傳yolo方框照片
def yolo_predict_photo_save(event, image_size=640):
    try:
        user_profile = get_profile(event)
        group_summary = get_group_summary(event)
        group_count = get_group_members_count(event)
    except:
        user_profile = get_profile(event)
    finally:
        pass
    message_content = line_bot_api.get_message_content(event.message.id)
    filename = f"./Images/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
    image = Image.open(filename)
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

    ## Visualize the result 
    image = cv2.imread(filename)  # queryImage
    result_text = "影像偵測到可能有：\n"
    i = 1
    pred_list = []  
    # potato_range_list = []
    # print(pred)
    
    for x1, y1, x2, y2, conf, class_id in pred:
        # if conf >= 0.4:
        text = f"{CLASSES_zh[int(class_id)]}  {conf:.2f}"
        # print(x1, y1, x2,  y2, conf, class_id) 
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # print(x1, y1, x2, y2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
        cv2.putText(image, text, (x1, y1), 2, 1, (30,250,255), 2)
        # print(f"{CLASSES_zh[int(class_id)]}  {conf:.2f}")
        if int(class_id) == 0:
            # coordinate = (x1, y1, x2, y2)
            # potato_range_list.append(coordinate)
            pred_list.append(int(class_id))

        else:
            # for j in potato_range_list:
            #     if ((j[0] <= x1 <= j[2]) and (j[1] <= y1 <= j[3])) or ((j[0] <= x2 <= j[2]) and (j[1] <= y2 <= j[3])) or ((j[0] <= x1 <= j[2]) and (j[1] <= y2 <= j[3])) or ((j[0] <= x2 <= j[2]) and (j[1] <= y1 <= j[3])):
                    pred_list.append(int(class_id))
                    result_text += f"{i}. {CLASSES_zh[int(class_id)]}  (Conf: {conf:.2f})\n"
                    i += 1           

        # pred_list.append(int(class_id))
    # print(potato_range_list)
    # print(result_text)
    # print(pred_list)

    # cv2.imshow('Predict', image)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()
    # # cv2.waitKey(1)
    if not os.path.exists("./static"):
        os.mkdir("./static")
    pred_img_file = f"./static/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
    cv2.imwrite(pred_img_file, image)

    if {0} == set(pred_list):
        text="辨識完成，AI目前沒有偵測到瑕疵"
    elif {0} <= set(pred_list):
        text=result_text
    elif 0 not in pred_list:
        text="沒有偵測到馬鈴薯，請重新拍照"

    send_img = ImageSendMessage(  #傳送圖片
                        original_content_url = f"{end_point}{pred_img_file[1:]}",
                        preview_image_url = f"{end_point}{pred_img_file[1:]}"
                    )
    send_pred_text = TextSendMessage(text=text)
    try:
        send_profile = TextSendMessage(  #傳送文字
                        text = f"""🥔 上傳照片者: {user_profile[0]}
🥔 UserID: {user_profile[1]}
🥔 頭像URL: {user_profile[2]}
🥔 狀態顯示: {user_profile[3]}
🥔 設定的語言: {user_profile[4]}

🥔 群組名稱: {group_summary[1]}
🥔 群組id: {group_summary[0]}
🥔 群組圖像: {group_summary[2]}

❤ 群組人數: {group_count}"""
                    )
    except:
        send_profile = TextSendMessage(  #傳送文字
                        text = f"❤ 你是{user_profile[0]}\n🥔 UserID: {user_profile[1]}\n🥔 頭像URL: {user_profile[2]}\n\
🥔 狀態顯示: {user_profile[3]}\n🥔 設定的語言: {user_profile[4]}"
                    )
    message = [
            send_img,
            send_pred_text,
            send_profile
            ]
    line_bot_api.reply_message(event.reply_token, message)

## YOLOv7(接收照片存入Google Cloud Storage)
def yolo_predict_photoText(event, image_size=640):
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    b = b''
    for chunk in message_content.iter_content():
        b += chunk
    # Save to GCS
    filename = f"images/User_Upload_Images/{message_id}.{message_content.content_type.split('/')[1].lower()}"
    upload_blob_from_memory(bucket_name, b, filename)

    image = Image.open(io.BytesIO(b))
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
    
    # return pred

    ## Visualize the result 直接從記憶體取得照片
    npimg = np.fromstring(b, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)  # queryImage
    
    result_text = "影像偵測到可能有：\n"
    i = 1
    pred_list = []  
    # potato_range_list = []
    # print(pred)
    
    for cls_index in range(pred.shape[0]):
        if pred[cls_index][-1] == 0 and pred[cls_index][-2] >= 0.8: 

            for x1, y1, x2, y2, conf, class_id in pred:
                # if conf >= 0.4:
                if int(class_id) == 0 and conf >= 0.8:
                    text = f"{CLASSES_zh[int(class_id)]}  {conf:.2f}"
                    # print(x1, y1, x2,  y2, conf, class_id) 
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # print(x1, y1, x2, y2)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)

                    # 更新:添加中文字
                    # OpenCV圖片轉換為PIL圖片格式，使用PIL繪製文字
                    image = Image.fromarray(image[..., ::-1])
                    draw = ImageDraw.Draw(image)
                    fontText = ImageFont.truetype("NotoSansTC-Regular.otf", size=45, encoding="utf-8")
                    draw.text((x1, y1-60), text, fill=(255, 0, 255), font=fontText)
                    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)    # PIL圖片格式轉換成OpenCV的圖片格式
                    # cv2.putText(image, text, (x1, y1), 2, 1, (30,250,255), 2)

                    # print(f"{CLASSES_zh[int(class_id)]}  {conf:.2f}")
                    # coordinate = (x1, y1, x2, y2)
                    # potato_range_list.append(coordinate)
                    pred_list.append(int(class_id))
                elif int(class_id) != 0 and conf > 0.3:
                    text = f"{CLASSES_zh[int(class_id)]}  {conf:.2f}"
                    # print(x1, y1, x2,  y2, conf, class_id) 
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # print(x1, y1, x2, y2)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)

                    # 更新:添加中文字
                    # OpenCV圖片轉換為PIL圖片格式，使用PIL繪製文字
                    image = Image.fromarray(image[..., ::-1])
                    draw = ImageDraw.Draw(image)
                    fontText = ImageFont.truetype("NotoSansTC-Regular.otf", size=45, encoding="utf-8")
                    draw.text((x1, y1-60), text, fill=(255, 0, 255), font=fontText)
                    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)    # PIL圖片格式轉換成OpenCV的圖片格式
                    
                    # cv2.putText(image, text, (x1, y1), 2, 1, (30,250,255), 2)
                    # print(f"{CLASSES[int(class_id)]}  {conf:.2f}")
    
                    # coordinate = (x1, y1, x2, y2)
                    # potato_range_list.append(coordinate)
                    pred_list.append(int(class_id))
                    result_text += f"{i}. {CLASSES_zh[int(class_id)]}  (Conf: {conf:.2f})\n"
                    i += 1
            break
    
    # if not os.path.exists("./static"):
    #     os.mkdir("./static")
    # pred_img_file = f"./static/{message_id}.{message_content.content_type.split('/')[1].lower()}"
    # cv2.imwrite(pred_img_file, image)
    # print("YOLO Image was saved")

    
    img_encode = cv2.imencode('.jpeg', image)[1]

    # Converting the image into numpy array
    data_encode = np.array(img_encode)
    # Converting the array to bytes.
    byte_encode = data_encode.tobytes()
    pred_imgName_to_GCS = f"images/yolo_predImg/{message_id}.{message_content.content_type.split('/')[1].lower()}"
    upload_blob_from_memory(bucket_name, byte_encode, pred_imgName_to_GCS)

    send_img = ImageSendMessage(  #傳送圖片
                        # original_content_url = f"{end_point}{pred_img_file[1:]}",
                        # preview_image_url = f"{end_point}{pred_img_file[1:]}"
                         original_content_url = f"https://storage.googleapis.com/{bucket_name}/images/yolo_predImg/{message_id}.{message_content.content_type.split('/')[1].lower()}",
                         preview_image_url = f"https://storage.googleapis.com/{bucket_name}/images/yolo_predImg/{message_id}.{message_content.content_type.split('/')[1].lower()}"
                    )
    situation = "0"
    if {0} == set(pred_list):
        text="辨識完成，AI目前沒有偵測到瑕疵"
    elif {0} <= set(pred_list):
        text=result_text
    elif 0 not in pred_list:
        text="沒有偵測到馬鈴薯，請重新拍照"
        situation = "1"

    send_pred_text = TextSendMessage(text=text)
    
    if situation == "0":
        message = [
                send_img,
                send_pred_text,
                ]
    else:
        message = send_pred_text
    line_bot_api.reply_message(event.reply_token, message)    


    # update db
    potato = sprout = green = scab = black = hole = deformation = mold = 0

    for i in pred_list:
        if i == 0:
            potato += 1
        elif i == 1:
            sprout += 1
        elif i == 2:
            green += 1
        elif i == 3:
            scab += 1
        elif i == 4:
            black += 1
        elif i == 5:
            hole += 1
        elif i == 6:
            deformation += 1
        elif i == 7:
            mold += 1
    user_id = event.source.user_id
    time = datetime.fromtimestamp(event.timestamp/1000)

    sql_cmd = f"""insert into potato.DEFECT_MARK (`IMAGE`, `USER_ID`, `TIME`, `POTATO`, `SPROUT`, `GREEN`, `SCAB`, `BLACK`, `HOLE`, `DEFORMATION`, `MOLD`) values
        ('{message_id}','{user_id}','{time}', '{potato}', '{sprout}', '{green}', '{scab}', '{black}', '{hole}', '{deformation}', '{mold}');"""
    return sql_cmd


## Who am I
def whoami(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)    
    f = open("./events/whoami.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    contents_json["hero"]["url"]=profile.picture_url if profile.picture_url else "https://storage.googleapis.com/louisai/LineBot/%E7%84%A1%E9%A0%AD%E5%83%8F.jfif"
    contents_json["body"]["contents"][0]["contents"][0]["contents"][1]["text"] = profile.display_name if profile.display_name else "-"
    contents_json["body"]["contents"][0]["contents"][1]["contents"][1]["text"] = profile.user_id
    contents_json["body"]["contents"][0]["contents"][2]["contents"][1]["text"] = profile.status_message if profile.status_message else "-"
    contents_json["body"]["contents"][0]["contents"][3]["contents"][1]["text"] = profile.language

    flex_message = FlexSendMessage(alt_text='感謝您', contents=contents_json)
    f.close()
    
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)


## Get user profile information.
def get_profile(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_display_name = profile.display_name
    user_id = profile.user_id
    picture_url = profile.picture_url
    status_message = profile.status_message
    language = profile.language
    user_profile = [user_display_name, user_id, picture_url, status_message, language]
    print(user_display_name)
    print(user_id)
    print(picture_url)
    print(status_message)
    print(language)
    
    return user_profile

# 取得使用者在群組中的profile
def get_group_member_profile(event):
    group_id = event.source.group_id
    user_id = event.source.user_id
    profile = line_bot_api.get_group_member_profile(group_id, user_id)

    group_name = profile.display_name
    group_userID = profile.user_id
    group_picture_url = profile.picture_url
    
    group_member_profile = [group_name, group_userID, group_picture_url]
    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    return group_member_profile

# 取得群組資訊
def get_group_summary(event):
    group_id = event.source.group_id
    summary = line_bot_api.get_group_summary(group_id)
    print(summary.group_id)
    print(summary.group_name)
    print(summary.picture_url)
    group_summary_id = summary.group_id
    group_summary_name = summary.group_name
    group_summary_url = summary.picture_url
    group_summary = [group_summary_id, group_summary_name, group_summary_url]
    return group_summary

# 取得群組人數
def get_group_members_count(event):
    group_id = event.source.group_id
    group_count = line_bot_api.get_group_members_count(group_id)
    print(group_count)
    return group_count


