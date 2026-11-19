
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DATABASE_PATH = BASE_DIR / "data" / "email_system.db"

CONTACTS_PATH = BASE_DIR / "data" / "contacts.csv"

REMINDERS_PATH = BASE_DIR / "data" / "reminders.csv"

TEMPLATE_PATH = BASE_DIR / "templates" / "reminder.html"

OUTPUT_DIR = BASE_DIR / "outputs"

LOG_DIR = BASE_DIR / "logs"

EMAIL_MODE = os.getenv("EMAIL_MODE", "simulation").lower()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

for folder in [OUTPUT_DIR, LOG_DIR, DATABASE_PATH.parent]:
    folder.mkdir(parents=True, exist_ok=True)
