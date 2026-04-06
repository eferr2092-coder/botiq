@echo off
echo Criando estrutura V140 PRO...

mkdir logs

echo Criando arquivos...

echo fila = [] > signals.py
echo def get_sinais(): return fila >> signals.py
echo def adicionar_sinal(s): >> signals.py
echo.    if s not in fila: fila.append(s) >> signals.py
echo def remover_sinal(s): >> signals.py
echo.    if s in fila: fila.remove(s) >> signals.py

echo import requests, config > telegram_api.py
echo def enviar(msg): >> telegram_api.py
echo.    try: >> telegram_api.py
echo.        requests.post(f"https://api.telegram.org/bot{config.TOKEN}/sendMessage", data={"chat_id": config.CHAT_ID, "text": msg}) >> telegram_api.py
echo.    except: print("Erro Telegram") >> telegram_api.py

echo TOKEN="SEU_TOKEN" > config.py
echo CHAT_ID="SEU_CHAT_ID" >> config.py
echo EMAIL="SEU_EMAIL" >> config.py
echo SENHA="SUA_SENHA" >> config.py
echo VALOR=2 >> config.py
echo STOP_GAIN=20 >> config.py
echo STOP_LOSS=-20 >> config.py

echo from iqoptionapi.stable_api import IQ_Option > connection.py
echo import config >> connection.py
echo Iq=None >> connection.py
echo def conectar(): >> connection.py
echo.    global Iq >> connection.py
echo.    Iq=IQ_Option(config.EMAIL,config.SENHA) >> connection.py
echo.    Iq.connect() >> connection.py
echo.    return Iq >> connection.py

echo import time >> scheduler.py
echo from datetime import datetime >> scheduler.py
echo from signals import get_sinais, remover_sinal >> scheduler.py
echo from trader import executar >> scheduler.py
echo from telegram_api import enviar >> scheduler.py
echo def rodar(): >> scheduler.py
echo.    while True: >> scheduler.py
echo.        now=datetime.now().strftime("%%H:%%M") >> scheduler.py
echo.        for s in get_sinais()[:]: >> scheduler.py
echo.            if s["hora"]==now: >> scheduler.py
echo.                enviar(f"Executando {s['par']}") >> scheduler.py
echo.                res,l=executar(s["par"],s["dir"],s["tf"]) >> scheduler.py
echo.                enviar(f"Resultado {res} {l}") >> scheduler.py
echo.                remover_sinal(s) >> scheduler.py
echo.        time.sleep(1) >> scheduler.py

echo from connection import Iq >> trader.py
echo import config,time >> trader.py
echo def executar(par,dir,tf): >> trader.py
echo.    v=config.VALOR >> trader.py
echo.    status,id=Iq.buy(v,par,dir,tf) >> trader.py
echo.    if status: >> trader.py
echo.        while True: >> trader.py
echo.            r=Iq.check_win_v4(id) >> trader.py
echo.            if r!=None: return ("win" if r>0 else "loss"),r >> trader.py
echo.            time.sleep(1) >> trader.py
echo.    return "erro",0 >> trader.py

echo import threading,time >> main.py
echo from connection import conectar >> main.py
echo from scheduler import rodar >> main.py
echo print("BOT V140 PRO") >> main.py
echo conectar() >> main.py
echo threading.Thread(target=rodar).start() >> main.py
echo while True: time.sleep(1) >> main.py

echo Instalando dependencias...
pip install iqoptionapi requests

echo FINALIZADO!
pause