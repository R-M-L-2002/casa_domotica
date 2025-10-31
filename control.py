from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)

HOME_SERVER = "http://181.230.232.16:5000" 

@app.route("/")
def index():
    try:
        res = requests.get(f"{HOME_SERVER}/api/status", timeout=5)
        devices = res.json()
        return render_template("control.html", devices=devices)
    except Exception as e:
        return f"No se pudo conectar con el servidor de la casa: {e}"

@app.route("/toggle/<device>")
def toggle(device):
    try:
        requests.get(f"{HOME_SERVER}/api/toggle/{device}", timeout=5)
        return redirect(url_for("index"))
    except Exception as e:
        return f"Error al enviar comando: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
