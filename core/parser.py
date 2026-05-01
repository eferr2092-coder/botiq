def parse_sinal(msg):
    try:
        partes = msg.split(";")
        return {
            "timeframe": partes[0],
            "ativo": partes[1],
            "horario": partes[2],
            "direcao": partes[3]
        }
    except:
        return None
