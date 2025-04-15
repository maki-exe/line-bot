# main.py

import os
from line_bot import app  # Flaskアプリをインポート（実際のインポートパスに応じて調整）

if __name__ == "__main__":
    # Renderが提供するPORT環境変数を取得、デフォルトは5000
    port = int(os.getenv("PORT", 5000))
    # ホストを0.0.0.0に設定して外部アクセスを許可
    app.run(host="0.0.0.0", port=port, debug=False)
