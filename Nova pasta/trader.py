import time
from iq_connection import get_iq
from config import VALOR
from logger import log

# 🧠 IA opcional
try:
    from ia_filter import analisar_tendencia
except:
    analisar_tendencia = None

# 🔥 MODOS
MODO_SNIPER = False
MODO_MTF = False

# 🔥 IA
IA_ATIVA = False

# 📊 STATUS
status = {
    "lucro": 0,
    "wins": 0,
    "loss": 0,
    "stop_gain": 50,
    "stop_loss": -20
}


def get_status():
    return status


def ativar_ia(valor: bool):
    global IA_ATIVA
    IA_ATIVA = valor
    log(f"IA {'ATIVADA' if valor else 'DESATIVADA'}")


def set_stop(gain, loss):
    status["stop_gain"] = float(gain)
    status["stop_loss"] = -abs(float(loss))


def pode_operar():
    if status["lucro"] >= status["stop_gain"]:
        return False, "🎯 STOP GAIN ATINGIDO"

    if status["lucro"] <= status["stop_loss"]:
        return False, "🛑 STOP LOSS ATINGIDO"

    return True, ""


# 🧠 MTF
def confirmar_mtf(Iq, par, direcao):
    try:
        velas_m1 = Iq.get_candles(par, 60, 5, time.time())
        velas_m5 = Iq.get_candles(par, 300, 5, time.time())

        def tendencia(velas):
            alta = sum(1 for v in velas if v["close"] > v["open"])
            baixa = sum(1 for v in velas if v["close"] < v["open"])
            return "call" if alta > baixa else "put"

        t1 = tendencia(velas_m1)
        t5 = tendencia(velas_m5)

        if t1 == direcao and t5 == direcao:
            return True, f"🧠 MTF OK ({t1}/{t5})"
        else:
            return False, f"❌ MTF FALHOU ({t1}/{t5})"

    except Exception as e:
        log(f"Erro MTF: {e}")
        return False, "Erro MTF"


def executar(par, direcao, timeframe):
    ok_operar, msg = pode_operar()

    if not ok_operar:
        return "STOP", 0, msg

    Iq = get_iq()

    if Iq is None:
        return "ERRO_CONEXAO", 0, ""

    info = ""

    # 🧠 IA
    if IA_ATIVA and analisar_tendencia:
        try:
            tendencia, info = analisar_tendencia(par)
            if tendencia != direcao:
                return "IGNORADO_IA", 0, info
        except Exception as e:
            log(f"Erro IA: {e}")

    # 🧠 MTF
    if MODO_MTF:
        ok, info_mtf = confirmar_mtf(Iq, par, direcao)
        if not ok:
            return "IGNORADO_MTF", 0, info_mtf

    try:
        ok, order_id = Iq.buy(VALOR, par, direcao, timeframe)

        if not ok:
            return "ERRO_ORDEM", 0, ""

        log(f"🚀 Ordem enviada {par}")

        time.sleep(timeframe * 60)

        resultado = Iq.check_win_v4(order_id)

        if isinstance(resultado, tuple):
            resultado = resultado[0]

        if isinstance(resultado, str):
            resultado = VALOR * 0.8 if resultado.lower() == "win" else -VALOR

        resultado = round(float(resultado), 2)

    except Exception as e:
        log(f"❌ ERRO EXECUÇÃO: {e}")
        return "ERRO", 0, ""

    status["lucro"] += resultado

    if resultado > 0:
        status["wins"] += 1
        return "WIN", resultado, info
    else:
        status["loss"] += 1
        return "LOSS", resultado, info