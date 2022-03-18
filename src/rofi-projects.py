#!/usr/bin/env python3

"""
Author: Hashem Damrah
Date: 2020-04-24
"""

import os
import sys
import glob
import ntpath


class Projects:
    """
    Attributes:
        home: The home directory of the user
        tex_types: The types of tex files to look for
        new_chap: The name of the new chapter file
        discourage_folders: The folders to not look for
        rofi: The rofi command
        editor: The editor to open the new chapter file
        terminal: The terminal to open the new chapter file
        notes_dir: The directory to look for notes
        root: The root directory of the school
        current_course: The current course being worked on
        projects_dir: The directory to look for projects
        source_lesson_location: The location of the source lessons
        commands: The commands to be used in the rofi menu
        rofi_options: The options to be used in the rofi menu

    Methods:
        _get_folder_status: Gets the status of the project
        _get_options: Gets all of the projects
        _commands: Returns a list of possible commands
        _get_flash_drives: Gets all of the flash drives

        open_pdf: Opens the pdf of the project
        open_source: Opens the source of the project
        open_notes: Opens the notes of the project
        chapter: Creates a new chapter
        mark_project_complete: Marks the project as complete/incomplete
        delete: Deletes the project
    """

    def __init__(self):
        """ Initialize the class """

        self.home = os.path.expanduser('~')
        sys.path.insert(0, '{}/Singularis/local/scripts/school/'.format(
            self.home))

        from config import tex_types, new_chap, discourage_folders, rofi, r
        from config import EDITOR, TERMINAL, NOTES_DIR, ROOT
        from config import CURRENT_COURSE, SOURCE_LESSONS_LOCATION

        self.tex_types = tex_types
        self.new_chap = new_chap
        self.discourage_folders = discourage_folders

        self.rofi = rofi
        self.r = r

        self.editor = EDITOR
        self.terminal = TERMINAL
        self.notes_dir = NOTES_DIR
        self.root = ROOT
        self.current_course = CURRENT_COURSE
        self.projects_dir = str(self.notes_dir) + '/projects'
        self.source_lesson_location = SOURCE_LESSONS_LOCATION

        self.user = os.getenv('USER')

        self.options, self.folders, self.projects_head, \
            self.projects_tail = self._get_options()
        self.commands = self._commands()

        self.rofi_options = [
            '-scroll-method', 1,
            '-lines', 5,
            '-markup-rows',
            '-kb-row-down', 'Down',
            '-kb-custom-1', 'Ctrl+n',
            '-keep-left'
        ]

    def _get_folder_status(self, folder):
        """ This folder gets the status of the project

        Args:
            folder (str): The folder to get the status of

        Returns:
            str: The status of the project
        """

        try:
            # Try to get the status of the project
            with open(folder + '/complete.txt', 'r') as file:
                return file.read()

        except FileNotFoundError:
            # If we fail, create the file, write and return incomplete
            with open(folder + '/complete.txt', 'w') as file:
                file.write('Incomplete')
                return 'Incomplete'

    def _get_options(self):
        """ This function gets all of the projects

        Returns:
            options         (list): The options for the rofi menu
            folders         (list): The folders to look for
            projects_head   (list): The head of the projects
            projects_tail   (list): The tail of the projects
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
            complete_status = self._get_folder_status(folder)

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

    def _commands(self):
        """ This function just returns a list of possible commands """

        # Return the commands
        return ['<span color="purple">Open PDF</span>',
                '<span color="purple">Open Source</span>',
                '<span color="blue">Open Notes</span>',
                '<span color="blue">New Chapter</span>',
                '<span color="brown">Copy PDF to flash drive</span>',
                '<span color="green">Mark as Complete</span>',
                '<span color="green">Mark as Incomplete</span>',
                '<span color="red">Delete</span>',
                '<span color="yellow">Exit</span>',
                '<span color="yellow">Back</span>']

    def _get_flash_drives(self, project_name):
        """ This function gets all of the flash drives that's connected
            to the computer/laptop/etc """

        # List all flash drives
        # drives = [x for x in os.listdir('/run/media/{}'.format(self.user))]
        drives = [x for x in os.listdir('/run/media/hashem/')]

        if not drives:
            self.r.error('No Flash Drives Found')
            exit(1)

        drives_with_style = []

        for drive in drives:
            new_drive = '<span color="brown">{}</span>'.format(drive)
            drives_with_style.append(new_drive)

        return drives, drives_with_style

    def open_pdf(self, project_name):
        """ This function opens the pdf of the project

        Args:
            project_name (str): The name of the project
        """

        # Replace spaces with - and make it lowercase
        project_folder_name = project_name.replace(' ', '-').lower()

        # Open the pdf
        os.system('zathura {}/{}/master.pdf'.format(self.projects_dir,
                                                    project_folder_name))

    def open_source(self, project_name):
        """ This function opens the source of the project

        Args:
            project_name (str): The name of the project
        """

        # Replace spaces with - and make it lowercase
        project_folder_name = project_name.replace(' ', '-').lower()

        # Open source code
        os.system('xfce4-terminal -e "nvim {}/{}"'.format(self.projects_dir,
                                                          project_folder_name))

    def open_notes(self, project_name):
        """ This function opens the notes of the project

        Args:
            project_name (str): The name of the project
        """

        # Replace spaces with - and make it lowercase
        project_folder_name = project_name.replace(' ', '-').lower()

        # Open notes
        os.system('xfce4-terminal -e "nvim {}/{}/notes.md"'.format(
            self.projects_dir, project_folder_name))

    def chapter(self, project_name):
        """ This function creates a new chapter.
            It then asks the user if they want to open the new chapter in the
            text editor.

        Args:
            project_name (str): The name of the project
        """

        # Replace spaces with - and make it lowercase
        project_folder_name = project_name.replace(' ', '-').lower()

        # Create the path to the project
        project_path = '{}/{}'.format(self.projects_dir,
                                      project_folder_name)

        # Get the last chapter number and then increment it by one
        chap_number = int([f for f in os.listdir(project_path + '/chapters')
                           if os.path.isfile(os.path.join(
                                             project_path + '/chapters',
                                             f))][-1][4:-4]) + 1

        # Create new chapter
        os.system('touch {}/chapters/chap{}.tex'.format(project_path,
                                                        chap_number))

        # Ask if the user wants to open the new chapter
        options = ['<span color="red">Yes</span>',
                   '<span color="red">No</span>']

        _, _, answer = projects.rofi('Are you sure', options,
                                     self.rofi_options)

        if answer == options[0]:
            # Open the new chapter
            os.system('xfce4-terminal -e "nvim {}/chapters/chap{}.tex"'.format(
                project_path, chap_number))

    def copy_pdf(self, project_name):
        """ This function copies the pdf of the project to the flash drive

        Args:
            project_name (str): The name of the project
        """

        # Get all flash drives
        drives, drives_with_style = self._get_flash_drives(project_name)

        # Ask the user which drive to use via rofi
        _, index, _ = self.rofi('Select command',
                                drives_with_style,
                                self.rofi_options)

        project_name = project_name.replace(' ', '-').lower()

        master_path = '{}/{}/master.pdf'.format(self.projects_dir,
                                                project_name)
        drive_path = '/run/media/{}/{}/'.format(self.user, drives[index])

        try:
            os.system('cp -r {} {}'.format(master_path, drive_path))
        except Exception:
            self.r.error('Couldn\'t move master.pdf to {}'.format(drive_path))
            exit(1)

        self.r.error('Copied master.pdf to {}'.format(drive_path))

    def mark_project(self, project_name, status):
        """ This function marks the project as complete or incomplete

        Args:
            project_name (str): The name of the project
            status (str): The status of the project
        """

        # Replace spaces with - and make it lowercase
        project_folder_name = project_name.replace(' ', '-').lower()

        # open the project complete.txt file
        with open('{}/{}/complete.txt'.format(
                self.projects_dir, project_folder_name), 'w') as complete_file:
            # Write the status to the file
            if status == 'complete':
                complete_file.write('Complete')
            elif status == 'incomplete':
                complete_file.write('Incomplete')

    def delete(self, project_name):
        """ This function deletes the project

        Args:
            project_name (str): The name of the project
        """

        # Ask for confirmation
        options = ['<span color="red">No</span>',
                   '<span color="red">Yes</span>']

        _, _, answer = projects.rofi('Are you sure', options,
                                     self.rofi_options)

        # If yes, delete the project
        if answer == options[1]:
            # Replace spaces with - and make it lowercase
            project_folder_name = project_name.replace(' ', '-').lower()

            # Delete the project folder
            os.system('rm -rf {}/{}'.format(self.projects_dir,
                                            project_folder_name))

    def run_func_based_on_command(self, command, project_name):
        """ This function runs the function based on the command

        Args:
            command (str): The command
            project_name (str): The name of the project
        """

        # Run the function based on the command
        if command == '<span color="purple">Open PDF</span>':
            self.open_pdf(project_name)
        elif command == '<span color="purple">Open Source</span>':
            self.open_source(project_name)
        elif command == '<span color="blue">Open Notes</span>':
            self.open_notes(project_name)
        elif command == '<span color="blue">New Chapter</span>':
            self.chapter(project_name)
        elif command == '<span color="brown">Copy PDF to flash drive</span>':
            self.copy_pdf(project_name)
        elif command == '<span color="green">Mark as Complete</span>':
            self.mark_project(project_name, 'complete')
        elif command == '<span color="green">Mark as Incomplete</span>':
            self.mark_project(project_name, 'incomplete')
        elif command == '<span color="red">Delete</span>':
            self.delete(project_name)
        elif command == '<span color="yellow">Exit</span>':
            sys.exit()
        elif command == '<span color="yellow">Back</span>':
            Main()


def Main():
    projects = Projects()

    key, index, selected = projects.rofi('Select project', projects.options,
                                         projects.rofi_options)

    key_command, index_command, \
        selected_command = projects.rofi(
                                         'Select command for the ' +
                                         '{} project'.format(
                                            projects.folders[index]),
                                         projects.commands,
                                         projects.rofi_options)

    projects.run_func_based_on_command(selected_command,
                                       projects.folders[index])

    return projects


if __name__ == "__main__":
    projects = Main()
