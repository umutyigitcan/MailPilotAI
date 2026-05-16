from fastapi import FastAPI

app = FastAPI(title="MailPilotAI Email Automation API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MailPilotAI",
    }
