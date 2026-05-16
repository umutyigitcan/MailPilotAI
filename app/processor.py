import logging

from sqlalchemy.orm import Session

from app.ai_analyzer import analyze_email
from app.email_client import fetch_unseen_emails
from app.email_parser import ParsedEmail
from app.mail_sender import send_reply
from app.models import StoredEmail


logger = logging.getLogger("mailpilotai.processor")


def save_email_analysis(
    db: Session,
    parsed_email: ParsedEmail,
    analysis: dict,
) -> StoredEmail:
    """
    Store an analyzed email in the database.
    """
    email_row = StoredEmail(
        message_id=parsed_email.message_id,
        subject=parsed_email.subject,
        sender=parsed_email.sender,
        recipient=parsed_email.recipient,
        received_at=parsed_email.received_at,
        body=parsed_email.plain_body,
        summary=analysis["summary"],
        category=analysis["category"],
        action=analysis["action"],
        urgency=analysis["urgency"],
        should_reply=bool(analysis["should_reply"]),
        reply_text=analysis.get("reply_text") or "",
        reply_sent=False,
    )

    db.add(email_row)
    db.commit()
    db.refresh(email_row)

    return email_row


def process_new_emails(db: Session) -> int:
    """
    Run one inbox processing cycle.

    Steps:
    1. Fetch unread emails.
    2. Skip emails that already exist in the database.
    3. Analyze each email with AI.
    4. Store the analysis result.
    5. Send a reply only when the analysis explicitly requires it.
    """
    new_emails = fetch_unseen_emails()
    logger.info("Emails queued for processing: %d", len(new_emails))

    processed_count = 0

    for parsed_email in new_emails:
        existing_email = (
            db.query(StoredEmail)
            .filter_by(message_id=parsed_email.message_id)
            .first()
        )

        if existing_email:
            logger.info("Email already exists, skipping: %s", parsed_email.message_id)
            continue

        try:
            analysis = analyze_email(parsed_email.subject, parsed_email.plain_body)
        except Exception as error:
            logger.error(
                "Email analysis failed for %s: %s",
                parsed_email.message_id,
                error,
            )
            continue

        email_row = save_email_analysis(db, parsed_email, analysis)
        processed_count += 1

        if email_row.should_reply and email_row.reply_text:
            try:
                send_reply(parsed_email, email_row.reply_text)

                email_row.reply_sent = True
                db.add(email_row)
                db.commit()

                logger.info("Reply sent for email: %s", parsed_email.message_id)

            except Exception as error:
                db.rollback()
                logger.error(
                    "Reply sending failed for %s: %s",
                    parsed_email.message_id,
                    error,
                )

    return processed_count
