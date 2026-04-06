import requests
import time
import re

from signals import add_sinal, listar_sinais, remover_por_indice
from trader import get_status, set_stop

TOKEN = "8421186323:AAEPQax_M1f5ZxHDM9DZElTBh5e_ZxHf5WY"
CHAT_ID_GLOBAL = None


def enviar(msg):
    if CHAT_ID_GLOBAL:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID_GLOBAL, "text": msg}
        )


def processar(msg):
    global CHAT_ID_GLOBAL

    chat_id = msg["chat"]["id"]
    CHAT_ID_GLOBAL = chat_id
    texto = msg.get("text", "")

    print("MSG:", texto)

    # 🔰 START
    if texto == "/start":
        enviar("🤖 BOT ONLINE\nEnvie sinais ou comandos")
        return

    # 📊 STATUS
    if texto == "/status":
        s = get_status()
        enviar(
            f"📊 PAINEL\n"
            f"💰 Lucro: {round(s['lucro'],2)}\n"
            f"✅ Wins: {s['wins']}\n"
            f"❌ Loss: {s['loss']}\n"
            f"🎯 Stop Gain: {s['stop_gain']}\n"
            f"🛑 Stop Loss: {s['stop_loss']}"
        )
        return

    # 🎯 STOP CONFIG
    if texto.startswith("/stop"):
        try:
            partes = texto.split()

            gain = float(partes[1])
            loss = float(partes[2])

            set_stop(gain, loss)

            enviar(f"🎯 Stop definido:\nGain: {gain}\nLoss: {loss}")

        except:
            enviar("⚠ Use: /stop 50 -20")
        return

    # ❌ REMOVER SINAL
    if texto.startswith("/remover"):
        try:
            indices = list(map(int, texto.split()[1:]))

            for i in sorted(indices, reverse=True):
                remover_por_indice(i)

            enviar(f"🗑 Removidos: {indices}")

        except:
            enviar("⚠ Use: /remover 1 2 3")
        return

    # 📋 LISTAR FILA
    if texto == "/fila":
        sinais = listar_sinais()

        if not sinais:
            enviar("Fila vazia")
            return

        msg_fila = "📋 FILA:\n"
        for i, s in enumerate(sinais):
            msg_fila += f"{i} - {s['par']} {s['horario']} {s['dir']}\n"

        enviar(msg_fila)
        return

    # 📥 MULTISINAIS
    if ";" in texto:
        linhas = texto.split("\n")

        for linha in linhas:
            try:
                tf, par, horario, direcao = linha.split(";")

                add_sinal({
                    "tf": int(tf.replace("M", "")),
                    "par": par,
                    "horario": horario,
                    "dir": direcao.lower()
                })

                enviar(f"✅ Sinal adicionado {par} {horario}")

            except:
                enviar(f"Erro no sinal: {linha}")


def iniciar():
    last_update = None

    while True:
        try:
            r = requests.get(
                f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                params={"offset": last_update, "timeout": 10}
            ).json()

            for update in r["result"]:
                last_update = update["update_id"] + 1

                if "message" in update:
                    processar(update["message"])

        except Exception as e:
            print("Erro Telegram:", e)

        time.sleep(1)