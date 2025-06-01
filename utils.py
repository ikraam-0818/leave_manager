from datetime import datetime
import dateparser

def is_valid_date(date_str):
    """Check if a string is a valid YYYY-MM-DD date."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def parse_natural_date(date_str):
    """Convert natural language date to YYYY-MM-DD string."""
    parsed_date = dateparser.parse(date_str)
    if parsed_date:
        return parsed_date.strftime('%Y-%m-%d')
    return None
