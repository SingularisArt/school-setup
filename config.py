#!/usr/bin/env python3

from pathlib import Path

import RofiLessonManager.utils as utils


# Load the data from the config file
data = utils.load_data("~/.config/lesson-manager/config.yaml", "yaml")

# Assign the data to the variables
home = Path(data["home"]).expanduser()
user = data["user"]

calendar_id = data["calendar_id"]
code_dir = Path(data["code_dir"]).expanduser()
editor = data["editor"]
terminal = data["terminal"]
terminal_commands = data["terminal_commands"]
pdf_viewer = data["pdf_viewer"]

notes_dir = Path(data["notes_dir"]).expanduser()
root = Path(data["root"]).expanduser()
templates_dir = Path(data["templates_dir"]).expanduser()
current_course = Path(data["current_course"]).expanduser()
current_course_watch_file = Path("/tmp/current_course").expanduser()

assignments_dir = Path(data["assignments_dir"]).expanduser()
graded_assignments_folder = Path(
    data["graded_assignments_folder"],
).expanduser()
online_assignments_folder = Path(
    data["online_assignments_folder"],
).expanduser()

my_assignments_image_folder = Path(
    data["my_assignments_image_folder"],
).expanduser()
my_assignments_latex_folder = Path(
    data["my_assignments_latex_folder"],
).expanduser()
my_assignments_yaml_folder = Path(
    data["my_assignments_yaml_folder"],
).expanduser()
my_assignments_pdf_folder = Path(
    data["my_assignments_pdf_folder"],
).expanduser()

rofi_options = data["rofi_options"]
files = data["files"]
folders = data["folders"]

date_format = data["date_format"]
