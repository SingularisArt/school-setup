from datetime import datetime


def get_week(d=datetime.today()):
    return (int(d.strftime('%W')) + 52 - 5) % 52
