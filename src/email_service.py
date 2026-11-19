
import smtplib
from email.message import EmailMessage

from src.config import (
    EMAIL_MODE,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASS
)


def send_email(to_email, subject, html):

    # Safe simulation mode
    if EMAIL_MODE == "simulation":

        print("\n[SIMULATION] Email prepared")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")

        return {
            "success": True,
            "mode": "simulation",
            "error": None
        }

    # Actual SMTP mode
    if EMAIL_MODE != "smtp":
        return {
            "success": False,
            "mode": EMAIL_MODE,
            "error": "Unsupported email mode"
        }

    if not all([SMTP_USER, SMTP_PASS]):
        return {
            "success": False,
            "mode": "smtp",
            "error": "SMTP credentials are missing"
        }

    message = EmailMessage()

    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(
        "Please view this email in an HTML-compatible email client."
    )

    message.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT,
            timeout=20
        ) as server:

            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(message)

        return {
            "success": True,
            "mode": "smtp",
            "error": None
        }

    except Exception as exc:

        return {
            "success": False,
            "mode": "smtp",
            "error": str(exc)
        }
