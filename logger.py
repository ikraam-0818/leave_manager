# logger.py

from datetime import datetime
from config import LOG_FILE

def log_action(user, action, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {user}: {action} | {details}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
