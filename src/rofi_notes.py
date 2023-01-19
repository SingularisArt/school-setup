#!/usr/bin/env python3

import os

import config
import utils
from RofiLessonManager.courses import Courses as Courses


def generate_options(notes, date_format):
    options = []
    for note in notes:
        option = (
            f"{utils.display_number(str(note.number)): >2}. "
            + f"<b>{utils.generate_short_title(note.title, 26): <{26}} </b> "
            + f"<span size='smaller'>{note.date.strftime(date_format): <{15}} "
            + f"(Week: {note.week})</span>"
        )
        options.append(option)

    return options


def main():
    courses = Courses()
    current_course = courses.current
    notes = current_course.notes

    if not notes:
        utils.rofi.msg("No notes found!", err=True)
        exit(1)

    sorted_notes = sorted(notes, key=lambda note: -int(note.number))

    options = generate_options(sorted_notes, config.date_format)

    _, index, _ = utils.rofi.select(
        "Select Note",
        options,
        config.rofi_options,
    )

    if index < 0:
        exit(1)

    os.chdir(notes.path)
    sorted_notes[index].edit()


if __name__ == "__main__":
    main()
