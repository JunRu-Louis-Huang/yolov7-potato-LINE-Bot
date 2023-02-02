# import json
import os

from flask import Flask
from flask import request, abort

from line_bot_api import *
from events.basic import detect_event, download_RealTime, save_img, yolo_predict, CLASSES

from PIL import Image
import cv2

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
       
    if mtext == '@馬鈴薯瑕疵檢測':
        try:
            detect_event(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    if mtext == '@即時影像辨識':
        try:
            download_RealTime(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == "action=download&items=iosAPP":
        try:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='好的，這裡是傳送門，請下載： \nhttps://___')
                )
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif event.postback.data == "action=download&items=googleplay":
        try:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="僅支援 ios 裝置")
                )
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    

# image message type 
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    try:
        message_content = line_bot_api.get_message_content(event.message.id)
        filename = f"./Images/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
        save_img(event)
        # yolo_detect(event)
        # print(filename)
        
        image = Image.open(filename)
        # Predict
        pred = yolo_predict(image)

        # Visualize the result 
        image = cv2.imread(filename)  # queryImage
        result_text = "影像偵測到可能有：\n"
        i = 1
        pred_list = []  
        CLASSES_zh = {0:"馬鈴薯", 1:"發芽", 2:"發綠", 3:"瘡痂", 4:"發黑", 5:"洞", 6:"畸形", 7:"白絹病"}
        for x1, y1, x2, y2, conf, class_id in pred:
            text = f"{CLASSES[int(class_id)]}  {conf:.2f}"
            # print(x1, y1, x2,  y2, conf, class_id) 
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # print(x1, y1, x2, y2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
            cv2.putText(image, text, (x1, y1), 2, 1, (30,250,255), 2)
            # print(f"{CLASSES[int(class_id)]}  {conf:.2f}")
            if int(class_id) != 0:
                result_text += f"{i}. {CLASSES_zh[int(class_id)]}  (Conf: {conf:.2f})\n"
                i += 1
            pred_list.append(int(class_id))
        # print(result_text)
        # print(pred_list)

        # cv2.imshow('Predict', image)
        if not os.path.exists("./User_pred"):
            os.mkdir("./User_pred")
        pred_img_file = f"./User_pred/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
        cv2.imwrite(pred_img_file, image)

        if {0} == set(pred_list):
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="辨識完成，AI目前沒有偵測到瑕疵"))
        elif {0} <= set(pred_list):
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result_text))
        elif 0 not in pred_list:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="沒有偵測到馬鈴薯，請重新拍照"))

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    
    
   

if __name__ == '__main__':
    app.run()
