import math


def format_date_and_time(begin, end):
    minutes = math.ceil((end - begin).seconds / 60)

    if minutes == 1:
        return "1 minute"

    if minutes < 60:
        return f"{minutes} minutes"

    hours = math.floor(minutes / 60)
    rest_minutes = minutes % 60

    if hours == 1 and rest_minutes == 0:
        return "1 hour"
    elif hours == 1:
        return f"1 hour {rest_minutes} min"
    elif rest_minutes == 0:
        return f"{hours} hours"
    elif hours > 5:
        return f"{hours} hours"

    return f"{hours} hr {rest_minutes:02d} min"
