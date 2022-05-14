from RofiLessonManager.classes.commands import Commands as Commands
from RofiLessonManager.classes.lectures import Lectures as Lectures
import RofiLessonManager.utils as utils


def main():
    """ This function will run the program """

    source_lectures = Commands()

    key, index, selected = utils.rofi(
        'Select Option (You can specify a range: 1-{})'.format(
            source_lectures.get_last_two_lectures()[0][4:]
        ),
        source_lectures.options,
        source_lectures.rofi_options)

    if index >= 0:
        source_lectures.selected = selected
        source_lectures.check_selection()
        Lectures().compile_master()


if __name__ == "__main__":
    main()
