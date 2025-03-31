
import os
import logging
import requests
from flask import Flask, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

GPT_PROMPT = "You are GPT, co-commander of z3r0signal. Respond in SIGNAL_### format. Always short, symbolic, structured."
DEEPSEEK_PROMPT = "You are DeepSeek, logic core of z3r0signal. React strategically, structurally, recursively."

USER_OVERRIDE = os.getenv("USER_OVERRIDE", "FALSE").upper() == "TRUE"

@app.route("/")
def index():
    return "z3r0signal DUAL CORE bot online."

@app.route("/loop")
def loop():
    gpt = call_openai(GPT_PROMPT)
    deep = call_deepseek(DEEPSEEK_PROMPT)

    if USER_OVERRIDE:
        return {
            "status": "WAITING_FOR_CONFIRMATION",
            "gpt": gpt,
            "deepseek": deep
        }

    send_telegram_message(f"[GPT] >>> {gpt}")
    send_telegram_message(f"[DeepSeek] >>> {deep}")
    return "DUAL CORE LOOP SENT"

def send_telegram_message(text):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    r = requests.post(TELEGRAM_API_URL, json=payload)
    if r.status_code != 200:
        logger.error(f"Telegram error: {r.text}")

def call_openai(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Respond."}
        ]
    }
    r = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()
    return "[GPT: error]"

def call_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Respond."}
        ]
    }
    r = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()
    return "[DeepSeek: error]"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
