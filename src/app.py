import os
import time
from flask import Flask
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpass")
DB_NAME = os.getenv("DB_NAME", "appdb")

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )

@app.route("/")
def home():
    for _ in range(30):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT 'Hola Mundo desde MySQL 🚀' as msg;")
            msg = cur.fetchone()[0]
            cur.close()
            conn.close()
            return f"<h1>Hola Mundo</h1><p>Conexión OK ✅</p><p>Mensaje BD: {msg}</p>"
        except Exception:
            time.sleep(1)

    return "<h1>Hola Mundo</h1><p>No pude conectar a MySQL ❌</p>", 500

@app.route("/health")
def health():
    try:
        conn = get_conn()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "fail", "error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)