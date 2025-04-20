#!/bin/bash
# ChromeとChromeDriverをインストール
apt-get update
apt-get install -y wget unzip
# Chromeをインストール
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable
# ChromeDriverをインストール
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} -O /tmp/chromedriver_version
wget -q https://chromedriver.storage.googleapis.com/$(cat /tmp/chromedriver_version)/chromedriver_linux64.zip -O /tmp/chromedriver.zip
unzip /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
