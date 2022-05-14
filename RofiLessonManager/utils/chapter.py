import os

from RofiLessonManager.utils.rofi import rofi


def chapter(project_name, projects_dir, rofi_options):
    """
    This function creates a new chapter.
    It then asks the user if they want to open the new chapter in the
    text editor.

    Args:
        project_name (str): The name of the project.
        projects_dir (str): The path to the projects directory.
        rofi_options (list): The rofi options.
    """

    # Replace spaces with - and make it lowercase
    project_folder_name = project_name.replace(' ', '-').lower()

    # Create the path to the project
    project_path = '{}/{}'.format(projects_dir,
                                  project_folder_name)

    # Get the last chapter number and then increment it by one
    try:
        chap_number = int(sorted([f for f in os.listdir(
            project_path + '/chapters')
            if os.path.isfile(os.path.join(
                project_path + '/chapters', f))])[-1][4:-4]) + 1
    except Exception:
        chap_number = 1

    with open('{}/chapters/chap-{}.tex'.format(project_path, chap_number), 'w'):
        pass

    # Ask if the user wants to open the new chapter
    options = ['<span color="red">Yes</span>',
               '<span color="red">No</span>']

    _, _, answer = rofi('Do you want to open the new chapter', options,
                        rofi_options)

    if answer == options[0]:
        # Open the new chapter
        os.system('xfce4-terminal -e "nvim {}/chapters/chap-{}.tex"'.format(
            project_path, chap_number))
