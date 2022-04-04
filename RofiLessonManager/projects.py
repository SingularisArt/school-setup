#!/usr/bin/env python3

"""
Author: Hashem Damrah
Date: 2020-04-24
"""

import sys
import glob
import ntpath

from RofiLessonManager import Basis
import RofiLessonManager.utils as utils


class Projects(Basis):
    def __init__(self):
        super().__init__()

        self.options, self.folders, self.projects_head, \
            self.projects_tail = self.get_options()
        self.commands = ['<span color="purple">Open PDF</span>',
                         '<span color="purple">Open Source</span>',
                         '<span color="blue">Open Notes</span>',
                         '<span color="blue">New Chapter</span>',
                         '<span color="brown">Copy PDF to flash drive</span>',
                         '<span color="green">Mark as Complete</span>',
                         '<span color="green">Mark as Incomplete</span>',
                         '<span color="red">Delete</span>',
                         '<span color="yellow">Exit</span>']

        self.rofi_options = [
            '-scroll-method', 1,
            '-lines', 5,
            '-markup-rows',
            '-kb-row-down', 'Down',
            '-kb-custom-1', 'Ctrl+n',
            '-keep-left'
        ]

    def get_options(self):
        """ This function gets all of the projects.

        Returns:
            options (list): The options for the rofi menu.
            folders (list): The folders to look for.
            projects_head (list): The head of the projects.
            projects_tail (list): The tail of the projects.
        """

        # The lists we will return later on
        options = []
        folders = []
        projects_head = []
        projects_tail = []

        # Iterate through all of the projects
        for x, folder in enumerate(glob.iglob('{}/*'.format(self.projects_dir),
                                   recursive=True)):
            # Split the project path
            project_head, project_tail = ntpath.split(folder)

            # Replace - with space
            option = project_tail.replace('-', ' ').title()

            # Get the status of the project
            complete_status = utils.get_folder_status(folder)

            # Append the project to the options
            # Here's how the format will look like:
            #       1. Project Name         Status: Incomplete
            # If the project is complete, the status color will be green.
            # If the project is incomplete, the status color will be red.
            current_option = "<span color='red'>{number: >2}</span>. " \
                "<b><span color='blue'>{project: <{fill}}</span></b>" \
                "<i><span color='yellow' size='smaller'>" \
                "Status:</span></i> " \
                "<i><span color='{color}' size='smaller'>{complete}" \
                "</span></i>".format(
                    fill=35,
                    number=str(int(x) + 1),
                    project=option,
                    color='green' if complete_status == 'Complete' else 'red',
                    complete=complete_status)

            # Append the option to the options
            options.append(current_option)
            # Append the project name to the folders
            folders.append(option)

            # Append the project head and tail
            projects_head.append(project_head)
            projects_tail.append(project_tail)

        # Return the needed data
        return options, folders, projects_head, projects_tail

    def run_func_based_on_command(self, command, project_name):
        """
        This function runs the function based on the command.

        Args:
            command (str): The command.
            project_name (str): The name of the project.
        """

        # Run the function based on the command
        if command == '<span color="purple">Open PDF</span>':
            utils.open_pdf(project_name, self.projects_dir)
        elif command == '<span color="purple">Open Source</span>':
            utils.open_source(project_name, self.projects_dir)
        elif command == '<span color="blue">Open Notes</span>':
            utils.open_notes(project_name, self.projects_dir)
        elif command == '<span color="blue">New Chapter</span>':
            utils.chapter(project_name, self.projects_dir, self.rofi_options)
        elif command == '<span color="brown">Copy PDF to flash drive</span>':
            utils.copy_pdf(project_name, self.projects_dir, self.rofi_options,
                           self.user)
        elif command == '<span color="green">Mark as Complete</span>':
            utils.mark_project(project_name, 'complete', self.projects_dir)
        elif command == '<span color="green">Mark as Incomplete</span>':
            utils.mark_project(project_name, 'incomplete', self.projects_dir)
        elif command == '<span color="red">Delete</span>':
            utils.delete(project_name, self.projects_dir, self.rofi_options)
        elif command == '<span color="yellow">Exit</span>':
            sys.exit()


def main():
    projects = Projects()

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
