from line_bot_api import *

# 瑕疵導覽
def defect_introduction(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='馬鈴薯瑕疵導覽', contents=contents_json[0])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 七種瑕疵轉盤
def introduct_all(event):
    f = open("./events/introduction_defect_all.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='一次看七種', contents=contents_json)
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 瑕疵介紹-發芽
def introduct_sprout(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='瑕疵介紹-發芽', contents=contents_json[1])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 瑕疵介紹-發綠
def introduct_green(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='瑕疵介紹-發綠', contents=contents_json[2])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 瑕疵介紹-瘡痂病
def introduct_scab(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='瑕疵介紹-瘡痂病', contents=contents_json[3])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 瑕疵介紹-發黑
def introduct_black(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='瑕疵介紹-發黑', contents=contents_json[4])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 瑕疵介紹-洞
def introduct_hole(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='瑕疵介紹-洞', contents=contents_json[5])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 瑕疵介紹-畸形
def introduct_deformation(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='瑕疵介紹-畸形', contents=contents_json[6])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 瑕疵介紹-白絹病
def introduct_mold(event):
    f = open("./events/introduction_defect.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='瑕疵介紹-白絹病', contents=contents_json[7])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)