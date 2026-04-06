from datetime import datetime

def log(msg):
    hora = datetime.now().strftime("%H:%M:%S")

    linha = f"[{hora}] {msg}"

    print(linha)

    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(linha + "\n")