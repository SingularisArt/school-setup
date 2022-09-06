#!/usr/bin/env python3


import datetime


def check_if_assignment_is_due(
    assignment_due_date: str, assignment_submitted: bool
) -> tuple:
    """
    Checks if an assignment is due or not. If it is due, it returns either if
    it' LATE, or if it's due TODAY, TOMORROW, or it returns the number of days
    left until the assignment is due.

    Args:
        assignment_due_date (str): The date the assignment is due.
        assignment_submitted (str): The assignment submitted (True/False).

    Returns:
        str: Returns either:
            "X DAYS LATE" if the assignment is late.
            "YESTERDAY" if the assignment was due yesterday.
            "TODAY" if the assignment is due today.
            "TOMORROW" if the assignment is due tomorrow.
            "X DAYS LEFT" if the assignment is due in X days.

    Example:
        check_if_assignment_is_due("09-10-22", False) -> (
            " (6 DAYS LEFT)", "Sep 10 (Sat)", False)
        )
        check_if_assignment_is_due("08-10-22", False) -> (
            " (25 DAYS LATE)", "Aug 10 (Wed)", True)
        )
    """

    now = datetime.datetime.now()
    assignment_date = datetime.datetime.strptime(
        assignment_due_date, "%m-%d-%y")
    logo = ""
    late = True

    # Check if the assignment is due today
    if now.date() == assignment_date.date():
        logo = " (TODAY)"
        late = True
    # Check if the assignment is due tomorrow
    elif now.date() + datetime.timedelta(days=1) == assignment_date.date():
        logo = " (TOMORROW)"
        late = True
    # Check if the assignment was due in the past
    elif now.date() > assignment_date.date() and not assignment_submitted:
        days = abs(int((assignment_date - now).days) + 1)
        late = True

        # Check if the assignment was due yesterday
        if days == 1:
            logo = " (YESTERDAY)"
        else:
            logo = " ({} DAYS LATE)".format(days)
    # The assignment is due in the future
    else:
        days = int((assignment_date - now).days) + 1
        logo = " ({} DAYS LEFT)".format(days)
        late = False

    # Format the assignment
    assignment_due_date_formatted = "{} {} ({})".format(
        assignment_date.strftime("%b"),
        assignment_date.strftime("%d"),
        assignment_date.strftime("%a"),
    )

    return logo, assignment_due_date_formatted, late
