import requests
import config

def send_telegram(msg):

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": config.CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=data)
    except:
        print("Erro ao enviar mensagem telegram")