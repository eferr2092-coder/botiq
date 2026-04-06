import config

lucro_total = 0

def atualizar(valor):
    global lucro_total
    lucro_total += valor

def stop():
    if lucro_total >= config.STOP_GAIN:
        return "GAIN"
    if lucro_total <= config.STOP_LOSS:
        return "LOSS"
    return None