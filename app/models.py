from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class StoredEmail(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    message_id = Column(String(255), unique=True, index=True, nullable=False)
    subject = Column(String(512))
    sender = Column(String(255))
    recipient = Column(String(255))
    received_at = Column(DateTime, index=True)
    body = Column(Text)

    summary = Column(Text)
    category = Column(String(128))
    action = Column(String(128))
    urgency = Column(String(32))

    should_reply = Column(Boolean, default=False)
    reply_sent = Column(Boolean, default=False)
    reply_text = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
