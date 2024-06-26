import datetime
import os
import re
import shutil

from RofiLessonManager.courses import Courses
import config
import utils


def copy_or_symlink(src, dst, action):
    try:
        if action == "symlink":
            os.symlink(src, dst)
        elif action == "copy":
            shutil.copy2(src, dst)
    except FileExistsError:
        return
    except FileNotFoundError:
        return


def get_start_date(start_date):
    return datetime.datetime.strptime(
        start_date,
        "%b %d %Y %a (%H:%M:%S)",
    ).strftime("%B %d, %Y")


def main():
    for course in Courses():
        notes = course.notes
        folders = config.folders
        files = config.files
        templates_dir = config.templates_dir

        title = course.info["title"]
        author = course.info["author"]
        start_date = get_start_date(course.info["start_date"])
        date = datetime.datetime.today().strftime("%B %d, %Y")
        term = course.info["term"]
        year = course.info["year"]
        faculty = course.info["faculty"]
        intro_type = course.info["notes_type"]
        note_type_abbr = ""
        if course.info["notes_type"].lower() == "lectures":
            note_type_abbr = "lec"
        else:
            note_type_abbr = "chap"
        note_type = course.info["notes_type"].lower()
        college = course.info["college"]
        professor_info = course.info["professor"]
        professor_short = professor_info["name"].split()[0]
        note_location = f"{course.info['notes_type']}/{note_type_abbr}"

        for folder in folders:
            (notes.root / folder).mkdir(exist_ok=True)
            if config.create_readme_file:
                (notes.root / folder / "README.md").touch(exist_ok=True)

        (notes.root / course.info["notes_type"]).mkdir(exist_ok=True)

        for file in files:
            key = files[file]
            file_src = templates_dir / file
            file_dst = course.root / file
            copy_or_symlink(file_src, file_dst, key)

            search = re.search(
                r"([a-zA-Z0-9/\-\.]+)?(master.tex|intro.tex)",
                file,
            )
            if search:
                placeholders = {
                    "CLASS": title,
                    "AUTHOR": author,
                    "START_DATE": start_date,
                    "DATE": date,
                    "TERM": term,
                    "YEAR": f"${year}$",
                    "FACULTY": faculty,
                    "INTRO_TYPE": intro_type.title(),
                    "TYPE_ABBR": note_type_abbr,
                    "TYPE": note_type.title()[:-1],
                    "COLLEGE": college,
                    "PROFESSOR_SHORT": professor_short,
                    "PROFESSOR": professor_info["name"],
                    "NOTE_LOCATION": note_location,
                }

                with file_dst.open() as f:
                    content = f.read()
                    for placeholder, value in placeholders.items():
                        content = content.replace(placeholder, value)
                    file_dst.write_text(content)

        utils.create_course_event(course.info)
