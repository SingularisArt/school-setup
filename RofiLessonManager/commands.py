#!/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: Mar 06 2022 Sun (02:29:21)

OPTIONS:
    Current Lectures: This one will ask the user to select a unit. Then,
        from that unit, the program will source the last lecture.

    Last Two Lectures: This one will ask the user to select a unit.
        Then, from that unit, the program will source the two lectures.

    All Lectures: This one will just source all of the lectures.

    Range of Lectures: This one will source a range of lectures.
"""

import os

from RofiLessonManager import Basis as Basis
from RofiLessonManager import utils as utils


class SourceLectures(Basis):
    """
    This class will source the lectures.
    """

    def __init__(self):
        """ Initialize the class """

        Basis.__init__(self)

        # The users options
        self.options = [
            "<i><b><span color='yellow'>Current Lecture</span></b></i>",
            "<i><b><span color='yellow'>Last Two Lectures</span></b></i>",
            "<i><b><span color='yellow'>All Lectures</span></b></i>",
        ]

        self.index = 0
        self.selected = self.options[self.index]

    def get_last_two_lectures(self):
        """
        This function will get the last two lectures

        Returns:
            last_lec (str): The last lecture
            sec_lec (str): The second last lecture. If the second last lecture
                doesn't exist, it will return None
        """
        # Iterate through a possible range of lectures
        for i in reversed(range(self.LESSON_RANGE_NUMBER)):
            # If that lecture exists, we're going to make it our last lecture
            if os.path.exists('{}/lectures/lec-{}.tex'.format(
                    self.current_course, i)):
                # If we have only one lecture, we're going to return it and
                # None for the second lecture
                if i == 1:
                    return ['lec-' + str(i), None]
                # If we have more than one lecture, we're going to check to see
                # if we have a second lecture
                else:
                    # If we have a second lecture, we're going to return it
                    if os.path.exists('{}/lectures/lec-{}.tex'.format(
                            self.current_course, i - 1)):
                        return ['lec-' + str(i), 'lec-' + str(i - 1)]
                    # Otherwise, we'll return None for the second lecture
                    else:
                        return ['lec-' + str(i), None]
                break

    def source_current_lecture(self):
        """ This function will source the last lecture """

        with open(self.source_lectures_location, 'w') as source_lectures_file:
            last_lec, _ = self.get_last_two_lectures()
            # Source the last lecture
            source_lectures_file.write('\\input{lectures/' +
                                       last_lec + '}\n')

    def source_last_two_lectures(self):
        """ This function will source the last two lectures """

        with open(self.source_lectures_location, 'w') as source_lectures_file:
            last_lec, sec_lec = self.get_last_two_lectures()
            # Checking if we have a second to last lecture
            if sec_lec:
                # If we do, we're going to source it
                source_lectures_file.write('\\input{lectures/' +
                                           sec_lec + '}\n')
            # Source the last lecture
            source_lectures_file.write('\\input{lectures/' +
                                       last_lec + '}\n')

    def source_all_lectures(self):
        """ This function will source all of the lectures """

        with open(self.source_lectures_location, 'w') as source_lectures_file:
            # Iterate through a possible range of lectures
            for i in range(self.LESSON_RANGE_NUMBER):
                lec = 'lec-' + str(i) + '.tex'

                # Check if that lecture exists
                if os.path.exists('{}/lectures/{}'.format(
                        self.current_course, lec)):
                    # If it does, we're going to source it
                    source_lectures_file.write('\\input{lectures/' +
                                               lec + '}\n')

    def source_range(self, lecture_range):
        """
        This function will source a range of lectures

        Args:
            lecture_range (str): The range of lectures to source (ex: 1-5)
        """

        range_list = lecture_range.split('-')

        with open(self.source_lectures_location, 'w') as source_lectures_file:
            for lecture_number in range(int(range_list[0]),
                                        int(range_list[1]) + 1):
                lec = 'lec-' + str(lecture_number) + '.tex'

                if os.path.exists('{}/lectures/{}'.format(
                        self.current_course, lec)):
                    source_lectures_file.write('\\input{lectures/' +
                                               lec + '}\n')

    def check_selection(self):
        """ This function will check the selection """

        if self.selected == self.options[0]:
            self.source_current_lecture()
        elif self.selected == self.options[1]:
            self.source_last_two_lectures()
        elif self.selected == self.options[2]:
            self.source_all_lectures()
        else:
            self.source_range(self.selected)


def main():
    """ This function will run the program """

    lecture = SourceLectures()

    _, _, selected = utils.rofi('Select Option (You can specify a range: 2-4)',
                                lecture.options,
                                ['-scroll-method', 1,
                                 '-lines', 5,
                                 '-markup-rows'])

    lecture.selected = selected

    lecture.check_selection()


if __name__ == "__main__":
    main()
