from datetime import datetime, timezone, timedelta

# IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    """Get current datetime in IST"""
    return datetime.now(IST)

def format_datetime_for_response(dt):
    """Format datetime for API response"""
    if isinstance(dt, str):
        # If it's already a string, try to parse it first
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt
    
    # Convert to IST if it's not already
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)
    elif dt.tzinfo != IST:
        dt = dt.astimezone(IST)
    
    return dt.strftime('%Y-%m-%d %H:%M:%S IST')

def parse_datetime_string(date_string):
    """Parse datetime string and convert to IST"""
    try:
        # Try to parse ISO format
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.astimezone(IST)
    except:
        try:
            # Try to parse without timezone info and assume IST
            dt = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            return dt.replace(tzinfo=IST)
        except:
            raise ValueError(f"Unable to parse datetime: {date_string}")