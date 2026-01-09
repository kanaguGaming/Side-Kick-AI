from datetime import datetime
from app.db import interactions

def analyze_struggle(student_id: str, current_keystrokes: int):
    # Fetch last interaction
    last_log = interactions.find_one(
        {"student_id": student_id}, 
        sort=[("timestamp", -1)]
    )
    
    if not last_log:
        return False
    # If student has typed > 200 chars without a successful compile or help request
    if current_keystrokes > 200:
        return True
    
    return False