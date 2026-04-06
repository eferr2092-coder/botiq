import time
from datetime import datetime
from trader import executar, MODO_SNIPER
from signals import get_sinais
from logger import log
from bot_control import get_bot
from iq_connection import get_iq


def rodar():
    from telegram_listener import enviar

    log("🧠 V1000 Scheduler PRO (SNIPER + SYNC IQ)")

    executados = set()

    while True:
        if not get_bot():
            time.sleep(1)
            continue

        Iq = get_iq()
        if Iq is None:
            time.sleep(1)
            continue

        try:
            timestamp = Iq.get_server_timestamp()
            agora = datetime.fromtimestamp(timestamp)
        except:
            time.sleep(1)
            continue

        hora_atual = agora.strftime("%H:%M")
        segundo = agora.second

        sinais = get_sinais()

        for i, s in enumerate(sinais):
            if s.get("executado"):
                continue

            chave = f"{i}-{s['hora']}"

            if hora_atual == s["hora"]:

                if MODO_SNIPER:
                    condicao = segundo >= 58
                else:
                    condicao = segundo <= 1

                if condicao and chave not in executados:

                    executados.add(chave)

                    enviar(f"⏳ Executando {s['par']}")

                    res, lucro, msg = executar(s["par"], s["dir"], s["tf"])

                    if msg:
                        enviar(msg)

                    if res == "WIN":
                        enviar(f"✅ WIN 💰 {lucro}")
                    elif res == "LOSS":
                        enviar(f"❌ LOSS 💸 {lucro}")
                    elif res == "STOP":
                        enviar(msg)
                    elif res == "IGNORADO_IA":
                        enviar("🧠 IA bloqueou")
                    elif res == "IGNORADO_MTF":
                        enviar("🧠 MTF bloqueou")

                    s["executado"] = True

        time.sleep(0.2)