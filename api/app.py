
import csv
import uuid

from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import text

from src.database import get_connection
from src.config import CONTACTS_PATH, REMINDERS_PATH, OUTPUT_DIR
from src.worker import process_due_reminders
from src.scheduler import start_scheduler, stop_scheduler


app = FastAPI(
    title="Email Automation & Reminder System",
    description="Automated email and reminder management API",
    version="1.0.0"
)


class Contact(BaseModel):
    name: str
    email: EmailStr
    company: str = "Demo Company"


class Reminder(BaseModel):
    name: str
    email: EmailStr
    title: str
    scheduled_at: datetime
    repeat: str = "none"


@app.on_event("startup")
def startup():
    from src.database import initialize_database
    initialize_database()
    start_scheduler()


@app.on_event("shutdown")
def shutdown():
    stop_scheduler()


@app.get("/")
def home():
    return {
        "project": "Email Automation & Reminder System",
        "status": "running",
        "mode": "simulation by default"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/contacts")
def create_contact(contact: Contact):

    try:
        with get_connection() as conn:

            cursor = conn.execute("""
                INSERT INTO contacts(name, email, company)
                VALUES (?, ?, ?)
            """, (
                contact.name,
                str(contact.email),
                contact.company
            ))

            conn.commit()

            return {
                "id": cursor.lastrowid,
                "message": "Contact created"
            }

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/contacts")
def get_contacts():

    with get_connection() as conn:

        rows = conn.execute(
            "SELECT * FROM contacts ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]


@app.post("/reminders")
def create_reminder(reminder: Reminder):

    scheduled = reminder.scheduled_at

    if scheduled.tzinfo is None:
        scheduled = scheduled.replace(tzinfo=timezone.utc)

    scheduled = scheduled.astimezone(timezone.utc)

    if scheduled <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Scheduled time must be in the future"
        )

    if reminder.repeat not in ("none", "daily", "weekly"):
        raise HTTPException(
            status_code=400,
            detail="Repeat must be none, daily, or weekly"
        )

    with get_connection() as conn:

        cursor = conn.execute("""
            INSERT INTO reminders
            (name, email, title, scheduled_at, repeat)
            VALUES (?, ?, ?, ?, ?)
        """, (
            reminder.name,
            str(reminder.email),
            reminder.title,
            scheduled.isoformat(),
            reminder.repeat
        ))

        conn.commit()

        return {
            "id": cursor.lastrowid,
            "message": "Reminder scheduled",
            "scheduled_at": scheduled.isoformat()
        }


@app.get("/reminders")
def get_reminders():

    with get_connection() as conn:

        rows = conn.execute(
            "SELECT * FROM reminders ORDER BY scheduled_at"
        ).fetchall()

        return [dict(row) for row in rows]


@app.post("/import/contacts")
def import_contacts():

    if not CONTACTS_PATH.exists():
        raise HTTPException(404, "contacts.csv not found")

    count = 0

    with get_connection() as conn:

        with open(
            CONTACTS_PATH,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO contacts
                        (name, email, company)
                        VALUES (?, ?, ?)
                    """, (
                        row["name"].strip(),
                        row["email"].strip(),
                        row.get("company", "Demo Company").strip()
                    ))

                    count += 1

                except (KeyError, AttributeError):
                    continue

        conn.commit()

    return {"imported_rows": count}


@app.post("/import/reminders")
def import_reminders():

    if not REMINDERS_PATH.exists():
        raise HTTPException(404, "reminders.csv not found")

    count = 0

    with get_connection() as conn:

        with open(
            REMINDERS_PATH,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:
                    scheduled = datetime.fromisoformat(
                        row["scheduled_at"].strip()
                    )

                    if scheduled.tzinfo is None:
                        scheduled = scheduled.replace(
                            tzinfo=timezone.utc
                        )

                    scheduled = scheduled.astimezone(timezone.utc)

                    if scheduled <= datetime.now(timezone.utc):
                        continue

                    conn.execute("""
                        INSERT INTO reminders
                        (name, email, title, scheduled_at, repeat)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        row["name"].strip(),
                        row["email"].strip(),
                        row["title"].strip(),
                        scheduled.isoformat(),
                        row.get("repeat", "none").strip()
                    ))

                    count += 1

                except (ValueError, KeyError):
                    continue

        conn.commit()

    return {"imported_reminders": count}


@app.post("/worker/run")
def run_worker():

    processed = process_due_reminders()

    return {
        "message": "Worker execution completed",
        "processed": processed
    }


@app.get("/messages")
def get_messages():

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT * FROM messages ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]


@app.get("/stats")
def get_stats():

    with get_connection() as conn:

        reminders = conn.execute("""
            SELECT status, COUNT(*) AS total
            FROM reminders GROUP BY status
        """).fetchall()

        messages = conn.execute("""
            SELECT status, COUNT(*) AS total
            FROM messages GROUP BY status
        """).fetchall()

        return {
            "reminders": {
                row["status"]: row["total"]
                for row in reminders
            },
            "messages": {
                row["status"]: row["total"]
                for row in messages
            }
        }


@app.get("/reports/export")
def export_report():

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT
                r.id,
                r.name,
                r.email,
                r.title,
                r.scheduled_at,
                r.status,
                r.last_error,
                m.sent_at
            FROM reminders r
            LEFT JOIN messages m
            ON r.id = m.reminder_id
            ORDER BY r.id
        """).fetchall()

        output_file = OUTPUT_DIR / "email_report.csv"

        if rows:
            import pandas as pd
            pd.DataFrame(
                [dict(row) for row in rows]
            ).to_csv(output_file, index=False)

        else:
            import pandas as pd
            pd.DataFrame(columns=[
                "id", "name", "email", "title",
                "scheduled_at", "status",
                "last_error", "sent_at"
            ]).to_csv(output_file, index=False)

    return {
        "message": "Report generated",
        "file": str(output_file)
    }
