#!/bin/bash

key="$1"
node="/usr/bin/node"

root="$HOME/Documents"
journal_dir="$root/journal"
today_journal_dir="$journal_dir/$(date +%Y/%m/%d)"

school_notes_root="$root/school-notes"
current_course="$school_notes_root/current-course"
papers="${current_course}/papers"
instant_reference="$HOME/.local/share/Singularis/third-party-tools/instant-reference/copy-reference.js"
master_pdf="$current_course/master.pdf"

basic_template="\time_of_day

\begin{env}
\end{env}
"

log_time="\\time{$(date '+%I:%M:%S %p')}"
morning_template=$(echo "$basic_template" | sed "s/time_of_day/morning/" | sed "s/env/goals/")
afternoon_template=$(echo "$basic_template" | sed "s/time_of_day/afternoon/" | sed "s/env/status/")
evening_template=$(echo "$basic_template" | sed "s/time_of_day/evening/" | sed "s/env/status/")
night_template=$(echo "$basic_template" | sed "s/time_of_day/night/" | sed "s/env/results/")
night_template+="

$log_time

\contentment{}"

open_browser () {
  url=$(shyaml get-value url < "$current_course/info.yaml" || exit)
  google-chrome-stable --profile-directory="Profile 1" --app="$url"
}

open_research_paper() {
  cd "$papers" || exit
  pdf_file="$(find . -maxdepth 1 -type f | rofi -i -dmenu -window-title "Select paper")"
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

open_note_for_today() {
  mkdir -p "$today_journal_dir";

  # Check the current time to see if it's the morning
  h=$(date +%k)

  # Times of day:
  #   Morning: 6 am - 12 pm
  #   Afternoon: 12 pm - 5 pm
  #   Evening: 5 pm - 10 pm
  #   Night: 10 pm - 6 am
  if [[ "$h" -ge 6 && "$h" -lt 12 ]]; then
    if ! grep -q '\\morning' "$today_journal_dir/note.tex"; then
      echo "$morning_template" >> "$today_journal_dir/note.tex"
    fi
  elif [[ "$h" -ge 12 && "$h" -lt 17 ]]; then
    if ! grep -q '\\afternoon' "$today_journal_dir/note.tex"; then
      echo "$afternoon_template" >> "$today_journal_dir/note.tex"
    fi
  elif [[ "$h" -ge 17 && "$h" -lt 22 ]]; then
    if ! grep -q '\\evening' "$today_journal_dir/note.tex"; then
      echo "$evening_template" >> "$today_journal_dir/note.tex"
    fi
  elif [[ "$h" -ge 22 || "$h" -lt 6 ]]; then
    if ! grep -q '\\night' "$today_journal_dir/note.tex"; then
      echo "$night_template" >> "$today_journal_dir/note.tex"
      launch_kitty --path "$today_journal_dir" --cmd "nvim note.tex"
      return
    fi
  fi

  echo "" >> "$today_journal_dir/note.tex"
  echo "$log_time" >> "$today_journal_dir/note.tex"

  launch_kitty --path "$today_journal_dir" --cmd "nvim note.tex"
}

open_xournal () {
  cd "$today_journal_dir" || exit

  xournalpp note.xopp
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

  kitty --directory="$path" "$cmd"
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
  # Get an instant reference to the current open pdf.
  f ) "$node" "$instant_reference" ;;
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

  ###################
  #  Journal Notes  #
  ###################

  x ) open_xournal ;;
  r ) launch_kitty --path "$today_journal_dir" --cmd "$HOME/.local/bin/lfub" ;;
  j ) open_note_for_today ;;
  O ) zathura "$journal_dir/master.pdf" ;;
esac
