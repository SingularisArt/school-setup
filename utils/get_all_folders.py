import ntpath
import os

from config import config


def get_all_folders():
    """
    This function returns all of the folders in a list.
    It returns them in this order
    folder_head, folder_tail

    folder_head: This is the absolute path to the folder
    folder_tail: This is just the name for the folder
    """

    # The lists, which we will return later on.
    folders_head = []
    folders_tail = []

    # Getting all of the folders within our current course
    sub_folders = sorted([f.path for f in os.scandir(config.current_course)
                          if f.is_dir()])

    # Iterating through each folder
    for folder in sub_folders:
        # Splitting the folder into the name and absolute path
        sub_folder_head, sub_folder_tail = ntpath.split(folder)

        # Checking if the folder doesn't equal to one of the folders
        # that we don't want
        if sub_folder_tail not in config.discourage_folders:
            # Adds the folder to the list of folders we want to return
            folders_head.append('{}/{}'.format(sub_folder_head,
                                sub_folder_tail))
            folders_tail.append(sub_folder_tail)

    return folders_head, folders_tail
