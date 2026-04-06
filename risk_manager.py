from config import *

lucro_total = 0

def atualizar_lucro(valor):
    global lucro_total
    lucro_total += valor

def check_stop():
    if lucro_total >= STOP_GAIN:
        return "STOP_GAIN"
    if lucro_total <= STOP_LOSS:
        return "STOP_LOSS"
    return None