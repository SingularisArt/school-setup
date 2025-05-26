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

get_figures() {
  declare -A figure_names

  for file in $(find "$current_course/figures/" | sort); do
    if [[ "$file" == "README.md" ]]; then
      continue
    fi

    figure_name=$(echo "$file" | sed -e 's/\.[^.]*$//')
  done

  declare -p figure_names
}

list_professor_notes() {
  declare -A note_files
  declare -A annotated_files
  declare -A blank_files

  for file in $(find "$current_course/professor-notes/" -mindepth 1 -maxdepth 1 -type f -exec basename {} \; | sort); do
    if [[ "$file" != *.pdf ]]; then
      continue
    fi

    note_num=$(echo "$file" | sed -s "s/[^0-9]//g")
    new_string=$(echo "$file" | sed -e "s/lec-/Lecture /" -e "s/chap-/Chapter /" -e "s/.pdf//" -e "s/\b0\+\([1-9][0-9]*\)/\1/" -e 's/-/ /g' -e 's/\b\(.\)/\u\1/g')

    file="$current_course/professor-notes/$file"

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

create_figure() {
  local figures=$(find "$current_course/figures/" -type f ! -name "README.md" \
    -exec basename {} \; | sed -e 's/\.[^.]*$//' | sort -u)

  selected=$(echo "$figures" | rofi -dmenu -p "Select a figure")

  if [ "$selected" != "" ]; then
    cd ~/Documents/school-setup/
    ./main.py create "$selected" "$current_course/figures" | xclip -selection clipboard;
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

  a ) lesson-manager --rofi-assignments ;;
  b ) lesson-manager --rofi-books ;;
  c ) lesson-manager --rofi-courses ;;
  n ) lesson-manager --rofi-notes ;;
  f ) lesson-manager --rofi-figures edit "$current_course/figures" ;;
  F ) create_figure ;;

  s ) lesson-manager --source-notes ;;
  S ) lesson-manager --sync-notes ;;

  o ) zathura "$master_pdf" ;;
  O ) list_professor_notes ;;
  w ) open_browser ;;
  y ) launch_kitty --path "$current_course" --cmd "nvim info.yaml" ;;
  p ) open_research_paper ;;
  k ) launch_kitty --path "$current_course" --cmd "nvim notes.md" ;;
  K ) launch_kitty --path "$school_notes_root" --cmd "nvim notes.md" ;;
  m ) launch_kitty --path "$current_course" --cmd "nvim master.tex" ;;
esac
