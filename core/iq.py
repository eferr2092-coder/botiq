from iqoptionapi.stable_api import IQ_Option
from config import EMAIL, SENHA
import time

def conectar():
    while True:
        Iq = IQ_Option(EMAIL, SENHA)
        Iq.connect()
        if Iq.check_connect():
            return Iq
        time.sleep(5)
