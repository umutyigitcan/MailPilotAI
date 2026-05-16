from fastapi import FastAPI

from app.config import settings


app = FastAPI(title="MailPilotAI Email Automation API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MailPilotAI",
        "model": settings.openai_model,
    }
