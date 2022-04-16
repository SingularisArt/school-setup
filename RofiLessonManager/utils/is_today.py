def is_today(assignment_due_date):
    import datetime
    today = datetime.date.today()
    return assignment_due_date == today
