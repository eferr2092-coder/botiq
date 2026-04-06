from flask import Flask
import sqlite3

app = Flask(__name__)


@app.route("/")

def dashboard():

    conn = sqlite3.connect("trades.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM trades")

    total = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(lucro) FROM trades")

    lucro = cursor.fetchone()[0]

    return f"""
    <h1>BOT V14 PRO</h1>
    <h2>Total operações: {total}</h2>
    <h2>Lucro acumulado: {lucro}</h2>
    """


def iniciar_web():

    app.run(port=5000)