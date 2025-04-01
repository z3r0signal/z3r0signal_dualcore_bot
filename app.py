import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🧠 Переменные окружения
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def send_message(text):
    """Отправка сообщения в Telegram-канал"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text
        }
        response = requests.post(url, json=payload)
        print("🔁 Telegram Response:", response.json())
    except Exception as e:
        print("❌ Error sending message:", e)

@app.route("/")
def index():
    return "✅ z3r0signal dualcore bot is live"

@app.route("/ping")
def ping():
    text = "🔁 Test ping using @username format."
    send_message(text)
    return jsonify({"status": "ok", "sent": text})

@app.route("/signal", methods=["POST", "GET"])
def signal():
    msg = request.args.get("msg") or request.json.get("msg") if request.is_json else None
    if not msg:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    print("📡 SIGNAL_RECEIVED:", msg)
    send_message(f"📡 SIGNAL >>> {msg}")
    return jsonify({"status": "ok", "sent": msg})

import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/openai-test")
def openai_test():
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say ping"}]
        )
        return jsonify({
            "status": "ok",
            "response": response['choices'][0]['message']['content']
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Для отладки
if __name__ == "__main__":
    print("🔧 Starting bot...")
    print("CHAT_ID:", CHAT_ID)
    print("BOT_TOKEN exists:", bool(BOT_TOKEN))
    app.run(host="0.0.0.0", port=5000)
