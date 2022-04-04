#!/usr/bin/env python3

import re
import os

import RofiLessonManager
import RofiLessonManager.utils as utils


class ViewLectures(RofiLessonManager.Basis):
    def __init__(self):
        super().__init__()

        self.folders_head, self.folders_tail = utils.get_all_folders(
            self.current_course, self.discourage_folders)
        self.units_head, self.units_tail = utils.get_all_units(
            self.folders_head)
        self.options, \
            self.lecture_numbers, \
            self.lecture_dates, self.lecture_names = self.get_lecture_info()

    def get_first_line(self, file):
        file_opened = open(file)
        for line in file_opened.readlines():
            return line

    def get_lecture_info(self):
        options = []
        lecture_numbers = []
        lecture_dates = []
        lecture_names = []

        lectures = [f for f in os.listdir(self.units_head[0]) if
                    os.path.isfile(os.path.join(self.units_head[0], f))]

        for lecture in lectures:
            for lecture_number in range(self.LESSON_RANGE_NUMBER):
                lecture = '{}/lec-{}.tex'.format(self.units_head[0],
                                                 lecture_number)

                if not os.path.isfile(lecture):
                    continue
                else:
                    with open(lecture, encoding='utf8'):
                        first_line = self.get_first_line(lecture)
                        lecture_match = re.search(self.lecture_regex,
                                                  first_line)

                        try:
                            lecture_number = lecture_match.group(1)
                            lecture_date = lecture_match.group(2)
                            lecture_name = lecture_match.group(3)

                            lecture_numbers.append(lecture_number)
                            lecture_dates.append(lecture_date)
                            lecture_names.append(lecture_name)

                            options.append(
                                "<span color='red'>{number: >2}</span>. "
                                "<b><span color='blue'>{title: <{fill}}</span>"
                                "</b> <i><span color='yellow' size='smaller'>"
                                "{date}</span></i>".format(
                                    fill=35,
                                    number=lecture_number,
                                    title=lecture_name,
                                    date=lecture_date,
                                ))
                        except Exception:
                            pass

        return options, lecture_numbers, lecture_dates, \
            lecture_names
