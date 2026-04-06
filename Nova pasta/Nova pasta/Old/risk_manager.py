import config

lucro_dia = 0


def atualizar_lucro(valor):

    global lucro_dia

    lucro_dia += valor


def verificar_stop():

    if lucro_dia >= config.STOP_WIN:
        return "STOP_WIN"

    if lucro_dia <= config.STOP_LOSS:
        return "STOP_LOSS"

    return "OK"


def status():

    return lucro_dia