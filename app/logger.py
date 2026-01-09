from datetime import datetime
from app.db import interactions

def log_interaction(student_id: str, request: str, response: str):
    interactions.insert_one({
        "student_id": student_id,
        "request": request,
        "response": response,
        "timestamp": datetime.utcnow()
    })