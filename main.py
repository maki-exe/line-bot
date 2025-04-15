# main.py
import os
from line_bot import app  # line_bot.py から Flask アプリをインポート

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Render の PORT を取得、デフォルトは 5000
    app.run(host="0.0.0.0", port=port, debug=False)  # 0.0.0.0 でリッスン
