def get_amount_of_lines_in_file(file):
    """
    Get the amount of lines within a file.

    Args:
        file (str): The file relative or absolute path.
            (Note: You must have the file already opened. You cannot just pass
            the file name. Ex:
                with open(file, 'r') as f:
                count = get_amount_of_lines_in_file(f)
            )

    Returns:
        count (int): The amount of lines within the file.
    """

    return len(file.readlines())
