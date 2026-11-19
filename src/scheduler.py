
from apscheduler.schedulers.background import BackgroundScheduler
from src.worker import process_due_reminders

scheduler = BackgroundScheduler(timezone="UTC")


def start_scheduler():

    if not scheduler.running:

        scheduler.add_job(
            process_due_reminders,
            trigger="interval",
            seconds=15,
            id="email_reminder_worker",
            replace_existing=True,
            max_instances=1
        )

        scheduler.start()


def stop_scheduler():

    if scheduler.running:
        scheduler.shutdown(wait=False)
