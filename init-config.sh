#!/usr/bin/env bash

export DOCUMENTS="$HOME/Documents"
export NOTES_DIR="$DOCUMENTS/school-notes"
export CURRENT_COURSE="$NOTES_DIR/current-course"
export ASSIGNMENTS_DIR="$CURRENT_COURSE/assignments"

echo "Adding configuration template ..."

echo "calendar_id: \"primary\"
base_url: \"URL\"

code_dir: \"$DOCUMENTS/school-setup\"
editor: \"$HOME/.local/bin/dvim\"
viewer: \"sioyek\"
terminal: \"xfce4-terminal\"

notes_dir: \"$DOCUMENTS/school-notes\"
root: \"$NOTES_DIR/College/Year-2/semester-1\"
current_course: \"$NOTES_DIR/current-course\"
master_file: \"$CURRENT_COURSE/master.tex\"
source_lessons_location: \"$CURRENT_COURSE/source-lectures.tex\"

assignments_dir: \"$CURRENT_COURSE/assignments\"
assignments_latex_folder: \"$ASSIGNMENTS_DIR/latex-files\"
assignments_yaml_folder: \"$ASSIGNMENTS_DIR/yaml-files\"
assignments_pdf_folder: \"$ASSIGNMENTS_DIR/pdf-files\"

new_chap: \"False\"
home: \"$HOME\"
user: \"$USER\"

rofi_options:
  - \"-lines\"
  - \"5\"
  - \"-markup-rows\"
  - \"-kb-row-down\"
  - \"Down\"
  - \"-kb-custom-1\"
  - \"Ctrl+n\"

tex_types:
  - \".tex\"
  - \".latex\"

discourage_folders:
  - \"images\"
  - \"assignments\"
  - \"figures\"
  - \"projects\"
  - \".git\"
  - \"media\"
  - \"current-course\"

folders:
  - \"assignments\"
  - \"assignments/image-files\"
  - \"assignments/latex-files\"
  - \"assignments/pdf-files\"
  - \"assignments/yaml-files\"
  - \"lectures\"
  - \"figures\"
  - \"UltiSnips\"" >> ~/.config/lesson-manager/config.yaml
