#!/usr/bin/env bash

source ~/.config/zsh/exports.zsh

#${BROWSER} "$(yq read ${CURRENT_COURSE}/info.yaml url)"
#google-chrome-stable --app=$(yq read ${CURRENT_COURSE}/info.yaml url)
google-chrome-stable --app=$(cat ${CURRENT_COURSE}/info.yaml | shyaml get-value url)

