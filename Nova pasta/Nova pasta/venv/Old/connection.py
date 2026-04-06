from iqoptionapi.stable_api import IQ_Option
import config

Iq = None

def conectar():
    global Iq
    Iq = IQ_Option(config.EMAIL, config.SENHA)
    status, reason = Iq.connect()

    if status:
        print("IQ conectada")
        return Iq
    else:
        print("Erro IQ:", reason)
        return None