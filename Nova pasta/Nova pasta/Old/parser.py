from signals import add_signal

def importar_sinais(texto):

    linhas = texto.split("\n")
    total = 0

    for linha in linhas:

        try:
            tf, par, horario, direcao = linha.split(";")

            sinal = {
                "tf": tf.strip(),
                "par": par.strip(),
                "horario": horario.strip(),
                "direcao": direcao.strip().upper(),
                "executado": False
            }

            add_signal(sinal)
            total += 1

        except:
            continue

    return total