import config
import utils
from RofiLessonManager.courses import Courses as Courses


def main():
    notes = Courses().current.notes

    if not notes:
        utils.rofi.msg("No notes found!", err=True)
        return

    commands = {
        "Current note": "last",
        "Last two notes": "prev_last",
        "All notes": "all",
        "Previous notes": "prev",
    }

    _, index, selected = utils.rofi.select(
        "Select one",
        commands,
        config.rofi_options,
    )

    if not selected:
        return

    if index >= 0:
        command = commands[selected]
    else:
        command = selected

    note_range = notes.parse_range_string(command)
    notes.update_notes_in_master(note_range)
    # notes.compile_master()


if __name__ == "__main__":
    main()
