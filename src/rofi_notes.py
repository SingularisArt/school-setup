import os

from RofiLessonManager.courses import Courses as Courses
import config
import utils


def format_option(note, date_format):
    number = utils.display_number(str(note.number))
    title = utils.generate_short_title(note.title, 24)
    date = note.date.strftime(date_format)
    week = note.week

    column_1 = f"{number: >2}. <b>{title: <26}</b>"
    column_2 = f"<span size='smaller'>{date: <{15}} (Week: {week})</span>"

    return f"{column_1} {column_2}"


def main():
    courses = Courses()
    current_course = courses.current
    notes = current_course.notes

    if not notes:
        utils.rofi.msg("No notes found!", err=True)
        exit(1)

    sorted_notes = sorted(notes, key=lambda note: -int(note.number))

    options = []
    for note in sorted_notes:
        options.append(format_option(note, config.date_format))

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
