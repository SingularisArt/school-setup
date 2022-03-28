#!/usr/bin/env python3


import argparse

import RofiLessonManager.change_course as cc
# import RofiLessonManager.commands as cm
# import RofiLessonManager.grades as gr
# import RofiLessonManager.new_lesson as nl
import RofiLessonManager.projects as pr
import RofiLessonManager.view_lessons as vl
import RofiLessonManager.utils as utils


def Main():
    parser = argparse.ArgumentParser(description='Lesson Manager')
    parser.add_argument('-c', '--change-course', help='Change course',
                        action='store_true')
    parser.add_argument('-n', '--new-lesson', help='Create new lesson',
                        action='store_true')
    parser.add_argument('-m', '--commands', help='Commands',
                        action='store_true')
    parser.add_argument('-g', '--grades', help='Grades',
                        action='store_true')
    parser.add_argument('-p', '--projects', help='Projects',
                        action='store_true')
    parser.add_argument('-l', '--lessons', help='View all Lessons',
                        action='store_true')

    args = parser.parse_args()

    if args.change_course:
        course = cc.ChangeCourse()
        key, index, selected = utils.rofi('Select Class', course.titles,
                                          course.rofi_options)
        utils.create_symlink_class(course.current_course,
                                   course.classes[index])
    # elif args.new_lesson:
    #     # new_lesson()
    # elif args.commands:
    #     # commands()
    # elif args.grades:
    #     # grades()
    elif args.projects:
        projects = pr.Projects()

        key, index, selected = utils.rofi('Select project',
                                          projects.options,
                                          projects.rofi_options)

        key_command, index_command, \
            selected_command = utils.rofi(
                                          'Select command for the ' +
                                          '{} project'.format(
                                             projects.folders[index]),
                                          projects.commands,
                                          projects.rofi_options)

        projects.run_func_based_on_command(selected_command,
                                           projects.folders[index])
    elif args.lessons:
        lesson = vl.ViewLessons()
        key, index, selected = utils.rofi('Select Lesson', lesson.options,
                                          lesson.rofi_options)
        utils.open_file(lesson.terminal, lesson.editor, lesson.current_course,
                        lesson.lesson_units[index],
                        lesson.lesson_numbers[index])


if __name__ == "__main__":
    Main()
