from fastapi import FastAPI

app = FastAPI(title="Trade AI API", version="0.1.0", description="AI-powered algorithmic trading platform")

@app.get("/")
async def root():
    return {"name": "Trade AI API", "version": "0.1.0", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "trade-ai-api"}

from app.ai.orchestrator import AIOrchestrator

ai_system = AIOrchestrator()

@app.post("/ai/analyze")
async def ai_analyze(data: dict):
    return await ai_system.analyze(data)
