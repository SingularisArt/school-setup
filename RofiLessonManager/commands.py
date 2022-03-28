#!/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: Mar 06 2022 Sun (02:29:21)

OPTIONS:
    Current Lesson: This one will ask the user to select a unit. Then,
        from that unit, the program will source the last lesson.

    Last Two Lessons: This one will ask the user to select a unit.
        Then, from that unit, the program will source the two lessons.

    All Lessons From in Unit: This one will ask the user to select a
        unit Then, the program will ask if he wants to source all
        lessons. The user can specify a range of lessons to source. The
        program will only source the lessons that exist.

    Source Selected Units: This one will give the user the list of all the
        units available. The user can select the units he wants to source. Then
        the program sources all of the lessons in each of the unit selected.
        IT'S COMING SOON!

    All Lessons: This one will just source all of the lessons.
"""

import os
from config import Configuration


class SourceLessons(Configuration):
    """
    Class for different ways to source your lessons.
    It's inherited from the config.py/Configuration class

    Methods:
    --------

    """

    def __init__(self):
        Configuration.__init__(self)

        """ This function initializes the class """

        # The users options
        self.options = [
            "<i><b><span color='yellow'>Current lesson</span></b></i>",
            "<i><b><span color='yellow'>Last two lessons</span></b></i>",
            "<i><b><span color='yellow'>All lessons in Unit</span></b></i>",
            "<i><b><span color='yellow'>Select Multiple Units</span></b></i>",
            "<i><b><span color='yellow'>All lessons</span></b></i>",
        ]

        self.index = 0
        self.selected = self.options[self.index]

    def source_current_lesson(self):
        with open(self.source_lessons_location, 'w') as source_lessons_file:
            # It writes this as an example: % Unit 1 Started
            source_lessons_file.write('% Unit {} Started\n'.format(
                self.last_unit_number))

            # Source the last lesson
            source_lessons_file.write('\\input{' + self.last_unit_name + '/' +
                                      self.last_lesson_tail + '}\n')

            # It writes this as an example: % Unit 1 Ended
            source_lessons_file.write('% Unit {} Ended'.format(
                self.last_unit_number))

    def source_last_two_lessons(self):
        # We're checking if we have a second to last lesson
        if self.second_to_last_lesson_head != 'NONE':
            # If we do, then we're going to write the last and second last
            # lesson to the source file
            with open(self.source_lessons_location, 'w') as \
                    source_lessons_file:
                # It writes this as an example: % Unit 1 Started
                source_lessons_file.write('% Unit {} Started\n'.format(
                    self.last_unit_number))

                # Source second to last lesson
                source_lessons_file.write('\\input{' + self.last_unit_name +
                                          '/' + self.second_to_last_lesson_tail
                                          + '}\n')
                # Source last lesson
                source_lessons_file.write('\\input{' + self.last_unit_name +
                                          '/' + self.last_lesson_tail + '}\n')

                # It writes this as an example: % Unit 1 Ended
                source_lessons_file.write('% Unit {} Ended'.format(
                    self.last_unit_number))
        # If we don't, we'll just source the last lesson
        else:
            self.source_current_lesson()

    def source_all_lessons_in_unit(self, unit):
        with open(self.source_lessons_location, 'w') as source_lessons_file:
            # It writes this as an example: % Unit 1 Started
            source_lessons_file.write('% Unit {} Started\n'.format(
                unit[5:]))

            # It writes this as an example: \input{unit-1/unit-info.tex}
            input_string = '\\input{' + unit + \
                           '/' + self.unit_info_name + '}'
            source_lessons_file.write('{}\n'.format(input_string))

            # The path to the selected unit
            unit_path = "{}/{}".format(self.current_course, unit)
            # This is complicated to explain. When I just iterated through
            # a list of all the lessons, it would output something like this:
            # lesson-1.tex lesson-10.tex lesson-2.tex lesson-3.tex
            # It would make big leaps like that. So, we create a forloop using
            # this number and we check if the lessons exists. Example:
            # lesson-1.tex, lesson-2.tex, lesson-3.tex, lesson-4.tex
            # If that exists, then we will write this:
            # \input{unit-1/lesson-1.tex}
            lesson_range_to_source = 1000

            # Iterating through the lesson_range_to_source variable
            for i in range(lesson_range_to_source):
                # The path to the lesson
                lesson_name = "{}/lesson-{}.tex".format(unit_path, i)
                # Checking if the lesson exists
                if os.path.exists(lesson_name):
                    # If it does, then write it to the source_lessons file.
                    # Example: \input{unit-1/lesson-1.tex}
                    input_string = '\\input{' + unit + '/lesson-' + str(i) + \
                                   '.tex}\n'
                    source_lessons_file.write(input_string)

            # It writes this as an example: % Unit 1 Ended
            source_lessons_file.write('% Unit {} Ended\n'.format(unit[5:]))

    def source_range(self, lesson_range, unit_number):
        range_list = lesson_range.split('-')

        unit_info_path = self.current_course + '/source-lessons.tex'

        with open(unit_info_path, 'w') as source_lessons_file:
            source_lessons_file.write('% Unit {} Started\n'.format(
                unit_number[5:]))
            source_lessons_file.write('\\input{' + unit_number +
                                      '/' + self.unit_info_name + '}\n')

            for lesson_number in range(int(range_list[0]),
                                       int(range_list[1]) + 1):
                # Check if lesson exists
                if os.path.exists('{}/{}/lesson-{}.tex'.format(
                            self.current_course, unit_number, lesson_number)):
                    # Write to the source-lessons.tex file
                    string = '\\input{' + unit_number + '/lesson-' + \
                             str(lesson_number) + '.tex}\n'

                    source_lessons_file.write(string)

            source_lessons_file.write('% Unit {} Ended'.format(
                unit_number[5:]))

    def source_specific_unit(self):
        units_style = []
        units = []

        for u in self.units_tail:
            units.append(u)
            units_style.append(
                f"<i><b><span color='yellow'>Unit {u[5:]}</span></b></i>"
            )

        key, index, selected = self.rofi('Select Unit',
                                         units_style,
                                         ['-scroll-method', 1,
                                          '-lines', 5,
                                          '-markup-rows'])

        unit = units[index]
        selection = ["<i><b><span color='yellow'>All Lessons</span></b></i>"]
        key, index, selected = self.rofi(
            'Select Option (You can also use a range. 1-{})'.format(
                len(self.all_lessons[unit]) - 1),
            selection,
            ['-scroll-method', 1,
             '-lines', 5,
             '-markup-rows']
        )

        if selected != selection[0]:
            self.source_range(selected, unit)
        else:
            self.source_all_lessons_in_unit(unit)

    def source_selected_units(self):
        self.r.status('Coming Soon ...')

    def source_all_lessons(self):
        with open(self.source_lessons_location, 'w') as source_lessons_file:
            for x, lesson in enumerate(self.all_lessons.values()):
                current_unit = self.units_tail[x]

                source_lessons_file.write('% Unit {} Started\n'.format(
                    current_unit[5:]))

                source_lessons_file.write('\\input{' + current_unit + '/' +
                                          self.unit_info_name + '}\n')

                for les in range(1000):
                    if os.path.exists('{}/{}/lesson-{}.tex'.format(
                            self.current_course, current_unit, les)):
                        source_lessons_file.write('\\input{' +
                                                  self.units_tail[x] +
                                                  '/lesson-' + str(les) +
                                                  '.tex}\n')

                if self.units_tail[x] == self.units_tail[-1]:
                    source_lessons_file.write('% Unit {} Ended'.format(
                        current_unit[5:]))
                else:
                    source_lessons_file.write('% Unit {} Ended\n\n\n'.format(
                        current_unit[5:]))

    def check_selection(self):
        if self.selected == self.options[0]:
            self.source_current_lesson()
        elif self.selected == self.options[1]:
            self.source_last_two_lessons()
        elif self.selected == self.options[2]:
            self.source_specific_unit()
        elif self.selected == self.options[3]:
            self.source_selected_units()
        elif self.selected == self.options[4]:
            self.source_all_lessons()


lesson = SourceLessons()

_, _, selected = lesson.rofi('Select Option',
                             lesson.options,
                             ['-scroll-method', 1,
                              '-lines', 5,
                              '-markup-rows'])

lesson._update_selection(selected)

lesson.check_selection()
