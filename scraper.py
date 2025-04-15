from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def login_and_scrape(url, username, password, target_page):
    # Selenium のオプション設定（ヘッドレスモード）
    options = Options()
    options.add_argument("--headless")  # ブラウザを非表示
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Render 環境用の設定
    driver = webdriver.Chrome(options=options)

    try:
        # ログインページにアクセス
        driver.get(url)
        time.sleep(2)  # ページ読み込み待機

        # ユーザー名とパスワードを入力
        driver.find_element(By.ID, "username").send_keys(username)  # ID は実際の要素に合わせる
        driver.find_element(By.ID, "password").send_keys(password)  # 同上
        driver.find_element(By.ID, "LoginBtn").click()  # ログインボタン
        time.sleep(3)  # ログイン処理待機

        # 対象ページに移動
        driver.get(target_page)
        time.sleep(2)

        # コンテンツを取得（例: お知らせリスト）
        content = driver.find_element(By.CLASS_NAME, "news-list").text  # 実際のセレクタに合わせる
        return content

    finally:
        driver.quit()

# テスト用
if __name__ == "__main__":
    login_url = "https://university.example.com/login"  # 大学のログインページ
    username = "your_username"
    password = "your_password"
    target_page = "https://university.example.com/news"  # 取得したいページ
    result = login_and_scrape(login_url, username, password, target_page)
    print(result)
