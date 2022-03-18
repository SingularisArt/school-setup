#!/usr/bin/env python3

import re
import os
import ntpath
from config import Configuration


class Lessons(Configuration):
    def __init__(self):
        super().__init__()

        self.units_head, self.units_tail = self.get_all_units()
        self.options, \
            self.lesson_numbers, \
            self.lesson_dates, self.lesson_names, \
            self.lesson_units = self.get_lesson_info()

    def get_lesson_info(self):
        options = []
        lesson_numbers = []
        lesson_dates = []
        lesson_names = []
        lesson_units = []

        for unit in self.units_head:
            unit_head, unit_tail = ntpath.split(unit)

            for lesson in range(self.LESSON_RANGE_NUMBER):
                lesson = '{}/{}/lesson-{}.tex'.format(self.current_course,
                                                      unit_tail, lesson)

                if not os.path.exists(lesson):
                    continue

                with open(lesson, encoding="utf8",
                          errors='ignore') as lesson_file:
                    for line in lesson_file:
                        count = self._get_amount_of_lines_in_file(
                            lesson_file)

                        lesson_match = re.search(self.lesson_regex, line)

                        try:
                            lesson_number = lesson_match.group(1)
                            lesson_date = lesson_match.group(2)
                            lesson_name = lesson_match.group(3)
                            lesson_unit = lesson_match.group(4)

                            lesson_numbers.append(lesson_number)
                            lesson_dates.append(lesson_date)
                            lesson_names.append(lesson_name)
                            lesson_units.append(
                                lesson_unit.lower().replace(' ', '-'))

                            if count <= 5:
                                lesson_unit += " File Empty"

                            options.append(
                                "<span color='red'>{number: >2}</span>. "
                                "<b><span color='blue'>{title: <{fill}}</span>"
                                "</b> <i><span color='yellow' size='smaller'>"
                                "{date}</span> <span color='green' "
                                "size='smaller'>({week})</span></i>".format(
                                    fill=35,
                                    number=lesson_number,
                                    title=lesson_name,
                                    date=lesson_date,
                                    week=lesson_unit
                                ))
                        except Exception:
                            pass

        return options, lesson_numbers, lesson_dates, \
            lesson_names, lesson_units


def Main():
    lesson = Lessons()

    key, index, selected = lesson.rofi('Select lesson', lesson.options, [
        '-scroll-method', 1,
        '-lines', 5,
        '-markup-rows',
        '-kb-row-down', 'Down',
        '-kb-custom-1', 'Ctrl+n',
        '-keep-left'
    ])

    lesson._open_file(lesson.lesson_units[index], lesson.lesson_numbers[index])


if __name__ == "__main__":
    Main()
