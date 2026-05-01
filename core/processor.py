from core.parser import parse_sinal
from core.executor import executar
from core.iq import get_iq
from core.risk import check_stop
from config import VALOR_ENTRADA
from utils.logger import log

def processar(msg):
    log(f"📩 {msg}")

    sinal = parse_sinal(msg)
    if not sinal:
        return None, 0, "Sinal inválido"

    stop = check_stop()
    if stop:
        return None, 0, stop

    iq = get_iq()
    if not iq:
        return None, 0, "Erro conexão IQ Option"

    try:
        resultado, lucro, erro = executar(iq, sinal, VALOR_ENTRADA)
        return resultado, lucro, erro
    except Exception as e:
        return None, 0, str(e)
