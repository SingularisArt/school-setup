import subprocess


def rofi(prompt, options, rofi_args=[], fuzzy=True):
    """
    Wrapper function for rofi.

    Parameters:
    -----------

    prompt: The prompt to display to the user
    options: A list of options to display to the user
    rofi_args: A list of arguments to pass to rofi ([])
    fuzzy: A boolean indicating if we should use fuzzy matching (True)
    """

    optionstr = '\n'.join(option.replace('\n', ' ') for option in options)

    args = ['rofi', '-sort', '-no-levenshtein-sort']

    if fuzzy:
        args += ['-matching', 'fuzzy']

    args += ['-dmenu', '-p', prompt, '-format', 's', '-i']
    args += rofi_args
    args = [str(arg) for arg in args]

    result = subprocess.run(args, input=optionstr,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    returncode = result.returncode
    stdout = result.stdout.strip()

    selected = stdout.strip()

    try:
        index = [opt.strip() for opt in options].index(selected)
    except ValueError:
        index = -1

    if returncode == 0:
        key = 0
    if returncode == 1:
        key = -1
    if returncode > 9:
        key = returncode - 9

    return key, index, selected
