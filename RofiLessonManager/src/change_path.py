import os

from RofiLessonManager.classes.change_path import ChangePath as ChangePath


def main():
    """
    This function will run the program
    """

    change_path = ChangePath()
    change_path.replace_path(change_path.placeholder, change_path.path)
    os.system('{}/init-config.sh'.format(change_path.code_dir))


if __name__ == "__main__":
    main()
