import os
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re

app = Flask(__name__)

# Line bot API credentials
line_bot_api = LineBotApi('q8MasGUuwFhWx+O1opafyqY9vwRoy7RvYQTjgGcyjNFaI4x063mir+fnikvoyk2QqD+2uiEKJneCeNscwao694ZT82rH7mpHOMjtD5FC3XIdImkPAUKoVrbGRyWqehPSav3eYPBxxFea7K3EjELWOQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7a4ff39e79a9b8961c5ddf5f3b9a8bbf')

# ChatGPT API credentials
CHATGPT_API_KEY = 'sk-proj-kNysSwucjLn3bm8TssDAT3BlbkFJ6TWhLbgELrgaTcXC6UWY'
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'

# Function to send message to ChatGPT API
def send_to_chatgpt(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHATGPT_API_KEY}',
    }
    data = {
        'model': 'text-davinci-002',  # You can choose a different model if needed
        'messages': [
            {
                'role': 'system',
                'content': message
            }
        ]
    }
    response = requests.post(CHATGPT_API_URL, json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']

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
        # Send the user's message to ChatGPT and get a response
        user_message = event.message.text
        reply = send_to_chatgpt(user_message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
