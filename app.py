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

'''------------------------------------------------------------'''
class log:  # Clase para almacenar valores de las dof. opciones
    login = int(0) # Si vale 1 = logueado, si vale 0 = no logueado
    user  = int(0)  # Id Usuario en numero
    nombre = str(0) # nombre Usuario para ver el perfil
    numHab = int(0) # Almacena el numero de la habitación
    rol = str(0) # None para usuario final, 1 para admin
'''------------------------------------------------------------'''

# Inicio de todo....
@app.route("/", methods=["GET"])
def index():
    return render_template ("index.html")

# Diana --> Login de Usuario
@app.route("/login", methods=['GET','POST'])
def login():
    print ("Funcion Login L.32")
    if request.method == 'POST':
        print ("Entramos al metodo L.34")
        user     = escape(request.form['user'])
        password = escape(request.form['psw'])
        try:
            with sqlite3.connect("dbh.db") as con:
                print ("Entramos a la base de datos L.39")
                cur   = con.cursor()
                query = cur.execute("SELECT password FROM usuario WHERE user=?",[user]).fetchone()
                idu = cur.execute("SELECT idusuario FROM usuario WHERE user=?",[user]).fetchone()
                rol = cur.execute("SELECT rol FROM usuario WHERE user=?",[user]).fetchone()
                if query!=None:
                    print ("Entramos al query vacío L.44")
                    if (query[0]==password):
                        print ("Pedimos usuario y contraseña L.46")
                        session['user']=user # Nombre de usuario
                        log.login=1 # Prueba con DIANA / YESSID #Sesion Iniciada
                        log.user = idu[0] # Id usuario
                        log.nombre = user
                        log.rol = rol[0] # None para usuario final, 1 para admin
                        print("el usuario es: ",log.user)
                        print("El nombre de usuario es: ",log.nombre)
                        print ("El rol del usuario es: ", log.rol)

                        #return redirect("/index") # Si hay error, borrar lo de abajo...
                        ''' Antes de inventar con el rol....
                        if int(log.numHab) > 0: # Yessid: Redirecciona a la página de la habitación vista...
                            numHab = str(log.numHab)
                            return redirect ("/ver/"+numHab)
                        else: # Yessid: Redirecciona al login si no hay habitación vista
                            return redirect("/index")
                    else:
                        print ("Clave incorrecta L.56")
                        return "Credenciales incorrectas"
                else:
                    print ("Usuario no existe L.59")
                    return "El usuario NO existe"
        except Error:
            print(Error) '''
                        #Aquí inicia la validación de usuario
                        if rol[0] == "admin":
                            return redirect ("/admin/dashboard")
                        else: 
                            if int(log.numHab) > 0: # Yessid: Redirecciona a la página de la habitación vista...
                                numHab = str(log.numHab)
                                return redirect ("/ver/"+numHab)
                            else: # Yessid: Redirecciona al login si no hay habitación vista
                                return redirect("/index")
                    else:
                        print ("Clave incorrecta L.56")
                        return "Credenciales incorrectas"
                else:
                    print ("Usuario no existe L.59")
                    return "El usuario NO existe"
        except Error:
            print(Error)

    #Hasta acá borrar si existe error
    if 'user' in session:
        print ("usuario en sesion??? L.65")
        if int(log.numHab)>0: # --> Vio hab (103)
            return redirect("/reservar/crear")
        else:
            return redirect('/index')
    else: #NO CAMBIAR...
        print ("Si no hay sesion de usuario L.71")
        return render_template ("login.html")

# Yessid --> Funcion de log out
@app.route('/logout',methods=['GET'])
def logout():
    if 'user' in session:
        log.login = 0
        log.nombre = 0
        log.user = 0
        log.numHab = 0
        log.rol = "0"
        session.clear()
        print ("log.login es: ",log.login)
        print ("log.nombre es: ", log.nombre)
        print ("log.user es: ", log.user)
        print ("log.numHab es: ", log.numHab)
        return redirect('/')
    else:
        return redirect("/login")

