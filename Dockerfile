# Usa la imagen oficial de Python 3.11 como base
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido del directorio actual al directorio /app en el contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar tu bot de Telegram (reemplaza 'bot.py' por el nombre de tu archivo principal)
CMD ["python", "bot.py"]
