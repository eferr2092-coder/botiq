fila = []

def adicionar(sinal):

    fila.append(sinal)

def remover(sinal):

    if sinal in fila:
        fila.remove(sinal)