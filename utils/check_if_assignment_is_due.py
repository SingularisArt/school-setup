#!/usr/bin/env python3


import datetime


def check_if_assignment_is_due(
    assignment_due_date: str, assignment_submitted: bool
) -> tuple:
    now = datetime.datetime.now()
    assignment_date = datetime.datetime.strptime(
        assignment_due_date, "%m-%d-%y")
    logo = ""

    if now.date() == assignment_date.date():
        logo = "(TODAY)"
    elif now.date() + datetime.timedelta(days=1) == assignment_date.date():
        logo = "(TOMORROW)"
    elif now.date() > assignment_date.date() and not assignment_submitted:
        days = abs(int((assignment_date - now).days) + 1)

        if days == 1:
            logo = "(YESTERDAY)"
        else:
            logo = "({} DAYS LATE)".format(days)
    else:
        days = int((assignment_date - now).days) + 1
        logo = "({} DAYS LEFT)".format(days)

    assignment_due_date_formatted = "{} {} ({})".format(
        assignment_date.strftime("%b"),
        assignment_date.strftime("%d"),
        assignment_date.strftime("%a"),
    )

    print(logo, assignment_due_date_formatted)
    return logo, assignment_due_date_formatted
