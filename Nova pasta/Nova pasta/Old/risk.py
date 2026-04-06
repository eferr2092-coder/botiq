import config

lucro_total = 0

def atualizar(valor):

    global lucro_total

    lucro_total += valor

def verificar():

    if lucro_total >= config.STOP_WIN:
        return "STOP WIN ATINGIDO"

    if lucro_total <= config.STOP_LOSS:
        return "STOP LOSS ATINGIDO"

    return None