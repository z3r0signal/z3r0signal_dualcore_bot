import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "7403673880:AAHoo7OD8HUYRY5Rwkv60CTR12nLlzFqSro"
CHAT_ID = "-1002604077163"

@app.route("/")
def index():
    return "z3r0signal dualcore bot is live"

@app.route("/ping")
def ping():
    text = "🔁 Test ping using @username format."
    send_message(text)
    return jsonify({"status": "ok", "sent": text})

@app.route("/signal")
def signal():
    msg = request.args.get("msg", "⚠️ Signal received.")
    send_message(f"📡 SIGNAL >>> {msg}")
    return jsonify({"status": "ok", "sent": msg})

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
