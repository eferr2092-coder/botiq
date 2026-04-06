
from connection import iq
import config

def payout_ok(par):

    payout = iq.get_digital_payout(par)

    if payout >= config.PAYOUT_MIN:
        return True

    print("Payout baixo:", payout)

    return False
