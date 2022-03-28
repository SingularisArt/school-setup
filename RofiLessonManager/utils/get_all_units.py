import ntpath


def get_all_units(folders_head):
    """
    Get all units from the current course.

    Args:
        folders_head (list): List of the absolute path to each folder within
        the current course. (You can use the utils.get_all_folders function to
                             get the needed list)

    Returns:
        units_head (list): List of the absolute path to each unit within the
            current course.
        units_tail (list): List of the relative path to each unit within the
            current course.
    """

    # The lists, which we will return later on.
    units_head = []
    units_tail = []

    # Iterating through all of the absolute path folders
    for folder in folders_head:
        # Splits the folder into the name and absolute path
        unit_head, unit_tail = ntpath.split(folder)

        # Adds the folder to the list of folders we want to return
        units_head.append('{}/{}'.format(unit_head, unit_tail))
        units_tail.append(unit_tail)

    return units_head, units_tail
