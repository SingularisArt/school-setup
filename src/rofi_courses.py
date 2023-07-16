import utils
from RofiLessonManager.courses import Courses as Courses

import config


def main():
    courses = Courses()

    if not courses:
        utils.rofi.msg("No courses found!", err=True)
        exit(1)

    options = [f"<b>{course.info['title']}</b>" for course in courses]

    _, index, _ = utils.rofi.select(
        "Select course",
        options,
        config.rofi_options,
    )

    if index >= 0:
        courses.current = courses[index]


if __name__ == "__main__":
    main()
