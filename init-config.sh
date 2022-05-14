#!/usr/bin/env bash

echo "Removing config.yaml ..."

source ~/.config/zsh/exports.zsh
true > config.yaml

echo "Adding configuration template ..."

echo "calendar_id: primary
code_dir: $(pwd)
editor: nvim
viewer: zathura
terminal: xfce4-terminal
notes_dir: ${HOME}/Documents/school-notes
root: ${ROOT}
current_course: ${HOME}/Documents/school-notes/current-course
master_file: ${HOME}/Documents/school-notes/current-course/master.tex
source_lessons_location: ${HOME}/Documents/school-notes/current-course/source-lectures.tex
projects_dir: ${HOME}/Documents/school-notes/projects
assignments_dir: ${HOME}/Documents/school-notes/current-course/assignments
assignments_folder: ${HOME}/Documents/school-notes/current-course/assignments/latex-files
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
  - current-course" >> config.yaml
  

mkdir -p ~/.config/lesson-manager/
rm -rf ~/.config/lesson-manager/config.yaml
cp $(pwd)/config.yaml ~/.config/lesson-manager/config.yaml
