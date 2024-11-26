from flask import Flask, abort, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import jsonify, render_template, request, flash, redirect, url_for
from flask_wtf import CSRFProtect
from flask import send_file
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
#RUTA LOGIN
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)
#_______________________________________________________________________________________________________
@app.route('/')
def index():
    return redirect(url_for('login')) #Redireccion directa a login

#_______________________________________________________________________________________________________

@app.route('/login', methods=["GET", "POST"])
def login():
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

#RUTA PARA EL REGISTRO DE USUARIOS
@app.route('/register', methods=["GET", "POST"])
def register():
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
                return('register')

        return render_template('auth/register.html')
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "danger")
        return render_template('auth/register.html')

#_______________________________________________________________________________________________________

#RUTA PARA EL HOME

@app.route('/home')
@login_required 
def home():
    try:
        ultimas_ventas = obtener_ultimas_ventas()
    except Exception as e:
        print(f"Error obteniendo las últimas ventas: {e}")
        abort(500) 
    return render_template('home.html', ultimas_ventas=ultimas_ventas)

#_______________________________________________________________________________________________________

#RUTA PARA OBTENER LISTA DE PROVEEDORES
@app.route('/proveedores')
@login_required
def get_proveedores():
    try:
        lista_proveedores = obtener_proveedores()
    except Exception as e:
        print(f"Error obteniendo al proveedor: {e}")
        abort(500) 
    return render_template('proveedores.html', proveedores=lista_proveedores)


def validar_correo(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo)

# RUTA PARA AÑADIR PROVEEDORES
@app.route('/proveedor', methods=['POST', 'GET'])
@login_required
def provedor():
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
            flash('Proveedor añadido exitosamente', 'success')
            return redirect('/proveedores')
        else: 
            return jsonify({'message': 'Error al añadir el proveedor'}), 500
    except Exception as e:
        print("Error al procesar la solicitud",e)
        return jsonify({'message': 'Error al procesar la solicitud'})

#RUTA PARA ELIMINAR PROVEEDORES
@app.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
@login_required
def eliminar_proveedor(id_proveedor):
    if request.method == 'DELETE':
        eliminar_proveedor(id_proveedor)
        return jsonify({'message': 'Proveedor eliminado correctamente'})
    else:
        return abort(405) 

#_______________________________________________________________________________________________________

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

#_______________________________________________________________________________________________________

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

#RUTA PARA OBTENER LISTA DE CATEGORIAS
@app.route('/categorias')
@login_required
def get_categorias():
    lista_categorias = obtener_categorias()
    return render_template('productos.html', lista_categorias=lista_categorias)

#_______________________________________________________________________________________________________

#RUTA PARA AÑADIR UNA CATEGORIA
@app.route('/addCategorias', methods=['POST'])
@login_required
def crear_categoria():
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
    lista_ventas = obtener_ventas()
    return render_template('ventas.html', ventas=lista_ventas)



#_______________________________________________________________________________________________________

# RUTA PARA OBTENER LISTA DE CLIENTES
@app.route('/clientes')
@login_required
def clientes():
    try:
        lista_clientes = obtener_lista_clientes()
        return render_template('clientes.html', clientes=lista_clientes)
    except Exception as e:
        print(f"Error al obtener la lista de clientes: {e}")
        mensaje_error = 'No se ha podido obtener la lista de clientes.'
        return render_template('clientes.html', clientes=lista_clientes, mensaje_error = mensaje_error)

#_______________________________________________________________________________________________________


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

#_______________________________________________________________________________________________________


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

        if not all([identificador_c, nombre, apellido, direccion, telefono, email, cedul]):
            return jsonify(success=False, message="Faltan datos"), 400
        if actualizar_cliente(identificador_c, nombre, apellido, direccion, telefono, email, cedul):
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Error al actualizar el cliente"), 400
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

#_______________________________________________________________________________________________________


#EN CASO DE METODO INCORRECTO
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(success=False, message="Método no permitido"), 405

#_______________________________________________________________________________________________________


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
#RUTA PARA VENDER
@app.route('/facturar', methods=['POST', 'GET'])
@login_required
def facturar():
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
                raise Exception(resultado_facturacion["message"])
            
            # Extraer datos de la factura generada
            numero_factura = resultado_facturacion["numero_factura"]
            id_factura = resultado_facturacion["id_factura"]
            
            # Confirmar éxito
            flash(f"Venta registrada exitosamente. Número de factura: {numero_factura}", "success")
            return redirect(url_for('ventas'))

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


    
#RUTA PARA IMPRIMIR FACTURAS
"""@app.route('/imprimir_factura/<int:id_factura>', methods=['GET'])
@login_required
def imprimir_factura(id_factura):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Obtener datos de la factura
        datos_factura, error = obtener_datos_factura(cursor, id_factura)
        if error:
            return f"Error al obtener datos de la factura: {error}", 404

        # Generar PDF
        pdf_path, error = generar_pdf_factura(datos_factura)
        if error:
            return f"Error al generar el PDF: {error}", 500

        # Enviar el archivo PDF como respuesta
        return send_file(pdf_path, as_attachment=True, download_name=f"factura_{datos_factura['numero_factura']}.pdf")

    except Exception as e:
        print("Error al procesar la solicitud:", str(e))
        return "Error interno del servidor.", 500
"""
#_______________________________________________________________________________________________________

#RUTA PARA EDITAR PRODUCTOS
@app.route('/editar_producto', methods=['PUT'])
@login_required
def editar_producto():
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


#RUTA PARA CERRAR SESION
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout'))

#_______________________________________________________________________________________________________

# MANEJO PARA EL 404 ERROR
def status404(error):
    return render_template('404handler.html'), 404

#_______________________________________________________________________________________________________

def status401(error):
    return redirect(url_for('login'))

#_______________________________________________________________________________________________________

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(404, status404)
    app.register_error_handler(401, status401)
    app.run(host="0.0.0.0", port=5000)
