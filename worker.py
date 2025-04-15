import schedule
import time
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from scraper import login_and_scrape
from summarize import summarize_content

# 環境変数から設定を読み込み
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def job():
    # 大学のウェブサイトのログインページと対象ページ
    login_url = "https://university.example.com/login"
    target_page = "https://university.example.com/news"
    
    # スクレイピング
    content = login_and_scrape(login_url, target_page)
    if not content:
        print("Failed to scrape content.")
        return
    
    # Gemini API で要約
    summary = summarize_content(content)
    
    # LINE にプッシュ通知
    line_bot_api.push_message(
        LINE_USER_ID,
        TextSendMessage(text=summary or "Failed to fetch or summarize content.")
    )
    print("Notification sent")

# 毎日9時に実行
schedule.every().day.at("09:00").do(job)

# スケジューラのループ
while True:
    schedule.run_pending()
    time.sleep(60)
