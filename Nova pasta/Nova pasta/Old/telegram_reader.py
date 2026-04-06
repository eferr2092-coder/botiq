import requests
import time
import config
from signals import adicionar
from telegram_api import enviar

last_update = None

def iniciar_leitura():

    global last_update

    print("Leitura Telegram ativa")

    while True:

        url = f"https://api.telegram.org/bot{config.TOKEN}/getUpdates"

        data = requests.get(url).json()

        for update in data["result"]:

            update_id = update["update_id"]

            if last_update is None:
                last_update = update_id
                continue

            if update_id <= last_update:
                continue

            last_update = update_id

            if "message" not in update:
                continue

            msg = update["message"]

            chat_id = msg["chat"]["id"]

            if chat_id not in config.GRUPOS_SINAIS and str(chat_id) != str(config.CHAT_ID):
                continue

            texto = msg.get("text","").strip()

            if texto == "":
                continue

            try:

                partes = texto.split(";")

                if len(partes) != 4:
                    continue

                timeframe = partes[0].strip()
                par = partes[1].strip()
                horario = partes[2].strip()
                direcao = partes[3].strip().lower()

                adicionar(timeframe,par,horario,direcao)

                print("SINAL CAPTURADO ->",par,horario,direcao)

                enviar(f"SINAL CAPTURADO\n{par} {horario} {direcao}")

            except:

                pass

        time.sleep(config.TELEGRAM_DELAY)