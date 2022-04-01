#!/usr/bin/env python3


import subprocess

from RofiLessonManager import Basis
from RofiLessonManager import utils as utils


class Scripts(Basis):
    def __init__(self):
        super().__init__()

        self.scripts = [
            'rofi-compile.sh',
            'rofi-file-browser.sh',
            'rofi-inkscape.sh',
            'rofi-nvim.sh',
            'rofi-source-code.sh',
            'rofi-web-browser.sh',
            'rofi-yaml.sh',
            'rofi-zathura.sh',
        ]
        self.scripts_with_style = [
            '<span color="blue">Compile</span>',
            '<span color="blue">File Browser</span>',
            '<span color="blue">Inkscape</span>',
            '<span color="blue">Nvim</span>',
            '<span color="blue">Source Code</span>',
            '<span color="blue">Web Browser</span>',
            '<span color="blue">Yaml</span>',
            '<span color="blue">Zathura</span>',
        ]

        self.file_to_run = self.ask_user_for_which_script_to_run()
        print(self.file_to_run)

    def ask_user_for_which_script_to_run(self):
        _, index, _ = utils.rofi('Select Which program to run',
                                 self.scripts_with_style,
                                 self.rofi_options)
        return 'RofiLessonManager/bash-stand-alones/{}'.format(
                self.scripts[index])

    def run_file(self):
        subprocess.run('{}/{}'.format(self.code_dir, self.file_to_run),
                       shell=True)


scripts = Scripts()
scripts.run_file()
