import time
from logger import log

def iniciar_watchdog():
    while True:
        log("🛡 Sistema ativo")
        time.sleep(180)