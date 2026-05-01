from flask import Flask, request
import telebot
import os
from core.processor import processar

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# 🔹 COMANDO START
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Botiq PRO ONLINE")

# 🔹 RECEBER SINAIS
@bot.message_handler(func=lambda m: True)
def handle(message):
    if ";" not in message.text:
        return

    resultado, lucro, erro = processar(message.text)

    if erro:
        bot.reply_to(message, f"❌ {erro}")
    else:
        bot.reply_to(message, f"✅ {resultado} | 💰 {lucro}")

# 🔹 WEBHOOK
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# 🔹 HEALTHCHECK (Railway)
@app.route("/")
def home():
    return "Botiq PRO rodando 🚀", 200

if __name__ == "__main__":
    bot.remove_webhook()
    print("🚀 Iniciando servidor...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
