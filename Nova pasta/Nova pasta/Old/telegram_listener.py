import requests
import time
from config import TOKEN
from signals import add_sinal, remover_multiplos, get_sinais
from trader import get_status
from logger import log

CHAT_ID = None
offset = None


def enviar(msg):
    global CHAT_ID

    if not CHAT_ID:
        return

    try:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg},
            timeout=5
        )
    except:
        log("⚠ Falha envio Telegram")


def painel():
    s = get_status()
    fila = get_sinais()

    total = s["wins"] + s["loss"]
    winrate = (s["wins"] / total * 100) if total > 0 else 0

    restantes = len([x for x in fila if not x.get("executado")])

    return (
        f"📊 V700 ELITE\n"
        f"💰 Lucro: {s['lucro']}\n"
        f"✅ Wins: {s['wins']} | ❌ Loss: {s['loss']}\n"
        f"📈 Assertividade: {winrate:.1f}%\n"
        f"📋 Fila: {len(fila)} | ⏳ Restantes: {restantes}"
    )


def iniciar():
    global offset, CHAT_ID

    log("🤖 Telegram V700 ON")

    while True:
        try:
            r = requests.get(
                f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                params={"offset": offset},
                timeout=10
            )

            data = r.json()

            for u in data.get("result", []):
                offset = u["update_id"] + 1

                msg = u.get("message")
                if not msg:
                    continue

                CHAT_ID = msg["chat"]["id"]
                texto = msg.get("text", "")

                log(f"MSG: {texto}")

                # 📊 STATUS
                if texto == "/status":
                    enviar(painel())
                    continue

                # 🗑 REMOVER
                if texto.startswith("/remover"):
                    try:
                        nums = texto.replace("/remover", "").strip().split(",")
                        indices = [int(n) - 1 for n in nums]

                        remover_multiplos(indices)
                        enviar("🗑 Removido com sucesso")
                    except:
                        enviar("⚠ Erro ao remover")
                    continue

                # 📥 SINAIS
                linhas = texto.split("\n")

                for l in linhas:
                    try:
                        tf, par, hora, d = l.split(";")

                        add_sinal({
                            "tf": int(tf.replace("M","")),
                            "par": par,
                            "hora": hora,
                            "dir": d.lower()
                        })

                        enviar(f"✅ {par} {hora}")

                    except:
                        enviar("⚠ Formato inválido")

        except Exception as e:
            log(f"⚠ Telegram reconectando: {e}")
            time.sleep(5)

        time.sleep(1)