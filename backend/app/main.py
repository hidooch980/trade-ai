from fastapi import FastAPI

app = FastAPI(title="Trade AI API", version="0.1.0", description="AI-powered algorithmic trading platform")

@app.get("/")
async def root():
    return {"name": "Trade AI API", "version": "0.1.0", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "trade-ai-api"}
