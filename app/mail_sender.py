import logging
import smtplib
from email.message import EmailMessage as OutgoingEmail
from email.utils import formataddr

from app.config import settings
from app.email_parser import ParsedEmail


logger = logging.getLogger("mailpilotai.mail_sender")


def send_reply(original_email: ParsedEmail, reply_text: str) -> None:
    """
    Send a reply to the original sender using the configured SMTP server.
    """
    settings.validate_required_settings()

    logger.info("Sending reply to: %s", original_email.sender)

    outgoing = OutgoingEmail()

    original_subject = original_email.subject or ""
    outgoing["Subject"] = (
        original_subject
        if original_subject.lower().startswith("re:")
        else f"Re: {original_subject}"
    )

    outgoing["From"] = formataddr(("MailPilotAI", settings.email_address))
    outgoing["To"] = original_email.sender
    outgoing.set_content(reply_text)

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.login(settings.email_address, settings.email_password)
        smtp.send_message(outgoing)
