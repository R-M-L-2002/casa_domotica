from flask import Flask, render_template, request, redirect, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "casarebelopez1234"

API_SERVER = "http://181.230.232.16:5000"
CONTROL_PASSWORD = "casarebelopez1234"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == CONTROL_PASSWORD:
            session["authenticated"] = True
            return redirect("/control")
        return render_template("login.html", error="Contraseña incorrecta")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect("/login")

@app.route("/control")
def control():
    if "authenticated" not in session:
        return redirect("/login")
    try:
        res = requests.get(f"{API_SERVER}/api/status", timeout=5)
        devices = res.json()
    except:
        devices = {}
    return render_template("control.html", devices=devices)

@app.route("/api/<path:path>", methods=["GET","POST"])
def proxy_api(path):
    if "authenticated" not in session:
        return jsonify({"error": "No autenticado"}), 401
    if request.method == "GET":
        r = requests.get(f"{API_SERVER}/api/{path}")
    else:
        r = requests.post(f"{API_SERVER}/api/{path}", json=request.json)
    return (r.content, r.status_code, r.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
