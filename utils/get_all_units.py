import ntpath

from config import config


def _get_all_units():
    """
    This function returns all of the units in a list.
    It returns them in this order

    unit_head: This is the absolute path to the unit
    unit_tail: This is just the name for the unit
    """

    # The lists, which we will return later on.
    units_head = []
    units_tail = []

    # Iterating through all of the absolute path folders
    for folder in config.folders_head:
        # Splits the folder into the name and absolute path
        unit_head, unit_tail = ntpath.split(folder)

        # Adds the folder to the list of folders we want to return
        units_head.append('{}/{}'.format(unit_head, unit_tail))
        units_tail.append(unit_tail)

    return units_head, units_tail
