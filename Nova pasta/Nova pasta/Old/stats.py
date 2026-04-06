wins = 0
loss = 0
lucro = 0

def add_result(valor):
    global wins, loss, lucro

    lucro += valor

    if valor > 0:
        wins += 1
    else:
        loss += 1

def get_status(fila):
    total = wins + loss
    assertividade = (wins / total * 100) if total > 0 else 0

    return f"""📊 STATUS BOT

💰 Lucro: {round(lucro,2)}
🏆 Wins: {wins}
💀 Loss: {loss}
📈 Assertividade: {round(assertividade,1)}%
📌 Sinais na fila: {len(fila)}
"""