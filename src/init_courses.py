#!/bin/python3

from config import folders
from RofiLessonManager.courses import Courses as Courses


def main():
    for course in Courses():
        course_title = course.info["title"]
        lectures = course.lectures

        lines = [
            r"% Finished mode.",
            r"% \documentclass[nocolor]{article}",
            r"% \documentclass{article}",
            r"% Draft mode.",
            r"% \documentclass[working,nocolor]{article}",
            r"\documentclass[working]{article}",
            "",
            r"\input{preamble.tex}",
            "",
            rf"\title{{{course_title}}}",
            r"\author{Hashem A. Damrah}",
            r"\date{\today}",
            "",
            r"\newcommand\linktootherpages{url}",
            r"\newcommand\shortlinkname{url}",
            r"\newcommand\term{}",
            r"\newcommand\academicyear{}",
            r"\newcommand\faculty{}",
            "",
            r"\begin{document}",
            r"  \createintro",
            "",
            r"  % start lectures",
            r"  % end lectures",
            "",
            r"  \listnotes",
            r"\end{document}",
        ]

        lectures.master_file.touch()
        lectures.master_file.write_text("\n".join(lines))
        (lectures.root / "notes.md").touch()

        for folder in folders:
            (lectures.root / folder).mkdir(exist_ok=True)
