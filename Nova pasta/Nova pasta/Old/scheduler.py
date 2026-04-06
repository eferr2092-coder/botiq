from datetime import datetime
from signals import fila, remover
from trader import executar
from telegram_api import enviar
from risk import atualizar, verificar
from logger import log
import time
import config

def iniciar():

    log("Scheduler iniciado")

    while True:

        agora = datetime.now()

        hora = agora.strftime("%H:%M")

        segundo = agora.second

        for sinal in fila[:]:

            if sinal["hora"] == hora and segundo >= 58:

                par = sinal["par"]
                direcao = sinal["dir"]
                tf = sinal["tf"]

                enviar(f"Executando {par}")

                log(f"EXECUTANDO -> {par}")

                res, lucro = executar(par, direcao, tf)

                atualizar(lucro)

                enviar(f"Resultado\n{res}\nLucro {lucro}")

                log(f"RESULTADO -> {res} {lucro}")

                remover(sinal)

                stop = verificar()

                if stop:

                    enviar(stop)

                    log(stop)

                    exit()

        time.sleep(config.CHECK_DELAY)