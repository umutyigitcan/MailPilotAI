import json

from openai import OpenAI

from app.config import settings


ANALYSIS_SYSTEM_PROMPT = """
You are MailPilotAI, an email triage assistant.

Your job is to classify incoming emails, summarize them, decide whether a
reply is needed, and draft a short professional reply when appropriate.

Return only valid JSON. Do not include markdown, comments, or extra text.
"""


ANALYSIS_USER_TEMPLATE = """
Analyze this email and return a JSON object with exactly these keys:

category: one of ["sales", "support", "invoice", "personal", "newsletter", "spam", "other"]
urgency: one of ["low", "medium", "high", "critical"]
action: one of ["reply", "ignore", "forward", "create_task"]
should_reply: boolean
summary: short 1-2 sentence English summary
reply_text: if should_reply is true, write a short professional reply. Otherwise return an empty string.

Subject:
{subject}

Body:
{body}
"""


def get_openai_client() -> OpenAI:
    settings.validate_required_settings()
    return OpenAI(api_key=settings.openai_api_key)


def parse_llm_json(raw_text: str) -> dict:
    """
    Parse a model response as JSON.

    The prompt asks for strict JSON, but this fallback makes the parser more
    tolerant when the model returns extra text around the JSON object.
    """
    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise

        return json.loads(raw_text[start : end + 1])


def validate_analysis_payload(data: dict) -> None:
    required_keys = [
        "category",
        "urgency",
        "action",
        "should_reply",
        "summary",
        "reply_text",
    ]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing key in analysis result: {key}")


def analyze_email(subject: str, body: str) -> dict:
    """
    Analyze an email and return a structured triage result.
    """
    client = get_openai_client()

    prompt = ANALYSIS_USER_TEMPLATE.format(
        subject=subject,
        body=body[:6000],
    )

    response = client.responses.create(
        model=settings.openai_model,
        instructions=ANALYSIS_SYSTEM_PROMPT,
        input=prompt,
    )

    analysis = parse_llm_json(response.output_text)
    validate_analysis_payload(analysis)

    return analysis
