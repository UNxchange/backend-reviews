# Dockerfile para el microservicio de Reviews
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./app ./app

# Exponer el puerto de la aplicación
EXPOSE 8003

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
