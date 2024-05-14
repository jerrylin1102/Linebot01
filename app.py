import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from openai import OpenAI

app = Flask(__name__)

# Line bot API credentials
line_bot_api = LineBotApi('q8MasGUuwFhWx+O1opafyqY9vwRoy7RvYQTjgGcyjNFaI4x063mir+fnikvoyk2QqD+2uiEKJneCeNscwao694ZT82rH7mpHOMjtD5FC3XIdImkPAUKoVrbGRyWqehPSav3eYPBxxFea7K3EjELWOQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7a4ff39e79a9b8961c5ddf5f3b9a8bbf')

# OpenAI API credentials
openai_client = OpenAI(api_key='sk-proj-kNysSwucjLn3bm8TssDAT3BlbkFJ6TWhLbgELrgaTcXC6UWY')

# Main callback route
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message handling
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.startswith('開始使用'):
        reply = "歡迎使用！請問您需要什麼幫助？"
    else:
        # Send the user's message to ChatGPT using OpenAI's Python SDK
        completion = openai_client.ChatCompletion.create(
            model="text-davinci-003",  # 更改為所需的模型
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": event.message.text}
            ]
        )
        reply = completion.choices[0].message

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
