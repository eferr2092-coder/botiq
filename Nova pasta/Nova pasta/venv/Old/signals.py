fila = []

def get_sinais():
    return fila

def adicionar_sinal(s):
    if s not in fila:
        fila.append(s)

def remover_sinal(s):
    if s in fila:
        fila.remove(s)