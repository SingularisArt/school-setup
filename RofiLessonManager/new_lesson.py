# !/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: Jan 23 2022 Sun (00:45:44)
This class is used to create a rofi menu for the user to select a command
to execute.
"""

from datetime import datetime
import os
from rofi import Rofi

from RofiLessonManager import Basis as Basis
from RofiLessonManager import utils as utils


class NewLesson(Basis):
    """
    This class will help you create lectures
    """

    def __init__(self):
        """ This function initializes the class """

        Basis.__init__(self)

        now = datetime.now()
        self.date = now.strftime('%b %d %Y %a (%H:%M:%S)')
        self.write_info()

    def template(self, lec_number, lec_name):
        return f"""\\lesson{{{lec_number}}}{{{self.date}}}{{{lec_name}}}



\\newpage"""

    def write_info(self):
        rofi = Rofi()

        lec_number = rofi.integer_entry('Enter Lecture Number')
        if not lec_number:
            exit(1)
        lec_path = '{}/lectures/lec-{}.tex'.format(self.current_course,
                                                   lec_number)
        if os.path.exists(lec_path):
            yes_no = ['<span color="#00ff00">No</span>',
                      '<span color="#ff0000">Yes</span>']

            rofi.error('Lecture already exists')

            _, _, confirm = utils.rofi('Would you like to overwrite this file',
                                       yes_no, self.rofi_options)

            if confirm == yes_no[0]:
                return

        lec_name = rofi.text_entry('Enter Lecture Name')
        if not lec_name:
            exit(1)

        with open('{}/lectures/lec-{}.tex'.format(
                self.current_course, lec_number), 'w') as file:
            file.write(self.template(lec_number, lec_name))


def main():
    NewLesson()


if __name__ == "__main__":
    main()
