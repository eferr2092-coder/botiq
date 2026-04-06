import requests
import config
from signals import adicionar_sinal
from telegram_api import enviar

offset = 0  # IMPORTANTE

def parse(txt):
    try:
        p = txt.split(";")
        return {
            "tf": int(p[0].replace("M", "")),
            "par": p[1],
            "hora": p[2],
            "dir": p[3].lower()
        }
    except:
        return None

def listen():
    global offset

    url = f"https://api.telegram.org/bot{config.TOKEN}/getUpdates?offset={offset+1}"

    try:
        r = requests.get(url).json()

        for u in r.get("result", []):
            offset = u["update_id"]

            msg = u.get("message", {}).get("text")

            if msg:
                sinal = parse(msg)

                if sinal:
                    add(sinal)
                    enviar(f"✅ Sinal adicionado {sinal['par']} {sinal['hora']}")

    except Exception as e:
        print("Erro Telegram:", e)