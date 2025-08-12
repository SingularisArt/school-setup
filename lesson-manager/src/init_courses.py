import datetime
import os
import re
import shutil

from core.courses import Courses
from lesson_manager import config
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
        topic = course.info["topic"]
        class_number = course.info["class_number"]
        short = course.info["short"]
        author = course.info["author"]
        term = course.info["term"]
        faculty = course.info["faculty"]
        college = course.info["college"]
        location = course.info["location"]
        year = course.info["year"]
        start_date = get_start_date(course.info["start_date"])
        date = datetime.datetime.today().strftime("%B %d, %Y")
        start_time = course.info["start_time"]
        professor_info = course.info["professor"]
        professor_name = professor_info["name"]
        professor_first_name = professor_name.split()[0]
        professor_last_name = professor_name.split()[-1]
        first_professor_letter = professor_first_name[0]

        for folder in folders:
            (notes.root / folder).mkdir(exist_ok=True)
            if config.create_readme_file:
                (notes.root / folder / "README.md").touch(exist_ok=True)

        (notes.root / "lectures").mkdir(exist_ok=True)

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
                    "CLASS_SHORT": short,
                    "CLASS": title,
                    "AUTHOR": author,
                    "START_DATE": start_date,
                    "START_TIME": start_time,
                    "DATE": date,
                    "TERM": term,
                    "YEAR": f"${year}$",
                    "FACULTY": faculty,
                    "COLLEGE": college,
                    "PROFESSOR_SHORT": professor_first_name,
                    "FIRST_LETTER": first_professor_letter,
                    "LAST_NAME": professor_last_name,
                    "PROFESSOR": professor_info["name"],
                }

                with file_dst.open() as f:
                    content = f.read()
                    for placeholder, value in placeholders.items():
                        content = content.replace(placeholder, value)
                    file_dst.write_text(content)

        utils.create_course_event(course.info)
