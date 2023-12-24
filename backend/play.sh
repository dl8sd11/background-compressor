#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <input.mp4>"
  exit 1
fi

input_file="$1"
fg_mp4="${input_file%.*}.fg.mp4"
bg_mp4="${input_file%.*}.bg.mp4"
python3 ./backend/player.py "$fg_mp4" "$bg_mp4"
