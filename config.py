# config.py

GEMINI_API_KEY = "AIzaSyCc_8Bqf6Inkd2zyrTx20V1mJbBthexAjQ"
MODEL_NAME = "models/gemini-2.0-flash"

LEAVE_TYPES = ["Sick Leave", "Annual Leave", "Maternity Leave", "Paternity Leave"]
DATA_FILE = "data/data.json"
LOG_FILE = "logs/actions.log"

LEAVE_TYPE_ALIASES = {
    "sick": "Sick Leave",
    "sick_leave": "Sick Leave",
    "annual": "Annual Leave",
    "annual_leave": "Annual Leave",
    "maternity": "Maternity Leave",
    "maternity_leave": "Maternity Leave",
    "paternity": "Paternity Leave",
    "paternity_leave": "Paternity Leave"
}

DEFAULT_LEAVE_BALANCE = {
    "Sick Leave": 12,
    "Annual Leave": 18,
    "Maternity Leave": 90,
    "Paternity Leave": 14
}
