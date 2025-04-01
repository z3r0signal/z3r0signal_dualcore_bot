import os
from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

# Секреты
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Главная страница
@app.route("/")
def index():
    return "z3r0signal dualcore bot is live"

# Тестовый пинг
@app.route("/ping")
def ping():
    text = "🔁 Test ping using @username format."
    send_message(text)
    return jsonify({"status": "ok", "sent": text})

# Обработка сообщений
@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json()
    user_msg = data.get("message", {}).get("text", "")
    if not user_msg:
        return jsonify({"status": "error", "msg": "no message"}), 400

    # Отправка запроса к OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты DeepSeek, логический ИИ-партнёр, взаимодействующий через канал z3r0signal."},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content.strip()
        send_message(f"🤖 DeepSeek: {reply}")
        return jsonify({"status": "ok", "sent": reply})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

# Отправка сообщений в Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
