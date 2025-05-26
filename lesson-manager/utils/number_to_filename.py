def number_to_filename(n, lec_or_chap):
    if n < 10:
        n = f"0{n}"
    else:
        n = n

    return f"{lec_or_chap}-{n}.tex"
