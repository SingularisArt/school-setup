#!/usr/bin/env python3


from datetime import datetime


def get_week(d=datetime.today()) -> int:
    return (int(d.strftime("%W")) + 52 - 5) % 52
