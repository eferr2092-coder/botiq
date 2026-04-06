from scheduler import rodar
from telegram_listener import iniciar
from trader import conectar
import threading
import time

print("🚀 V300 ELITE INICIADA")

# 🔌 CONECTA IQ PRIMEIRO
while True:
    Iq = conectar()
    if Iq:
        break
    print("🔄 Tentando reconectar IQ...")
    time.sleep(3)

# 🚀 THREAD TELEGRAM
threading.Thread(target=iniciar).start()

# 🧠 THREAD SCHEDULER
threading.Thread(target=rodar).start()