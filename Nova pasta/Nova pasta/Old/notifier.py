import asyncio
from telegram import Bot
import config

bot = None


def get_bot():

    global bot

    if bot is None:
        bot = Bot(token=config.TELEGRAM_TOKEN)

    return bot


async def enviar_alerta(bot, chat_id, texto):

    await bot.send_message(
        chat_id=chat_id,
        text=texto
    )


def enviar_alerta_scheduler(chat_id, texto):

    bot = get_bot()

    asyncio.run(
        bot.send_message(
            chat_id=chat_id,
            text=texto
        )
    )