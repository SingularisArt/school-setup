from core.courses import Courses as Courses
from lesson_manager import config
import utils


def main():
    courses = Courses()
    current = courses.current
    rofi_options = config.rofi_options

    if not courses:
        utils.rofi.msg("No courses found!", err=True)
        exit(1)

    if config.highlight_current_course:
        try:
            current_index = courses.index(current)
            rofi_options.extend(["-a", current_index])
        except ValueError:
            pass

    options = [f"<b>{course.info['title']}</b>" for course in courses]

    _, index, _ = utils.rofi.select(
        "Select course",
        options,
        rofi_options,
    )

    if index >= 0:
        courses.current = courses[index]


if __name__ == "__main__":
    main()
