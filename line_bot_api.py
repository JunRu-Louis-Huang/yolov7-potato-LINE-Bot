import json

from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage,\
     LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, CameraAction, CameraRollAction, ImageMessage,\
     FlexSendMessage, PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, FollowEvent, UnfollowEvent


with open('env_test.json', encoding="utf-8") as f:
    env = json.load(f)
line_bot_api = LineBotApi(env['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(env['CHANNEL_SECRET'])
WEIGHTS = env['WEIGHTS']
end_point = env['end_point']
SQLALCHEMY_DATABASE_URI = env['SQLALCHEMY_DATABASE_URI']