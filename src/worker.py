
import logging
from datetime import datetime, timezone

from src.database import get_connection
from src.renderer import render_email
from src.email_service import send_email
from src.config import LOG_DIR

logging.basicConfig(
    filename=LOG_DIR / "email_activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_due_reminders():

    now = datetime.now(timezone.utc)

    with get_connection() as conn:

        reminders = conn.execute("""
            SELECT * FROM reminders
            WHERE status = 'scheduled'
            AND scheduled_at <= ?
            ORDER BY scheduled_at
        """, (now.isoformat(),)).fetchall()

        for reminder in reminders:

            reminder_id = reminder["id"]

            try:

                subject, html = render_email(
                    reminder["name"],
                    reminder["title"]
                )

                result = send_email(
                    reminder["email"],
                    subject,
                    html
                )

                if result["success"]:

                    status = result["mode"]

                    conn.execute("""
                        UPDATE reminders
                        SET status = ?
                        WHERE id = ?
                    """, (status, reminder_id))

                    conn.execute("""
                        INSERT INTO messages
                        (reminder_id, recipient, subject,
                         status, sent_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        reminder_id,
                        reminder["email"],
                        subject,
                        status,
                        now.isoformat()
                    ))

                    logging.info(
                        "Reminder %s processed: %s",
                        reminder_id,
                        status
                    )

                else:

                    error = result["error"] or "Unknown sending error"

                    conn.execute("""
                        UPDATE reminders
                        SET status = 'failed',
                            last_error = ?
                        WHERE id = ?
                    """, (error, reminder_id))

                    conn.execute("""
                        INSERT INTO messages
                        (reminder_id, recipient, subject,
                         status, sent_at, error)
                        VALUES (?, ?, ?, 'failed', ?, ?)
                    """, (
                        reminder_id,
                        reminder["email"],
                        subject,
                        now.isoformat(),
                        error
                    ))

                    logging.error(
                        "Reminder %s failed: %s",
                        reminder_id,
                        error
                    )

            except Exception as exc:

                error = str(exc)

                conn.execute("""
                    UPDATE reminders
                    SET status = 'failed',
                        last_error = ?
                    WHERE id = ?
                """, (error, reminder_id))

                logging.exception(
                    "Error processing reminder %s",
                    reminder_id
                )

        conn.commit()

    return len(reminders)
