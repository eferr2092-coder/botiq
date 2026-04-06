import threading

from connection import conectar
from telegram_listener import iniciar as telegram
from scheduler import iniciar as scheduler
from telegram_api import enviar
from logger import log

log("BOT V90 PROFISSIONAL")

conectar()

enviar("BOT V90 ONLINE")

threading.Thread(target=scheduler).start()

telegram()