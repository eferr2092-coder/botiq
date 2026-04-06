
import time
from datetime import datetime

def esperar_inicio_vela():

    while True:

        segundos = datetime.now().second

        if segundos == 0:
            break

        time.sleep(0.5)
