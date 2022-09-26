#!/bin/bash

key="$1"
node="/usr/bin/node"

root="$HOME/Documents"
journal_dir="$root/journal"
today_journal_dir="$journal_dir/$(date +%Y/%m/%d)"

school_notes_root="$root/school-notes"
current_course="$school_notes_root/current-course"
papers="$current_course/papers"
instant_reference="$HOME/Singularis/third-party-tools/instant-reference/copy-reference.js"
master_pdf="$current_course/master.pdf"

# book_notes_root="$root/book-notes"

open_xournal () {
  cd "$today_journal_dir" || exit

  xournalpp note.xopp
}

compile () {
  cd "${1}" || exit
  pdflatex master.tex && pdflatex master.tex;
  status=$(echo "$?")
  if [[ "$status" == 130 ]]; then
    rofi -e "<span color='red'><b>Failed to compile!</b></span>" -markup
  elif [[ "$status" == 0 ]]; then
    rofi -e "<span color='green'><b>Compiled successfully!</b></span>" -markup
  fi
}

open_browser () {
  url=$(cat "$current_course/info.yaml" | shyaml get-value url)
  google-chrome-stable --profile-directory="Profile 1" --app="$url"
}

open_research_paper() {
  cd "$papers" || exit
  pdf_file="$(ls . | rofi -i -dmenu)"
  [ "$pdf_file" = "" ] && exit 0
  [ -f "$pdf_file" ] && zathura "$(realpath "$pdf_file")" || google-chrome-stable --profile-directory="Profile 2" --app="https://google.com/search?q=$pdf_file"
}

create_figure() {
  figure_name=$(rofi -dmenu -window-title "Inkscape figure name");
  if [ ! -z "$figure_name" ]; then
    inkscape-figures create "$figure_name" "$current_course/figures" | xclip -selection clipboard;
  else
    exit;
  fi
}

mkdir -p "$today_journal_dir";

case $key in
  # School Notes.
  # Open my class notes.
  o ) zathura "$master_pdf" ;;
  # Compile my class notes.
  O ) compile "$current_course" ;;
  # List all my inkscape figures.
  i ) inkscape-figures edit "$current_course/figures" ;;
  # Create inkscape figure.
  I ) create_figure ;;
  # Get an instant reference to the current open pdf.
  f ) "$node" "$instant_reference" ;;
  # Open my current course in the browser.
  w ) open_browser ;;
  # Open my info.yaml file.
  y ) cd "$current_course" || exit;
    xfce4-terminal -e "nvim info.yaml" ;;
  # Open the source code.
  m ) cd "$current_course" || exit;
    xfce4-terminal -e "nvim ." ;;
  # Search through my research papers.
  p ) open_research_paper ;;
  # Open my notes.norg file for the current course.
  n ) cd "$current_course" || exit;
    xfce4-terminal -e "nvim notes.norg" ;;

  # Custom made scripts.
  a ) ~/Documents/school-setup/main.py --rofi-assignments ;;
  c ) ~/Documents/school-setup/main.py --rofi-courses ;;
  l ) ~/Documents/school-setup/main.py --rofi-lectures ;;
  s ) ~/Documents/school-setup/main.py --source-lectures ;;
  A ) ~/Documents/school-setup/main.py --new-assignment ;;
  C ) ~/Documents/school-setup/main.py --new-course ;;
  L ) ~/Documents/school-setup/main.py --new-lecture ;;
esac
