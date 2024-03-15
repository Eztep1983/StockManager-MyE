from flask import Flask, jsonify, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config
from models.ModelUser import ModelUser 
from models.entities.user import User
from models.cliente import *
from flask_wtf import CSRFProtect
from models.producto import *
app = Flask(__name__)

# Configuración de la base de datos y del login manager
db = MySQL(app)
csrf= CSRFProtect()
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = User(0, request.form['identification'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password: # Si la contraseña es correcta
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Usuario no encontrado")
        else:
            flash("Contraseña invalida")
    return render_template('auth/login.html')



@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/inventario')
@login_required
def inventario():
    return render_template('inventario.html')

@app.route('/productos')
@login_required
def productos():
    return render_template('productos.html')


@app.route('/ventas')
@login_required
def ventas():
    return render_template('ventas.html')

@app.route('/proveedores')
@login_required
def proveedores():
    return render_template('proveedores.html')

@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html')

@app.route('/configuracion')
@login_required
def configuracion():
    return render_template('configuracion.html')

#RUTA PARA LA FACTURACION

@app.route('/facturar', methods=['POST', 'GET'])
@login_required
def facturar():
    lista_clientes = obtener_lista_clientes()  # Obtener la lista de clientes
    lista_productos = obtener_lista_productos()  # Obtener la lista de productos
    if request.method =='POST':
        # PARA PROCESAR LA FACTURA
        pass
    return render_template('facturar.html', lista_clientes=lista_clientes, lista_productos=lista_productos)


#RUTA PARA CERRAR SESION
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

def status404(error):
    return """<html>
                <head>
                    <title>Página no encontrada</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                        }
                        .container {
                            margin-top: 50px;
                        }
                        .button {
                            background-color: #007bff; /* Azul */
                            border: none;
                            color: white;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin-top: 20px;
                            cursor: pointer;
                            border-radius: 5px;
                        }
                        .button:hover {
                            background-color: #0056b3; /* Azul oscuro al pasar el ratón */
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <center>
                            <h1>No se pudo encontrar la página</h1>
                            <button class="button" onclick="window.location.href='/login'">Ir a login</button>
                        </center>
                    </div>
                </body>
            </html>""", 404
 

def status401(error):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(404, status404)
    app.register_error_handler(401, status401)
    app.run(host="0.0.0.0", port=5000)
