#!/usr/bin/env python3

def filename2number(s, type='lecture'):
    if type == 'lecture':
        return str(s).replace('lec-', '').replace('.tex', '')
    elif type == 'assignment':
        return s.replace("week-", "").replace(".yaml", "").replace(".tex", "")
