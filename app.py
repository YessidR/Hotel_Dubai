from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template ("index.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template ("login.html")

@app.route("/new_user", methods=["GET", "POST"])
def registrarse():
    return render_template ("new_user.html")

@app.route("/buscar", methods=["GET"])
def buscar():
    return render_template ("busquedaHab.html")

@app.route("/res_vercom", methods=["GET", "POST"])
def res_vercom():
    return render_template ("res_vercom.html")

@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    return render_template ("reservar.html")

@app.route("/comentarios", methods=["GET", "POST"])
def comentarios():
    return render_template ("comentarios.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template ("dashboard_index.html")

@app.route("/agregar_hab", methods=["GET", "POST"])
def agregar():
    return render_template ("agregar_hab.html")

@app.route("/calificar", methods=["GET", "POST"])
def calificar():
    return render_template ("calificar.html")

@app.route("/editar_hab", methods=["GET", "POST"])
def editar():
    return render_template ("editar_hab.html")

@app.route("/gestionarhabitaciones", methods=["GET", "POST"])
def gestionarH():
    return render_template ("gestionarhabitaciones.html")

@app.route("/gestionarreserva", methods=["GET", "POST"])
def gestionarR():
    return render_template ("gestionarreserva.html")

@app.route("/gestionarusuario", methods=["GET", "POST"])
def gestionarU():
    return render_template ("gestionarusuario.html")

@app.route("/li_reserva", methods=["GET", "POST"])
def lista():
    return render_template ("listaReserva.html")


if __name__ == "__main__":
    app.run(debug=True)
