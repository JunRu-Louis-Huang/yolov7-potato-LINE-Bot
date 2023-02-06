# import json
import os

from flask import Flask
from flask import request, abort

from line_bot_api import *
from events.basic import detect_event, download_RealTime, save_img, yolo_predict_text_save, yolo_predict_photo_save,\
     get_group_summary, get_profile, get_group_member_profile, get_group_members_count

from PIL import Image
# import cv2

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

    if mtext == '@我的資訊':
        try:
            user_profile = get_profile(event)
            print("取得使用者資訊")
            send_profile = TextSendMessage(  #傳送文字
                            text = f"❤ 你是{user_profile[0]}\n🥔 UserID: {user_profile[1]}\n🥔 頭像URL: {user_profile[2]}\n\
🥔 狀態顯示: {user_profile[3]}\n🥔 設定的語言: {user_profile[4]}"
                    )
            line_bot_api.reply_message(event.reply_token, send_profile)
        except AttributeError as e:
            print(e)
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
        save_img(event, filename)
        # yolo_detect(event)
        # print(filename)
        
        image = Image.open(filename)
        # Predict
        # yolo_predict_text_save(filename, image, event, message_content)
        yolo_predict_photo_save(filename, image, event, message_content)
        
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    

    
   

if __name__ == '__main__':
    app.run(debug=True)
