from fastapi import FastAPI, Query
from src.assistente import Assistente
from src.rag_system import buscar_politica, buscar_produto  # função que faz a busca no índice
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

assistente = Assistente()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/buscar")
def buscar(q: str = Query(..., description="Consulta do usuário")):
    resultados = buscar_produto(q)
    return {"resultados": resultados}

@app.get("/politicas")
def politicas(q: str = Query(..., description="Pergunta sobre políticas da loja")):
    resposta = buscar_politica(q)
    return {"resposta": resposta}

@app.get("/assistente")
def conversar(q: str = Query(...)):
    resposta = assistente.responder(q)
    return {"resposta": resposta}