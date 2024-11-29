.. StockManagerMyE documentation master file, created by
   sphinx-quickstart on Fri Nov 29 17:03:36 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenido a la documentación de **StockManagerMyE**
===================================================

**StockManagerMyE** es un sistema de gestión de inventarios sencillo, pero potente, diseñado para facilitar la administración de productos, proveedores y ventas. Utilizando tecnologías modernas como **Flask** para el backend y **Google Material Design** para la interfaz de usuario, proporciona una experiencia de usuario fluida y eficiente.

Este sistema es ideal para pequeñas y medianas empresas que necesitan gestionar su inventario de manera eficiente, desde el registro de productos hasta las ventas y pagos.

Tecnologías Usadas
------------------

- **Flask**: Framework usado para el desarrollo del backend.
- **Jinja2**: Motor de plantillas utilizado para generar el frontend dinámicamente.
- **Google Material Design**: Framework de diseño utilizado para crear una interfaz de usuario atractiva y responsiva.
- **JavaScript**: Para la interacción dinámica en el frontend.
- **MySQL**: Sistema de gestión de bases de datos utilizado para almacenar toda la información relacionada con el inventario.

Dependencias
------------

Para la autenticación y gestión de usuarios, se utilizan las siguientes dependencias:

- **Flask-Login**: Maneja las sesiones de usuario.
- **Flask-WTF**: Proporciona formularios seguros para la aplicación.
- **Werkzeug**: Proporciona utilidades para la autenticación y manejo de contraseñas.
- **Bcrypt**: Genera hashes de contraseñas para mayor seguridad.

Instalación y Configuración
===========================

Para instalar y configurar el proyecto correctamente, sigue estos pasos:

### Crear el entorno virtual

Crea un entorno virtual en la carpeta raíz del proyecto con el siguiente comando:

python3 -m venv nombre_del_entorno 

O si usas Windows:

python -m venv nombre_del_entorno

luego tienes que activar los scripts de el entorno virutal creado con el comando:

nombre_de_entorno \ Scripts \ activate

Una vez activado, instalar las dependencias dentro de la carpeta del proyecto, ejecuta el siguiente comando en la terminal:

pip install -r requirements.txt


### Configuración de la base de datos

1. **Configura la base de datos**:

   El proyecto utiliza **MySQL** para la gestión de datos. Debes ejecutar el script de la base de datos para crear las tablas necesarias. El nombre predeterminado de la base de datos es **StockManagerMyE**.

2. **Configura las variables de entorno**:

   Crea un archivo `.env` en la raíz del proyecto (si no existe) y agrega las siguientes variables, reemplazando con tus valores específicos:


MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=contraseña_db
MYSQL_DB=nombre_db
FLASK_ENV=development
DEBUG = True

Reemplazas los valores con los valores de la base de datos que creaste para el proyecto.

Asegúrate de que los valores sean correctos para tu entorno de base de datos.

Ejecución del Proyecto
======================

Para ejecutar el proyecto, abre la terminal y navega a la carpeta "src" donde se encuentra el archivo `app.py`. Luego, ejecuta el siguiente comando:

Ensayo
----------------------------------
Esto iniciará el servidor Flask. Verás algo similar a lo siguiente en la terminal:

 -Serving Flask app 'app'
 -Running on all addresses (0.0.0.0)
 -Running on http://127.0.0.1:5000  
 -Running on http://192.168.20.69:5000 
El proyecto también estará disponible en una red local para que puedas acceder desde otros dispositivos (por ejemplo, tu teléfono móvil):




Una vez que el servidor esté en funcionamiento, abre tu navegador, crea una cuenta de usuario y comienza a probar las funcionalidades del sistema.

Documentación de la API
========================

La API del sistema está construida sobre Flask y expone varios puntos de entrada para interactuar con los datos. Aquí se documentan las principales funcionalidades.

Cómo funciona la API
---------------------

.. automodule:: app
   :members:
   :undoc-members:
   :show-inheritance:

Clases y Modelos
================

El proyecto está compuesto por varios modelos que representan las entidades principales del sistema. Aquí se detallan las clases y sus métodos.

### Usuario

.. automodule:: models.ModelUser
   :members:
   :undoc-members:
   :show-inheritance:

### Entidad de Usuario

.. automodule:: models.entities.user
   :members:
   :undoc-members:
   :show-inheritance:

### Registro de Usuario

.. automodule:: models.register
   :members:
   :undoc-members:
   :show-inheritance:

### Categorías

.. automodule:: models.categorias
   :members:
   :undoc-members:
   :show-inheritance:

### Productos

.. automodule:: models.producto
   :members:
   :undoc-members:
   :show-inheritance:

### Proveedores

.. automodule:: models.proveedor
   :members:
   :undoc-members:
   :show-inheritance:

### Ventas

.. automodule:: models.ventas
   :members:
   :undoc-members:
   :show-inheritance:

### Últimas Ventas

.. automodule:: models.ultimas_ventas
   :members:
   :undoc-members:
   :show-inheritance:

### Pagos

.. automodule:: models.pagos
   :members:
   :undoc-members:
   :show-inheritance:

### Clientes

.. automodule:: models.cliente
   :members:
   :undoc-members:
   :show-inheritance:
