#!/usr/bin/env python3

from rofi import Rofi
import os

from RofiLessonManager import Basis as Basis
# import RofiLessonManager.utils as utils


class ChangePath(Basis):
    """
    This class will allow us to view the lectures in the current course.
    """

    def __init__(self):
        """ Initialize the class """

        Basis.__init__(self)

        self.theme = \
            'entry { placeholder: "' + self.placeholder + '"; ' + \
            'placeholder-color: grey; }'

        self.path = self.get_path()
        self.replace_path(self.placeholder, self.path)

    def get_path(self):
        options = ['-theme-str', self.theme]
        r = Rofi(rofi_args=options)

        return r.text_entry('New Path')

    def replace_path(self, placeholder, path):
        """
        Replace the current path with the new path.
        """

        file = open('{}/.config/zsh/exports.zsh'.format(self.home), 'r')
        replacement = ''

        for line in file:
            line = line.strip()
            changes = line.replace(placeholder, path)

            replacement += changes + '\n'

        file.close()

        fout = open('{}/.config/zsh/exports.zsh'.format(self.home), 'w')
        fout.write(replacement)
        fout.close()

    def create_new_config(self, new_path):
        """
        Create a new config file.
        """


def main():
    """ This function will run the program """

    change_path = ChangePath()
    # change_path.replace_path(change_path.placeholder, change_path.path)
    os.system('{}/init-config.sh'.format(change_path.code_dir))


if __name__ == "__main__":
    main()
