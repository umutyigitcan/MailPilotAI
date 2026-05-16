import email
import imaplib
import logging
from typing import List

from app.config import settings
from app.email_parser import (
    ParsedEmail,
    decode_mime_header,
    extract_email_body,
    parse_email_date,
)


logger = logging.getLogger("mailpilotai.email_client")


def fetch_unseen_emails() -> List[ParsedEmail]:
    """
    Connect to the configured inbox and fetch unread email messages.

    Only unseen messages are fetched. Duplicate protection is handled later
    at the database layer using the Message-ID header.
    """
    settings.validate_required_settings()

    logger.info("Connecting to IMAP server: %s", settings.imap_host)

    mailbox = imaplib.IMAP4_SSL(settings.imap_host, settings.imap_port)

    try:
        mailbox.login(settings.email_address, settings.email_password)
        mailbox.select("INBOX")

        status, data = mailbox.search(None, "UNSEEN")

        if status != "OK":
            logger.error("IMAP search failed with status: %s", status)
            return []

        email_ids = data[0].split()
        logger.info("Unseen emails found: %d", len(email_ids))

        parsed_emails: List[ParsedEmail] = []

        for email_id in email_ids:
            status, message_data = mailbox.fetch(email_id, "(RFC822)")

            if status != "OK":
                logger.warning("Could not fetch email id: %s", email_id)
                continue

            raw_email = message_data[0][1]
            message = email.message_from_bytes(raw_email)

            message_id = message.get("Message-ID") or f"<local-id-{email_id.decode()}>"
            subject = decode_mime_header(message.get("Subject", ""))
            sender = decode_mime_header(message.get("From", ""))
            recipient = decode_mime_header(message.get("To", ""))
            received_at = parse_email_date(message.get("Date"))
            body = extract_email_body(message)

            parsed_emails.append(
                ParsedEmail(
                    message_id=message_id,
                    subject=subject,
                    sender=sender,
                    recipient=recipient,
                    received_at=received_at,
                    plain_body=body,
                )
            )

        return parsed_emails

    finally:
        mailbox.logout()
