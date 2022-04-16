import os


def open_file(terminal, editor, current_course, lesson, type='lecture'):
    """
    Opens the lesson file in the wanted terminal with the wanted editor.

    Args:
        terminal (str): The terminal to use: Supported Terminals:
            - 'gnome-terminal'
            - 'xfce4-terminal'
        editor (str): The editor to use.
        current_course (str): The current course.
        unit (str): The unit.
        lesson (str): The lesson number.
        type (str): The type of the file:
            lecture (default): The lecture file.
            assignment: The assignment file.
    """

    if terminal == 'xfce4-terminal':
        if type == 'lecture':
            os.system('{} -e "{} {}"'.format(terminal, editor,
                      '{}/lectures/lec-{}.tex'.format(
                        current_course,
                        lesson)))
        if type == 'assignment':
            os.system('{} -e "{} {}"'.format(terminal, editor,
                      '{}/{}'.format(
                        current_course,
                        lesson)))
