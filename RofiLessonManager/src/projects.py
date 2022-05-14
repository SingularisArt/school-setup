import sys

from RofiLessonManager.classes.projects import Projects as Projects
import RofiLessonManager.utils as utils


def main():
    projects = Projects()

    key, index, selected = utils.rofi('Select project',
                                      projects.rofi_names,
                                      projects.rofi_options)

    if index < 0:
        sys.exit()

    key_command, index_command, \
        selected_command = utils.rofi(
            'Select command for the ' +
            '{} project'.format(
                projects[index].name),
            projects.commands,
            projects.rofi_options)

    projects.run_func_based_on_command(selected_command,
                                       projects[index].name)


if __name__ == "__main__":
    main()
