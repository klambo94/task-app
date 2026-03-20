from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="Psinaptic",
    version="0.1.0",
    debug=settings.environment == "dev",
)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}