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
        from potato.PROFILE;
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
    user_id = event.source.user_id
    user_profile = get_profile(event)
    try:
        time = datetime.fromtimestamp(event.timestamp/1000)
        user_display_name = user_profile[0]
        picture_url = user_profile[2]
        status_message = user_profile[3]
        language = user_profile[4]

        sql_cmd = f"""select `USER_ID` from potato.PROFILE where USER_ID= '{user_id}';"""
        query_data = db.engine.execute(sql_cmd)
        if len(list(query_data)) == 0:
            sql_cmd = f"""insert into potato.PROFILE (`USER_ID`, `NICK_NAME`, `STATE`, `JOIN_TIME`,
                `TIME`, `LANGUAGE`, `PROFILE_PHOTO_URL`) values
            ('{user_id}','{user_display_name}', '{status_message}', '{time}', '{time}', '{language}', '{picture_url}');"""
            db.engine.execute(sql_cmd)

            sql_cmd = f"""insert into potato.DESCRIPTION_OF_DEFECTS (`USER_ID`, `I1_SPROUT`, `I2_GREEN`, `I3_SCAB`,
            `I4_BLACK`, `I5_HOLE`, `I6_DEFORMATION`, `I7_MOLD`)
            values ('{user_id}', 0, 0, 0, 0, 0, 0, 0);"""
            db.engine.execute(sql_cmd)
            
            sql_cmd = f"""insert into potato.FUNCTION (`USER_ID`, `PREDICT`, `DEFECT`, `CULTIVAR`, `INSTRUCTIONS_FOR_USE`, `ABOUT`)
            values ('{user_id}', 0, 0, 0, 0, 0);"""
            db.engine.execute(sql_cmd)
        else:
            print("舊用戶傳送文字訊息")
    except:
        print("message 事件新增資料庫發生錯誤")

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

    if mtext == '@馬鈴薯小學堂':
        try:
            introduction(event)
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
    if mtext == '@使用說明':
        try:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mtext))
            sql_cmd = updateDB_FUNCTION(user_id, instructions_for_use=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    if mtext == '@關於':
        try:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mtext))
            sql_cmd = updateDB_FUNCTION(user_id, about=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    
    sql_cmd = f"""update potato.PROFILE set `TIME` = '{time}' where `USER_ID` = '{user_id}';"""
    db.engine.execute(sql_cmd)

    sql_cmd = insertDB_USAGE_COUNT(time=time, user_id=user_id)
    db.engine.execute(sql_cmd)
        

# image message type 
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    user_profile = get_profile(event)
    
    try:
        time = datetime.fromtimestamp(event.timestamp/1000)
        user_display_name = user_profile[0]
        picture_url = user_profile[2]
        status_message = user_profile[3]
        language = user_profile[4]

        sql_cmd = f"""select `USER_ID` from potato.PROFILE where USER_ID= '{user_id}';"""
        query_data = db.engine.execute(sql_cmd)
        if len(list(query_data)) == 0:
            sql_cmd = f"""insert into potato.PROFILE (`USER_ID`, `NICK_NAME`, `STATE`, `JOIN_TIME`,
                `TIME`, `LANGUAGE`, `PROFILE_PHOTO_URL`) values
            ('{user_id}','{user_display_name}', '{status_message}', '{time}', '{time}', '{language}', '{picture_url}');"""
            db.engine.execute(sql_cmd)

            sql_cmd = f"""insert into potato.DESCRIPTION_OF_DEFECTS (`USER_ID`, `I1_SPROUT`, `I2_GREEN`, `I3_SCAB`,
            `I4_BLACK`, `I5_HOLE`, `I6_DEFORMATION`, `I7_MOLD`)
            values ('{user_id}', 0, 0, 0, 0, 0, 0, 0);"""
            db.engine.execute(sql_cmd)

            sql_cmd = f"""insert into potato.FUNCTION (`USER_ID`, `PREDICT`, `DEFECT`, `CULTIVAR`, `INSTRUCTIONS_FOR_USE`, `ABOUT`)
            values ('{user_id}', 0, 0, 0, 0, 0);"""
            db.engine.execute(sql_cmd)
        else:
            print("舊用戶傳送了照片")
    except:
        print("Image 事件")
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
        sql_cmd = yolo_predict_photoText(event)
        db.engine.execute(sql_cmd)
        user_id = event.source.user_id
        
        sql_cmd = updateDB_profile(user_id, user_display_name, status_message, time, language, picture_url)
        db.engine.execute(sql_cmd)
        
        sql_cmd = updateDB_FUNCTION(user_id, predict=1)
        db.engine.execute(sql_cmd)

        sql_cmd = insertDB_USAGE_COUNT(time=time, user_id=user_id)
        db.engine.execute(sql_cmd)

        sql_cmd = f"""update potato.PROFILE set `TIME` = '{time}' where `USER_ID` = '{user_id}';"""
        db.engine.execute(sql_cmd)

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
    
    sql_cmd = f"""select `USER_ID` from potato.PROFILE where USER_ID= '{user_id}';"""
    query_data = db.engine.execute(sql_cmd)
    if len(list(query_data)) == 0:
        sql_cmd = f"""insert into potato.PROFILE (`USER_ID`, `NICK_NAME`, `STATE`, `JOIN_TIME`,
             `TIME`, `LANGUAGE`, `PROFILE_PHOTO_URL`) values
        ('{user_id}','{user_display_name}', '{status_message}', '{create_time}', '{create_time}', '{language}', '{picture_url}');"""
        db.engine.execute(sql_cmd)
        sql_cmd = f"""insert into potato.DESCRIPTION_OF_DEFECTS (`USER_ID`, `I1_SPROUT`, `I2_GREEN`, `I3_SCAB`,
            `I4_BLACK`, `I5_HOLE`, `I6_DEFORMATION`, `I7_MOLD`)
        values ('{user_id}', 0, 0, 0, 0, 0, 0, 0);"""
        db.engine.execute(sql_cmd)
        sql_cmd = f"""insert into potato.FUNCTION (`USER_ID`, `PREDICT`, `DEFECT`, `CULTIVAR`, `INSTRUCTIONS_FOR_USE`, `ABOUT`)
        values ('{user_id}', 0, 0, 0, 0, 0);"""
        db.engine.execute(sql_cmd)
    sql_cmd = insertDB_USAGE_COUNT(time=create_time, user_id=user_id)
    db.engine.execute(sql_cmd)

@handler.add(UnfollowEvent)
def handle_follow(event):
    print(event)
    print()
    print("UserID: ", event.source.user_id)
    print("封鎖時間: ", datetime.fromtimestamp(event.timestamp/1000))
    print(event.type)

    user_id = event.source.user_id
    block_time = datetime.fromtimestamp(event.timestamp/1000)
    
    sql_cmd = f"""update potato.PROFILE set 
        `BLOCK_TIME` = '{block_time}',
        `TIME` = '{block_time}'
    where `USER_ID` = '{user_id}';"""
    db.engine.execute(sql_cmd)
    sql_cmd = insertDB_USAGE_COUNT(time=block_time, user_id=user_id)
    db.engine.execute(sql_cmd)

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id    
    if event.postback.data == "defect_introduction":
        try:
            defect_introduction(event)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Sprout":
        try:
            introduct_sprout(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I1_sprout=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Green":
        try:
            introduct_green(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I2_green=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Scab":
        try:
            introduct_scab(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I3_scab=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Black":
        try:
            introduct_black(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I4_black=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Hole":
        try:
            introduct_hole(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I5_hole=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Deformation":
        try:
            introduct_deformation(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I6_deformation=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Mold":
        try:
            introduct_mold(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I7_mold=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif event.postback.data == "Class7":
        try:
            introduct_all(event)
            sql_cmd = updateDB_DESCRIPTION_OF_DEFECTS(user_id, I1_sprout=1, I2_green=1, I3_scab=1, I4_black=1, I5_hole=1, I6_deformation=1, I7_mold=1)
            db.engine.execute(sql_cmd)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    time = datetime.fromtimestamp(event.timestamp/1000)

    sql_cmd = f"""update potato.PROFILE set `TIME` = '{time}' where `USER_ID` = '{user_id}';"""
    db.engine.execute(sql_cmd)

    sql_cmd = f"""select `TIME` from potato.USAGE_COUNT where TIME= '{time}';"""
    query_data = db.engine.execute(sql_cmd)
    if len(list(query_data)) == 0:
        sql_cmd = insertDB_USAGE_COUNT(time=time, user_id=user_id)
        db.engine.execute(sql_cmd)


# Insert/Update DB 
def updateDB_profile(user_id, user_display_name, status_message, time, language, picture_url):
    sql_cmd = f"""update potato.PROFILE set 
        `NICK_NAME` = '{user_display_name}',
        `STATE` = '{status_message}',
        `TIME` = '{time}',
        `LANGUAGE` = '{language}',
        `PROFILE_PHOTO_URL` = '{picture_url}'
    where `USER_ID` = '{user_id}';"""
    print(f"{user_id} 更新DB使用者資料")
    return sql_cmd

def updateDB_DESCRIPTION_OF_DEFECTS(user_id, I1_sprout=0, I2_green=0, I3_scab=0, I4_black=0, I5_hole=0, I6_deformation=0, I7_mold=0):
    sql_cmd = f"""update potato.DESCRIPTION_OF_DEFECTS set
        `I1_SPROUT` = `I1_SPROUT` + {I1_sprout},
        `I2_GREEN` = `I2_GREEN` + {I2_green},
        `I3_SCAB` = `I3_SCAB` + {I3_scab},
        `I4_BLACK` = `I4_BLACK` + {I4_black},
        `I5_HOLE` = `I5_HOLE` + {I5_hole},
        `I6_DEFORMATION` = `I6_DEFORMATION` + {I6_deformation},
        `I7_MOLD` = `I7_MOLD` + {I7_mold}
    where `USER_ID` = '{user_id}';"""
    print(f"{user_id} 更新DB瑕疵介紹點閱數")
    return sql_cmd

def updateDB_FUNCTION(user_id, predict=0, defect=0, cultivar=0, instructions_for_use=0, about=0):
    sql_cmd = f"""update potato.FUNCTION set
        `PREDICT`= `PREDICT` + {predict},
        `DEFECT` =`DEFECT` + {defect},
        `CULTIVAR` = `CULTIVAR` + {cultivar},
        `INSTRUCTIONS_FOR_USE` = `INSTRUCTIONS_FOR_USE` + {instructions_for_use},
        `ABOUT` = `ABOUT` + {about}
    where `USER_ID` = '{user_id}';"""
    print(f"{user_id} 更新DB主要功能點閱數")
    return sql_cmd

def insertDB_USAGE_COUNT(time, user_id):
    sql_cmd = f"""insert into potato.USAGE_COUNT
        values ('{user_id}', '{time}');"""
    print("新增time事件")
    return sql_cmd


if __name__ == '__main__':
    app.run(debug=True)
