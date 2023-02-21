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

# 品種介紹-總攬
def cultivar(event):
    f = open("./events/cultivar_all.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='品種介紹總攬，請選擇品種', contents=contents_json)
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-克尼伯
def cultivar_0(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-克尼伯', contents=contents_json[0])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-台農一號
def cultivar_1(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-台農一號', contents=contents_json[1])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-台農三號
def cultivar_2(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-台農三號', contents=contents_json[2])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-台農四號
def cultivar_3(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-台農四號', contents=contents_json[3])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-種苗二號
def cultivar_4(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-種苗二號', contents=contents_json[4])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-種苗四號
def cultivar_5(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-種苗四號', contents=contents_json[5])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-種苗六號
def cultivar_6(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-種苗六號', contents=contents_json[6])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-大利
def cultivar_7(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-大利', contents=contents_json[7])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹-大西洋
def cultivar_8(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-大西洋', contents=contents_json[8])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹- 紅皮馬鈴薯
def cultivar_9(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-紅皮馬鈴薯', contents=contents_json[9])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹- 褐皮馬鈴薯
def cultivar_10(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-褐皮馬鈴薯', contents=contents_json[10])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹- 白玉馬鈴薯
def cultivar_11(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-白玉馬鈴薯', contents=contents_json[11])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)

# 品種介紹- 彩色馬鈴薯
def cultivar_12(event):
    f = open("./events/cultivar.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到品種介紹-彩色馬鈴薯', contents=contents_json[12])
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)


# 關於
def test(event):
    f = open("./events/test.json", "r", encoding="utf-8")
    contents_json = json.load(f)
    flex_message = FlexSendMessage(alt_text='你來到關於我', contents=contents_json)
    f.close()
    line_bot_api.reply_message(
            event.reply_token,
            flex_message)
    
def manual(event):
    text1 = "本AI辨識結果具一定的準確度，但辨識結果可能受光線、背景等因素影響。\n提醒您，在選購、料理前仍要再檢查是否有發芽、發綠、發霉等瑕疵喔"
    text2 = "祝您使用愉快。 🙂\n使用後別忘了填寫問卷唷！❤"
    send_img = ImageSendMessage(  #傳送圖片
                        original_content_url = "https://storage.googleapis.com/louisai/LineBot/%E6%AD%A5%E9%A9%9F%E6%95%99%E5%AD%B8.jpg",
                        preview_image_url = "https://storage.googleapis.com/louisai/LineBot/%E6%AD%A5%E9%A9%9F%E6%95%99%E5%AD%B8.jpg"
                    )
    send_img_2 = ImageSendMessage(  #傳送圖片
                        original_content_url = "https://storage.googleapis.com/louisai/LineBot/%E6%8B%8D%E6%94%9D%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A0%85.jpg",
                        preview_image_url = "https://storage.googleapis.com/louisai/LineBot/%E6%8B%8D%E6%94%9D%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A0%85.jpg"
                    )
    send_pred_text1 = TextSendMessage(text=text1)
    send_pred_text2 = TextSendMessage(text=text2)
    message = [
            send_img,
            send_img_2,
            send_pred_text1,
            send_pred_text2,
            ]
    line_bot_api.reply_message(event.reply_token, message)