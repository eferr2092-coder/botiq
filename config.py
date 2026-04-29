import os

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

VALOR_ENTRADA = float(os.getenv("VALOR_ENTRADA", 10))
STOP_WIN = float(os.getenv("STOP_WIN", 50))
STOP_LOSS = float(os.getenv("STOP_LOSS", -30))
