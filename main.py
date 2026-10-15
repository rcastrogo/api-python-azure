import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from openai import AzureOpenAI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


# Cargamos las variables del archivo .env si existe localmente
load_dotenv()

app = FastAPI(title="API Python con Azure OpenAI")
app.mount("/static", StaticFiles(directory="public"), name="static")


DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Inicializamos el cliente de Azure OpenAI con las variables de entorno
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)


class Message(BaseModel):
    role: str
    content: str

class ChatPayload(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)


# 2. Servir el archivo HTML principal en la ruta raíz
@app.get("/", response_class=HTMLResponse)
def read_root():
  with open("public/index.html", "r", encoding="utf-8") as f:
    return f.read()

@app.post("/api/azure")
def consultar_ia(payload: ChatPayload):
    if not os.getenv("AZURE_OPENAI_KEY"):
        raise HTTPException(status_code=500, detail="Faltan las credenciales de Azure OpenAI en el entorno.")
    
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=payload.messages,
            max_tokens=150,
            temperature=payload.temperature
        )        
        return {"content": response.choices[0].message.content}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))