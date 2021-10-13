from flask import Flask

app = Flask(__name__)

lista_usuarios = ["Yessid", "Diana", "Carlos", "Laura", "camilo"]

#Si se desea mostrar (consultar) info usamos 'GET'
#Si se requiere enviar info de regreso (consulta) usamos 'POST'
@app.route("/", methods=["GET"])
def inicio():
    #Si ya inicio sesion --> Lista de noticias
    #Si no pagina de bienvenida
    return "Pagina principal"

@app.route("/registro", methods=["GET", "POST"])
def registrarse():
    return "Pagina de registro"

@app.route("/ingreso", methods=["GET", "POST"])
def ingreso():
    return "Pagina de ingreso"

#Si los datos se pueden actualizar, usamos ambos métodos,
#de lo contrario usamos solo "GET"
@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    return "Pagina de perfil del usuario"

#La idea es que <variable> haga el match con la funcion en nommbre y posicion
@app.route("/usuario/<id_usuario>", methods=["GET"])
def usuario_info(id_usuario):
    if id_usuario in lista_usuarios:
        return f"Estas viendo el perfil del usuario: {id_usuario}"
    else:
        return f"El usuario {id_usuario}, no existe"

@app.route("/noticia/<id_noticia>", methods=["GET"])
def noticia_detalle(id_noticia):
    return f"Estas viendo el detalle de la noticia: {id_noticia}"

#Si se desea mostrar (consultar) info usamos 'GET'




if __name__ == "__main__":
    app.run(debug=True)