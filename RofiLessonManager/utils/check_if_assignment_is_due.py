import datetime


def check_if_assignment_is_due(assignment_due_date, assignment_submitted):
    """
    Checks if an assignment is due or not. If it is due, it returns either if
    it' LATE, or if it's due TODAY, TOMORROW, or it returns the number of days
    left until the assignment is due.

    Args:
        assignment_due_date (str): The date the assignment is due.
        assignment_submitted (str): The assignment submitted (True/False).

    Returns:
        str: Returns either:
            - "LATE" if the assignment is late.
            - "TODAY" if the assignment is due today.
            - "TOMORROW" if the assignment is due tomorrow.
            - "Days: X" if the assignment is due in X days.
    """

    now = datetime.datetime.now()
    assignment_date = datetime.datetime.strptime(assignment_due_date,
                                                 '%m-%d-%y')
    logo = ''

    # Check if the assignment is due today
    if now.date() == assignment_date.date():
        logo = ' (TODAY)'
    # Check if the assignment is due tomorrow
    elif now.date() + datetime.timedelta(days=1) == \
            assignment_date.date():
        logo = ' (TOMORROW)'
    # Check if the assignment is due in the past
    elif now.date() > assignment_date.date() and \
            not assignment_submitted:
        logo = ' (LATE)'
    else:
        days = int((assignment_date - now).days) + 1
        logo = ' (DAYS: {})'.format(days)

    assignment_due_date_formatted = '{} {} ({})'.format(
        assignment_date.strftime('%b'),
        assignment_date.strftime('%d'),
        assignment_date.strftime('%a')
    )

    return logo, assignment_due_date_formatted
