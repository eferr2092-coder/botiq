import telebot
from main import processar

TOKEN = "8421186323:AAEPQax_M1f5ZxHDM9DZElTBh5e_ZxHf5WY"
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

    if ";" not in msg.text:
        return

    try:
        # 📡 Confirma recebimento
        bot.reply_to(msg, "📡 Sinal recebido! Processando...")

        # 🚀 PROCESSA SINAL
        resultado, lucro, erro = processar(msg.text)

        # 📊 RESPOSTA PROFISSIONAL
        if erro:
            bot.send_message(
                msg.chat.id,
                f"❌ ERRO\n{erro}"
            )
        else:
            if resultado == "WIN":
                bot.send_message(
                    msg.chat.id,
                    f"✅ WIN\n💰 Lucro: +{lucro}"
                )
            elif resultado == "LOSS":
                bot.send_message(
                    msg.chat.id,
                    f"❌ LOSS\n💸 Lucro: {lucro}"
                )
            else:
                bot.send_message(
                    msg.chat.id,
                    f"⚠️ Resultado: {resultado}\n💰 {lucro}"
                )

    except Exception as e:
        bot.send_message(
            msg.chat.id,
            f"❌ Erro inesperado:\n{e}"
        )


# 🔁 LOOP
print("🤖 Bot Telegram rodando...")
bot.polling(none_stop=True)