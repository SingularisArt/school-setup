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

create_figure() {
  figure_name=$(rofi -dmenu -window-title "Inkscape figure name");
  if [ "$figure_name" != "" ]; then
    inkscape-figures create "$figure_name" "$current_course/figures" | xclip -selection clipboard;
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
    esac

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
  # List all my inkscape figures.
  i ) inkscape-figures edit "$current_course/figures" ;;
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

  A ) ~/Documents/school-setup/main.py --create-assignment ;;
  C ) ~/Documents/school-setup/main.py --rofi-courses-all ;;
  N ) ~/Documents/school-setup/main.py --create-note ;;

  s ) ~/Documents/school-setup/main.py --source-notes ;;
  S ) ~/Documents/school-setup/main.py --sync-notes ;;
esac
