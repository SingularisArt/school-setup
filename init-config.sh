#!/usr/bin/env bash

echo "Removing config.yaml ..."

true > config.yaml

echo "editor: nvim
viewer: zathura
terminal: xfce4-terminal
notes_dir: ${HOME}/Documents/notes
root: ${HOME}/Documents/notes/Grade-10/semester-2
current_course: ${HOME}/Documents/notes/current-course
source_lessons_location: ${HOME}/Documents/notes/current-course/source-lessons.tex
projects_dir: ${HOME}/Documents/notes/projects
unit_info_name: unit-info.tex
new_chap: False
home: ${HOME}
user: ${USER}
LESSON_RANGE_NUMBER: 1000

rofi_options:
  - -lines
  - 5
  - -markup-rows
  - -kb-row-down
  - Down
  - -kb-custom-1
  - Ctrl+n

tex_types:
  - .tex
  - .latex

discourage_folders:
  - images
  - assignments
  - figures
  - projects
  - .git
  - media
  - current-course
" >> config.yaml
