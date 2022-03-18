import ntpath

from config import config


def _get_latest_lesson(config, lessons: list) -> str:
    """
    This function gets you the last two lessons.
    It returns them in this order
    latest_lesson_head: This is the absolute path to the last lesson
    latest_lesson_tail: This is the name of the last lesson

    second_to_last_lesson_head: This is the absolute path to the second to
        last lesson
    second_to_last_lesson_tail: This is the name of the
        second to last lesson
    :param lessons list: This is a list with all of the lessons
    """

    if len(lessons) == 0:
        config.r.error('No lessons found')
        # sys.exit(1)
    elif len(lessons) == 1:
        latest_lesson_head = ntpath.split(lessons[-1])[0]
        latest_lesson_tail = ntpath.split(lessons[-1])[1]

        second_to_last_lesson_head = 'NONE'
        second_to_last_lesson_tail = 'NONE'

        last_unit_name = ntpath.split(latest_lesson_head)[1]
        last_unit_number = last_unit_name[5:]
    elif len(lessons) == 2:
        latest_lesson_head = ntpath.split(lessons[-1])[0]
        latest_lesson_tail = ntpath.split(lessons[-1])[1]

        second_to_last_lesson_head = ntpath.split(lessons[-2])[0]
        second_to_last_lesson_tail = ntpath.split(lessons[-2])[1]

        last_unit_name = ntpath.split(latest_lesson_head)[1]
        last_unit_number = last_unit_name[5:]
    elif len(lessons) >= 3:
        if ntpath.split(lessons[-1])[1] == config.unit_info_name:
            latest_lesson_head = ntpath.split(lessons[-2])[0]
            latest_lesson_tail = ntpath.split(lessons[-2])[1]
        else:
            latest_lesson_head = ntpath.split(lessons[-1])[0]
            latest_lesson_tail = ntpath.split(lessons[-2])[1]

        if ntpath.split(lessons[-2])[1] == config.unit_info_name:
            latest_lesson_head = ntpath.split(lessons[-3])[0]
            latest_lesson_tail = ntpath.split(lessons[-3])[1]
        else:
            if ntpath.split(lessons[-2])[1] == latest_lesson_tail:
                second_to_last_lesson_head = ntpath.split(lessons[-3])[0]
                second_to_last_lesson_tail = ntpath.split(lessons[-3])[1]
            else:
                second_to_last_lesson_head = ntpath.split(lessons[-2])[0]
                second_to_last_lesson_tail = ntpath.split(lessons[-2])[1]

        last_unit_name = ntpath.split(latest_lesson_head)[1]
        last_unit_number = last_unit_name[5:]

    return latest_lesson_head, \
        latest_lesson_tail, \
        second_to_last_lesson_head, \
        second_to_last_lesson_tail, \
        last_unit_name, \
        last_unit_number
