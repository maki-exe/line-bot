import os
import schedule
import time
import threading
from linebot import LineBotApi
from linebot.models import TextSendMessage
from line_bot import app
from scraper import login_and_scrape
from summarize import summarize_content

# LINE Botの設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 定期タスク
def job():
    login_url = "https://example-univ.ac.jp/login"  # 実際のURLに変更
    target_page = "https://example-univ.ac.jp/news"
    content = login_and_scrape(login_url, target_page)
    if not content:
        print("Failed to scrape content.")
        return
    summary = summarize_content(content)
    line_bot_api.push_message(
        LINE_USER_ID,
        TextSendMessage(text=summary or "Failed to fetch or summarize content.")
    )
    print("Notification sent")

# スケジューラを別スレッドで実行
def run_scheduler():
    schedule.every().day.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # スケジューラをスレッドで開始
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Flaskアプリを起動
    port = int(os.getenv("PORT", 5000))  # RenderのPORTを取得
    app.run(host="0.0.0.0", port=port, debug=False)
