from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json
import re
# from gpt import aiProcess   # Descomente se tiver o módulo GPT

# Criar app FastAPI
app = FastAPI(
    title="Quiz Battle Multiplayer API",
    description="API para gerenciar um jogo de quiz multiplayer.",
    version="0.1.0"
)

# Permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho do frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Servir frontend como estático
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Página inicial -> frontend
@app.get("/")
def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Endpoint de saúde
@app.get("/api/health", tags=["Status"])
def health_check():
    """
    Verifica se o serviço está no ar
    """
    return {"status": "ok"}

# Endpoint de resposta de quiz (exemplo simples)
@app.post("/api/submit-answer")
def submit_answer(question_id: int, answer: str):
    correct = answer.lower() == "b"  # Lógica de exemplo
    points = 10 if correct else 0
    return {"correct": correct, "points": points}

# Endpoint de quiz usando GPT (simulado)
@app.post("/api/quiz")
def quiz(token: str, msg: str):
    regex = r'[\\.\n]'
    request_template_gpt = (
        "Crie para mim um json. Este json deve conter uma pergunta, cinco opções, "
        "sendo uma verdadeira e as demais falsas, a última chave do json, deve conter a resposta correta. "
        "O tema abordado será {}. Essa estrutura de opções, deverá ser de A até E. "
        "Para cada opções, a sua chave deve ser apena 'A', 'B', 'C', 'D' e 'E'. "
        "Por fim, transforme tudo isso em uma string sem quebras de linhas e sem caractéres especiais. "
        "GPT, essa última etapa é a que você deve me devolver em português do Brasil"
    ).format(msg)

    # Simulação de resposta, substitua pelo aiProcess real
    response = {
        "question": "Qual é a capital do Brasil?",
        "A": "São Paulo",
        "B": "Brasília",
        "C": "Rio de Janeiro",
        "D": "Salvador",
        "E": "Belo Horizonte",
        "answer": "B"
    }
    return response
