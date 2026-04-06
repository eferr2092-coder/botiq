from iq_connection import get_iq
from parser import parse_sinal
from executor import executar
from config import VALOR_ENTRADA
from risk_manager import check_stop
from logger import log


def processar(msg):
    """
    Processa um sinal no formato:
    M1;EURUSD;12:30;CALL

    Retorna:
    (resultado, lucro, erro)
    """

    log(f"📩 Sinal recebido: {msg}")

    # 🧠 PARSER
    sinal = parse_sinal(msg)

    if not sinal:
        log("❌ Erro ao interpretar sinal")
        return None, 0, "❌ Sinal inválido"

    log(f"🧠 Sinal interpretado: {sinal}")

    # 🛑 CHECK STOP
    stop = check_stop()
    if stop:
        log(f"🛑 {stop} atingido")
        return None, 0, f"🛑 {stop}"

    # 🔌 CONEXÃO
    Iq = get_iq()

    if not Iq:
        log("❌ Falha ao conectar na IQ")
        return None, 0, "❌ Sem conexão com IQ Option"

    log("🔗 Conectado à IQ Option")

    # 🚀 EXECUÇÃO
    try:
        resultado, lucro, erro = executar(Iq, sinal, VALOR_ENTRADA)

        if erro:
            log(f"❌ Erro execução: {erro}")
            return None, 0, erro

        log(f"📊 Resultado: {resultado} | Lucro: {lucro}")

        return resultado, lucro, None

    except Exception as e:
        log(f"❌ Erro crítico: {e}")
        return None, 0, f"❌ Erro crítico: {e}"


# 🧪 MODO TESTE (opcional)
if __name__ == "__main__":
    print("🤖 Modo teste iniciado")

    while True:
        try:
            msg = input("\nDigite um sinal (ou 'sair'): ")

            if msg.lower() == "sair":
                break

            resultado, lucro, erro = processar(msg)

            if erro:
                print(f"❌ {erro}")
            else:
                print(f"✅ {resultado} | 💰 {lucro}")

        except KeyboardInterrupt:
            print("\n⛔ Encerrado pelo usuário")
            break