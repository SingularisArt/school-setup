from RofiLessonManager.courses import Courses as Courses
from RofiLessonManager import utils as utils


def main():
    """ This main function will change the current course. """

    courses = Courses()

    code, index, selected = utils.rofi('Select course',
                                       courses.rofi_names,
                                       courses.rofi_options)
    if index >= 0:
        courses.current = courses[index]


if __name__ == "__main__":
    main()
