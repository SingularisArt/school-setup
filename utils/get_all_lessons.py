import ntpath
import os
import sys

from config import config


def _get_all_lessons():
    """
    This function returns all of the lessons in a list.
    It returns them in this order

    lesson_head: list: This is the absolute path to the lesson
    lesson_tail: list: This is just the name for the lesson
    all_lessons: dict:
        {'unit-1': ['lesson-1.tex', 'lesson-2.tex', ...], 'unit-2', [...]}
    """

    # The lists, which we will return later on.
    lessons_head = []
    lessons_tail = []

    # This stores the unit number as the key and the lessons within that
    # unit as the values within a list
    # This will be returned at the end of the function
    all_lessons = {}

    # Iterating through all of the units absolute path
    for unit in config.units_head:
        # Getting all of the lessons within that unit
        lessons = sorted([os.path.join(unit, f) for f in os.listdir(unit)
                          if os.path.isfile(os.path.join(unit, f))])

        # Iterating through the lessons we got
        for lesson in lessons:
            # splitting the lesson into the naame and absolute path
            lesson_head, lesson_tail = ntpath.split(lesson)

            # Appending all of the information respectfully
            lessons_head.append('{}/{}'.format(lesson_head, lesson_tail))
            lessons_tail.append(lesson_tail)

    # Try just in case there are any lessons
    try:
        # Get the amount of lessons
        size = len(lessons_tail)
        # Don't know exactly what this does
        lessons_tail_splited = [idx + 1 for idx, val in
                                enumerate(lessons_tail)
                                if val == config.unit_info_name]

        # Don't know exactly what this does
        lessons_tail_new = [lessons_tail[i: j] for i, j in
                            zip([0] + lessons_tail_splited,
                                lessons_tail_splited +
                                ([size] if lessons_tail_splited[-1] != size
                                    else []))]

        # Iterate through all of our lessons
        for x, lesson in enumerate(lessons_tail_new):
            # Add the unit as the key and lessons as the value in a list
            # form
            all_lessons[config.units_tail[x]] = lesson
    # Create an exception error if now lessons found
    except Exception:
        # Have rofi say no lessons found
        config.r.error('No lessons found')
        # Exit program
        sys.exit(1)

    return lessons_head, lessons_tail, all_lessons
