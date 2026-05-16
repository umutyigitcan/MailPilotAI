from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app import models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="MailPilotAI Email Automation API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MailPilotAI",
        "model": settings.openai_model,
    }
