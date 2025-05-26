def convert_number(n, display=False):
    if not display:
        if int(n) < 10 and len(str(n)) == 2:
            return int(n[1])
        else:
            return int(n)
    else:
        if int(n) < 10 and len(str(n)) == 1:
            return f"0{n}"
        else:
            return str(n)
