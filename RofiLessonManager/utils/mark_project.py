#!/usr/bin/env python3

"""
Function mark_project:
    - RofiLessonManager.utils.mark_project

    This function marks the project as complete or incomplete

    Args:
        - project_name (str): The name of the project.
        - status (str): The status of the project.
        - projects_dir (str): The path to the projects directory.
"""


def mark_project(project_name, status, projects_dir):
    """
    This function marks the project as complete or incomplete

    Args:
        - project_name (str): The name of the project.
        - status (str): The status of the project.
        - projects_dir (str): The path to the projects directory.
    """

    # Replace spaces with - and make it lowercase
    project_folder_name = project_name.replace(' ', '-').lower()

    # open the project complete.txt file
    with open('{}/{}/complete.txt'.format(
            projects_dir, project_folder_name), 'w') as complete_file:
        # Write the status to the file
        if status == 'complete':
            complete_file.write('Complete')
        elif status == 'incomplete':
            complete_file.write('Incomplete')
