import datetime
from typing import Tuple


def check_if_assignment_is_due(
    assignment_due_date,
    assignment_submitted,
):
    now = datetime.datetime.now()
    assignment_date = datetime.datetime.strptime(
        assignment_due_date,
        "%m-%d-%y",
    )
    assignment_due_date_formatted = assignment_date.strftime("%b %d (%a)")
    logo = ""

    if assignment_submitted:
        return "(Submitted)", assignment_due_date_formatted
    elif now.date() == assignment_date.date():
        logo = "(TODAY)"
    elif now.date() + datetime.timedelta(days=1) == assignment_date.date():
        logo = "(TOMORROW)"
    elif now.date() > assignment_date.date() and not assignment_submitted:
        days = abs(int((assignment_date - now).days) + 1)

        if days == 1:
            logo = "(YESTERDAY)"
        else:
            logo = f"({abs(days)} DAYS LATE)"
    else:
        days = int((assignment_date - now).days) + 1
        logo = f"({days} DAYS LEFT)"

    return logo, assignment_due_date_formatted
