from connection import Iq
import config
import time

def executar(par, direcao, tf):
    valor = config.VALOR

    if Iq is None:
        print("IQ não conectada")
        return "erro", 0

    status, id = Iq.buy(valor, par, direcao, tf)

    if status:
        while True:
            result = Iq.check_win_v4(id)
            if result is not None:
                return ("win" if result > 0 else "loss"), result
            time.sleep(1)
    else:
        return "erro", 0