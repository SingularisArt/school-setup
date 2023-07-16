Managing LaTeX Lecture Notes
============================

## Demos

GO HERE

## Features

- Switch between courses with ease.
- Create lecture notes and assignments one keybinding.
- View the latex code, yaml code and all the pdf files for any assignment in a
  split second.
- Open any lecture note with a twinkle of an eye.
- Sync your notes to the cloud.
- Get notifications when your next class/lab starts.
- Source all lecture notes, the current one, the last two, specific lecture
  notes, or a range of lecture notes.
- Insane keymappings already setup for you.
- Beautiful UI, via Rofi.
- Easy to install.
- Will take about 5 minutes to setup after installation.

## Setup

Run the following install commands:
```bash
git https://github.com/SingularisArt/school-setup/
cd school-setup
./install
```

### Setting up the notes

### Configuration

The configuration file's located at `$HOME/.config/lesson-manager/config.yaml`.
Here are all the variable meanings:

- `calendar_id`: The id of the calendar. By default, it's `primary`.
- `drive_folder_id`: The id of the google drive folder that you want to use to
  sync your notes to.
- `code_dir`: Where you cloned the code to.
- `editor`: The text editor you want to use.
- `terminal`: The terminal you want to use.
- `pdf_viewer`: The pdf viewer you want to use.
- `create_readme_file`: If you want README.md files created when initializing
  courses.
- `notes_dir`: The root directory of your notes.
- `root`: The root directory of your current course notes.
- `templates_dir`: The location to the templates folder.
- `current_course`: The directory you want to use to store the current course.
- `books_dir`: Where you store your books in regards to the current course.
- `figures_dir`: Where you store your figures in regards to the current course.
- `assignments_dir`: The root directory where you store all your assignments in
  regards to the current course.
- `assignments_dir`:
- `graded_assignments_folder`:
- `my_assignments_folder`:
- `online_assignments_folder`:
- `my_assignments_image_folder`:
- `my_assignments_bibtex_folder`:
- `my_assignments_latex_folder`:
- `my_assignments_yaml_folder`:
- `my_assignments_pdf_folder`:
- `date_format`:
- `home`:
- `user`:
- `rofi_options`:
- `folders`:
- `files`:
