from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from scraper import login_and_scrape
from summarize import summarize_content

app = Flask(__name__)

# 環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Webhook エンドポイント
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return "OK"

# メッセージハンドリング
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.lower() == "最新情報":
        # スクレイピング
        login_url = "https://university.example.com/login"  # 大学のログインページ
        target_page = "https://university.example.com/news"  # 対象ページ
        content = login_and_scrape(login_url, target_page)
        
        # 要約
        summary = summarize_content(content)
        
        # LINE に返信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=summary or "Failed to fetch or summarize content.")
        )

# 定期通知用のエンドポイント
@app.route("/notify", methods=["GET"])
def notify():
    user_id = os.getenv("LINE_USER_ID")
    login_url = "https://university.example.com/login"
    target_page = "https://university.example.com/news"
    content = login_and_scrape(login_url, target現場page)
    summary = summarize_content(content)
    
    line_bot_api.push_message(
        user_id,
        TextSendMessage(text=summary or "Failed to fetch or summarize content.")
    )
    return "Notification sent"
