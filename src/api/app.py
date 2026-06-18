# Lab 2 buổi chiều: Flask app với /metrics
import hashlib
import os
import random
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
PrometheusMetrics(app)  # Tự thêm /metrics

ERROR_RATE = float(os.getenv("ERROR_RATE", "0"))
VERSION = os.getenv("VERSION", "v1")
DB_PASSWORD_FILE = os.getenv("DB_PASSWORD_FILE", "")


def read_db_password():
    if not DB_PASSWORD_FILE:
        return ""
    try:
        with open(DB_PASSWORD_FILE, "r", encoding="utf-8") as secret_file:
            return secret_file.read().strip()
    except OSError:
        return ""


def password_fingerprint(secret_value):
    if not secret_value:
        return ""
    return hashlib.sha256(secret_value.encode("utf-8")).hexdigest()[:12]

@app.get("/")
def index():
    db_password = read_db_password()
    if random.random() < ERROR_RATE:
        return jsonify(
            error="injected",
            version=VERSION,
            db_password_loaded=bool(db_password),
            db_password_fingerprint=password_fingerprint(db_password),
        ), 500
    return jsonify(
        ok=True,
        version=VERSION,
        db_password_loaded=bool(db_password),
        db_password_fingerprint=password_fingerprint(db_password),
    )

@app.get("/healthz")
def healthz():
    return "ok", 200


@app.get("/configz")
def configz():
    db_password = read_db_password()
    return jsonify(
        version=VERSION,
        db_password_loaded=bool(db_password),
        db_password_fingerprint=password_fingerprint(db_password),
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
