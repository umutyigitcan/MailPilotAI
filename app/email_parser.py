import email
import re
from dataclasses import dataclass
from datetime import datetime
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from typing import Optional


@dataclass
class ParsedEmail:
    message_id: str
    subject: str
    sender: str
    recipient: str
    received_at: datetime
    plain_body: str


def decode_mime_header(value: Optional[str]) -> str:
    """
    Decode MIME headers such as encoded subjects or sender names.
    """
    if not value:
        return ""

    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def html_to_text(html: str) -> str:
    """
    Convert basic HTML email content into readable plain text.
    """
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_email_body(message: email.message.Message) -> str:
    """
    Extract the most readable body from an email message.

    Plain text is preferred. If only HTML exists, it is converted into text.
    Attachments are ignored.
    """
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            if "attachment" in disposition.lower():
                continue

            if content_type == "text/plain":
                try:
                    return part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8",
                        errors="ignore",
                    ).strip()
                except Exception:
                    continue

        for part in message.walk():
            if part.get_content_type() == "text/html":
                try:
                    html = part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8",
                        errors="ignore",
                    )
                    return html_to_text(html)
                except Exception:
                    continue

        return ""

    try:
        return message.get_payload(decode=True).decode(
            message.get_content_charset() or "utf-8",
            errors="ignore",
        ).strip()
    except Exception:
        return ""


def parse_email_date(date_header: Optional[str]) -> datetime:
    """
    Convert an email Date header into a datetime object.
    """
    if not date_header:
        return datetime.utcnow()

    try:
        return parsedate_to_datetime(date_header)
    except Exception:
        return datetime.utcnow()
