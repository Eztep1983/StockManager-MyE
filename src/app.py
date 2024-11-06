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
from models.ventas import *

#Ejecutar la API
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
    try: 
        if request.method == 'POST':
            nombre_empresa = request.form.get("NameProvider")
            direccion = request.form.get("addressProvider")
            telefono = request.form.get("phoneProvider")
            correo_electronico = request.form.get("emailProvider")
            
            añadir_proveedor(nombre_empresa=nombre_empresa, direccion=direccion, telefono=telefono, correo_electronico=correo_electronico)
        return render_template('proveedores.html')
    except Exception as e:
        print("Error al procesar la solicitud",e)
        return jsonify({'message': 'Error al procesar la solicitud'})

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
    try:
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
    except Exception as e:
        print("Error al procesar la solicitud DELETE:", e)
        return jsonify({'message': 'Error al procesar la solicitud'}), 500

    # Obtener las listas de proveedores y categorías
    lista_proveedores = obtener_proveedores()
    lista_categorias = obtener_categorias()
    lista_productos = obtener_lista_productos() 

    return render_template('productos.html', proveedores=lista_proveedores, categorias=lista_categorias, productos=lista_productos)

#PARA ELIMINAR PRODUCTOS
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
#RUTA PARA VENTAS
@app.route('/ventas')
@login_required
def ventas():
    lista_ventas = obtener_ventas()
    return render_template('ventas.html', ventas=lista_ventas)


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
    try: 
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
    except Exception as e:
        return jsonify({'message': 'Error al procesar la solicitud'}),500
    return render_template('clientes.html')

# RUTA PARA EDITAR CLIENTES
@app.route('/editar_cliente', methods=['PUT'])
@login_required
def editar_cliente():
    try:
        # Obtener los datos del formulario de edicion (esta en un swal alert de js "EditClientModal")
        identificador_c = request.form.get('cliente_id')
        nombre = request.form.get('edit_NameClient')
        apellido = request.form.get('edit_LastNameClient')
        direccion = request.form.get('edit_addressClient')
        telefono = request.form.get('edit_phoneClient')
        email = request.form.get('edit_emailClient')
        cedul = request.form.get('edit_cedulaClient')

        # Verificar que todos los campos necesarios estén presentes
        if not all([identificador_c, nombre, apellido, direccion, telefono, email, cedul]):
            return jsonify(success=False, message="Faltan datos"), 400

        # Actualizar cliente
        if actualizar_cliente(identificador_c, nombre, apellido, direccion, telefono, email, cedul):
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Error al actualizar el cliente"), 400
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

#EN CASO DE METODO INCORRECTO
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(success=False, message="Método no permitido"), 405


#RUTA PARA ELIMINAR CLIENTES
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

#RUTA PARA EDITAR PRODUCTOS
@app.route('/editar_producto', methods=['PUT'])
@login_required
def editar_producto():
    if request.method == 'PUT':
        try:
            # Obtener los datos desde el formulario HTML
            data = request.form
            identificador_p = data.get('producto_id')
            nombre = data.get('edit_NameProduct')
            descripcion = data.get('edit_Description')
            precio = data.get('edit_Price')
            stock = data.get('edit_Stock')

            # Verificación de que los datos no estén vacíos
            if not all([nombre, descripcion, precio, stock, identificador_p]):
                return jsonify(success=False, message="Datos incompletos o inválidos"), 400

            # Validar que el precio y el stock sean números válidos
            try:
                precio = float(precio)
                stock = int(stock)
                if precio < 0 or stock < 0:
                    return jsonify(success=False, message="Precio y stock deben ser numeros positivos"), 400
            except ValueError:
                return jsonify(success=False, message="Precio o stock inválido"), 400

            # Intentar actualizar el producto
            if actualizar_producto(identificador_p, nombre, descripcion, precio, stock):
                return jsonify(success=True)
            else:
                return jsonify(success=False, message="Error en la actualización del producto"), 400

        except Exception as e:
            return jsonify(success=False, message=f"Ocurrió un error en el servidor: {str(e)}"), 500

    return jsonify(success=False, message="Solo se permite el método PUT"), 405


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

# MANEJO PARA EL 404 ERROR
def status404(error):
    return render_template('404handler.html'), 404
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
