#!/usr/bin/env python3

import datetime


def format_time(time: datetime.datetime, format="%I:%M %p"):
    return time.strftime(format)
