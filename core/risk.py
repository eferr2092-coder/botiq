lucro_total = 0

def check_stop(valor):
    global lucro_total
    lucro_total += valor
    if lucro_total >= 50:
        return "STOP WIN"
    if lucro_total <= -30:
        return "STOP LOSS"
    return None
