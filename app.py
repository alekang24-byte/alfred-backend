import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="Alfred - Cérebro Back-end")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEMORY_FILE = "alfred_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"user_profile": {}, "notes": []}
    return {"user_profile": {}, "notes": []}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "online", "name": "Alfred Backend"}

@app.post("/chat")
def chat(req: ChatRequest):
    user_msg = req.message.strip()
    memory = load_memory()
    
    if "lembre-se" in user_msg.lower() or "guarde" in user_msg.lower():
        memory["notes"].append(user_msg)
        save_memory(memory)
        return {
            "response": f"Compreendido, patrão. Guardei esta informação na minha memória permanente: '{user_msg}'"
        }
    
    if "o que você sabe" in user_msg.lower() or "memória" in user_msg.lower():
        notes_text = ", ".join(memory["notes"]) if memory["notes"] else "Nenhum registro específico salvo ainda."
        return {
            "response": f"Aqui está o que tenho registrado na minha memória, patrão: {notes_text}"
        }

    return {
        "response": f"Às suas ordens, patrão. Recebi a mensagem: '{user_msg}'. Como posso ajudar mais?"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
