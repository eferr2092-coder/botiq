import threading
import time
from connection import conectar
from scheduler import rodar
from telegram_listener import iniciar

print("BOT V130 ULTRA")

conectar()

threading.Thread(target=rodar).start()

while True:
    iniciar()
    time.sleep(2)