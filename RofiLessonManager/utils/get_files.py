from os import listdir
from os.path import join, isfile


def get_files(path):
    return sorted([file for file in listdir(path) if isfile(join(path, file))])
