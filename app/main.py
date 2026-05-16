from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app.models import StoredEmail
from app.processor import process_new_emails
from app import models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="MailPilotAI Email Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MailPilotAI",
        "model": settings.openai_model,
    }


@app.post("/process-cycle")
def process_cycle(db: Session = Depends(get_db)):
    """
    Manually trigger one inbox processing cycle.
    """
    processed_count = process_new_emails(db)

    return {
        "status": "ok",
        "processed": processed_count,
    }


@app.get("/emails")
def list_emails(
    db: Session = Depends(get_db),
    limit: int = 50,
):
    emails = (
        db.query(StoredEmail)
        .order_by(StoredEmail.received_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": item.id,
            "subject": item.subject,
            "sender": item.sender,
            "received_at": item.received_at,
            "summary": item.summary,
            "category": item.category,
            "action": item.action,
            "urgency": item.urgency,
            "should_reply": item.should_reply,
            "reply_sent": item.reply_sent,
        }
        for item in emails
    ]


@app.get("/emails/{email_id}")
def get_email(
    email_id: int,
    db: Session = Depends(get_db),
):
    email_row = db.query(StoredEmail).filter_by(id=email_id).first()

    if not email_row:
        raise HTTPException(status_code=404, detail="Email not found")

    return {
        "id": email_row.id,
        "message_id": email_row.message_id,
        "subject": email_row.subject,
        "sender": email_row.sender,
        "recipient": email_row.recipient,
        "received_at": email_row.received_at,
        "body": email_row.body,
        "summary": email_row.summary,
        "category": email_row.category,
        "action": email_row.action,
        "urgency": email_row.urgency,
        "should_reply": email_row.should_reply,
        "reply_sent": email_row.reply_sent,
        "reply_text": email_row.reply_text,
    }
