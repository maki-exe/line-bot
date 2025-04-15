from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def login_and_scrape(login_url, target_page):
    # 環境変数から認証情報を取得
    username = os.getenv("UNIVERSITY_USERNAME")
    password = os.getenv("UNIVERSITY_PASSWORD")
    
    # Selenium のオプション設定
    options = Options()
    options.add_argument("--headless")  # ヘッドレスモード
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # ログインページにアクセス
        driver.get(login_url)
        time.sleep(2)

        # ログイン情報入力（セレクタは大学のサイトに合わせる）
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # 対象ページに移動
        driver.get(target_page)
        time.sleep(2)

        # コンテンツを取得（例: お知らせリスト）
        content = driver.find_element(By.CLASS_NAME, "news-list").text  # セレクタを調整
        return content

    except Exception as e:
        print(f"Scraping error: {e}")
        return None

    finally:
        driver.quit()
