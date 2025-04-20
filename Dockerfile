# Ubuntuベースイメージ（Renderの無料プランで動作確認済み）
FROM ubuntu:22.04

# 環境変数を設定（非対話モードでapt-getをスムーズに）
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    python3 \
    python3-pip \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriverをインストール
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} -O /tmp/chromedriver_version && \
    wget -q https://chromedriver.storage.googleapis.com/$(cat /tmp/chromedriver_version)/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# 作業ディレクトリを設定
WORKDIR /app

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# Gunicornでアプリを起動
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "line_bot:app"]
