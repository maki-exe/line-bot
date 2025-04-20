from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from scraper import login_and_scrape
# from summarize import summarize_content  # 未実装なのでコメントアウト

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(f"User ID: {event.source.user_id}")
    if event.message.text.lower() == "最新情報":
        login_url = "https://ecsylms1.kj.yamagata-u.ac.jp/webclass/login.php"
        target_page = "https://ecsylms1.kj.yamagata-u.ac.jp/webclass/ip_mods.php/plugin/score_summary_table/dashboard"
        content = login_and_scrape(login_url, target_page)
        response = content if content else "Failed to scrape content."
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response[:1000])
        )

@app.route("/notify", methods=["GET"])
def notify():
    user_id = os.getenv("LINE_USER_ID")
    login_url = "https://ecsylms1.kj.yamagata-u.ac.jp/webclass/login.php"
    target_page = "https://ecsylms1.kj.yamagata-u.ac.jp/webclass/ip_mods.php/plugin/score_summary_table/dashboard"
    content = login_and_scrape(login_url, target_page)
    response = content if content else "Failed to fetch content."
    line_bot_api.push_message(
        user_id,
        TextSendMessage(text=response[:1000])
    )
    return "Notification sent"
