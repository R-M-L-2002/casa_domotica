from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  

# Contraseña para acceder al control 
CONTROL_PASSWORD = "casarebelopez1234"  

devices = {
    #luces
    "luz_dormitorio1": {"state": False, "type": "light", "room": "Dormitorio 1"},
    "luz_dormitorio2": {"state": False, "type": "light", "room": "Dormitorio 2"},
    "luz_living": {"state": False, "type": "light", "room": "Living"},
    "luz_cocina": {"state": False, "type": "light", "room": "Cocina"},
    "luz_bano": {"state": False, "type": "light", "room": "Baño"},
    "luz_garaje": {"state": False, "type": "light", "room": "Garaje"},
    #aires
    "aire_dormitorio1": {"state": False, "type": "ac", "room": "Dormitorio 1", "temp": 24},
    "aire_dormitorio2": {"state": False, "type": "ac", "room": "Dormitorio 2", "temp": 24},
    "aire_living": {"state": False, "type": "ac", "room": "Living", "temp": 24},
    #otros
    "tv_living": {"state": False, "type": "tv", "room": "Living"},
    "ventilador_cocina": {"state": False, "type": "fan", "room": "Cocina"},
    #puertas
    "puerta_principal": {"state": False, "type": "door", "room": "Entrada"},
    "porton_garaje": {"state": False, "type": "garage", "room": "Garaje"},
    #camaras
    "camara_exterior": {"state": True, "type": "camera", "room": "Exterior"},
    "camara_living": {"state": True, "type": "camera", "room": "Living"}
}

# ===============================
# DECORADOR PARA PROTEGER RUTAS
# ===============================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===============================
# RUTAS DE AUTENTICACIÓN
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == CONTROL_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('control'))
        else:
            return render_template("login.html", error="Contraseña incorrecta")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

# Devuelve el estado de la APi
@app.route("/api/status")
def status():
    return jsonify(devices)

# Cambia el estado del dispositivo (on/off)
@app.route("/api/toggle/<device>")
def toggle(device):
    if device in devices:
        devices[device]["state"] = not devices[device]["state"]
        return jsonify({"success": True, "device": device, "state": devices[device]["state"]})

# temperatura del aire
@app.route("/api/temp/<device>/<int:temp>")
def set_temp(device, temp):
    if device in devices and devices[device]["type"] == "ac":
        devices[device]["temp"] = temp
        return jsonify({"success": True, "device": device, "temp": temp})

# visualizacion de la casa
@app.route("/")
@app.route("/display")
def display():
    return render_template("display.html")

# vista de control
@app.route("/control")
@login_required
def control():
    return render_template("control.html")

# ejecucion del server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
