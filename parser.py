def parse_sinal(msg):
    try:
        tf, par, hora, direcao = msg.split(";")

        return {
            "timeframe": int(tf.replace("M", "")),
            "par": par.strip().upper(),
            "hora": hora.strip(),
            "direcao": direcao.strip().lower()
        }

    except:
        return None