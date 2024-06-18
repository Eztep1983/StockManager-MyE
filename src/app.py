from flask import Flask, abort, render_template, jsonify, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import CSRFProtect
from config import config
from models.proveedor import *
from models.ModelUser import ModelUser 
from models.register import *
from models.entities.user import User
from models.cliente import *
from models.categorias import *
from models.producto import *

app = Flask(__name__)

# Configuración de la base de datos y del login manager
app.config.from_object(config['development'])
db = MySQL(app)
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'

# Inicialización de la protección CSRF
csrf.init_app(app)

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#RUTA LOGIN
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
@app.route('/')
def index():
    return redirect(url_for('login'))

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

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

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

#RUTA PARA EL REGISTRO DE USUARIOS
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        identification = request.form['identification']
        password = request.form['password']
        fullname = request.form['fullname']
        for i in identification, password, fullname:
            if i is not None:
                # Crear un objeto User con los datos del formulario
                user = User(None, identification, password, fullname)  # El ID se establecerá automáticamente al registrar el usuario
                
                # Llamar al método register de la clase Register para registrar al usuario
                registered_user = Register.register(db, user)
                if registered_user:
                    return redirect(url_for('login'))
                else:
                    flash("Error al registrar usuario")
            else:
                flash("Debes llenar los campos")
            
    else:
        # Si la solicitud no es POST, renderizar el formulario de registro
        return render_template('auth/register.html')

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

#RUTA PARA EL HOME
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

#RUTA PARA OBTENER LISTA DE PROVEEDORES
@app.route('/proveedores')
@login_required
def get_proveedores():
    lista_proveedores = obtener_proveedores()
    return render_template('proveedores.html', proveedores=lista_proveedores)

# RUTA PARA AÑADIR PROVEEDORES
@app.route('/proveedor', methods=['POST','DELETE'])
@login_required
def provedorees():
    if request.method == 'POST':
        nombre_empresa = request.form.get("NameProvider")
        direccion = request.form.get("addressProvider")
        telefono = request.form.get("phoneProvider")
        correo_electronico = request.form.get("emailProvider")
        
        añadir_proveedor(nombre_empresa=nombre_empresa, direccion=direccion, telefono=telefono, correo_electronico=correo_electronico)
    return render_template('proveedores.html')

#RUTA PARA ELIMINAR PROVEEDORES
@app.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
@login_required
def eliminar_proveedor(id_proveedor):
    if request.method == 'DELETE':
        eliminar_proveedor(id_proveedor)
        # Puedes redirigir a otra página o devolver algún mensaje JSON si es necesario
        return jsonify({'message': 'Proveedor eliminado correctamente'})
    else:
        return abort(405)  # Método no permitido

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
# RUTA PARA OBTENER LISTA DE PRODUCTOS

