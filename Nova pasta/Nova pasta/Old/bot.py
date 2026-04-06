import threading
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import config
from parser import importar_sinais
from scheduler import scheduler_loop

async def start(update, context):

    config.CHAT_ID = update.message.chat_id

    await update.message.reply_text("BOT V15 ULTRA STABLE ATIVO")

async def sinais(update, context):

    if not update.message:
        return

    if not update.message.text:
        return

    texto = update.message.text.strip()

    total = importar_sinais(texto)

    await update.message.reply_text(f"{total} sinais carregados")

def main():

    threading.Thread(target=scheduler_loop, daemon=True).start()

    app = Application.builder().token(config.TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, sinais))

    print("BOT V15 ULTRA STABLE RODANDO")

    app.run_polling()

if __name__ == "__main__":
    main()