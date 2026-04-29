def parse_sinal(msg):
    try:
        m, par, horario, direcao = msg.split(";")
        return {"par": par, "hora": horario, "dir": direcao.upper()}
    except:
        return None
