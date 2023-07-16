def filename_to_number(s):
    n = (
        s.replace("lec-", "")
        .replace("chap-", "")
        .replace(".yaml", "")
        .replace(".tex", "")
        .replace(".pdf", "")
        .replace(".bib", "")
        .replace(".png", "")
    )

    if int(n) < 10 and len(str(n)) == 1:
        return str(f"0{n}")
    return str(n)
