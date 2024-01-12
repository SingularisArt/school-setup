from pathlib import Path

import utils

# Load the data from the config file
data = utils.load_data("~/.config/lesson-manager/config.yaml", "yaml")

# Assign the data to the variables
home = Path(data["home"]).expanduser()
user = data["user"]

create_readme_file = data["create_readme_file"]
highlight_current_course = data["highlight_current_course"]

calendar_id = data["calendar_id"]
drive_folder_id = data["drive_folder_id"]
editor = data["editor"]
terminal = data["terminal"]
pdf_viewer = data["pdf_viewer"]

notes_dir = Path(data["notes_dir"]).expanduser()
root = Path(data["root"]).expanduser()
templates_dir = Path(data["templates_dir"]).expanduser()
current_course = Path(data["current_course"]).expanduser()
current_course_watch_file = Path("~/.local/share/current_course").expanduser()

books_dir = current_course / Path(data["books_dir"]).expanduser()
figures_dir = current_course / Path(data["figures_dir"]).expanduser()

assignments_dir = current_course / Path(data["assignments_dir"]).expanduser()
assignment_folders = {
    folder: assignments_dir / Path(data["assignment_folders"][folder])
    for folder in data["assignment_folders"]
}

rofi_options = data["rofi_options"]
files = data["files"]
folders = data["folders"]

date_format = data["date_format"]
