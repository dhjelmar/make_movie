#%%
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pathlib",
#     "pillow",
#     "pillow-heif",
#     "ipykernel",
# ]
# ///

'''
Creates mp4 movie using FFmpeg from mov, mp4, jpg, and heic files.

Input:
  - background_audio.mp3
  - image and/or movie files

Input Options:
  - Supply list of image and/or movie files in files_order.txt file.
  - Supply image and/or movie files in pictures_and_movie_clips folder.

Output:
  - mymovie.mp4
'''

import subprocess
import shutil
import json
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
import os

register_heif_opener()

#%%
# --- CONFIGURATION ---
SOURCE_DIR = Path("pictures_and_movie_clips")   # only used if file_order.txt not provided
TEMP_DIR = Path("temp_jpgs")
AUDIO_FILE = "background_audio.mp3"
OUTPUT_FILE = "myvideo.mp4"
RESOLUTION = "1920:1080"

# # Specify by filename (e.g., "IMG_7561.mov" or "IMG_7022.HEIC")
# FIRST_FILE = "redheaded.jpg" 
# LAST_FILE = "moose.mp4"
# ---------------------

def get_duration(file_path):
    """Uses ffprobe to get duration of a media file."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", str(file_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])

def create_movie():
    TEMP_DIR.mkdir(exist_ok=True)
    
    if os.path.exists('file_order.txt'):
        # read order of files for use in movie
        with open('file_order.txt', 'r') as f:
          ordered_inputs = [line.strip() for line in f]

    else:
        # use alphabetical order of files in SOURCE_DIR to make movie

        # 1. Gather and Sort Files
        all_files = sorted(list(SOURCE_DIR.glob("*.*")))
        all_files = [f for f in all_files if f.suffix.lower() in ['.mp4', ".mov", '.jpg', ".heic"]]
        
        # # 2. Handle First/Last Logic
        # first_file = next((f for f in all_files if f.name == FIRST_FILE), None)
        # last_file = next((f for f in all_files if f.name == LAST_FILE), None)
        # middle_files = [f for f in all_files if f.name not in [FIRST_FILE, LAST_FILE]]
        
        # ordered_inputs = []
        # if first_file: ordered_inputs.append(first_file)
        # ordered_inputs.extend(middle_files)
        # if last_file: ordered_inputs.append(last_file)

        ordered_inputs = all_files

    # 3. Calculate Durations
    #breakpoint()
    music_len = get_duration(AUDIO_FILE)
    # video_paths = [f for f in ordered_inputs if (f.suffix.lower() == ".mov")|(f.suffix.lower() == ".mp4")]
    # picture_paths = [f for f in ordered_inputs if (f.suffix.lower() == ".heic")|(f.suffix.lower() == ".jpg")]
    video_paths   = [f for f in ordered_inputs if ((os.path.basename(f).split(".")[-1].lower() == "mov") |
                                                   (os.path.basename(f).split(".")[-1].lower() == "mp4") )]
    picture_paths = [f for f in ordered_inputs if ((os.path.basename(f).split(".")[-1].lower() == "heic") |
                                                   (os.path.basename(f).split(".")[-1].lower() == "jpg") )]


    total_video_time = sum(get_duration(f) for f in video_paths)
    
    # set duration for images between 0.5 and 5 seconds
    if len(picture_paths) > 0:
        # figure out duration available for each picgture based on time remaining when subtract out video time
        img_duration = (music_len - total_video_time) / len(picture_paths)
        # Ensure duration isn't negative or ridiculously
        img_duration = max(img_duration, 0.5)
    else:
        # there are no pictures so set each picture time to 0 sec
        img_duration = 0

    # 4. Prepare JPGs and Command
    final_input_paths = []
    cmd = ["ffmpeg", "-y"]
    
    for f in ordered_inputs:

        if f in picture_paths:
            # f is a picture

            # # first assume f is a jpg
            # target = TEMP_DIR / f"{f.stem}.jpg"
            # if not target.exists():
            #     # target is not a jpg so convert it
            #     Image.open(f).save(target, "JPEG")

            base = os.path.basename(f)
            if base.split(".")[-1].lower() == "jpg":
                # target is already a jpg
                target = f
            else:
                # not a jpg so convert it and save to TEMP_DIR
                target = os.path.join(TEMP_DIR, base)
                Image.open(f).save(target, "JPEG")

            cmd.extend(["-loop", "1", "-t", str(img_duration), "-i", str(target)])
            final_input_paths.append(target)
            
        else:
            # f is a video
            cmd.extend(["-i", str(f)])
            final_input_paths.append(f)
            
    # Add Audio (No loop needed since we calculated the duration to match)
    cmd.extend(["-i", AUDIO_FILE])
    
    # 5. Build movie file
    filter_parts = []
    for i in range(len(final_input_paths)):
        f_str = (f"[{i}:v]scale={RESOLUTION}:force_original_aspect_ratio=decrease,"
                 f"pad={RESOLUTION}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]")

        filter_parts.append(f_str)
    
    concat_v = "".join([f"[v{i}]" for i in range(len(final_input_paths))])
    filter_parts.append(f"{concat_v}concat=n={len(final_input_paths)}:v=1:a=0[outv]")
    
    cmd.extend([
        "-filter_complex", ";".join(filter_parts),
        "-map", "[outv]",
        "-map", f"{len(final_input_paths)}:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        OUTPUT_FILE
    ])

    # print('')
    # print('running command:')
    # print(cmd)
    # print('')

    subprocess.run(cmd)
    shutil.rmtree(TEMP_DIR)

    print(f"Success! Movie synced to music length.")
    visuals_time = total_video_time + img_duration * len(picture_paths)
    print(f"Music           : {music_len:.2f}s")
    print(f"Videos          : {total_video_time:.2f}s")
    print(f"Videos + Images : {visuals_time:.2f}s")
    print(f"Images          : {img_duration:.2f}s per photo")
    print(f"Number of Images: {len(picture_paths):.0f}")

    return ordered_inputs

if __name__ == "__main__":
    out = create_movie()

out
#%%
