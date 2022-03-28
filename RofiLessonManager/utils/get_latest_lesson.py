import ntpath


def get_latest_lesson(lessons, unit_info_name, rofi):
    """
    Get the last one/two lessons for the last unit.

    Args:
        lessons (list): List of lessons.
        unit_info_name (str): Name of the unit.
        rofi (object): Rofi object.

    Returns:
        latest_lesson_head (str): Absolute path to the last lesson in the last
            unit.
        latest_lesson_tail (str): Relative path to the last lesson in the last
            unit.
        second_to_last_lesson_head (str): Absolute path to the second to last
            lesson in the last unit.
        second_to_last_lesson_tail (str): Relative path to the second to last
            lesson in the last unit.
        last_unit_name (str): Name of the last unit.
        last_unit_number (int): Number of the last unit.
    """

    # Check if there are any lessons available
    if len(lessons) == 0:
        rofi.exit_with_error('No lessons found')
    # If there's only one lesson
    elif len(lessons) == 1:
        # Get the absolute and relative path to the last lesson
        latest_lesson_head = ntpath.split(lessons[-1])[0]
        latest_lesson_tail = ntpath.split(lessons[-1])[1]

        # Note that there isn't a second lesson
        second_to_last_lesson_head = 'NONE'
        second_to_last_lesson_tail = 'NONE'

        # Get the last unit number
        last_unit_name = ntpath.split(latest_lesson_head)[1]
        last_unit_number = last_unit_name[5:]
    # If there are two lessons
    elif len(lessons) == 2:
        # Get the absolute and relative path to the last lesson
        latest_lesson_head = ntpath.split(lessons[-1])[0]
        latest_lesson_tail = ntpath.split(lessons[-1])[1]

        # Get the absolute and relative path to the second to last lesson
        second_to_last_lesson_head = ntpath.split(lessons[-2])[0]
        second_to_last_lesson_tail = ntpath.split(lessons[-2])[1]

        # Get the last unit number
        last_unit_name = ntpath.split(latest_lesson_head)[1]
        last_unit_number = last_unit_name[5:]
    # If there are more than two lessons
    elif len(lessons) >= 3:
        # Check if the last lesson is equal to the unit info name
        if ntpath.split(lessons[-1])[1] == unit_info_name:
            # Get the absolute and relative path to the last lesson
            # but we're getting the second last item in the list because the
            # last item is the unit info file
            latest_lesson_head = ntpath.split(lessons[-2])[0]
            latest_lesson_tail = ntpath.split(lessons[-2])[1]
        # If the last lesson isn't the unit info file
        else:
            # Get the absolute and relative path to the last lesson
            # This time, we're getting the last item in the list because the
            # last item isn't the unit info file
            latest_lesson_head = ntpath.split(lessons[-1])[0]
            latest_lesson_tail = ntpath.split(lessons[-2])[1]

        # Check if the second to last lesson is equal to the unit info name
        if ntpath.split(lessons[-2])[1] == unit_info_name:
            # Get the absolute and relative path to the last lesson
            # but we're getting the third last item in the list because the
            # second last item is the unit info file
            latest_lesson_head = ntpath.split(lessons[-3])[0]
            latest_lesson_tail = ntpath.split(lessons[-3])[1]
        # If the second to last lesson isn't the unit info file
        else:
            # Checking if the second to last lesson is the last lesson
            if ntpath.split(lessons[-2])[1] == latest_lesson_tail:
                # Get the absolute and relative path to the second to last
                # lesson but we're getting the third last item in the list
                # because the second last item is the last lesson
                second_to_last_lesson_head = ntpath.split(lessons[-3])[0]
                second_to_last_lesson_tail = ntpath.split(lessons[-3])[1]
            # If the second to last item in the list isn't the last lesson
            else:
                # Get the absolute and relative path to the second to last
                # lesson but we're getting the second last item in the list
                # because the last lesson is the last item in the list
                second_to_last_lesson_head = ntpath.split(lessons[-2])[0]
                second_to_last_lesson_tail = ntpath.split(lessons[-2])[1]

        # Get the last unit number
        last_unit_name = ntpath.split(latest_lesson_head)[1]
        last_unit_number = last_unit_name[5:]

    # Return the latest lesson head, tail, second to last lesson head, tail,
    # last unit name, and last unit number
    return latest_lesson_head, \
        latest_lesson_tail, \
        second_to_last_lesson_head, \
        second_to_last_lesson_tail, \
        last_unit_name, \
        last_unit_number
