#!/usr/bin/env python3

import yaml

import RofiLessonManager
import RofiLessonManager.utils as utils


class ChangeCourse(RofiLessonManager.Basis):
    def __init__(self):
        super().__init__()

        self.classes = sorted(utils.get_classes(self.root))
        self.titles = sorted(self.get_titles())

    def activate(self, index):
        if index == -1:
            return

        utils.create_symlink_class(self.current_course,
                                   self.classes[index])

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
            except Exception as e:
                raise e

        return titles


def main():
    course = ChangeCourse()

    key, index, selected = utils.rofi('Select Class', course.titles,
                                      course.rofi_options)
    utils.create_symlink_class(course.current_course,
                               course.classes[index])
