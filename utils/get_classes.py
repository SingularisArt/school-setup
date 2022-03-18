import os

from config import config


def _get_classes():
    return sorted([os.path.join(config.root, o)
                   for o in os.listdir(config.root)
                   if os.path.isdir(os.path.join(config.root, o))])
