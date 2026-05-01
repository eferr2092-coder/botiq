import time

def executar(iq, sinal, valor):
    try:
        ativo = sinal["ativo"]
        direcao = sinal["direcao"].lower()
        timeframe = 1

        status, id = iq.buy(valor, ativo, direcao, timeframe)

        if not status:
            return None, 0, "Erro ao executar ordem"

        while True:
            check, lucro = iq.check_win_v4(id)
            if check:
                resultado = "WIN" if lucro > 0 else "LOSS"
                return resultado, lucro, None
            time.sleep(1)

    except Exception as e:
        return None, 0, str(e)
