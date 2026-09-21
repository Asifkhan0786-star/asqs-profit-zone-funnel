import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

CHANNEL_URL = os.getenv("TELEGRAM_CHANNEL_URL", "https://t.me/your_channel")
BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "your_bot")

@app.get("/")
def home():
    return render_template(
        "index.html",
        channel_url=CHANNEL_URL,
        bot_username=BOT_USERNAME,
    )

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "asqs-profit-zone-web"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
