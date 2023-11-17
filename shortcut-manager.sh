#!/bin/bash

key="$1"
root="$HOME/Documents"

school_notes_root="$root/school-notes"
current_course="$school_notes_root/current-course"
papers="$current_course/papers"
master_pdf="$current_course/master.pdf"

rofi() {
  /usr/bin/rofi -markup-rows -kb-row-down Down -kb-custom-1 Ctrl+n -no-fixed-num-lines "$@"
}

open_research_paper() {
  cd "$papers" || exit
  pdf_file="$(find . -maxdepth 1 -type f | grep -v "README.md" | rofi -i -dmenu -window-title "Select paper")"
  [ "$pdf_file" = "" ] && exit 0
  ([ -f "$pdf_file" ] && zathura "$(realpath "$pdf_file")") || google-chrome-stable --profile-directory="Profile 2" --app="https://google.com/search?q=$pdf_file"
}

get_figure_folders() {
  declare -A figure_folders
  for file in $(find "$current_course/figures/" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort); do
    new_string=$(echo "$file" | sed -e "s/lec-/Lecture /" -e "s/chap-/Chapter /" -e "s/\b0\+\([1-9][0-9]*\)/\1/")
    figure_folders["$new_string"]="$file"
  done

  declare -p figure_folders
}

list_online_notes() {
  declare -A note_files
  declare -A annotated_files
  declare -A blank_files

  for file in $(find "$current_course/online-lecture-notes/" -mindepth 1 -maxdepth 1 -type f -exec basename {} \; | sort); do
    if [[ "$file" != *.pdf ]]; then
      continue
    fi

    note_num=$(echo "$file" | sed -s "s/[^0-9]//g")
    new_string=$(echo "$file" | sed -e "s/lec-/Lecture /" -e "s/chap-/Chapter /" -e "s/.pdf//" -e "s/\b0\+\([1-9][0-9]*\)/\1/" -e 's/-/ /g' -e 's/\b\(.\)/\u\1/g')

    file="$current_course/online-lecture-notes/$file"

    if [[ "$file" == *annotated* ]]; then
      annotated_files["$note_num"]="$file"
    elif [[ "$file" == *blank* ]]; then
      blank_files["$note_num"]="$file"
    fi

    new_string=$(echo "$new_string" | sed -e "s/Annotated//" -e "s/Blank//")
    note_files["$new_string"]="$note_num"
  done

  declare -p note_files
  declare -p annotated_files
  declare -p blank_files

  note_file=$(printf "%s\n" "${!note_files[@]}" | sort -t " " -k2,2n -k1,1 -r | rofi -dmenu -window-title "Select Online Note");
  selected_note_num="${note_files["$note_file"]}"

  annotated_file="${annotated_files["$selected_note_num"]}"
  blank_file="${blank_files["$selected_note_num"]}"

  if [[ "$annotated_file" && "$blank_file" ]]; then
    selected_note_type=$(echo -e "Annotated\nBlank" | rofi -dmenu -window-title "Select Note Type")

    [ "$selected_note_type" == "Annotated" ] && zathura "$annotated_file"
    [ "$selected_note_type" == "Blank" ] && zathura "$blank_file"
  elif [[ "$annotated_file" ]]; then
    zathura "${annotated_file}"
  elif [[ "$blank_file" ]]; then
    zathura "${blank_file}"
  fi
}

inkscape_figures() {
  eval "$(get_figure_folders)";

  figure_folder=$(printf "%s\n" "${!figure_folders[@]}" | sort -t " " -k2,2n -k1,1 -r | rofi -dmenu -window-title "Select Week");
  [ "$figure_folder" = "" ] && exit 0;

  week="${figure_folders[$figure_folder]}";
  inkscape-figures edit "$current_course/figures/$week";
}

create_figure() {
  eval "$(get_figure_folders)";

  figure_folder=$(printf "%s\n" "${!figure_folders[@]}" | sort -t " " -k2,2n -k1,1 -r | rofi -dmenu -window-title "Select Week");
  [ "$figure_folder" = "" ] && exit 0;

  week="${figure_folders[$figure_folder]}";

  figure_name=$(rofi -dmenu -window-title "Inkscape figure name");
  if [ "$figure_name" != "" ]; then
    inkscape-figures create "$figure_name" "$current_course/figures/$week" | xclip -selection clipboard;
  else
    exit;
  fi
}

open_browser () {
  url=$(shyaml get-value url < "$current_course/info.yaml" || exit)
  google-chrome-stable --profile-directory="Profile 1" --app="$url"
}

launch_kitty() {
  local path cmd

  while [[ ${1} ]]; do
    case "${1}" in
      --path)
        path=${2}; shift ;;
      --cmd)
        cmd=${2}; shift ;;
      *)
        echo "Unknown parameter: ${1}" >&2
        return 1
    ;; esac

    if ! shift; then
      echo "Missing parameter argument." >&2
      return 1
    fi
  done

  kitty --directory="$path" $cmd
}

case $key in
  ##################
  #  School Notes  #
  ##################

  # Open my class notes.
  o ) zathura "$master_pdf" ;;
  # List all online notes.
  O ) list_online_notes ;;
  # List all my inkscape figures.
  i ) inkscape_figures ;;
  # Create inkscape figure.
  I ) create_figure ;;
  # Open my current course in the browser.
  w ) open_browser ;;
  # Open my info.yaml file.
  y ) launch_kitty --path "$current_course" --cmd "nvim info.yaml" ;;
  # Search through my research papers.
  p ) open_research_paper ;;
  # Open my notes.md file for the current course.
  k ) launch_kitty --path "$current_course" --cmd "nvim notes.md" ;;
  # Open my notes.md file for everything.
  K ) launch_kitty --path "$school_notes_root" --cmd "nvim notes.md" ;;
  # Open the master.tex file.
  m ) launch_kitty --path "$current_course" --cmd "nvim master.tex" ;;

  # Custom made scripts.
  a ) ~/Documents/school-setup/main.py --rofi-assignments ;;
  b ) ~/Documents/school-setup/main.py --rofi-books ;;
  c ) ~/Documents/school-setup/main.py --rofi-courses ;;
  n ) ~/Documents/school-setup/main.py --rofi-notes ;;

  s ) ~/Documents/school-setup/main.py --source-notes ;;
  S ) ~/Documents/school-setup/main.py --sync-notes ;;
esac
