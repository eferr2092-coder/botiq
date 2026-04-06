import requests, config, time
from signals import add

def enviar(msg):
    requests.post(f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage",
                  data={"chat_id":config.CHAT_ID,"text":msg})

def parse(txt):
    for l in txt.split("\n"):
        try:
            tf,par,hor,dir=l.split(";")
            s={"par":par,"horario":hor,"dir":dir.lower(),"tf":1}
            if add(s):
                enviar(f"✅ Sinal {par} {hor}")
        except: pass

def iniciar():
    last=None
    while True:
        try:
            r=requests.get(f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/getUpdates").json()
            for u in r["result"]:
                if last==u["update_id"]: continue
                last=u["update_id"]
                if "message" in u:
                    parse(u["message"].get("text",""))
        except: pass
        time.sleep(1)
