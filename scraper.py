from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def login_and_scrape(login_url, target_page):
    username = os.getenv("UNIVERSITY_USERNAME")
    password = os.getenv("UNIVERSITY_PASSWORD")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-images")
    
    driver = webdriver.Chrome(options=options)  # driverを定義！
    
    try:
        driver.get(login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "m251525")))
        driver.find_element(By.ID, "m251525").send_keys(username)
        driver.find_element(By.ID, "5yG5NEmQ8Z").send_keys(password)
        driver.find_element(By.ID, "LoginBtn").click()
        WebDriverWait(driver, 10).until(EC.url_contains("/webclass"))
        
        driver.get(target_page)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "score-summary")))
        
        content = driver.find_element(By.CLASS_NAME, "score-summary").text
        return content
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return None
    
    finally:
        driver.quit()
