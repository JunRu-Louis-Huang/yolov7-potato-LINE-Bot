import json

from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, CameraAction, CameraRollAction, ImageMessage, FlexSendMessage, PostbackEvent


with open('env.json') as f:
    env = json.load(f)
line_bot_api = LineBotApi(env['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(env['CHANNEL_SECRET'])
end_point = env['end_point']