# Yessid --> Pagina de index con usuario logueado
@app.route("/index", methods=['GET'])
def logged():
    user=log.nombre
    print ("el usuario es: ", user )
    return render_template ("index_usuario.html", user=user) #, user=user)

# Diana --> registro nuevo usuario
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

#Yessid --> busqueda de habitaciones
@app.route("/buscar", methods=["GET","POST"])
def buscar():
    if request.method == 'POST':
        options = request.form['tipo']
        if options == "Buscar":
            flash('Debe seleccionar alguna opción')
            # Reemplazar con caja con alerta
            # return flash('Debe seleccionar alguna opción')
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

# Diana/Yessid --> Ver habitacion
@app.route("/ver/<numHab>")
def busqueda(numHab):
    log.numHab = str(numHab)
    print ("La habitacion es: ", log.numHab)
    return render_template (str(numHab)+".html")

#Yessid --> Comentarios habitacion
@app.route("/reservar/comentarios/listar/", methods=["GET", "POST"])
def comentarios_listar():
    print (log.numHab)
    print ("Entramos a la func coment_list")
    if request.method == 'GET':
        print("Metodo Get")
        # log.hab = str(request.form['hab'])
        # X =int (hab)
        print ("El numero de la habitación es: ", log.numHab)
        # hab = escape (request.form['hab']) #Buscamos los comentarios de la HAB
        try:
            with sqlite3.connect("dbh.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                #cur.execute("SELECT * FROM comentario WHERE idhabitacion = ?", [log.numHab])
                cur.execute("SELECT * FROM comentario INNER JOIN usuario ON usuario.idusuario=comentario.idusuario WHERE idhabitacion = ?", [log.numHab])
                row = cur.fetchall()
                x = log.numHab
                
                #Busqueda de usuario

            if row is None:
                flash('No hay comentarios de esta habitación')
            return render_template("comentarios.html", row=row,x=x)
            # return tipo
        except Error:
            return "Fallo en conexion"

#--------------------------------------------reservar:usuario final---------------------

# Diana --> Nueva reserva
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
                # sql    = "SELECT * FROM usuario WHERE user='{}'".format(log.login)

                cur.execute("INSERT INTO reserva(idusuario, fechaingreso, fechasalida, idhabitacion) VALUES (?,?,?,?)",(log.user,fechaingreso,fechasalida, log.numHab))
                con.commit()
                print ("Guardado con éxito")
        except Error:
            return (Error)
    return render_template("reservar.html")

# Yessid --> Historial de reservas
@app.route("/reservar/listar", methods=["GET", "POST"])
def listar():
    if request.method == 'GET':
        id = log.user
        print ("el usuario es: ", id)
        try:
            with sqlite3.connect("dbh.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM reserva WHERE idusuario = ?", [id])
                row = cur.fetchall()
            if row is None:
                flash('No hay habitaciones disponibles, de acuerdo a tu búsqueda')
        except Error:
            return "fallamos, donde???"
    else:
        print("error en el metodo")
    return render_template ("listaReserva.html", row=row, nombre=log.nombre)

# ---------------------------------------------------------- #
@app.route("/reservar/comentar", methods=["GET", "POST"])
def res_vercom():
    return render_template ("res_vercom.html")


@app.route("/reservar/crear/comentarios", methods=["GET", "POST"])
def comentarios():
    return render_template ("calificar.html")

#----------------------------------------admin/index------------------------------------
# Yessid --> Validacion admin/user
@app.route("/admin/dashboard", methods=["GET", "POST"])
def dashboard():
    print ('el rol del usuario es: ', log.rol)
    if log.rol == "0":
        return redirect("/")
    elif log.rol == None:
        return redirect("/index")
    else:
        return render_template("dashboard_index.html", nombre=log.nombre)

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
# Camilo --> (En proceso) Lista usuarios registrados en la vista admin
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



if __name__ == "__main__":
    app.run(debug=True)
