import subprocess


def get_input(prompt: str, rofi_args=[]):
    args = [
        "rofi",
        "-lines",
        "0",
        "-separator-style",
        "'none'",
    ]

    args += ["-dmenu", "-p", prompt]
    args += rofi_args

    args = [str(arg) for arg in args]

    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )

    returncode = result.returncode

    if returncode == 0:
        code = 0
    if returncode == 1:
        code = -1
    if returncode > 9:
        code = returncode - 9
    else:
        code = -1

    return code, result.stdout.strip("\n")
