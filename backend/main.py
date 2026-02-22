from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from core.engine import PrimersEngine
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="PrimersGPT", description="Sovereign Intelligence Backend", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = PrimersEngine()

# Phase 5: Auto-Ingest current directory on startup
@app.on_event("startup")
async def startup_event():
    print("Initial Scan: Ingesting local workspace...")
    engine.process("ingest .")

class ChatRequest(BaseModel):
    message: str
    mode: str = "default"

class IngestRequest(BaseModel):
    target: str # e.g. "github"
    params: dict 

@app.get("/")
def read_root():
    return {"system": "PRIMERS GPT", "status": "ONLINE", "version": "2.0.0"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response_obj = engine.process(request.message, mode=request.mode)
    # Convert dataclass to dict for JSON serialization
    return {"response": response_obj.to_dict()}

@app.post("/ingest")
async def ingest_endpoint(request: IngestRequest):
    if request.target == "github":
        username = request.params.get("username")
        if not username:
             raise HTTPException(400, "Username required")
        
        # Route through the core engine process
        response_obj = engine.process(f"learn from github {username}")
        return {"status": "success", "response": response_obj.to_dict()}
    
    return {"status": "error", "message": "Unknown target"}

@app.get("/stats")
async def get_stats():
    # Knowledge stats
    with sqlite3.connect("primers_knowledge.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM repo_analysis")
        knowledge_nodes = cursor.fetchone()[0]
    
    # Simple simulated load for demo, or real if we add psuil
    # For now, let's provide knowledge breadcrumbs
    return {
        "cpu": 12, # Static for now
        "memory": 24, # Static for now
        "knowledge_nodes": knowledge_nodes,
        "uptime": "3h 42m",
        "intelligence_mode": "SYMBOLIC_FALLBACK"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
