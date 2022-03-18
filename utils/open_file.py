import os

from config import config


def _open_file(unit, lesson):
    os.system('xfce4-terminal -e "{} {}"'.format(config.editor,
              '{}/{}/lesson-{}.tex'.format(
                config.current_course,
                unit,
                lesson)))
