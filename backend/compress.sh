#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input.mp4> <mask.mp4>"
    exit 1
fi

input_file=$1
mask_file=$2

if [ ! -f "$input_file" ]; then
    echo "File '$input_file' does not exist."
    exit 1
fi

if [ ! -f "$mask_file" ]; then
    echo "File '$mask_file' does not exist."
    exit 1
fi

fg_avi="${input_file%.*}.fg.avi"
bg_avi="${input_file%.*}.bg.avi"
fg_mp4="${input_file%.*}.fg.mp4"
bg_mp4="${input_file%.*}.bg.mp4"

if [ ! -f "$fg_avi" ]; then
    time python3 splitter.py "$input_file" "$mask_file"
    echo "Done splitting $input_file using $mask_file mask."
else
    echo "Skipping the compressing since the file already exists."
fi

echo "Here is the information of the original video input."

ffmpeg -i data/raw.mp4 2>&1 | grep bitrate

echo "Please enter the bitrate limit for the foreground and the background video:"

echo -n "Forground bitrate (2M): "
read foreground_bitrate
echo -n "Background bitrate (100K): "
read background_bitrate

echo "Compressing the video of bitrate $foreground_bitrate and $background_bitrate using ffmpeg."

ffmpeg -i "$fg_avi" -loglevel quiet -b:v "$foreground_bitrate" -c:v libx264 -c:a aac "$fg_mp4"
ffmpeg -i "$bg_avi" -loglevel quiet -b:v "$background_bitrate" -c:v libx264 -c:a aac "$bg_mp4"

rm "$fg_avi" "$bg_avi"