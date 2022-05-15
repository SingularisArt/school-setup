#!/usr/bin/env python3

"""
Function check_if_assignment_is_due:
    - RofiLessonManager.utils.check_if_assignment_is_due

    Checks if an assignment is due or not. If it is due, it returns either if
    it' LATE, or if it's due TODAY, TOMORROW, or it returns the number of days
    left until the assignment is due.

    Args:
        - assignment_due_date (str): The date the assignment is due.
        - assignment_submitted (str): The assignment submitted (True/False).

    Returns:
        - str: Returns either:
            - "LATE" if the assignment is late.
            - "TODAY" if the assignment is due today.
            - "TOMORROW" if the assignment is due tomorrow.
            - "Days: X" if the assignment is due in X days.
"""

import datetime


def check_if_assignment_is_due(assignment_due_date, assignment_submitted):
    """
    Checks if an assignment is due or not. If it is due, it returns either if
    it' LATE, or if it's due TODAY, TOMORROW, or it returns the number of days
    left until the assignment is due.

    Args:
        - assignment_due_date (str): The date the assignment is due.
        - assignment_submitted (str): The assignment submitted (True/False).

    Returns:
        - str: Returns either:
            - "LATE" if the assignment is late.
            - "TODAY" if the assignment is due today.
            - "TOMORROW" if the assignment is due tomorrow.
            - "Days: X" if the assignment is due in X days.
    """

    now = datetime.datetime.now()
    assignment_date = datetime.datetime.strptime(assignment_due_date,
                                                 '%m-%d-%y')
    logo = ''
    late = True

    # Check if the assignment is due today
    if now.date() == assignment_date.date():
        logo = ' (TODAY)'
        late = True
    # Check if the assignment is due tomorrow
    elif now.date() + datetime.timedelta(days=1) == \
            assignment_date.date():
        logo = ' (TOMORROW)'
        late = True
    # Check if the assignment is due in the past
    elif now.date() > assignment_date.date() and \
            not assignment_submitted:
        days = abs(int((assignment_date - now).days) + 1)
        logo = ' ({} DAYS LATE)'.format(days)
        late = True
    else:
        days = int((assignment_date - now).days) + 1
        logo = ' ({} DAYS LEFT)'.format(days)
        late = False

    assignment_due_date_formatted = '{} {} ({})'.format(
        assignment_date.strftime('%b'),
        assignment_date.strftime('%d'),
        assignment_date.strftime('%a')
    )

    return logo, assignment_due_date_formatted, late
