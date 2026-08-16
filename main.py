. main.py

"""
AUDMAX IA QUANTUM v9.1 DEPTH - Backend Python
Cérebro Hexagonal 4D - Frontal + Pré-Frontal
Compatível com GitHub + Vercel + Render
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import json, math, os

app = FastAPI(
    title="AUDMAX IA QUANTUM v9.1 DEPTH",
    description="Cérebro Hexagonal 4D - Frontal (assimila) + Pré-Frontal (analisa/aprende/responde) + Guarda + IDA/VOLTA",
    version="9.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CÓRTEX 4D - MESMA LÓGICA DO FRONTEND ===
class Cortex4D:
    def process(self, pergunta: str, hits_count: int = 0, dias: int = 0):
        t = pergunta.lower()
        altura = min(6, max(1, len(t.split())/6 + (2 if hits_count>0 else 0)))
        largura = min(10, max(1, len(set(t.split()))/2))
        comprimento = min(100, dias + 10 + 1)
        profundidade = min(10, max(1, (4 if any(x in t for x in ["como criar","por que","explique","como fazer"]) else 1) + hits_count/5))
        volume = altura * largura * comprimento * profundidade
        
        if profundidade >= 6:
            cognicao = "CRIACAO_DE_SOLUCAO"
        elif profundidade >= 4:
            cognicao = "COMPREENSAO_PROFUNDA"
        elif profundidade >= 2:
            cognicao = "ENTENDIMENTO"
        else:
            cognicao = "BUSCA_SUPERFICIAL"
            
        return {
            "altura": round(altura,1),
            "largura": round(largura,1),
            "comprimento": round(comprimento,1),
            "profundidade": round(profundidade,1),
            "volume": round(volume,1),
            "cognicao": cognicao,
            "frontal": "Assimila pergunta - IDA Chat -> API",
            "pre_frontal": "Analisa / Aprende / Responde - VOLTA com solução",
            "guarda": "Memoria vetorial 4D + 1% dia + Sono",
            "comunicacao": "IDA 22 APIs, VOLTA fusão + ranking"
        }

cortex = Cortex4D()

class Pergunta(BaseModel):
    pergunta: str
    hits: int = 0
    dias_ativo: int = 0

@app.get("/", response_class=HTMLResponse)
def root():
    # Serve o index.html se existir
    if os.path.exists("index.html"):
        with open("index.html","r",encoding="utf-8") as f:
            return f.read()
    return "<h1>AUDMAX v9.1 DEPTH ONLINE - Use /docs para API</h1>"

@app.post("/api/cortex4d/process")
def process_4d(p: Pergunta):
    dim = cortex.process(p.pergunta, p.hits, p.dias_ativo)
    return {
        "pergunta": p.pergunta,
        "dimensoes": dim,
        "entendimento": f"Conceito com volume {dim['volume']} - {dim['cognicao']}",
        "solucao": "Prototipar MVP 4D -> Testar volume -> Iterar com sono -> Escalar 1% dia" if dim["cognicao"]=="CRIACAO_DE_SOLUCAO" else "Aplicar + registrar memoria 4D",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/sinapses")
def get_sinapses():
    if os.path.exists("sinapses.json"):
        with open("sinapses.json","r",encoding="utf-8") as f:
            return json.load(f)
    return {"error": "sinapses.json não encontrado"}

@app.get("/api/health")
def health():
    return {"status":"AUDMAX v9.1 DEPTH ONLINE","cortex":"HEXAGONAL 4D","apis":22,"frontal":"OK","pre_frontal":"OK"}

# Para rodar: uvicorn main:app --reload --port 8000

