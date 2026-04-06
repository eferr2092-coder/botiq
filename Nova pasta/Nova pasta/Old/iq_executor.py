from iqoptionapi.stable_api import IQ_Option
import config
from risk_manager import atualizar_lucro

iq = None


def conectar_iq():

    global iq

    print("Conectando na IQ Option...")

    iq = IQ_Option(config.IQ_EMAIL, config.IQ_SENHA)

    iq.connect()

    if config.CONTA == "PRACTICE":
        iq.change_balance("PRACTICE")

    else:
        iq.change_balance("REAL")

    print("Conectado na IQ Option")


def executar_ordem(par, direcao):

    valor = config.VALOR_ENTRADA

    for gale in range(config.GALE + 1):

        status, order_id = iq.buy(valor, par, direcao, 1)

        if not status:
            return "Erro ao enviar ordem"

        while True:

            check, lucro = iq.check_win_v4(order_id)

            if check:

                atualizar_lucro(lucro)

                if lucro > 0:
                    return f"WIN +{lucro}"

                else:

                    if gale < config.GALE:

                        valor *= config.MULTIPLICADOR_GALE

                        print("Executando Gale", gale + 1)

                        break

                    return f"LOSS {lucro}"