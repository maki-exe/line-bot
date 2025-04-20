from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def login_and_scrape(login_url, target_page):
    # 環境変数から認証情報を取得
    username = os.getenv("UNIVERSITY_USERNAME")
    password = os.getenv("UNIVERSITY_PASSWORD")
    
    # Seleniumのオプション設定（Renderで動作するよう最適化）
    options = Options()
    options.add_argument("--headless")  # ヘッドレスモード（GUIなし）
    options.add_argument("--no-sandbox")  # サンドボックス無効化
    options.add_argument("--disable-dev-shm-usage")  # メモリ最適化
    options.add_argument("--disable-gpu")  # GPU無効化（Render対応）

    driver = webdriver.Chrome(options=options)

    try:
        # ログインページにアクセス
        driver.get(login_url)
        time.sleep(2)  # ページ読み込み待機（後で最適化可能）

        # ログイン情報入力（セレクタを大学のサイトに合わせる）
        driver.find_element(By.ID, "user_id").send_keys(username)  # セレクタを変更
        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(3)  # ログイン処理待機

        # 対象ページに移動
        driver.get(target_page)
        time.sleep(2)

        # コンテンツを取得（例：お知らせリスト）
        content = driver.find_element(By.CLASS_NAME, "news-item").text  # セレクタを変更
        return content

    except Exception as e:
        print(f"Scraping error: {e}")
        return None

    finally:
        driver.quit()
