from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# あなたのチャネルアクセストークンとシークレット
LINE_CHANNEL_ACCESS_TOKEN = 'o8T0V8Y+K/DEvrChn7REIkaBnosq9wtc0WXYA5QePh+NMKMBpx+DkJiS5HWjdJQ6J+J8VEfDd8ZK7qdP/pbHymEzyrSJqzHGlF2hP6eBl4TQ5gztovqaKrTEbaIigYv5ByR/bTk93+Y1DVjJ2XjM2AdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '380e4885058d6dc7c8f3cf7b2af37dfe'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_text = f"あなたが送ったのは「{event.message.text}」ですね！"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
