# import json
import os
from datetime import datetime

from flask import Flask
from flask import request, abort
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from line_bot_api import *
from events.basic import detect_event, download_RealTime, save_img, yolo_predict_text_save, yolo_predict_photo_save,\
     yolo_predict_photoText, get_group_summary, get_profile, get_group_member_profile, get_group_members_count,\
     introduction, whoami
from events.postback_event import *

# from PIL import Image
# import cv2

app = Flask(__name__)
# 定義 SQL 連線字串
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

@app.route('/')
def index():
 
    sql_cmd = """
        select *
        from potato.profile;
        """
 
    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'


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
    print("=============================")
    print(event)
    # user_profile = get_profile(event)
    mtext = event.message.text

    if mtext == '@馬鈴薯瑕疵檢測':
        try:
            detect_event(event)
            # for i in user_profile:
            #     print(i)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    if mtext == '@即時影像辨識':
        try:
            download_RealTime(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    if mtext == '@馬鈴薯小學堂':
        try:
            introduction(event)
            # for i in user_profile:
            #     print(i)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    if mtext == '@我是誰':
        try:
            # user_profile = get_profile(event)
            print("使用者資訊")
            whoami(event)
#             send_profile = TextSendMessage(  #傳送文字
#                             text = f"❤ 你是{user_profile[0]}\n🥔 UserID: {user_profile[1]}\n🥔 頭像URL: {user_profile[2]}\n\
# 🥔 狀態顯示: {user_profile[3]}\n🥔 設定的語言: {user_profile[4]}"
#                     )
#             line_bot_api.reply_message(event.reply_token, send_profile)
        except AttributeError as e:
            print(e)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

        

# image message type 
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    user_profile = get_profile(event)
    try:
        # message_content = line_bot_api.get_message_content(event.message.id)
        # filename = f"./Images/{event.message.id}.{message_content.content_type.split('/')[1].lower()}"
        # save_img(event)
        # yolo_detect(event)
        # print(filename)
        
        # image = Image.open(filename)
        ## Predict
        # yolo_predict_text_save(event)
        # yolo_predict_photo_save(event)  # 需與save_img()一起執行
        yolo_predict_photoText(event)
        # for i in user_profile:
        #         print(i)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

@handler.add(FollowEvent)
def handle_follow(event):
    print(event)
    print()
    print("UserID: ", event.source.user_id)
    print("加入好友時間: ", datetime.fromtimestamp(event.timestamp/1000))
    print(event.type)
    user_profile = get_profile(event)
    user_id = event.source.user_id
    create_time = datetime.fromtimestamp(event.timestamp/1000)
    user_display_name = user_profile[0]
    picture_url = user_profile[2]
    status_message = user_profile[3]
    language = user_profile[4]
    
    sql_cmd = f"""select `user_id` from potato.profile where user_id= '{user_id}';"""
    query_data = db.engine.execute(sql_cmd)
    if len(list(query_data)) == 0:
        sql_cmd = f"""insert into potato.profile (`user_id`, `nick_name`, `state`, `join_time`,
             `time`, `language`, `profile_photo_url`) values
        ('{user_id}','{user_display_name}', '{status_message}', '{create_time}', '{create_time}', '{language}', '{picture_url}');"""
        db.engine.execute(sql_cmd)


@handler.add(UnfollowEvent)
def handle_follow(event):
    print(event)
    print()
    print("UserID: ", event.source.user_id)
    print("封鎖時間: ", datetime.fromtimestamp(event.timestamp/1000))
    print(event.type)
    # user_profile = get_profile(event)
    user_id = event.source.user_id
    block_time = datetime.fromtimestamp(event.timestamp/1000)
    
    sql_cmd = f"""update potato.profile set 
        `block_time` = '{block_time}',
        `time` = '{block_time}'
    where `user_id` = '{user_id}';"""
    db.engine.execute(sql_cmd)

@handler.add(PostbackEvent)
def handle_postback(event):
    # user_profile = get_profile(event)
    if event.postback.data == "defect_introduction":
        try:
            defect_introduction(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Sprout":
        try:
            introduct_sprout(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Green":
        try:
            introduct_green(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Scab":
        try:
            introduct_scab(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Black":
        try:
            introduct_black(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Hole":
        try:
            introduct_hole(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Deformation":
        try:
            introduct_deformation(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Mold":
        try:
            introduct_mold(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Class7":
        try:
            introduct_all(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    # print(user_profile)


   

if __name__ == '__main__':
    app.run(debug=True)
