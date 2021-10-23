from flask import Flask,render_template,request, session, redirect, flash
from markupsafe import escape
import os
import sqlite3
from sqlite3 import Error

#librerias hash
import hashlib
#from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template ("index.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template ("login.html")

@app.route("/register", methods=["GET"])
def registrarse():
    return render_template ("new_user.html")

#Yessid (Actualizacion de busqueda)
@app.route("/buscar", methods=["GET","POST"])
def buscar():
    
    if request.method == 'POST':   
        options = request.form['tipo']
        if options == "Buscar":
            #Reemplazar con caja con alerta
            return ('Debe seleccionar alguna opción')
            
        else:
            tipo = int(options)
            try:
                print("Entramos al try")
                with sqlite3.connect("dbh.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM habitacion WHERE tipohabitacion = ? AND ocupado = 0", [tipo])
                    row = cur.fetchall()
                if row is None: 
                    flash('No hay habitaciones disponibles, de acuerdo a tu búsqueda')
                return render_template("busquedaHab.html", row=row)
                # return tipo
            except Error:
                return "Fallo en conexion"
    return "LLego hasta el final"

#Diana (creado para hacer pruebas de habitación)
@app.route("/reservar/<numHab>")
def busqueda(numHab):
    return render_template (str(numHab)+".html")



#--------------------------------------------reservar:usuario final---------------------
@app.route("/reservar/comentar", methods=["GET", "POST"])
def res_vercom():
    return render_template ("res_vercom.html")

@app.route("/reservar/crear", methods=["GET", "POST"])
def crear():
    return render_template ("reservar.html")

@app.route("/reservar/listar", methods=["GET", "POST"])
def listar():
    return render_template ("listaReserva.html")

@app.route("/reservar/crear/comentarios", methods=["GET", "POST"])
def comentarios():
    return render_template ("calificar.html")

@app.route("/reservar/comentarios/listar", methods=["GET", "POST"])
def comentarios_listar():
    return render_template ("comentarios.html")

#----------------------------------------admin/index------------------------------------
@app.route("/admin/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard_index.html")

#---------------------------------------admin/habitaciones-------------------------------
@app.route("/admin/dashboard/habitaciones", methods=["GET", "POST"])
def gestionarH():
    return render_template ("gestionarhabitaciones.html")

@app.route("/admin/dashboard/habitaciones/agregar", methods=["GET", "POST"])
def agregar():
    return render_template ("agregar_hab.html")

@app.route("/admin/dashboard/habitaciones/editar", methods=["GET", "POST"])
def editar():
    return render_template ("editar_hab.html")

@app.route("/admin/dashboard/habitaciones/delete", methods=["GET", "POST"])
def delete():
    return render_template ("gestionarhabitaciones.html")

#-----------------------------------------admin/Reservas------------------------------

@app.route("/admin/dashboard/reservas/listar", methods=["GET", "POST"])
def reserva_listar():
    return render_template ("gestionarreserva.html")

@app.route("/admin/dashboard/reservas/editar", methods=["GET", "POST"])
def reserva_editar():
    return render_template ("reservar.html")

@app.route("/admin/dashboard/reservas/delete", methods=["GET", "POST"])
def reserva_delete():
    return render_template ("gestionarreserva.html")

#-----------------------------------------admin/Usuarios-------------------------------------------------
@app.route("/admin/dashboard/usuarios/listar", methods=["GET", "POST"])
def usuario_listar():
    if request.method == 'GET':
        try:
            with sqlite3.connect("dbh.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT nombre, idusuario FROM usuario WHERE rol IS NULL")
                row = cur.fetchall()
                if row is None:
                    print('No hay registros')
                return render_template ("gestionarusuario.html", row=row)
        except Error:
            print(Error)

@app.route("/admin/dashboard/usuarios/editar", methods=["GET", "POST"])
def usuario_editar():
    return render_template ("new_user.html")

@app.route("/admin/dashboard/usuarios/delete", methods=["GET", "POST"])
def usuario_delete():
    return render_template ("gestionarusuario.html")

#seccion o ruta nueva
@app.route("/index/logueado", methods=["GET","POST"])
def indexuser():
    return render_template ("index_usuario.html")

if __name__ == "__main__":
    app.run(debug=True)
