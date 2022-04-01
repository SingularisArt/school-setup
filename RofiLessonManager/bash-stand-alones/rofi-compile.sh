#!/usr/bin/env bash

source ~/.config/zsh/exports.zsh

cd ${CURRENT_COURSE}
pdflatex master.tex
rubber --clean master

open=$(echo -e "Open PDF\nExit" | rofi -dmenu)

case ${open} in
  "Open PDF" )
    zathura ${CURRENT_COURSE}/master.pdf;;
  "Exit" )
    exit 0;;
esac
