# Email Automation & Reminder System

**A Python-based email automation and reminder management application built with FastAPI, SQLite, APScheduler, Jinja2, and Next.js.**

## Project Overview

Email Automation & Reminder System automates repetitive email communication and scheduled reminders.

The application allows users to manage contacts, create personalized email reminders, schedule notifications, monitor processing status, and generate CSV reports.

It includes a Python backend, REST API, automated scheduler, email worker, and a modern web dashboard.

## Problem Statement

Organizations frequently send repetitive emails for meetings, assignments, payments, interviews, training sessions, and customer follow-ups.

Manual communication requires time and can lead to missed reminders.

This project demonstrates how Python automation can reduce repetitive work and improve communication management.

## Key Features

- Contact management
- CSV contact import
- CSV reminder import
- Personalized HTML email templates
- Scheduled reminders
- FastAPI REST endpoints
- SQLite database
- Automatic background scheduler
- SMTP integration
- Safe email simulation mode
- Email status tracking
- Error logging
- CSV report generation
- Next.js dashboard

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| FastAPI | Backend API |
| SQLite | Database |
| SQLAlchemy | Database toolkit |
| Pandas | CSV reporting |
| APScheduler | Background scheduling |
| Jinja2 | Email personalization |
| smtplib | Email sending |
| HTML/CSS | Email templates |
| Next.js | Frontend dashboard |
| Tailwind CSS | UI styling |
| Git/GitHub | Version control |

## Project Structure

```text
Email-Automation-Reminder-System/
├── api/
│   └── app.py
├── data/
│   ├── contacts.csv
│   └── reminders.csv
├── templates/
│   └── reminder.html
├── src/
│   ├── config.py
│   ├── database.py
│   ├── renderer.py
│   ├── email_service.py
│   ├── scheduler.py
│   └── worker.py
├── apps/
│   └── web/
├── outputs/
├── logs/
├── images/
├── docs/
├── tests/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Email-Automation-Reminder-System.git
cd Email-Automation-Reminder-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example`.

Default configuration:

```env
EMAIL_MODE=simulation
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=
SMTP_PASS=
```

Simulation mode is enabled by default.

### 5. Run the backend

```bash
python main.py
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the frontend

```bash
cd apps/web
npm install
npm run dev
```

Dashboard:

```text
http://localhost:3000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Application information |
| GET | /health | Health check |
| POST | /contacts | Create contact |
| GET | /contacts | List contacts |
| POST | /reminders | Create reminder |
| GET | /reminders | List reminders |
| POST | /import/contacts | Import contacts CSV |
| POST | /import/reminders | Import reminders CSV |
| POST | /worker/run | Process due reminders |
| GET | /messages | Message history |
| GET | /stats | System statistics |
| GET | /reports/export | Generate CSV report |

## Email Simulation

The application supports local simulation without sending actual emails.

Simulation mode displays the recipient and subject and records a simulated processing result.

Actual SMTP sending can be configured using Gmail App Passwords.

## Sample Output

```text
[SIMULATION] Email prepared
To: rahul@example.com
Subject: Reminder: Project Meeting
```

## Reports and Logs

Generated files:

- `outputs/email_report.csv`
- `logs/email_activity.log`
- `data/email_system.db`

The report records recipients, reminder titles, scheduled timestamps, statuses, and errors.

## Industry Relevance

Potential applications include:

- HR interview reminders
- Employee onboarding notifications
- Educational class reminders
- Payment follow-ups
- Sales communication
- Meeting notifications
- Customer support follow-ups

## Future Improvements

- Recurring reminder execution
- Retry queues
- Duplicate-send protection
- Contact unsubscribe management
- Campaign management
- Email attachments
- PostgreSQL integration
- Email analytics
- Role-based authentication
- Docker deployment
- Cloud hosting

## Learning Outcomes

Through this project, I practiced:

- Python application development
- REST API development
- Database integration
- CSV data processing
- Email automation
- Scheduling background jobs
- Template rendering
- Error handling and logging
- Frontend/backend integration
- Git and GitHub version control

## Author

**ER.CHAND KUJRA**

GitHub: https://github.com/erchandkujra-ai

---

*Built as a practical Python automation and software development portfolio project.*