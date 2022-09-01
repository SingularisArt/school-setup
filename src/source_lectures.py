from RofiLessonManager.lectures import Lectures as Lectures
import RofiLessonManager.utils as utils


def main():
    lectures = Lectures()
    if not lectures:
        utils.rofi.error_message("No lectures found!")
        return

    commands = ["last", "prev_last", "all", "prev"]
    options = [
        "Current lecture",
        "Last two lectures",
        "All lectures",
        "Previous lectures",
    ]

    key, index, selected = utils.rofi.select(
        "Select view", options, ["-lines", 4, "-auto-select"]
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
