from flask import Flask, abort, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import jsonify, render_template, request, flash, redirect, url_for
from flask_wtf import CSRFProtect
from functools import wraps
from config import config
from models.proveedor import *
from models.ModelUser import ModelUser 
from models.register import *
from models.entities.user import User
from models.cliente import *
from models.categorias import *
from models.producto import *
from models.ventas import *
from models.usuarios import *
from models.pagos import *
from models.ultimas_ventas import *
import re
import logging
import os
#Ejecutar la API
app = Flask(__name__)

# Cargar configuración según el entorno
env = os.getenv("FLASK_ENV", "development")
app.config.from_object(config[env])


# Inicializar extensiones
db = MySQL(app)
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'
csrf.init_app(app)

# Configuración de logs
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO if env == "development" else logging.ERROR)


#_______________________________________________________________________________________________________
#PARA ELIMINAR EL CACHE

@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


#_______________________________________________________________________________________________________
#RUTA LOGIN
@app.route('/')
def index():
    """
    Redirige automáticamente a la ruta de inicio de sesión por defecto.

    Flujo:
        1. Llama a la función `login` utilizando `url_for`.
        2. Redirige al usuario a la página de inicio de sesión.

    Returns:
        - Redirección a la vista de inicio de sesión.
    """
    return redirect(url_for('login')) #Redireccion directa a login

@login_manager_app.user_loader
def load_user(user_id):
    """
    Carga un usuario específico en base a su ID.

    Flujo:
        1. Utiliza el ID proporcionado por Flask-Login.
        2. Llama a la función `get_by_id` del modelo `ModelUser` para recuperar los datos del usuario desde la base de datos.

    Returns:
        - Una instancia del usuario si se encuentra, o `None` si no se encuentra.
    """
        # Busca el usuario en la base de datos
    db_user = ModelUser.get_by_id(db, user_id)
    if db_user:
        return db_user  # Devuelve una instancia de User
    return None

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.is_active() or not current_user.has_role(role_name):
                return jsonify(success=False, message="No tiene permiso para realizar esta acción"), 403
            return f(*args, **kwargs)
        return wrapped_function
    return decorator

#RUTA PARA CERRAR SESION
@app.route('/logout')
@login_required
def logout():
    """
    Cierra la sesión del usuario actual y redirige a la página de cierre de sesión.

    Flujo:
        1. Llama a `logout_user` para finalizar la sesión del usuario.
        2. Redirige al usuario a la página de cierre de sesión definida por la función `logout`.

    Returns:
        - Redirección a la vista de cierre de sesión.
    """
    logout_user()
    return redirect(url_for('login'))

#_______________________________________________________________________________________________________
                                                #Login
@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Maneja el inicio de sesión de los usuarios.

    Métodos permitidos:
        - GET: Renderiza la página de inicio de sesión.
        - POST: Procesa el formulario de inicio de sesión.

    Flujo del método POST:
        1. Valida que los campos `identification` y `password` no estén vacíos.
        2. Crea una instancia temporal de usuario (`User`) con los datos ingresados.
        3. Busca al usuario en la base de datos mediante `ModelUser.login`.
        4. Si el usuario es encontrado:
            - Verifica si la contraseña proporcionada es correcta usando `User.check_password`.
            - Si la contraseña es válida, inicia sesión y redirige a la página principal.
            - Si la contraseña es inválida, muestra un mensaje de error.
        5. Si el usuario no es encontrado, muestra un mensaje de error.

    Returns:
        - GET: Renderiza el template `auth/login.html`.
        - POST: Dependiendo de la validación:
            - Redirige a la página principal si las credenciales son válidas.
            - Renderiza `auth/login.html` con un mensaje de error si hay fallas en la autenticación.
    """
    if request.method == 'POST':
        identification = request.form.get('identification')
        password = request.form.get('password')

        # Validar campos
        if not identification or not password:
            flash("Por favor, completa todos los campos", "warning")
            return render_template('/login.html')

        # instancia temporal de User
        temp_user = User(0, identification, password)

        # Buscar usuario en la base de datos
        logged_user = ModelUser.login(db, temp_user)

        if logged_user:
            # Verificar la contraseña
            if User.check_password(logged_user.password, password):
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña inválida", "danger")
        else:
            flash("Usuario no encontrado", "danger")
    return render_template('auth/login.html')

#_______________________________________________________________________________________________________
                                            #Registro de usuarios
#RUTA PARA EL REGISTRO DE USUARIOS
@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Maneja el registro de nuevos usuarios.

    Métodos permitidos:
        - GET: Renderiza la página de registro.
        - POST: Procesa el formulario para registrar un nuevo usuario.

    Flujo del método POST:
        1. Valida que los campos `identification`, `password` y `fullname` no estén vacíos.
        2. Crea un objeto `User` con los datos proporcionados.
        3. Intenta registrar al usuario en la base de datos utilizando `Register.register`.
        4. Si el registro es exitoso, redirige a la página de inicio de sesión.
        5. Maneja posibles errores:
            - `ValueError`: Mensaje de advertencia específico.
            - Otros errores: Mensaje genérico de error y redirección a la página de registro.

    Manejo de excepciones:
        - Captura errores inesperados y muestra un mensaje de error en la página de registro.

    Returns:
        - GET: Renderiza el template `auth/register.html`.
        - POST: Redirige al login si el registro es exitoso o vuelve al formulario con mensajes de error.
    """
    try:
        if request.method == 'POST':
            identification = request.form.get('identification')
            password = request.form.get('password')
            fullname = request.form.get('fullname')

            if not identification or not password or not fullname:
                flash("Por favor, completa todos los campos", "warning")
                return render_template('auth/register.html')

            # Crear objeto User
            user = User(None, identification, password, fullname)

            try:
                registered_user = Register.register(db, user)
                return redirect(url_for('login'))
            except ValueError as ve:
                flash(str(ve), "warning")
            except Exception as e:
                flash("Error al registrar usuario", "danger")
                return redirect(url_for('register'))

        return render_template('auth/register.html')
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "danger")
        return render_template('auth/register.html')
    
    
