import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Centralized runtime settings for MailPilotAI.

    Sensitive values are loaded from environment variables instead of being
    hardcoded into the source code.
    """

    def __init__(self) -> None:
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        self.imap_host = os.getenv("IMAP_HOST", "imap.gmail.com")
        self.imap_port = int(os.getenv("IMAP_PORT", "993"))

        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "465"))

        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")

        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./mailpilotai.db")

    def validate_required_settings(self) -> None:
        if not self.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing.")

        if not self.email_address or not self.email_password:
            raise RuntimeError("EMAIL_ADDRESS or EMAIL_PASSWORD is missing.")


settings = Settings()
