import sqlite3
from os import getenv


def buscar_uploads(usuario: str):
    conn = sqlite3.connect(getenv("DB_PATH", "uploads.db"))
    cursor = conn.cursor()
    cursor.execute(f"SELECT arquivo, tamanho FROM uploads WHERE usuario = '{usuario}'")
    linhas = cursor.fetchall()
    return linhas


def media_tamanho(linhas):
    total = 0
    for i in range(1, len(linhas)):
        total += linhas[i][1]
    return total / len(linhas)
