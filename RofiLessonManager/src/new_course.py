from rofi import Rofi

import RofiLessonManager.utils as utils
from RofiLessonManager.classes.courses import Courses as Courses
from RofiLessonManager import Basis as Basis
from RofiLessonManager.classes.courses import Course as Course


def main():
    b = Basis()
    r = Rofi()
    name = r.text_entry('Course Name')
    name = name.replace(' ', '-').replace('_', '-').lower()

    if '{}/{}'.format(b.root, name) in Courses().paths:
        utils.error_message('Course already exists')
        return

    Course('{}/{}'.format(b.root, name))


if __name__ == "__main__":
    main()