#_______________________________________________________________________________________________________
                                                 #Admin panel
#RUTA PARA EL PANEL DE ADMINISTRADOR
@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    """
    Renderiza la página de administrador.

    Requisitos:
        - El usuario debe estar autenticado (`@login_required`).
        - El usuario debe tener el rol de administrador (`@role_required('admin')`).

    Returns:
        - Renderiza el template `admin.html`.
    """
    app.jinja_env.globals['now'] = datetime.datetime.now

    return render_template('admin.html')
#_______________________________________________________________________________________________________
                                                 #Inicio
#RUTA PARA EL HOME
@app.route('/home')
@login_required 
def home():
    """
    Renderiza la página principal del sistema.

    Requisitos:
        - El usuario debe estar autenticado (`@login_required`).

    Flujo:
        1. Obtiene las últimas ventas llamando a `obtener_ultimas_ventas`.
        2. Maneja posibles errores al obtener las ventas:
            - Si ocurre un error, registra el mensaje en consola y devuelve un código HTTP 500.

    Returns:
        - Renderiza el template `home.html` con las últimas ventas.
    """
    try:
        if current_user.is_authenticated():
            ultimos_productos = obtener_ultimas_ventas()
        else:
            return jsonify(success=False, message="El usuario no esta autenticado."), 403
    except Exception as e:
        print(f"Error obteniendo las últimas ventas: {e}")
        abort(500) 
    return render_template('home.html', ultimas_ventas=ultimos_productos)

#_______________________________________________________________________________________________________
                                                #Proveedores
#RUTA PARA OBTENER LISTA DE PROVEEDORES
@app.route('/proveedores')
@login_required
@role_required('admin')
def get_proveedores():
    """
    Muestra la lista de proveedores en el sistema.

    Requisitos:
        - El usuario debe estar autenticado (`@login_required`).

    Flujo:
        1. Obtiene la lista de proveedores llamando a `obtener_proveedores` 
            (ubicada en `models/proveedor.py`).
        2. Maneja posibles errores al obtener los proveedores:
            - Si ocurre un error, registra el mensaje en consola y devuelve un código HTTP 500.

    Returns:
        - Renderiza el template `proveedores.html` con la lista de proveedores.
    """
    if not current_user.is_authenticated():
        return jsonify(success=False, message="No tiene permiso para realizar esta acción"), 403
    else:
        try:
            lista_proveedores = obtener_proveedores()
        except Exception as e:
            logging.error(f"Error retrieving providers: {e}")
            return jsonify(success=False, message="Error interno del servidor"), 500
    return render_template('proveedores.html', proveedores=lista_proveedores)

