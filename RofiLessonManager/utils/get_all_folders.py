import ntpath
import os


def get_all_folders(current_course, discourage_folders):
    """
    This function gets all of the folders from the current course location.

    Args:
        current_course (str): The current course location.
        discourage_folders (list): A list of folders to not include.

    Returns:
        folders_here (list): A list of all of the absolute paths to each folder
            that isn't included in the discourage folders parameter.
        folders_tail (list): A list of all of the relative paths to each folder
            that isn't included in the discourage folders parameter.
    """

    # The lists, which we will return later on.
    folders_head = []
    folders_tail = []

    # Getting all of the folders within our current course
    sub_folders = sorted([f.path for f in os.scandir(current_course)
                          if f.is_dir()])

    # Iterating through each folder
    for folder in sub_folders:
        # Splitting the folder into the name and absolute path
        sub_folder_head, sub_folder_tail = ntpath.split(folder)

        # Checking if the folder doesn't equal to one of the folders
        # that we don't want
        if sub_folder_tail not in discourage_folders:
            # Adds the folder to the list of folders we want to return
            folders_head.append('{}/{}'.format(sub_folder_head,
                                sub_folder_tail))
            folders_tail.append(sub_folder_tail)

    return folders_head, folders_tail
