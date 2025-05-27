from subprocess import check_output
from TexSoup import TexSoup

from core.courses import Courses as Courses
from lesson_manager import config
import utils
from utils import rofi


def format_option(note, date_format):
    number = utils.convert_number(str(note.number))
    title = utils.generate_short_title(note.title, 24)
    date = note.date.strftime(date_format)
    week = note.week

    column_1 = f"{number: >2}. <b>{title: <26}</b>"
    column_2 = f"<span size='smaller'>{date: <{15}} (Week: {week})</span>"

    return f"{column_1} {column_2}"


def main(output):
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

    _, environmentsList = rofi.get_input(
        "Enter environments seperated by comma",
        config.rofi_options,
    )
    environmentsList = environmentsList.split(",")
    environmentsList = [
        "nte",
        "part",
        "chapter",
        "section",
        "subsection",
        "subsubsection",
        "paragraph",
        "subparagraph",
    ] + environmentsList

    with open(sorted_notes[index].file_path) as fileContent:
        soup = TexSoup(fileContent.read())
        foundEnvironmentsList = soup.find_all(environmentsList)
        environments = ""
        for environment in foundEnvironmentsList:
            environments += f"{environment}\n\n"
        environments = environments[:-1]
        environments += "\n\\newpage"

        with open(output, "w") as file:
            file.write(environments)

        out = check_output(["latexindent", output]).decode("utf-8")
        open(output, "w").write(out)


if __name__ == "__main__":
    main()
