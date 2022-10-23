from rofi import Rofi

from RofiLessonManager.assignments import Assignment as Assignment
from RofiLessonManager.assignments import Assignments as Assignments


def main():
    assignments = Assignments()

    rofi = Rofi()
    n = rofi.integer_entry("Enter assignment number")

    if not n:
        return

    Assignment(f"{assignments.assignments_latex_folder}/week-{n}.tex")


if __name__ == "__main__":
    main()
