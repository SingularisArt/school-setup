#!/usr/bin/env python3

import os
import yaml
from config import Configuration


class ChangeCourse(Configuration):
    def __init__(self):
        super().__init__()

        self.titles = sorted(self.get_titles())

    def get_titles(self):
        titles = []
        file_info = ''

        for current_class in self.classes:
            try:
                info = open('{}/info.yaml'.format(current_class))
                file_info = yaml.load(info, Loader=yaml.FullLoader)

                titles.append("<b><span color='blue'>{: <{}}</span></b>"
                              "<span color='grey'>(</span><i>"
                              "<span color='yellow'>{}</span></i>"
                              "<span color='grey'>)</span>".format(
                                        file_info['title'],
                                        25,
                                        file_info['short']))
            except Exception:
                pass

        return titles


def Main():
    course = ChangeCourse()

    key, index, selected = course.rofi('Select class', course.titles,
                                       course.rofi_options)

    # course.symlink_class(course.classes[index])
    current_class = os.path.realpath(course.current_course)
    current_class = os.path.basename(os.path.normpath(current_class))
    current_class = current_class.replace('-', ' ').replace(
        'hs', 'Honors').title()

    new_class = os.path.basename(os.path.normpath(course.classes[index]))
    new_class = new_class.replace('-', ' ').replace('hs', 'Honors').title()

    if os.path.isdir(course.current_course):
        os.remove(course.current_course)
    os.symlink(course.classes[index], course.current_course)


if __name__ == '__main__':
    Main()
