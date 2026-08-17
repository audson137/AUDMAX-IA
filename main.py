"""
AUDMAX IA QUANTUM v12
Cérebro Vivo - IDA/VOLTA
Memória + Fusão + 6 Sinapses + Motores Cognitivos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import json
import re


BASE = Path(_file_).resolve().parent
MEMORY_FILE = BASE / "knowledge" / "brain_memory.json"


app = FastAPI(
    title="AUDMAX IA QUANTUM v12",
    description="Cérebro cognitivo IDA/VOLTA com memória persistente",
    version="12.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pergunta(BaseModel):
    pergunta: str
    hits: int = 0
    dias_ativo: int = 0
    fontes: list[dict] = []


class Cortex4D:

    def process(
        self,
        pergunta: str,
        hits_count: int = 0,
        dias: int = 0
    ):

        t = pergunta.lower()

        altura = min(
            6,
            max(
                1,
                len(t.split()) / 6 +
                (2 if hits_count > 0 else 0)
            )
        )

        largura = min(
            10,
            max(
                1,
                len(set(t.split())) / 2
            )
        )

        comprimento = min(
            100,
            dias + 10 + 1
        )

        profundidade = min(
            10,
            max(
                1,
                (
                    4
                    if any(
                        x in t
                        for x in [
                            "como criar",
                            "por que",
                            "explique",
                            "como fazer"
                        ]
                    )
                    else 1
                )
                + hits_count / 5
            )
        )

        volume = (
            altura *
            largura *
            comprimento *
            profundidade
        )

        if profundidade >= 6:
            cog = "CRIACAO_DE_SOLUCAO"
        elif profundidade >= 4:
            cog = "COMPREENSAO_PROFUNDA"
        elif profundidade >= 2:
            cog = "ENTENDIMENTO"
        else:
            cog = "BUSCA_SUPERFICIAL"

        return {
            "altura": round(altura, 1),
            "largura": round(largura, 1),
            "comprimento": round(comprimento, 1),
            "profundidade": round(profundidade, 1),
            "volume": round(volume, 1),
            "cognicao": cog,
            "frontal": "assimila/normaliza",
            "pre_frontal": "analisa/funde/responde",
            "guarda": "memória persistente",
            "comunicacao": "IDA fontes -> VOLTA fusão"
        }


cortex = Cortex4D()


def load_memory():

    if not MEMORY_FILE.exists():

        return {
            "engrams": [],
            "synapses": [],
            "level": 1.959,
            "growth": 9
        }

    try:

        return json.loads(
            MEMORY_FILE.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        return {
            "engrams": [],
            "synapses": [],
            "level": 1.959,
            "growth": 9
        }


def save_memory(memory):

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    MEMORY_FILE.write_text(
        json.dumps(
            memory,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def tokens(text):

    return set(
        re.findall(
            r"[a-zá-ú0-9]{3,}",
            str(text).lower()
        )
    )


def similarity(a, b):

    A = tokens(a)
    B = tokens(b)

    return len(A & B) / max(
        len(A | B),
        1
    )


def synthesize(pergunta, fontes):

    valid = []

    for fonte in fontes:

        if not isinstance(fonte, dict):
            continue

        data = str(
            fonte.get("data", "")
        ).strip()

        if len(data) >= 20:

            valid.append(
                {
                    "source": fonte.get(
                        "source",
                        "fonte"
                    ),
                    "data": data[:3000]
                }
            )

    if not valid:

        return (
            "Nenhuma fonte retornou conteúdo "
            "suficiente para formar conhecimento confiável."
        )

    blocos = []

    for item in valid:

        blocos.append(
            f"[{item['source']}] "
            f"{item['data']}"
        )

    return (
        "FUSÃO COGNITIVA\n"
        f"Pergunta: {pergunta}\n\n"
        +
        "\n\n".join(blocos)
    )


@app.get("/api/health")
def health():

    memory = load_memory()

    return {
        "status": "online",
        "version": "12.0.0",
        "apis": 22,
        "engrams": len(
            memory["engrams"]
        ),
        "synapses": max(
            6,
            len(memory["synapses"])
        ),
        "ida_volta": True
    }


@app.post("/api/cortex4d/process")
def process_4d(p: Pergunta):

    dimensions = cortex.process(
        p.pergunta,
        p.hits,
        p.dias_ativo
    )

    fused = synthesize(
        p.pergunta,
        p.fontes
    )

    return {
        "pergunta": p.pergunta,
        "dimensoes": dimensions,
        "fontes_processadas": len(
            p.fontes
        ),
        "conhecimento_fundido": fused,
        "timestamp":
            datetime.now().isoformat()
    }


@app.post("/api/brain/learn")
def learn(p: Pergunta):

    memory = load_memory()

    fused = synthesize(
        p.pergunta,
        p.fontes
    )

    if fused.startswith(
        "Nenhuma fonte"
    ):

        return {
            "learned": False,
            "reason":
                "sem evidência suficiente"
        }

    engram = {
        "id": datetime.now().timestamp(),
        "concept":
            p.pergunta[:180],
        "data":
            fused[:5000],
        "source":
            "fusão ida/volta",
        "created":
            datetime.now().isoformat(),
        "strength": 65,
        "connections": []
    }

    for other in memory["engrams"]:

        if similarity(
            engram["concept"],
            other.get(
                "concept",
                ""
            )
        ) >= 0.25:

            engram[
                "connections"
            ].append(
                other["id"]
            )

            memory[
                "synapses"
            ].append(
                {
                    "from":
                        engram["id"],
                    "to":
                        other["id"],
                    "weight": 0.5
                }
            )

    memory["engrams"].append(
        engram
    )

    memory["level"] = (
        float(
            memory.get(
                "level",
                1.959
            )
        ) * 1.02
    )

    memory["growth"] = min(
        100,
        int(
            memory.get(
                "growth",
                9
            )
        ) + 1
    )

    memory["synapses"] = (
        memory["synapses"][-10000:]
    )

    save_memory(memory)

    return {
        "learned": True,
        "engram": engram,
        "engrams":
            len(memory["engrams"]),
        "synapses":
            max(
                6,
                len(memory["synapses"])
            )
    }


@app.get("/api/sinapses")
def get_sinapses():

    path = BASE / "sinapses.json"

    if not path.exists():

        return {
            "corticais": 6,
            "entradas": 9,
            "nivel": 1.959,
            "crescimento_hoje": 9
        }

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


@app.get("/")
def root():

    return {
        "name":
            "AUDMAX IA QUANTUM",
        "version":
            "12.0.0",
        "message":
            "Backend online"
    }
