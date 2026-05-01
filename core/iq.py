from iqoptionapi.stable_api import IQ_Option
import os

def get_iq():
    email = os.getenv("IQ_EMAIL")
    senha = os.getenv("IQ_PASSWORD")

    iq = IQ_Option(email, senha)
    status, _ = iq.connect()

    if status:
        iq.change_balance("PRACTICE")
        return iq
    return None
