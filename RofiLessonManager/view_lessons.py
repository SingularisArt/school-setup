#!/usr/bin/env python3

import re
import os

from RofiLessonManager import Basis as Basis
import RofiLessonManager.utils as utils


class ViewLectures(Basis):
    """
    This class will allow us to view the lectures in the current course.
    """

    def __init__(self):
        """ Initialize the class """

        Basis().__init__()

        self.folders_head, self.folders_tail = utils.get_all_folders(
            self.current_course, self.discourage_folders)
        self.units_head, self.units_tail = utils.get_all_units(
            self.folders_head)
        self.options, \
            self.lecture_numbers, \
            self.lecture_dates, self.lecture_names = self.get_lecture_info()

    def get_first_line(self, file):
        """
        This function gets the first line of a file

        Args:
            file (str): The absolute path to the file
                NOTE: You shouldn't have this file opened already
                      It should just the be the name of the file

        Returns:
            str: The first line of the file
        """

        # Open the file
        file_opened = open(file)
        # Iterate through all of the lines
        for line in file_opened.readlines():
            # Return the first one
            return line

    def get_lecture_info(self):
        """
        This function will get all of the lecture information

        Returns:
            options (list): The options for the rofi menu
            lecture_numbers (list): The lecture numbers
            lecture_dates (list): The lecture dates
            lecture_names (list): The lecture names
        """

        # Initialize the variables that we will return later
        options = []
        lecture_numbers = []
        lecture_dates = []
        lecture_names = []

        # Iterate through a possible range of lectures
        for lecture_number in range(self.LESSON_RANGE_NUMBER):
            lecture = '{}/lec-{}.tex'.format(self.units_head[0],
                                             lecture_number)

            # If the lecture exists
            if os.path.isfile(lecture):
                # Opening the file
                with open(lecture, encoding='utf8'):
                    # Getting the first line
                    first_line = self.get_first_line(lecture)
                    try:
                        # Performing regex on the first line to get the needed
                        # information
                        lecture_match = re.search(self.lecture_regex,
                                                  first_line)

                        # Getting the needed information into variables
                        lecture_number = lecture_match.group(1)
                        lecture_date = lecture_match.group(2)
                        lecture_name = lecture_match.group(3)

                        # Appending the information to the lists
                        lecture_numbers.append(lecture_number)
                        lecture_dates.append(lecture_date)
                        lecture_names.append(lecture_name)

                        # Appending the options to the list
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

        # Returning the variables
        return options, lecture_numbers, lecture_dates, \
            lecture_names


def main():
    """ This function will run the program """

    lecture = ViewLectures()

    key, index, selected = utils.rofi('Select Lesson', lecture.options,
                                      lecture.rofi_options)
    utils.open_file(lecture.terminal, lecture.editor,
                    lecture.current_course, lecture.lecture_numbers[index])


if __name__ == "__main__":
    main()
