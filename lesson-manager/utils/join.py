def join(*args, separator=" "):
    return separator.join(str(e) for e in args if e)
