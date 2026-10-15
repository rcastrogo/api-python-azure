# Python Lab: asistente con Azure OpenAI

Aplicación web de chat orientada a consultas de programación en Python. FastAPI sirve la interfaz de `public/` y expone un endpoint que envía el historial de conversación a un deployment de Azure OpenAI. La clave de Azure se mantiene en el backend y no se entrega al navegador.

## Requisitos

- Python 3.13 o posterior para desarrollo local.
- Una cuenta/recurso de Azure OpenAI con un deployment disponible.
- Docker Desktop u otro motor compatible, si se quiere ejecutar en contenedor.

## Configuración

Crea un archivo `.env` en la raíz del proyecto con los datos de tu recurso:

```dotenv
AZURE_OPENAI_ENDPOINT=https://<tu-recurso>.openai.azure.com/
AZURE_OPENAI_KEY=<tu-clave>
AZURE_OPENAI_DEPLOYMENT=<nombre-del-deployment>
```

`AZURE_OPENAI_DEPLOYMENT` debe ser el nombre del deployment de Azure, no necesariamente el nombre de la familia del modelo. No subas `.env` a GitHub ni incluyas credenciales en la imagen de Docker.

## Desarrollo local

En PowerShell, desde la carpeta del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Abre <http://localhost:8000> para usar el chat. La documentación interactiva de FastAPI está en <http://localhost:8000/docs>.

## API

`POST /api/azure` recibe el historial de mensajes y devuelve el contenido de la respuesta del deployment. El parámetro `temperature` es opcional y acepta valores entre `0` y `2` (por defecto, `0.7`).

Ejemplo de cuerpo JSON:

```json
{
  "messages": [
    { "role": "user", "content": "¿Cómo puedo leer un archivo JSON en Python?" }
  ],
  "temperature": 0.1
}
```

Los mensajes usan los roles `system`, `user` o `assistant`. La respuesta tiene esta forma:

```json
{
  "content": "..."
}
```

## Docker

Ejecuta estos comandos desde la raíz del proyecto. El primero construye la imagen; el segundo inicia el contenedor y pasa las variables del archivo `.env` en tiempo de ejecución:

```powershell
docker build -t python-lab .
docker run --rm -p 8000:8000 --env-file .env python-lab
```

Después, abre <http://localhost:8000>. El contenedor escucha en el puerto `8000`; `-p 8000:8000` publica ese puerto en tu equipo. `.dockerignore` evita enviar archivos locales, secretos y entornos virtuales al contexto de construcción.

## Archivos principales

- `main.py`: aplicación FastAPI y conexión con Azure OpenAI.
- `public/index.html`: interfaz del chat.
- `public/js/ai-azure.js`: cliente del navegador para llamar al endpoint.
- `requirements.txt`: dependencias de Python.
- `Dockerfile`: imagen y comando de inicio del contenedor.
- `.env`: configuración local de Azure; no debe versionarse.
