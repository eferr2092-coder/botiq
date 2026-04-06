from iqoptionapi.stable_api import IQ_Option
from config import EMAIL, SENHA
import time

Iq = None
ULTIMA_CONEXAO = 0


def conectar():
    global Iq, ULTIMA_CONEXAO

    print("🔄 Conectando na IQ...")

    try:
        Iq = IQ_Option(EMAIL, SENHA)

        check, reason = Iq.connect()

        if check:
            print("✅ IQ CONECTADA")
            ULTIMA_CONEXAO = time.time()
            return Iq
        else:
            print(f"❌ Falha: {reason}")
            return None

    except Exception as e:
        print(f"❌ ERRO CONEXÃO IQ: {e}")
        return None


def get_iq():
    global Iq, ULTIMA_CONEXAO

    # 🔥 Se nunca conectou
    if Iq is None:
        return conectar()

    # 🔥 Verifica conexão
    try:
        if not Iq.check_connect():
            print("⚠ IQ desconectada, reconectando...")
            return reconectar()

    except:
        print("⚠ Falha check_connect, reconectando...")
        return reconectar()

    # 🔥 Reconexão preventiva a cada 5 minutos
    if time.time() - ULTIMA_CONEXAO > 300:
        print("🔄 Reconexão preventiva...")
        return reconectar()

    return Iq


def reconectar():
    global Iq, ULTIMA_CONEXAO

    tentativas = 0

    while tentativas < 5:
        try:
            Iq = IQ_Option(EMAIL, SENHA)
            check, reason = Iq.connect()

            if check:
                print("✅ IQ RECONECTADA")
                ULTIMA_CONEXAO = time.time()
                return Iq

            else:
                print(f"❌ Falha reconexão: {reason}")

        except Exception as e:
            print(f"❌ Erro reconectar: {e}")

        tentativas += 1
        print(f"🔄 Tentando novamente ({tentativas}/5)...")
        time.sleep(3)

    print("🚨 NÃO FOI POSSÍVEL RECONECTAR IQ")
    return None