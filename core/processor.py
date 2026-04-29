from core.parser import parse_sinal
from core.executor import executar
from core.iq import conectar
from core.risk import check_stop
from config import VALOR_ENTRADA
from utils.logger import log

Iq = None

def processar(msg):
    global Iq
    log(f"📩 {msg}")

    sinal = parse_sinal(msg)
    if not sinal:
        return None, 0, "Sinal inválido"

    stop = check_stop(0)
    if stop:
        return None, 0, stop

    if not Iq:
        Iq = conectar()

    resultado, lucro, erro = executar(Iq, sinal, VALOR_ENTRADA)

    if erro:
        return None, 0, erro

    check_stop(lucro)

    return resultado, lucro, None
