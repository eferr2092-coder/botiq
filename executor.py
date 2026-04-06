# -*- coding: utf-8 -*-

import time
import threading
import sys
from datetime import datetime

from validator import validar_ativo
from risk_manager import atualizar_lucro
from logger import log


# 🔥 IGNORA ERRO INTERNO DA IQ (underlying)
def ignore_thread_exception(args):
    if "underlying" in str(args.exc_value):
        return
    sys.__excepthook__(args.exc_type, args.exc_value, args.exc_traceback)


threading.excepthook = ignore_thread_exception


# ⏳ SINCRONIZAÇÃO COM HORÁRIO DA IQ (PROFISSIONAL)
def esperar_horario(Iq, hora):
    log(f"⏳ Sincronizando com horario da IQ para {hora}")

    while True:
        try:
            timestamp = Iq.get_server_timestamp()
            agora_dt = datetime.fromtimestamp(timestamp)

            agora = agora_dt.strftime("%H:%M")
            segundos = agora_dt.strftime("%S")

            # 🔥 ENTRADA PRECISA (segundo 59 → antes do candle virar)
            if agora == hora and int(segundos) >= 58:
                log(f"🚀 Entrada precisa no segundo {segundos}")
                break

        except Exception as e:
            log(f"⚠ Erro ao obter horario IQ: {e}")

        time.sleep(0.2)


# 🚀 EXECUÇÃO PRINCIPAL
def executar(Iq, sinal, valor):
    par = sinal["par"]
    direcao = sinal["direcao"]
    timeframe = sinal["timeframe"]

    log(f"🎯 Preparando ordem: {par} {direcao} M{timeframe}")

    # 🔎 VALIDAR ATIVO
    par_valido = validar_ativo(Iq, par)

    if not par_valido:
        log("❌ Ativo indisponivel")
        return "ERRO", 0, "Ativo fechado ou invalido"

    log(f"✅ Ativo validado: {par_valido}")

    # ⏳ SINCRONIZAR COM IQ
    esperar_horario(Iq, sinal["hora"])

    # 🔁 TENTATIVAS DE EXECUÇÃO
    for tentativa in range(3):
        try:
            log(f"🚀 Tentativa {tentativa+1}")

            status, trade_id = Iq.buy(valor, par_valido, direcao, timeframe)

            log(f"📡 Status: {status} | ID: {trade_id}")

            if status:
                log("✅ Ordem executada com sucesso")
                break

        except Exception as e:
            log(f"❌ Erro execução: {e}")

        time.sleep(1)

    else:
        log("❌ Falha total ao executar ordem")
        return "ERRO", 0, "Falha execucao (IQ Option)"

    # ⏱️ AGUARDAR RESULTADO COM TIMEOUT
    timeout = time.time() + (timeframe * 60 + 30)

    while time.time() < timeout:
        try:
            check, lucro = Iq.check_win_v4(trade_id)

            if check:
                lucro = round(lucro, 2)

                atualizar_lucro(lucro)

                if lucro > 0:
                    log(f"✅ WIN {lucro}")
                    return "WIN", lucro, None
                else:
                    log(f"❌ LOSS {lucro}")
                    return "LOSS", lucro, None

        except Exception:
            pass

        time.sleep(1)

    log("⏳ Timeout ao obter resultado")
    return "ERRO", 0, "Timeout resultado"