def validar_correo(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' #Funcion auxiliar para validar correo electronico
    return re.match(patron, correo)

# RUTA PARA AÑADIR PROVEEDORES
@app.route('/proveedor', methods=['POST', 'GET'])
@role_required('admin')
@login_required
def provedor():
    """
    Maneja la creación de un nuevo proveedor y muestra el formulario de registro.

    Métodos permitidos:
        - GET: Renderiza la página de registro de proveedores.
        - POST: Procesa los datos enviados para registrar un nuevo proveedor.

    Flujo del método POST:
        1. Recoge los datos del formulario:
            - `NameProvider`: Nombre de la empresa.
            - `addressProvider`: Dirección del proveedor.
            - `phoneProvider`: Teléfono del proveedor.
            - `emailProvider`: Correo electrónico del proveedor.
        2. Valida que todos los campos estén completos:
            - Si falta algún campo, devuelve un mensaje de error con un código HTTP 400.
        3. Valida el correo electrónico usando `validar_correo`:
            - Si el correo es inválido, devuelve un mensaje de error con un código HTTP 400.
        4. Intenta añadir el proveedor usando la función `añadir_proveedor`:
            - Si la operación es exitosa, redirige a la lista de proveedores y muestra un mensaje de éxito.
            - Si ocurre un error durante la inserción, devuelve un mensaje de error con un código HTTP 500.

    Manejo de excepciones:
        - Captura errores inesperados durante el procesamiento y devuelve un mensaje de error genérico en formato JSON.

    Returns:
        - GET: Renderiza el formulario para el registro de proveedores.
        - POST:
            - Redirige a `/proveedores` si el registro es exitoso.
            - Devuelve un mensaje de error en formato JSON si hay fallas en la validación o en la operación.

    HTTP Responses:
        - 200: Proveedor añadido exitosamente.
        - 400: Error en los datos proporcionados (campos incompletos o correo inválido).
        - 500: Error interno al añadir el proveedor.
    """
    try:
        if request.method == 'POST':
            nombre_empresa = request.form.get("NameProvider")
            direccion = request.form.get("addressProvider")
            telefono = request.form.get("phoneProvider")
            correo_electronico = request.form.get("emailProvider")
        if not nombre_empresa or not direccion or not telefono or not correo_electronico:
            return jsonify({'message': 'Los campos están incompletos'}), 400
        if not validar_correo(correo_electronico):  # Validación adicional (función auxiliar)
            return jsonify({'message': 'Correo electrónico inválido'}), 400

        if añadir_proveedor(nombre_empresa, direccion, telefono, correo_electronico):
            return redirect('/proveedores')
        else: 
            return jsonify({'message': 'Error al añadir el proveedor'}), 500
    except Exception as e:
        print("Error al procesar la solicitud",e)
        return jsonify({'message': 'Error al procesar la solicitud'})

#RUTA PARA ELIMINAR PROVEEDORES
@app.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
@login_required
@role_required('admin')
def eliminar_proveedor(id_proveedor):
    """
    Elimina un proveedor del sistema.

    Método permitido:
        - DELETE: Elimina el proveedor con el ID proporcionado.

    Flujo:
        1. Llama a la función `eliminar_proveedor` con el ID proporcionado.
        2. Si la operación es exitosa, devuelve un mensaje de confirmación en formato JSON.
        3. Si se utiliza un método no permitido, devuelve un código HTTP 405 (Método no permitido).

    Returns:
        - JSON con un mensaje de éxito si la eliminación es exitosa.
        - Código HTTP 405 si se intenta acceder con un método diferente a DELETE.
    """
    if request.method == 'DELETE':
        eliminar_proveedor(id_proveedor)
        return jsonify({'message': 'Proveedor eliminado correctamente'})
    else:
        return abort(405) 

#_______________________________________________________________________________________________________

                                                    #Productos
#RUTA PARA AÑADIR PRODUCTOS 
@app.route('/productos', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    """
    Maneja la creación de nuevos productos y muestra la lista de productos existentes.

    Métodos permitidos:
        - GET: Renderiza la página para añadir productos y muestra la lista de productos actuales.
        - POST: Procesa el formulario para crear un nuevo producto.

    Flujo del método POST:
        1. Recoge los datos del formulario:
            - `NameProduct`: Nombre del producto.
            - `Description`: Descripción del producto.
            - `PriceProduct`: Precio del producto.
            - `StockProduct`: Cantidad en inventario.
            - `CategoryProduct`: Categoría del producto.
            - `ProviderProduct`: Proveedor del producto.
            - `IngresoProduct`: Fecha de ingreso.
        2. Valida que todos los campos estén completos.
        3. Intenta convertir `PriceProduct` y `StockProduct` a los tipos de datos apropiados.
            - Si la conversión falla, devuelve un mensaje de error.
        4. Llama a la función `crear_producto` para registrar el producto en el sistema.
            - Si la operación es exitosa, redirige a `/productos`.
        5. Maneja excepciones generales devolviendo un mensaje de error en formato JSON.

    Flujo del método GET:
        1. Obtiene listas de proveedores, categorías y productos existentes.
        2. Renderiza el template `productos.html` con las listas obtenidas.

    Returns:
        - POST: Redirige a `/productos` si la creación es exitosa o devuelve un mensaje de error en caso de falla.
        - GET: Renderiza el template `productos.html` con los datos necesarios.
        - 400: Si hay datos inválidos o incompletos.
        - 500: Si ocurre un error interno.
    """
    try:
        if request.method == 'POST':
            nombre = request.form.get('NameProduct')
            descripcion = request.form.get('Description')
            precio = request.form.get('PriceProduct')
            stock = request.form.get('StockProduct')
            categoria = request.form.get('CategoryProduct')
            proveedor = request.form.get('ProviderProduct')
            fecha_ingreso = request.form.get('IngresoProduct')
            
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

    lista_proveedores = obtener_proveedores()
    lista_categorias = obtener_categorias()
    lista_productos = obtener_lista_productos() 

    return render_template('productos.html', proveedores=lista_proveedores, categorias=lista_categorias, productos=lista_productos)

#DECORADOR PARA VER SI EXISTE EL PRODUCTO
def producto_existe(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        producto_id = kwargs.get('id')
        if not obtener_producto_id(producto_id):
            return jsonify({'message': 'Producto no encontrado'}), 404
        return f(*args, **kwargs)
    return wrap

#RUTA PARA ELIMINAR EL PRODUCTO
@app.route('/eliminar_productos/<int:id>', methods=['DELETE'])
@login_required
@producto_existe
@role_required('admin')
def eliminar_producto(id):
    """
    Elimina un producto del sistema.

    Flujo:
        1. Verifica si el usuario tiene permiso para eliminar productos usando `current_user.can_delete_product`.
            - Si no tiene permisos, devuelve un código HTTP 403.
        2. Llama a la función `eliminar_productos` con el ID proporcionado.
            - Si la eliminación es exitosa, devuelve un mensaje de éxito con código HTTP 200.
            - Si falla, devuelve un mensaje de error con código HTTP 400.
        3. Captura y registra cualquier error inesperado, devolviendo un mensaje de error genérico con código HTTP 500.

    Returns:
        - 200: Producto eliminado exitosamente.
        - 400: No se pudo eliminar el producto.
        - 403: El usuario no tiene permiso para eliminar productos.
        - 500: Error interno al procesar la solicitud.
    """
    try:
        if not current_user.can_delete_product(): #can_delete_product aun no manejo roles pero se usa cuando el user esta activo
            return jsonify({'message': 'No tiene permiso para eliminar productos'}), 403
        
        if eliminar_productos(id):
            return jsonify({'message': 'Producto eliminado exitosamente'}), 200
        else:
            return jsonify({'message': 'No se pudo eliminar el producto'}), 400
    except Exception as e:
        logger.error(f"Error interno al eliminar producto con id {id}: {e}")
        return jsonify({'message': 'Error al procesar la solicitud'}), 500


#RUTA PARA EDITAR PRODUCTOS
@app.route('/editar_producto', methods=['PUT'])
@login_required
@role_required('admin')
def editar_producto():
    """
    Edita los datos de un producto existente.

    Flujo:
        1. Recoge los datos del formulario:
            - `producto_id`: Identificador del producto.
            - `edit_NameProduct`: Nombre del producto.
            - `edit_Description`: Descripción del producto.
            - `edit_Price`: Precio del producto.
            - `edit_Stock`: Cantidad en inventario.
        2. Valida que todos los campos estén completos.
            - Si falta algún campo, devuelve un mensaje de error con código HTTP 400.
        3. Convierte `edit_Price` a flotante y `edit_Stock` a entero.
            - Si la conversión falla o los valores son negativos, devuelve un mensaje de error con código HTTP 400.
        4. Llama a la función `actualizar_producto` para guardar los cambios.
            - Si la operación es exitosa, devuelve un código HTTP 200.
            - Si falla, devuelve un mensaje de error con código HTTP 400.
        5. Maneja excepciones generales devolviendo un mensaje de error con código HTTP 500.

    Returns:
        - 200: Producto actualizado exitosamente.
        - 400: Error en los datos proporcionados o fallo en la operación.
        - 500: Error interno al procesar la solicitud.
    """
    if request.method == 'PUT':
        try:
            data = request.form
            identificador_p = data.get('producto_id')
            nombre = data.get('edit_NameProduct')
            descripcion = data.get('edit_Description')
            precio = data.get('edit_Price')
            stock = data.get('edit_Stock')
        
            if not all([nombre, descripcion, precio, stock, identificador_p]):
                return jsonify(success=False, message="Faltan datos"), 400

            # Validar de los datos correctos
            try:
                precio = float(precio)
                stock = int(stock)
                if precio < 0 or stock < 0:
                    return 
            except ValueError:
                return 
            # Intentar actualizar el producto
            if actualizar_producto(identificador_p, nombre, descripcion, precio, stock):
                return jsonify(success=True), 200
            else:
                return jsonify(success=False, message="Error al actualizar el producto"), 400
        
        except Exception as e:
            print(f"Error al procesar la solicitud {e}")
            return jsonify({'message': 'Error al procesar la solicitud'}),500

#_______________________________________________________________________________________________________
                                                #Categorias
#RUTA PARA OBTENER LISTA DE CATEGORIAS
@app.route('/categorias')
@login_required
def get_categorias():
    """
    Obtiene y muestra la lista de categorías disponibles.

    Flujo:
        1. Llama a la función `obtener_categorias` para recuperar las categorías desde la base de datos.
        2. Captura cualquier error y lo registra en la consola.

    Returns:
        - Renderiza el template `productos.html` con la lista de categorías.
    """
    try: 
        lista_categorias = obtener_categorias()
    except Exception as e:
        print("Error al obtener las categoras", str(e))
    return render_template('productos.html', lista_categorias=lista_categorias)


#RUTA PARA AÑADIR UNA CATEGORIA
@app.route('/addCategorias', methods=['POST'])
@login_required
def crear_categoria():
    """
    Crea una nueva categoría en el sistema.

    Flujo:
        1. Recoge el nombre de la categoría desde el formulario.
            - Si el campo está vacío, devuelve un mensaje de error con código HTTP 400.
        2. Llama a la función `ingresar_categoria` para guardar la categoría en la base de datos.
            - Si la operación es exitosa, devuelve un mensaje de éxito con el ID de la categoría creada.
            - Si falla, devuelve un mensaje de error con código HTTP 500.
        3. Captura cualquier excepción y devuelve el mensaje del error con código HTTP 500.

    Returns:
        - JSON con mensaje de éxito y ID de la categoría creada.
        - 400: El nombre de la categoría es obligatorio.
        - 500: Error interno al añadir la categoría.
    """
    try:
        nombre_categoria = request.form.get('CategoryName')  
        if not nombre_categoria: 
            return jsonify(success=False, message="El nombre de la categoría es obligatorio."), 400

        # Llamar a la función para insertar la categoría
        categoria_id = ingresar_categoria(nombre_categoria)
        if categoria_id:  # Verifica si se obtuvo un ID válido
            return jsonify(success=True, id=categoria_id, message="Categoría creada exitosamente") 
        else:
            return jsonify(success=False, message="Error al añadir la categoría."), 500
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


#_______________________________________________________________________________________________________
#RUTA PARA VENTAS
@app.route('/ventas')
@login_required
def ventas():
    """
    Muestra la lista de ventas realizadas.

    Flujo:
        1. Llama a la función `obtener_ventas` para recuperar las ventas desde la base de datos.
        2. Captura cualquier error y lo registra en la consola.

    Returns:
        - Renderiza el template `ventas.html` con la lista de ventas.
    """
    try:
        lista_ventas = obtener_ventas()
    except Exception as e:
        print("Error al obtener las ventas", str(e))
    return render_template('ventas.html', ventas=lista_ventas)


#_______________________________________________________________________________________________________
                                              #Clientes

# RUTA PARA OBTENER LISTA DE CLIENTES
@app.route('/clientes')
@login_required
def clientes():
    """
    Muestra la lista de clientes registrados en el sistema.

    Flujo:
        1. Llama a la función `obtener_lista_clientes` para recuperar los datos de los clientes.
        2. Captura cualquier error y lo registra en la consola.
        3. Si ocurre un error, incluye un mensaje de error en el contexto del template.

    Returns:
        - Renderiza el template `clientes.html` con la lista de clientes.
        - Incluye un mensaje de error si no se pudieron obtener los datos.
    """
    try:
        lista_clientes = obtener_lista_clientes()
        return render_template('clientes.html', clientes=lista_clientes)
    except Exception as e:
        print(f"Error al obtener la lista de clientes: {e}")
        mensaje_error = 'No se ha podido obtener la lista de clientes.'
    return render_template('clientes.html', clientes=lista_clientes, mensaje_error = mensaje_error)


#RUTA PARA AÑADIR CLIENTES 
@app.route('/cliente', methods=['POST'])
@login_required
def nuevo_cliente():
    """
    Registra un nuevo cliente en el sistema.

    Flujo:
        1. Recoge los datos del cliente desde el formulario:
            - `DNIClient`: Cédula del cliente.
            - `NameClient`: Nombre del cliente.
            - `LastNameClient`: Apellido del cliente.
            - `addressClient1`: Dirección del cliente.
            - `phoneClient`: Teléfono del cliente.
            - `emailClient`: Correo electrónico del cliente.
        2. Verifica que todos los campos requeridos estén completos.
            - Si falta algún dato, devuelve un mensaje de error con código HTTP 400.
        3. Llama a la función `añadir_cliente` para registrar al cliente.
            - Si la operación es exitosa, redirige a la página de clientes.
            - Si falla, muestra un mensaje de error.

    Returns:
        - Renderiza el template `clientes.html` en caso de éxito o error.
    """
    try: 
        if request.method == 'POST':
            cedula = request.form.get('DNIClient')
            nombres = request.form.get('NameClient')
            apellidos = request.form.get('LastNameClient')
            direccion = request.form.get('addressClient1')
            telefono = request.form.get('phoneClient')
            email = request.form.get('emailClient')
            
            # Verificar si alguno de los campos requeridos está vacío
            if not all([cedula, nombres, apellidos, direccion, telefono, email]):
                return jsonify(success=False, message="Faltan datos"), 400

            # Llamado a la función con los datos del nuevo cliente
            if añadir_cliente(cedula, nombres, apellidos, direccion, telefono, email):
                return redirect('/clientes')
            else:
                return "Error al añadir cliente"
    except Exception as e:
        print(f"Error al procesar la solicitud {e}")
        return jsonify({'message': 'Error al procesar la solicitud'}),500
    return render_template('clientes.html')

#RUTA PARA VER LAS COMPRAS HECHAS POR EL CLIENTE
@app.route('/mostrar_compras_cliente/<int:cliente_id>', methods=['GET'])
@login_required
def ruta_mostrar_compras_cliente(cliente_id):
    """
    Maneja la solicitud para obtener las compras realizadas por un cliente específico.

    Esta función utiliza el identificador del cliente (`cliente_id`) para consultar 
    las compras asociadas a dicho cliente en la base de datos. Devuelve los datos 
    en formato JSON.

    Args:
        cliente_id (int): El identificador único del cliente para el que se 
        desean consultar las compras.

    Returns:
        flask.Response: Respuesta HTTP con el siguiente contenido:
            - Si se encuentran compras:
                - Código de estado 200.
                - JSON con las compras del cliente en el formato:
                  {
                      "success": True,
                      "compras": [lista de compras]
                  }
            - Si no se encuentran compras:
                - Código de estado 200.
                - JSON con una lista vacía:
                  {
                      "success": True,
                      "compras": []
                  }
            - En caso de error de validación:
                - Código de estado 400.
                - JSON con el mensaje de error:
                  {
                      "success": False,
                      "message": "Error de validación: [detalle del error]"
                  }
            - En caso de error inesperado:
                - Código de estado 500.
                - JSON con un mensaje genérico de error:
                  {
                      "success": False,
                      "message": "Ocurrió un error al procesar la solicitud."
                  }

    Exceptions:
        ValueError: Manejado específicamente para errores de validación.
        Exception: Cualquier otro error no previsto se captura y se registra.

    Notes:
        - La función requiere que el usuario esté autenticado para acceder
          (decorador @login_required).
        - Los errores inesperados se registran en los logs del servidor para
          facilitar la depuración.
    """
    try:
        # Obtener las compras del cliente
        compras = mostrar_compas_cliente(cliente_id)
        
        # Si no hay compras, devolver una lista vacía
        if not compras:
            return jsonify(success=True, compras=[]), 200

        # Retornar las compras
        return jsonify(success=True, compras=compras), 200

    except ValueError as ve:
        # Manejar errores específicos
        return jsonify(success=False, message=f"Error de validación: {str(ve)}"), 400
    except Exception as e:
        # Manejar errores generales
        app.logger.error(f"Error al obtener las compras del cliente {cliente_id}: {str(e)}")
        return jsonify(success=False, message="Ocurrió un error al procesar la solicitud."), 500

    
# RUTA PARA EDITAR CLIENTES
@app.route('/editar_cliente', methods=['PUT'])
@login_required
def editar_cliente():
    """
    Actualiza los datos de un cliente existente.

    Flujo:
        1. Recoge los datos del cliente desde el formulario de edición:
            - `cliente_id`: ID del cliente.
            - `edit_NameClient`: Nuevo nombre.
            - `edit_LastNameClient`: Nuevo apellido.
            - `edit_addressClient`: Nueva dirección.
            - `edit_phoneClient`: Nuevo teléfono.
            - `edit_emailClient`: Nuevo correo electrónico.
            - `edit_cedulaClient`: Nueva cédula.
        2. Verifica que todos los campos requeridos estén completos.
            - Si falta algún dato, devuelve un mensaje de error con código HTTP 400.
        3. Llama a la función `actualizar_cliente` para guardar los cambios.
            - Si la operación es exitosa, devuelve un JSON de éxito.
            - Si falla, devuelve un mensaje de error con código HTTP 400.

    Returns:
        - JSON con el resultado de la operación.
    """
    try:
        # Obtener los datos del formulario de edicion (esta en un swal alert de js "EditClientModal")
        identificador_c = request.form.get('cliente_id')
        nombre = request.form.get('edit_NameClient')
        apellido = request.form.get('edit_LastNameClient')
        direccion = request.form.get('edit_addressClient')
        telefono = request.form.get('edit_phoneClient')
        email = request.form.get('edit_emailClient')
        cedul = request.form.get('edit_cedulaClient')


        if not all([identificador_c, nombre, apellido, direccion, telefono, email, cedul]):
            return jsonify(success=False, message="Faltan datos"), 400
        if actualizar_cliente(identificador_c, nombre, apellido, direccion, telefono, email, cedul):
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Error al actualizar el cliente"), 400

    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


#RUTA PARA ELIMINAR CLIENTES
@app.route('/eliminar_cliente/<int:cliente_id>', methods=['DELETE'])
@login_required
def eliminar_cliente(cliente_id):
    """
    Elimina un cliente del sistema.

    Flujo:
        1. Recibe el ID del cliente a eliminar como parámetro en la URL.
        2. Llama a la función `eliminarr_client` para realizar la operación.
            - Si la operación es exitosa, devuelve un mensaje de éxito con código HTTP 200.
            - Si falla, devuelve un mensaje de error con código HTTP 500.

    Returns:
        - JSON con el mensaje del resultado de la operación.
    """

    try:
        if role_required('admin'):
            if request.method=='DELETE':
                eliminarr_client(cliente_id)
                return jsonify({'message': 'Cliente eliminado exitosamente'}),200
            else:
                return jsonify({'message': '>Error al elimina al cliente'}),500
        else:
            return jsonify({'message': 'No tiene permiso para eliminar clientes'}),403

    except Exception as e:
        print("Error al procesar la solicitud DELETE:", e)
        return jsonify({'message': 'Error al procesar la solicitud'}),500


#_______________________________________________________________________________________________________
                                                #Ventas

#RUTA PARA VENDER
@app.route('/facturar', methods=['POST', 'GET'])
@login_required
def facturar():
    """
    Procesa la facturación de una venta.

    Flujo:
        1. Recoge los datos generales de la venta:
            - ID del usuario y cliente.
            - Fecha y hora de la venta.
        2. Recoge los datos de los pagos:
            - Fecha y hora del pago.
            - Total de la venta y notas adicionales.
        3. Recoge los detalles de los productos:
            - ID, cantidad, precio unitario y descripción.
            - Verifica que todos los datos sean consistentes y válidos.
        4. Llama a la función `añadir_facturacion` para registrar la venta y generar la factura.
            - Si la operación falla, captura y maneja las excepciones.
        5. En caso de éxito, muestra un mensaje de confirmación con el número de factura.

    Returns:
        - Redirige a la página de ventas en caso de éxito.
        - Renderiza el template `facturar.html` con los datos necesarios en caso de error.
    """
    try:
        if request.method == 'POST':
            # Datos de la venta
            usuario = int(request.form.get("id_usuario"))
            cliente = int(request.form.get("id_cliente"))
            fecha_venta = request.form.get("fecha_venta")
            hora_venta = request.form.get("hora_venta")
            
            # Datos de los pagos
            fecha_pago = request.form.get("fecha_pago")
            hora_pago = request.form.get("hora_pago")
            total = float(request.form.get("total"))
            nota = request.form.get("notas")
            
            if total <= 0:
                raise ValueError("El total no puede ser menor o igual a cero.")

            # Detalles de los productos
            productos = []
            productos_ids = request.form.getlist("productos[]")
            cantidades = request.form.getlist("cantidad[]")
            precios = request.form.getlist("precio[]")
            descripciones = request.form.getlist("servicio[]")

            
            if not (len(productos_ids) == len(cantidades) == len(precios) == len(descripciones)):
                raise ValueError("Datos incompletos en la lista de productos.")

            for i in range(len(productos_ids)):
                cantidad = int(cantidades[i])
                precio_unitario = float(precios[i])
                descripcion = descripciones[i] if i < len(descripciones) else ""
                if cantidad <= 0 or precio_unitario <= 0:
                    raise ValueError(f"Valores inválidos en el producto {i + 1}.")
                productos.append({
                    'id_producto': int(productos_ids[i]),
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'descripcion': descripcion.strip()
                })

            # Registrar la venta y la factura
            resultado_facturacion = añadir_facturacion(usuario, cliente, fecha_venta, hora_venta, productos, total, fecha_pago, hora_pago, nota)
            
            if resultado_facturacion["status"] != "success":
                return jsonify({"status": "error", "message": resultado_facturacion["message"]}), 400
            
            
            # Extraer datos de la factura generada
            numero_factura = resultado_facturacion["numero_factura"]
            id_factura = resultado_facturacion["id_factura"]
            
            # Confirmar éxito
            return jsonify({
            "status": "success",
            "message": "Venta registrada exitosamente.",
            "numero_factura": resultado_facturacion["numero_factura"]
            }), 200

    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "danger")
        print("Error inesperado:", str(e))

    # Renderizar formulario de facturación
    lista_clientes = obtener_lista_clientes()
    lista_productos = obtener_lista_productos()
    return render_template('facturar.html', lista_clientes=lista_clientes, lista_productos=lista_productos), 200
 
#RUTA PARA OBTENER FACTURAS
@app.route('/obtener_pago/<int:id_venta>', methods=['GET'])
@login_required
def obtener_pago(id_venta):
    try:
        """
        Obtiene la información del pago asociado a una venta específica.

        Flujo:
            1. Recibe el ID de la venta como parámetro en la URL.
            2. Consulta la base de datos para obtener los detalles del pago relacionado, incluyendo:
                - `id_pagos`: ID del pago.
                - `id_venta`: ID de la venta.
                - `monto`: Monto del pago.
                - `fecha_pago`: Fecha en que se realizó el pago.
                - `hora_pago`: Hora en que se realizó el pago.
                - `nota`: Nota adicional del pago.
                - `id_factura`: ID de la factura asociada.
                - `numero_factura`: Número de la factura asociada.
            3. Si no se encuentra información del pago, devuelve un error con código HTTP 404.
            4. Si ocurre un error en la consulta, devuelve un mensaje de error con código HTTP 500.

        Returns:
            - JSON con los datos del pago en caso de éxito.
            - Mensaje de error con los códigos HTTP correspondientes en caso de fallo.
        """
        conn = mysql.connection
        cursor = conn.cursor()
        sql_pago = """
            SELECT 
                p.id_pagos, p.id_venta, p.monto, p.fecha_pago, 
                p.hora_pago, p.nota, p.id_factura, f.numero_factura
            FROM pagos p
            LEFT JOIN facturas f ON p.id_factura = f.id_factura
            WHERE p.id_venta = %s;
        """
        cursor.execute(sql_pago, (id_venta,))
        pago = cursor.fetchone()

        # Verifica si no se encontró ningún pago
        if not pago:
            return jsonify({"status": "error", "message": "No se encontró información del pago."}), 404

        # Devuelve los datos del pago como JSON
        return jsonify({
            "status": "success",
            "pago": {
                "id_pagos": pago[0],
                "id_venta": pago[1],
                "monto": float(pago[2]),
                "fecha_pago": str(pago[3]),
                "hora_pago": str(pago[4]),
                "nota": pago[5],
                "id_factura": pago[6],
                "numero_factura": pago[7]
            }
        }), 200

    except Exception as e:
        print("Error al obtener el pago:", str(e))
        return jsonify({"status": "error", "message": "Error al obtener el pago."}), 500


#_______________________________________________________________________________________________________
@app.route('/reportes', methods=['GET', 'POST'])
@login_required
def reportes():
    
    return render_template('reportes.html'), 200

#_______________________________________________________________________________________________________

# MANEJO PARA EL 404 ERROR
def status404(error):
    """
    Muestra la página personalizada para manejar errores 404.

    Flujo:
        1. Renderiza el template `404handler.html` en caso de que una página solicitada no sea encontrada.

    Returns:
        - Template HTML con un mensaje de error 404.
    """
    return render_template('404handler.html'), 404

#_______________________________________________________________________________________________________

#EN CASO DE METODO INCORRECTO
@app.errorhandler(405)
def method_not_allowed(e):
    """
    Devuelve un mensaje de error para solicitudes con un método HTTP no permitido.

    Flujo:
        1. Captura el error 405 y devuelve un mensaje en formato JSON indicando que el método no está permitido.

    Returns:
        - JSON con un mensaje de error y código HTTP 405.
    """

    return jsonify(success=False, message="Método no permitido"), 405

#_______________________________________________________________________________________________________

def status401(error):
    """
    Redirige al usuario a la página de inicio de sesión en caso de error 401 (no autorizado).

    Flujo:
        1. Captura el error 401 y redirige al usuario a la función `login`.

    Returns:
        - Redirección a la vista de inicio de sesión.
    """
    return redirect(url_for('login'))

#_______________________________________________________________________________________________________

if __name__ == '__main__':
    app.config.from_object(config['production'])
    csrf.init_app(app)
    app.register_error_handler(404, status404)
    app.register_error_handler(401, status401)
    app.run(host="0.0.0.0", port=5000)
