# MailPilotAI

MailPilotAI is an AI-powered email triage and auto-reply assistant built with FastAPI, OpenAI, IMAP, SMTP, and SQLAlchemy.

The system reads unread inbox messages, extracts clean email content, analyzes each message with AI, stores the result in a database, and can send professional replies when a response is needed.

## Features

- Read unread emails through IMAP
- Extract plain text from email messages
- Decode MIME email headers
- Convert basic HTML email bodies into readable text
- Analyze emails with OpenAI
- Classify email category and urgency
- Decide the required action for each email
- Generate professional reply drafts
- Store analyzed emails with SQLAlchemy
- Send replies through SMTP
- Expose API endpoints with FastAPI

## Tech Stack

- Python
- FastAPI
- OpenAI API
- SQLAlchemy
- SQLite
- IMAP
- SMTP
- Uvicorn

## Project Structure

mailpilotai/
  app/
    __init__.py
    main.py
    config.py
    database.py
    models.py
    email_parser.py
    email_client.py
    ai_analyzer.py
    mail_sender.py
    processor.py
  .env.example
  .gitignore
  requirements.txt
  README.md

## Setup

Clone the repository:

git clone https://github.com/umutyigitcan/MailPilotAI.git
cd MailPilotAI

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

cp .env.example .env

Fill in the required environment variables:

OPENAI_API_KEY=
EMAIL_ADDRESS=
EMAIL_PASSWORD=
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
DATABASE_URL=sqlite:///./mailpilotai.db
OPENAI_MODEL=gpt-4o-mini

## Running the API

Start the FastAPI server:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

GET /health

Returns the API status.

POST /process-cycle

Reads unread emails, analyzes them, stores the results, and sends replies when required.

GET /emails

Returns analyzed email records.

GET /emails/{email_id}

Returns full details for a stored email analysis.

## Email Account Notes

For Gmail, an app password is usually required instead of the normal account password.

The email account must allow IMAP access.

## Security Notes

Do not commit real secrets, passwords, API keys, or .env files.

This project uses .env.example only as a configuration template.

## Status

MailPilotAI is currently under development.
