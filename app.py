# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
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
    
    if event.message.text.startswith('開始使用'):
        line_bot_api.push_message('Uaf6d62add8a5bce9a9a64d1d1d97abd2', TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=CarouselTemplate(
                columns=[
                    # 正確使用 Column
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/YSJayCb.jpeg',
                        title='記帳機器人',
                        text='這是按鈕樣板',
                        actions=[
                            PostbackAction(
                                label='User',
                                display_text='新增',
                                data='發送 postback'
                            ),
                            PostbackAction(
                                label='Start',
                                display_text='記帳',
                                data='發送 postback'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/YSJayCb.jpeg',
                        title='記帳機器人',
                        text='這是按鈕樣板',
                        actions=[
                            PostbackAction(
                                label='User',
                                display_text='新增',
                                data='發送 postback'
                            ),
                            PostbackAction(
                                label='Start',
                                display_text='記帳',
                                data='發送 postback'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/YSJayCb.jpeg',
                        title='記帳機器人',
                        text='這是按鈕樣板',
                        actions=[
                            PostbackAction(
                                label='User',
                                display_text='新增',
                                data='發送 postback'
                            ),
                            PostbackAction(
                                label='Start',
                                display_text='記帳',
                                data='發送 postback'
                            )
                        ]
                    )
                ]
            )
        ))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)