#!/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: Mar 06 2022 Sun (02:29:21)

OPTIONS:
    Current Lesson: This one will ask the user to select a unit. Then,
        from that unit, the program will source the last lecture.

    Last Two Lessons: This one will ask the user to select a unit.
        Then, from that unit, the program will source the two lectures.

    All Lessons From in Unit: This one will ask the user to select a
        unit Then, the program will ask if he wants to source all
        lectures. The user can specify a range of lectures to source. The
        program will only source the lectures that exist.

    Source Selected Units: This one will give the user the list of all the
        units available. The user can select the units he wants to source. Then
        the program sources all of the lectures in each of the unit selected.
        IT'S COMING SOON!

    All Lessons: This one will just source all of the lectures.
"""

import os
from config import Configuration


class SourceLessons(Configuration):
    """
    Class for different ways to source your lectures.
    It's inherited from the config.py/Configuration class

    Methods:
    --------

    """

    def __init__(self):
        Configuration.__init__(self)

        """ This function initializes the class """

        # The users options
        self.options = [
            "<i><b><span color='yellow'>Current lecture</span></b></i>",
            "<i><b><span color='yellow'>Last two lectures</span></b></i>",
            "<i><b><span color='yellow'>All lectures in Unit</span></b></i>",
            "<i><b><span color='yellow'>Select Multiple Units</span></b></i>",
            "<i><b><span color='yellow'>All lectures</span></b></i>",
        ]

        self.index = 0
        self.selected = self.options[self.index]

    def source_current_lecture(self):
        with open(self.source_lectures_location, 'w') as source_lectures_file:
            # It writes this as an example: % Unit 1 Started
            source_lectures_file.write('% Unit {} Started\n'.format(
                self.last_unit_number))

            # Source the last lecture
            source_lectures_file.write('\\input{' + self.last_unit_name + '/' +
                                      self.last_lecture_tail + '}\n')

            # It writes this as an example: % Unit 1 Ended
            source_lectures_file.write('% Unit {} Ended'.format(
                self.last_unit_number))

    def source_last_two_lectures(self):
        # We're checking if we have a second to last lecture
        if self.second_to_last_lecture_head != 'NONE':
            # If we do, then we're going to write the last and second last
            # lecture to the source file
            with open(self.source_lectures_location, 'w') as \
                    source_lectures_file:
                # It writes this as an example: % Unit 1 Started
                source_lectures_file.write('% Unit {} Started\n'.format(
                    self.last_unit_number))

                # Source second to last lecture
                source_lectures_file.write('\\input{' + self.last_unit_name +
                                           '/' + self.second_to_last_lecture_tail
                                           + '}\n')
                # Source last lecture
                source_lectures_file.write('\\input{' + self.last_unit_name +
                                          '/' + self.last_lecture_tail + '}\n')

                # It writes this as an example: % Unit 1 Ended
                source_lectures_file.write('% Unit {} Ended'.format(
                    self.last_unit_number))
        # If we don't, we'll just source the last lecture
        else:
            self.source_current_lecture()

    def source_all_lectures_in_unit(self, unit):
        with open(self.source_lectures_location, 'w') as source_lectures_file:
            # This is complicated to explain. When I just iterated through
            # a list of all the lectures, it would output something like this:
            # lecture-1.tex lecture-10.tex lecture-2.tex lecture-3.tex
            # It would make big leaps like that. So, we create a forloop using
            # this number and we check if the lectures exists. Example:
            # lecture-1.tex, lecture-2.tex, lecture-3.tex, lecture-4.tex
            # If that exists, then we will write this:
            # \input{unit-1/lecture-1.tex}
            lecture_range_to_source = 1000

            # Iterating through the lecture_range_to_source variable
            for i in range(lecture_range_to_source):
                # The path to the lecture
                lecture_name = "lectures/lec-{}.tex".format(i)
                # Checking if the lecture exists
                if os.path.exists(lecture_name):
                    # If it does, then write it to the source_lectures file.
                    # Example: \input{lectures/lec-1.tex}
                    input_string = '\\input{lectures/' + '/lec-' + str(i) + \
                                   '.tex}\n'
                    source_lectures_file.write(input_string)

    def source_range(self, lecture_range, unit_number):
        range_list = lecture_range.split('-')

        unit_info_path = self.current_course + '/source-lectures.tex'

        with open(unit_info_path, 'w') as source_lectures_file:
            for lecture_number in range(int(range_list[0]),
                                        int(range_list[1]) + 1):
                # Check if lecture exists
                if os.path.exists('{}/{}/lecture-{}.tex'.format(
                            self.current_course, unit_number, lecture_number)):
                    # Write to the source-lectures.tex file
                    string = '\\input{' + unit_number + '/lecture-' + \
                             str(lecture_number) + '.tex}\n'

                    source_lectures_file.write(string)

            source_lectures_file.write('% Unit {} Ended'.format(
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
                len(self.all_lectures[unit]) - 1),
            selection,
            ['-scroll-method', 1,
             '-lines', 5,
             '-markup-rows']
        )

        if selected != selection[0]:
            self.source_range(selected, unit)
        else:
            self.source_all_lectures_in_unit(unit)

    def source_selected_units(self):
        self.r.status('Coming Soon ...')

    def source_all_lectures(self):
        with open(self.source_lectures_location, 'w') as source_lectures_file:
            for x, lecture in enumerate(self.all_lectures.values()):
                current_unit = self.units_tail[x]

                source_lectures_file.write('\\input{lectures/' +
                                           self.unit_info_name + '}\n')

                for les in range(1000):
                    if os.path.exists('{}/{}/lecture-{}.tex'.format(
                            self.current_course, current_unit, les)):
                        source_lectures_file.write('\\input{lectures/' +
                                                   '/lec-' + str(les) +
                                                   '.tex}\n')

    def check_selection(self):
        if self.selected == self.options[0]:
            self.source_current_lecture()
        elif self.selected == self.options[1]:
            self.source_last_two_lectures()
        elif self.selected == self.options[2]:
            self.source_specific_unit()
        elif self.selected == self.options[3]:
            self.source_selected_units()
        elif self.selected == self.options[4]:
            self.source_all_lectures()


lecture = SourceLessons()

_, _, selected = lecture.rofi('Select Option',
                              lecture.options,
                              ['-scroll-method', 1,
                               '-lines', 5,
                               '-markup-rows'])

lecture._update_selection(selected)

lecture.check_selection()
