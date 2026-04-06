import requests, config

def enviar(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{config.TOKEN}/sendMessage",
            data={"chat_id": config.CHAT_ID, "text": msg}
        )
    except:
        print("Erro Telegram envio")