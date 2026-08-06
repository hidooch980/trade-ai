from fastapi import FastAPI

app = FastAPI(
    title="Trade-AI Core",
    version="0.1"
)

@app.get("/")
def home():
    return {
        "system": "TRADE-AI",
        "status": "ONLINE",
    "phase": "CORE FOUNDATION"
    }
