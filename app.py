import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from openai import OpenAI

app = Flask(__name__)

# Line bot API credentials
line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

# OpenAI API credentials
openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

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
        completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": event.message.text,
                }
            ],
            model="gpt-3.5-turbo"
        )
        reply = completion.choices[0].message.content

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)