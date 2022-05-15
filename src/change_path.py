import os

from RofiLessonManager.path import Path as Path


def main():
    """
    This function will run the program
    """

    change_path = Path()
    change_path.replace_path(change_path.placeholder, change_path.path)
    os.system('{}/init-config.sh'.format(change_path.code_dir))


if __name__ == "__main__":
    main()
