from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
login_url = "https://ecsylms1.kj.yamagata-u.ac.jp/webclass/login.php"
target_page = "https://ecsylms1.kj.yamagata-u.ac.jp//webclass/ip_mods.php/plugin/score_summary_table/dashboard"

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
        time.sleep(3)  # ページ読み込み待機（後で最適化可能）

        # ログイン情報入力（セレクタを大学のサイトに合わせる）
        driver.find_element(By.ID, "username").send_keys(username)  # セレクタを変更
        driver.find_element(By.ID, "passward").send_keys(password)
        driver.find_element(By.ID, "LoginBtn").click()
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
