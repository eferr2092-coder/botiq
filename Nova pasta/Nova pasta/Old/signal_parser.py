
def parse_signal(msg):

    sinais = []
    linhas = msg.split("\n")

    for linha in linhas:
        try:
            partes = linha.strip().split(";")

            if len(partes) != 4:
                continue

            timeframe = partes[0]
            par = partes[1]
            horario = partes[2]
            direcao = partes[3].upper()

            if direcao not in ["CALL","PUT"]:
                continue

            sinais.append((timeframe, par, horario, direcao))

        except:
            pass

    return sinais
