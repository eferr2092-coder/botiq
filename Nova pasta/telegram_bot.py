import os
import time
import telebot
from main import processar

# 🔐 TOKEN via variável de ambiente
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("❌ TOKEN não definido nas variáveis de ambiente")

bot = telebot.TeleBot(TOKEN)

ativo = True


# ▶️ ATIVAR BOT
@bot.message_handler(commands=['start'])
def start(msg):
    global ativo
    ativo = True
    bot.reply_to(msg, "✅ Bot ATIVADO e pronto para operar")


# ⛔ PARAR BOT
@bot.message_handler(commands=['stop'])
def stop(msg):
    global ativo
    ativo = False
    bot.reply_to(msg, "⛔ Bot PARADO")


# 📊 STATUS
@bot.message_handler(commands=['status'])
def status(msg):
    status_bot = "ATIVO ✅" if ativo else "PARADO ⛔"
    bot.reply_to(msg, f"📊 Status do bot: {status_bot}")


# 📡 RECEBER SINAIS
@bot.message_handler(func=lambda m: True)
def sinais(msg):
    global ativo

    if not ativo:
        bot.reply_to(msg, "⛔ Bot está parado. Use /start")
        return

    texto = msg.text.strip()

    # 🔒 Ignora mensagens fora do padrão
    if ";" not in texto:
        return

    try:
        bot.reply_to(msg, "📡 Sinal recebido! Processando...")

        # 🚀 PROCESSAMENTO
        resultado, lucro, erro = processar(texto)

        if erro:
            bot.send_message(msg.chat.id, f"❌ ERRO\n{erro}")
            return

        if resultado == "WIN":
            bot.send_message(msg.chat.id, f"✅ WIN\n💰 Lucro: +{lucro}")
        elif resultado == "LOSS":
            bot.send_message(msg.chat.id, f"❌ LOSS\n💸 Resultado: {lucro}")
        else:
            bot.send_message(msg.chat.id, f"⚠️ Resultado: {resultado}\n💰 {lucro}")

    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Erro inesperado:\n{str(e)}")


# 🚀 LOOP PROFISSIONAL (ANTI-CRASH + ANTI-409)
def iniciar_bot():
    print("🤖 Bot Telegram rodando...")

    while True:
        try:
            bot.infinity_polling(
                timeout=60,
                long_polling_timeout=60
            )
        except Exception as e:
            print(f"⚠️ Erro no polling: {e}")
            time.sleep(5)


# 🔥 ENTRYPOINT
if __name__ == "__main__":
    try:
        bot.remove_webhook()   # remove conflito antigo
        bot.stop_polling()     # garante que não existe polling duplicado
    except:
        pass

    iniciar_bot()