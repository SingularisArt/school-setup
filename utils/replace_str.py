def replace_str(string, *args):
    for arg in args:
        string = string.replace(arg[0], arg[1])

    return string
