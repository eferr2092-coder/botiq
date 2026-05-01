import os
from flask import Flask, request
import telebot

# ========================
# CONFIG
# ========================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN não definido!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========================
# LOG SIMPLES
# ========================
def log(msg):
    print(f"[BOT] {msg}", flush=True)

# ========================
# ROTA HOME (IMPORTANTE)
# ========================
@app.route("/")
def home():
    return "Botiq PRO rodando 🚀", 200

# ========================
# WEBHOOK TELEGRAM
# ========================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        log(f"Erro webhook: {e}")
        return "ERROR", 500

# ========================
# COMANDOS BOT
# ========================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "🤖 Bot online! Envie sinal.")

@bot.message_handler(func=lambda m: True)
def handle(msg):
    text = msg.text.strip()
    log(f"Mensagem recebida: {text}")

    try:
        # Exemplo: M1;EURUSD;12:30;CALL
        parts = text.split(";")

        if len(parts) != 4:
            bot.send_message(msg.chat.id, "Formato inválido.\nUse: M1;EURUSD;12:30;CALL")
            return

        timeframe, ativo, horario, direcao = parts

        resposta = (
            f"📊 SINAL RECEBIDO\n\n"
            f"⏱ Timeframe: {timeframe}\n"
            f"💱 Ativo: {ativo}\n"
            f"🕒 Horário: {horario}\n"
            f"📈 Direção: {direcao}"
        )

        bot.send_message(msg.chat.id, resposta)

    except Exception as e:
        log(f"Erro processamento: {e}")
        bot.send_message(msg.chat.id, "Erro ao processar sinal.")

# ========================
# START SERVER
# ========================
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    log(f"Rodando na porta {PORT}")
    app.run(host="0.0.0.0", port=PORT)
