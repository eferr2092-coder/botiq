import time
from iq_connection import get_iq

def analisar_tendencia(par):
    Iq = get_iq()

    if Iq is None:
        return None, "⚠ Sem conexão IQ"

    try:
        velas = Iq.get_candles(par, 60, 25, time.time())

        if not velas or len(velas) < 10:
            return None, "⚠ Poucos dados"

        altas = 0
        baixas = 0

        for v in velas[-15:]:
            if v["close"] > v["open"]:
                altas += 1
            else:
                baixas += 1

        # 📊 FORÇA (CORPO DAS VELAS)
        forca_alta = sum([v["close"] - v["open"] for v in velas if v["close"] > v["open"]])
        forca_baixa = sum([v["open"] - v["close"] for v in velas if v["close"] < v["open"]])

        # 🔥 DECISÃO FINAL
        if altas > baixas and forca_alta > forca_baixa:
            return "call", f"📈 Alta FORTE ({altas}x{baixas})"

        elif baixas > altas and forca_baixa > forca_alta:
            return "put", f"📉 Baixa FORTE ({baixas}x{altas})"

        else:
            return None, "⚠ Mercado lateral"

    except Exception as e:
        return None, f"⚠ IA erro"