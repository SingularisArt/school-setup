import os


def create_symlink_class(current_course, class_path):
    """
    Creates a symlink from the given folder to the current class folder.

    Args:
        current_course (str): Path to the current course folder.
        class_path (str): Path to the class folder.
    """

    if os.path.isdir(current_course):
        os.remove(current_course)
    os.symlink(class_path, current_course)
