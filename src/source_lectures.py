from RofiLessonManager.courses import Courses as Courses
import RofiLessonManager.utils as utils


def main():
    lectures = Courses().current.lectures

    if not lectures:
        utils.rofi.msg("No lectures found!", err=True)
        return

    commands = ["last", "prev_last", "all", "prev"]
    options = [
        "Current lecture",
        "Last two lectures",
        "All lectures",
        "Previous lectures",
    ]

    _, index, selected = utils.rofi.select(
        "Select one",
        options,
        ["-lines", 4, "-auto-select"],
    )

    if not selected:
        return

    if selected == "None":
        return
    if index >= 0:
        command = commands[index]
    else:
        command = selected

    lecture_range = lectures.parse_range_string(command)
    lectures.update_lectures_in_master(lecture_range)
    lectures.compile_master()


if __name__ == "__main__":
    main()
