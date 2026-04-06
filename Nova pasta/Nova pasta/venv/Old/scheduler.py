import time
from datetime import datetime
from signals import get_sinais, remover_sinal
from trader import executar
from telegram_api import enviar
from risk import atualizar, stop

def rodar():
    print("Scheduler ON")

    while True:
        agora = datetime.now().strftime("%H:%M")

        sinais = get_sinais()

        for s in sinais[:]:
            if s["hora"] == agora:
                enviar(f"🚀 Executando {s['par']}")

                res, lucro = executar(s["par"], s["dir"], s["tf"])

                atualizar(lucro)

                enviar(f"📊 Resultado: {res.upper()}\n💰 {lucro}")

                remover_sinal(s)

                s_stop = stop()
                if s_stop:
                    enviar(f"⛔ STOP {s_stop} atingido")
                    exit()

        time.sleep(1)