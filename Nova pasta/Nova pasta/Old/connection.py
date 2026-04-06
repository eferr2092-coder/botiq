from iqoptionapi.stable_api import IQ_Option
import config
import time
from logger import log

Iq = None

def conectar():

    global Iq

    while True:

        log("Conectando na IQ Option...")

        Iq = IQ_Option(config.EMAIL, config.SENHA)

        Iq.connect()

        if Iq.check_connect():

            Iq.change_balance(config.CONTA)

            log("Conectado com sucesso")

            return

        log("Falha conexão. Tentando novamente...")

        time.sleep(config.RECONNECT_DELAY)