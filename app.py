from flask import Flask,render_template,request, session, redirect, flash
from markupsafe import escape
import os
import sqlite3
from sqlite3 import Error

#librerias hash
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key=os.urandom(24)

@app.route("/", methods=["GET"])
def index():
    return render_template ("index.html")

class login:  # Prueba con DIANA / YESSID
    login = int(0)
    user  = int(0)  # Prueba con DIANA / YESSID

# Diana (OK)
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user     = escape(request.form['user'])
        password = escape(request.form['psw'])
        
        try:
            with sqlite3.connect("dbh.db") as con:
                cur   = con.cursor()
                query = cur.execute("SELECT password FROM usuario WHERE user=?",[user]).fetchone()
                idu = cur.execute("SELECT idusuario FROM usuario WHERE user=?",[user]).fetchone() 
                if query!=None:
                    if (query[0]==password):
                    # if check_password_hash(query[0],password):
                        login.login=1 # Prueba con DIANA / YESSID
                        login.user = idu[0]
                        session['user']=user
                        # print ("El valor de login es: ",login.login)
                        # print ("El codigo de usuario es: ",idu)
                        # print ("login.user es: ",login.user)
                        return render_template("index_usuario.html") 
                    else:
                        return "Credenciales incorrectas"
                else:
                    return "El usuario NO existe"
        except Error:
            print(Error)

    if 'user' in session:
        if int(static.numHab)>0: # --> Vio hab (103)
            return redirect("/reservar/crear")
        else:
            return redirect('/')
    else:
        return render_template ("login.html")

# Diana O.K.
@app.route("/register", methods=['GET','POST'])
def registrarse():
    if request.method == 'POST':
        email  = escape(request.form['email'])
        nombre = escape(request.form['nombre'])
        user1  = escape(request.form['user'])
        pass_1 = escape(request.form['pass1'])
        pass_2 = escape(request.form['pass2'])
        
        if pass_1 != pass_2:
            return "Las contraseñas no coinciden"
        else:
            hash_clave=generate_password_hash(pass_1)
            try:
                with sqlite3.connect("dbh.db") as con:
                    cur    = con.cursor()
                    sql    = "SELECT * FROM usuario WHERE user='{}'".format(user1)  #,[user1]  
                    existe = cur.execute(sql).fetchall()

                    if existe:
                        return "El Usuario ya existe, por favor intente de nuevo"
                    else:
                        cur.execute("INSERT INTO usuario(user,password,nombre,email) VALUES (?,?,?,?)",(user1,hash_clave,nombre,email))
                        con.commit()
                        return "Guardado con exito"               
            except Error:
                print(Error)
                return "Registro no completado"
    return render_template ("new_user.html")

#Yessid (O.K.)
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
                # print("Entramos al try")
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

# Camilo/Yessid: Creado para estandarizar el id Hab
class static:
    numHab = 0 #idHabitacion

# Diana/Yessid (O.K.)
@app.route("/ver/<numHab>")
def busqueda(numHab):
    static.numHab = str(numHab)
    print ("La habitacion es: ", static.numHab)
    return render_template (str(numHab)+".html")


#Yessid
@app.route("/reservar/comentarios/listar/", methods=["GET", "POST"])
def comentarios_listar():
    print (static.numHab)
    print ("Entramos a la func coment_list")
    
    if request.method == 'GET':
        print("Metodo Get")
        # static.hab = str(request.form['hab'])
        # X =int (hab)
        print ("El valor de variable es: "+static.numHab)
        # hab = escape (request.form['hab']) #Buscamos los comentarios de la HAB
        try:
            with sqlite3.connect("dbh.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM comentario WHERE idhabitacion = ?", [static.numHab])
                row = cur.fetchall()
                x = static.numHab
            if row is None:
                flash('No hay comentarios de esta habitación')
            return render_template("comentarios.html", row=row,x=x)
            # return tipo
        except Error:
            return "Fallo en conexion"


''''''

#--------------------------------------------reservar:usuario final---------------------
@app.route("/reservar/comentar", methods=["GET", "POST"])
def res_vercom():
    return render_template ("res_vercom.html")

# ______________________________________________________________
# Diana
@app.route("/reservar/crear", methods=["GET", "POST"])
def crear():
    if request.method == 'POST':
        print ("Ingresamos al post...")
        fechaingreso = escape(request.form['fechaingreso'])
        fechasalida  = escape(request.form['fechasalida'])
        try:
            print("Base de datos. yuhuuuuu")
            with sqlite3.connect("dbh.db") as con:
                cur    = con.cursor()
                # sql    = "SELECT * FROM usuario WHERE user='{}'".format(login.login)
                cur.execute("INSERT INTO reserva(idusuario, fechaingreso, fechasalida, idhabitacion) VALUES (?,?,?,?)",(login.user,fechaingreso,fechasalida, static.numHab))
                con.commit()
                print ("Guardado con éxito")
        except Error:
            print(Error)
    return render_template("reservar.html")
            
 
# login.login # --> Estado (1=activo), (0=noactivo)
# login.user # --> nombre usuario
# static.numHab # --> numero habitacion consultada

# ____________________________________________________________

    return render_template ("reservar.html")

@app.route("/reservar/listar", methods=["GET", "POST"])
def listar():
    return render_template ("listaReserva.html")

@app.route("/reservar/crear/comentarios", methods=["GET", "POST"])
def comentarios():
    return render_template ("calificar.html")

#Yessid
# @app.route("/reservar/comentarios/listar", methods=["GET", "POST"])
# def comentarios_listar():
#     return render_template ("comentarios.html")

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
