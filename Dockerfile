# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo a /src (donde está tu app.py)
WORKDIR /src

# Instala las dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "src/app.py"]
