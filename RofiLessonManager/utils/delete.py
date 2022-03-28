import os

from RofiLessonManager.utils import rofi


def delete(project_name, projects_dir, rofi_options):
    """
    Delete the project.

    Args:
        project_name (str): The name of the project.
        projects_dir (str): The path to the projects directory.
        rofi_options (list): The rofi options.
    """

    # Ask for confirmation
    options = ['<span color="red">No</span>',
               '<span color="red">Yes</span>']

    _, _, answer = rofi('Are you sure', options,
                        rofi_options)

    # If yes, delete the project
    if answer == options[1]:
        # Replace spaces with - and make it lowercase
        project_folder_name = project_name.replace(' ', '-').lower()

        # Delete the project folder
        os.system('rm -rf {}/{}'.format(projects_dir,
                                        project_folder_name))
