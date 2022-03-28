#!/usr/bin/env python3

import re
import os
import ntpath

import RofiLessonManager
import RofiLessonManager.utils as utils


class ViewLessons(RofiLessonManager.Basis):
    def __init__(self):
        super().__init__()

        self.folders_head, self.folders_tail = utils.get_all_folders(
            self.current_course, self.discourage_folders)
        self.units_head, self.units_tail = utils.get_all_units(
            self.folders_head)
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
                        count = utils.get_amount_of_lines_in_file(lesson_file)

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
