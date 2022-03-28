import os


def open_file(terminal, editor, current_course, unit, lesson):
    """
    Opens the lesson file in the wanted terminal with the wanted editor.

    Args:
        terminal (str): The terminal to use.
        editor (str): The editor to use.
        current_course (str): The current course.
        unit (str): The unit.
        lesson (str): The lesson number.
    """

    if terminal == 'xfce4-terminal':
        os.system('{} -e "{} {}"'.format(terminal, editor,
                  '{}/{}/lesson-{}.tex'.format(
                    current_course,
                    unit,
                    lesson)))
