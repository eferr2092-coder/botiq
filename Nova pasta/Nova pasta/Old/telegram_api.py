import requests
import config

def enviar(msg):

    url = f"https://api.telegram.org/bot{config.TOKEN}/sendMessage"

    try:

        requests.post(url, data={
            "chat_id": config.CHAT_ID,
            "text": msg
        })

    except:
        print("Erro ao enviar Telegram")