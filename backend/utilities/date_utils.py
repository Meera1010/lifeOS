"""
LifeOS Date Arithmetic & Period Range Utilities
"""

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def parse_date_string(date_str: str) -> date:
    """Parses YYYY-MM-DD string into Python date object."""
    if not date_str:
        return date.today()
    if isinstance(date_str, (date, datetime)):
        return date_str if isinstance(date_str, date) else date_str.date()
    try:
        return datetime.strptime(date_str.split("T")[0], "%Y-%m-%d").date()
    except ValueError:
        return date.today()

def parse_datetime_string(dt_str: str) -> datetime:
    """Parses ISO or standard datetime string into Python datetime object."""
    if not dt_str:
        return datetime.utcnow()
    if isinstance(dt_str, datetime):
        return dt_str
    try:
        dt_str = dt_str.replace("Z", "")
        if "T" in dt_str:
            return datetime.fromisoformat(dt_str)
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d")
        except ValueError:
            return datetime.utcnow()

def get_day_start_end(target_date: date) -> tuple:
    """Returns datetime range for start (00:00:00) and end (23:59:59) of a given date."""
    start = datetime.combine(target_date, datetime.min.time())
    end = datetime.combine(target_date, datetime.max.time())
    return start, end

def get_week_range(target_date: date = None) -> tuple:
    """Returns start (Monday) and end (Sunday) of the week for a target date."""
    target_date = target_date or date.today()
    start_week = target_date - timedelta(days=target_date.weekday())
    end_week = start_week + timedelta(days=6)
    return start_week, end_week

def get_month_range(year: int = None, month: int = None) -> tuple:
    """Returns start and end dates for a specific month/year."""
    today = date.today()
    year = year or today.year
    month = month or today.month
    start_month = date(year, month, 1)
    next_month = start_month + relativedelta(months=1)
    end_month = next_month - timedelta(days=1)
    return start_month, end_month

def get_last_n_days(n: int = 7) -> list:
    """Returns list of last N date objects up to today inclusive."""
    today = date.today()
    return [today - timedelta(days=i) for i in reversed(range(n))]

def format_date_human(d: date) -> str:
    """Formats date in human readable style e.g. Mon, Aug 29, 2026."""
    if not d:
        return ""
    return d.strftime("%a, %b %d, %Y")
