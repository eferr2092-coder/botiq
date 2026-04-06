from iqoptionapi.stable_api import IQ_Option
from config import EMAIL, SENHA
from logger import log
import time

Iq = None

def conectar():
    global Iq

    for tentativa in range(5):
        try:
            log("🔌 Conectando na IQ...")
            Iq = IQ_Option(EMAIL, SENHA)
            status, _ = Iq.connect()

            if status:
                log("✅ IQ CONECTADA")
                return Iq

        except Exception as e:
            log(f"❌ Erro conexão: {e}")

        time.sleep(3)

    return None


def get_iq():
    global Iq

    try:
        if Iq is None:
            return conectar()

        Iq.get_balance()
        return Iq

    except:
        log("⚠ Reconectando...")
        Iq = None
        return conectar()