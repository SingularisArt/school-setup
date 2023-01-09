import utils
from RofiLessonManager.courses import Courses as Courses


def main():
    lectures = Courses().current.lectures

    if not lectures:
        utils.rofi.msg("No lectures found!", err=True)
        return

    commands = {
        "Current lecture": "last",
        "Last two lectures": "prev_last",
        "All lectures": "all",
        "Previous lectures": "prev",
    }

    _, index, selected = utils.rofi.select(
        "Select one",
        commands,
        ["-lines", 4, "-auto-select"],
    )

    if not selected:
        return

    if index >= 0:
        command = commands[selected]
    else:
        command = selected

    lecture_range = lectures.parse_range_string(command)
    lectures.update_lectures_in_master(lecture_range)
    lectures.compile_master()


if __name__ == "__main__":
    main()
