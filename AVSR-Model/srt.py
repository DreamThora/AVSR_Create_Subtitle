import os
import cv2
import numpy as np
import math
# from moviepy.editor import VideoFileClip, AudioFileClip
import subprocess

def create_srt_file(text_list, output_path,duration_per_subtitle=None):
    with open(output_path, 'w', encoding='utf-8') as file:
        # start_time = 0
        for i, line in enumerate(text_list):
            index = i + 1
            start_time = (0 + i) * duration_per_subtitle * 1000
            end_time = start_time + duration_per_subtitle * 1000
            subtitle_text = line

            if subtitle_text.strip():
                file.write(f"{index}\n")
                file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                file.write(f"{subtitle_text}\n\n")

            start_time = end_time


def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"



def merge_video_with_subtitle_ffmpeg(video_path, subtitle_path, output_path):
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'subtitles={subtitle_path}',
        '-c:a', 'copy',
        output_path
    ]
    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def create_thumbnail(video_path,thumbnail_path):
    # command = f"ffmpeg -i {video_path} -vf 'thumbnail' -frames:v 1 {thumbnail_path}"
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', 'thumbnail',
        '-frames:v', '1' , thumbnail_path
    ]
    try:
        subprocess.run(command)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")