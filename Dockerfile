# Imagen base ligera de Python
FROM python:3.13-slim

# Directorio de trabajo
WORKDIR /app

# Instalamos las dependencias globales del contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente de la aplicación
COPY . .

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para arrancar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]