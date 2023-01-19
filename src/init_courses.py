#!/usr/bin/env python3

import datetime
import os
import re
import shutil
from typing import Dict

import config
from RofiLessonManager.courses import Courses


def copy_or_symlink(src: str, dst: str, action: str) -> None:
    try:
        if action == "symlink":
            os.symlink(src, dst)
        elif action == "copy":
            shutil.copy2(src, dst)
    except FileExistsError:
        return
    except FileNotFoundError:
        return


def main() -> None:
    for course in Courses():
        notes = course.notes
        folders = config.folders
        files = config.files
        templates_dir = config.templates_dir

        title = course.info["title"]
        author = course.info["author"]
        professor_info = course.info["professor"]
        professor_short = professor_info["name"].split()[0]
        date = datetime.datetime.today().strftime("%B %d, %Y")
        term = course.info["term"]
        year = course.info["year"]
        faculty = course.info["faculty"]
        intro_type = course.info["notes_type"]
        college = course.info["college"]

        for folder in folders:
            (notes.root / folder).mkdir(exist_ok=True)

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
                placeholders: Dict[str, str] = {
                    "CLASS": title,
                    "AUTHOR": author,
                    "DATE": date,
                    "TERM": term,
                    "YEAR": f"${year}$",
                    "FACULTY": faculty,
                    "INTRO_TYPE": intro_type.title(),
                    "TYPE": course.info["notes_type"].lower(),
                    "COLLEGE": college,
                    "PROFESSOR_SHORT": professor_short,
                    "PROFESSOR": professor_info["name"],
                }

                with file_dst.open() as f:
                    content = f.read()
                    for placeholder, value in placeholders.items():
                        content = content.replace(placeholder, value)
                    file_dst.write_text(content)
