#!/usr/bin/env python3

from pathlib import Path

import RofiLessonManager.utils as utils


# Load the data from the config file
data = utils.load_data("~/.config/lesson-manager/config.yaml", "yaml")

# Assign the data to the variables
home = Path(data["home"]).expanduser()
user = data["user"]

calendar_id = data["calendar_id"]
base_url = data["base_url"]
code_dir = Path(data["code_dir"]).expanduser()
editor = data["editor"]
viewer = data["viewer"]
terminal = data["terminal"]

notes_dir = Path(data["notes_dir"]).expanduser()
root = Path(data["root"]).expanduser()
current_course = Path(data["current_course"]).expanduser()
master_file = Path(data["master_file"]).expanduser()
source_lectures_location = Path(data["source_lessons_location"]).expanduser()

assignments_dir = Path(data["assignments_dir"]).expanduser()
graded_assignments_folder = Path(
    data["graded_assignments_folder"]).expanduser()
online_assignments_folder = Path(
    data["online_assignments_folder"]).expanduser()

my_assignments_latex_folder = Path(
    data["my_assignments_latex_folder"]).expanduser()
my_assignments_yaml_folder = Path(
    data["my_assignments_yaml_folder"]).expanduser()
my_assignments_pdf_folder = Path(
    data["my_assignments_pdf_folder"]).expanduser()

rofi_options = data["rofi_options"]
tex_types = data["tex_types"]
discourage_folders = data["discourage_folders"]
folders = data["folders"]

date_format = data["date_format"]

placeholder = utils.get_placeholder(root.name, notes_dir.name)