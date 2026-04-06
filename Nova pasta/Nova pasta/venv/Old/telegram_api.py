import requests
import config

def enviar(msg):
    url = f"https://api.telegram.org/bot{config.TOKEN}/sendMessage"
    data = {"chat_id": config.CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except:
        print("Erro ao enviar Telegram")