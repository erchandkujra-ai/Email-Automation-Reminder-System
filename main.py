
import uvicorn
from src.database import initialize_database

if __name__ == "__main__":

    initialize_database()

    print("=" * 55)
    print(" EMAIL AUTOMATION & REMINDER SYSTEM")
    print("=" * 55)
    print("Database initialized.")
    print("Starting FastAPI server...")
    print("Email mode: Simulation by default")
    print("Dashboard API: http://127.0.0.1:8000")
    print("API documentation: http://127.0.0.1:8000/docs")
    print("=" * 55)

    uvicorn.run(
        "api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
