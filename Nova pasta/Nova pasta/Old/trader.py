import time
from iq_connection import conectar
from config import VALOR
from telegram_listener import enviar
from stats import add_result
from logger import log

def executar(par, direcao, tf):
    Iq = conectar()

    if not Iq:
        enviar("❌ Erro conexão IQ")
        return 0

    log(f"EXECUTANDO {par} {direcao}")
    enviar(f"🚀 Executando {par} {direcao.upper()}")

    status, id = Iq.buy(VALOR, par, direcao, tf)

    if not status:
        enviar("❌ Falha ao enviar ordem")
        return 0

    while True:
        check, lucro = Iq.check_win_v4(id)

        if check:
            log(f"RESULTADO {lucro}")

            add_result(lucro)

            if lucro > 0:
                enviar(f"🏆 WIN {round(lucro,2)}")
            else:
                enviar(f"💀 LOSS {round(lucro,2)}")

            return lucro

        time.sleep(1)