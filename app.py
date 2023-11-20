# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('q8MasGUuwFhWx+O1opafyqY9vwRoy7RvYQTjgGcyjNFaI4x063mir+fnikvoyk2QqD+2uiEKJneCeNscwao694ZT82rH7mpHOMjtD5FC3XIdImkPAUKoVrbGRyWqehPSav3eYPBxxFea7K3EjELWOQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('7a4ff39e79a9b8961c5ddf5f3b9a8bbf')

line_bot_api.push_message('Uaf6d62add8a5bce9a9a64d1d1d97abd2', TextSendMessage(text='歡迎使用1'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token,message)
    if re.match('開始使用',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='這個看不到',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/YSJayCb.jpeg',
            title='記帳機器人',
            text='選單功能',
            actions=[
                PostbackAction(
                    label='使用者',
                    display_text='請輸入姓名:',
                    data='action=檯面下'
                    #line_bot_api.push_message('Uaf6d62add8a5bce9a9a64d1d1d97abd2', TextSendMessage(text='歡迎使用'))
                ),
                PostbackAction(
                    label='記帳',
                    text='我就是資料'
                ),
            ]
        )
    )

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)