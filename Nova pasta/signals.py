from datetime import datetime

# 📦 FILA GLOBAL
sinais = []


# ➕ ADD
def add_sinal(sinal):
    sinais.append(sinal)


# 📋 LISTAR
def listar_sinais():
    return sinais


# 📤 GET
def get_sinais():
    return sinais


# ❌ REMOVER 1
def remover_por_indice(indice):
    if 0 <= indice < len(sinais):
        return sinais.pop(indice)
    return None


# ❌ REMOVER VÁRIOS (🔥 NOVO)
def remover_multiplos(indices):
    removidos = []

    # remove do maior pro menor (evita bug de índice)
    for i in sorted(indices, reverse=True):
        if 0 <= i < len(sinais):
            removidos.append(sinais.pop(i))

    return removidos


# ⏱️ BUSCAR POR HORA
def get_sinal_por_horario(hora_atual):
    for s in sinais:
        if s["horario"] == hora_atual:
            return s
    return None


# 🧹 REMOVER SINAL EXECUTADO
def remover_sinal(sinal):
    if sinal in sinais:
        sinais.remove(sinal)