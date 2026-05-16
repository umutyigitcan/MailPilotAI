# MailPilotAI

MailPilotAI is an AI-powered email triage and auto-reply assistant built with FastAPI, OpenAI, IMAP, SMTP, and SQLAlchemy.

It is designed to read unread inbox messages, analyze their category and urgency, store the analysis results, and prepare professional replies when needed.

## Features

- FastAPI backend service
- Health check endpoint
- Environment-based configuration
- IMAP inbox integration
- AI-powered email analysis
- SMTP reply support
- SQLAlchemy-based email storage

## Tech Stack

- Python
- FastAPI
- OpenAI API
- SQLAlchemy
- IMAP
- SMTP
- SQLite

## Local Development

Install dependencies:

pip install -r requirements.txt

Run the API:

uvicorn app.main:app --reload

Health check:

GET /health

## Environment Variables

Create a `.env` file based on `.env.example`.

Required variables:

OPENAI_API_KEY
EMAIL_ADDRESS
EMAIL_PASSWORD
IMAP_HOST
IMAP_PORT
SMTP_HOST
SMTP_PORT
DATABASE_URL
OPENAI_MODEL

## Status

MailPilotAI is currently under development.
