from datetime import date
from datetime import datetime


def get_current_date():
    """ Get current date.

    Returns:
        current_date (date): Current date.
        current_time (datetime): Current time.
    """
    today = date.today()
    now = datetime.now()

    current_date = today.strftime('%b %d %Y %a')
    current_time = now.strftime('(%H:%M:%S)')

    return current_date, current_time