#RUTA PARA AÑADIR PRODUCTOS 
@app.route('/productos', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('NameProduct')
        descripcion = request.form.get('Description')
        precio = request.form.get('PriceProduct')
        stock = request.form.get('StockProduct')
        categoria = request.form.get('CategoryProduct')
        proveedor = request.form.get('ProviderProduct')
        fecha_ingreso = request.form.get('IngresoProduct')
        
        # Verificar si alguno de los campos requeridos está vacío
        if not nombre or not descripcion or not precio or not stock or not categoria or not proveedor or not fecha_ingreso:
            return "Por favor, complete todos los campos del formulario.", 400

        # Convertir el precio y el stock a los tipos de datos apropiados
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            return "Datos inválidos en precio o stock.", 400

        if crear_producto(nombre, descripcion, precio, stock, fecha_ingreso, proveedor, categoria):
            return redirect('/productos')

    # Obtener las listas de proveedores y categorías
    lista_proveedores = obtener_proveedores()
    lista_categorias = obtener_categorias()
    lista_productos = obtener_lista_productos() 

    return render_template('productos.html', proveedores=lista_proveedores, categorias=lista_categorias, productos=lista_productos)

@app.route('/eliminar_productos/<int:id>', methods=['DELETE'])
@login_required
def eliminar_producto(id):
    try:
        if eliminar_productos(id):
            return jsonify({'message': 'Producto eliminado exitosamente'}), 200
        else:
            return jsonify({'message': 'Error al eliminar el producto'}), 500
    except Exception as e:
        print("Error al procesar la solicitud DELETE:", e)
        return jsonify({'message': 'Error al procesar la solicitud'}), 500

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

#RUTA PARA OBTENER LISTA DE CATEGORIAS
@app.route('/categorias')
@login_required
def get_categorias():
    lista_categorias = obtener_categorias()
    return render_template('productos.html', lista_categorias=lista_categorias)


#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

@app.route('/ventas')
@login_required
def ventas():
    return render_template('ventas.html')

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

# RUTA PARA OBTENER LISTA DE CLIENTES
@app.route('/clientes')
@login_required
def clientes():
    lista_clientes = obtener_lista_clientes()  
    return render_template('clientes.html', clientes=lista_clientes)

#RUTA PARA AÑADIR CLIENTES 
@app.route('/cliente', methods=['POST'])
@login_required
def nuevo_cliente():
    if request.method == 'POST':
        cedula = request.form.get('DNIClient')
        nombres = request.form.get('NameClient')
        apellidos = request.form.get('LastNameClient')
        direccion = request.form.get('addressClient1')
        telefono = request.form.get('phoneClient')
        email = request.form.get('emailClient')
        
        # Verificar si alguno de los campos requeridos está vacío
        if not cedula or not nombres or not apellidos or not direccion or not telefono or not email:
            return "Por favor, complete todos los campos del formulario."

        # Llamado a la función con los datos del nuevo cliente
        if añadir_cliente(cedula, nombres, apellidos, direccion, telefono, email):
            
            return redirect('/clientes')
        else:
            return "Error al añadir cliente"

    return render_template('clientes.html')

#RUTA PARA EDITAR CLIENTES
@app.route('/editar_cliente', methods=['POST'])
@login_required
def editar_cliente():
    if request.method == 'POST':
        # Obtener los datos del formulario
        cedula = request.form.get('cliente_id')
        nombre = request.form.get('edit_NameClient')
        apellido = request.form.get('edit_LastNameClient')
        direccion = request.form.get('edit_addressClient')
        telefono = request.form.get('edit_phoneClient')
        email = request.form.get('edit_emailClient')
        
        if actualizr_cliente(cedula, nombre, apellido, direccion, telefono, email):
            flash('Cliente actualizado con éxito!', 'success')
        else:
            flash('Error al actualizar el cliente.', 'error')
    return render_template('clientes.html')

# RUTA PARA ELIMINAR CLIENTES
@app.route('/eliminar_cliente/<int:cliente_id>', methods=['DELETE'])
@login_required
def eliminar_cliente(cliente_id):
    try:
        if request.method=='DELETE':
            eliminarr_client(cliente_id)
            return jsonify({'message': 'Cliente eliminado exitosamente'}),200
        else:
            return jsonify({'message': '>Error al elimina al cliente'}),500

    except Exception as e:
        print("Error al procesar la solicitud DELETE:", e)
        return jsonify({'message': 'Error al procesar la solicitud'}),500

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

#RUTA PARA LA CONFIGURACION
@app.route('/configuracion')
@login_required
def configuracion():
    return render_template('configuracion.html')

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

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
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

#RUTA PARA CERRAR SESION
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout'))
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
@app.route('/actualizar_cliente')
@login_required
def actualizar_cliente():
    return render_template('actualizar_cliente.html')
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________


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
 #_______________________________________________________________________________________________________

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

def status401(error):
    return redirect(url_for('login'))

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(404, status404)
    app.register_error_handler(401, status401)
    app.run(host="0.0.0.0", port=5000)
