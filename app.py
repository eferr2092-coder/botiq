import os
import threading
from flask import Flask, request
import telebot

from config import TOKEN, WEBHOOK_URL
from core.processor import processar
from utils.queue import fila
from utils.logger import log

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def worker():
    while True:
        msg = fila.get()
        try:
            resultado, lucro, erro = processar(msg)
            if erro:
                log(f"❌ {erro}")
            else:
                log(f"✅ {resultado} {lucro}")
        except Exception as e:
            log(f"Erro worker: {e}")

threading.Thread(target=worker, daemon=True).start()

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot institucional rodando 🚀"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Bot ativo")

@bot.message_handler(func=lambda m: True)
def sinais(msg):
    if ";" in msg.text:
        fila.put(msg.text)
        bot.reply_to(msg, "📡 Sinal recebido")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    log("🚀 Webhook ativo")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
