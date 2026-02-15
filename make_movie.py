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

import subprocess
import shutil
import json
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

#%%
# --- CONFIGURATION ---
SOURCE_DIR = Path("pictures_and_movie_clips")
TEMP_DIR = Path("temp_jpgs")
AUDIO_FILE = "background_audio.mp3"
OUTPUT_FILE = "myvideo.mp4"
RESOLUTION = "1920:1080"

# Specify by filename (e.g., "IMG_7561.mov" or "IMG_7022.HEIC")
FIRST_FILE = "moose.mov" 
LAST_FILE = "downy.jpg"
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
    
    # 1. Gather and Sort Files
    all_files = sorted(list(SOURCE_DIR.glob("*.*")))
    all_files = [f for f in all_files if f.suffix.lower() in ['.mp4', ".mov", '.jpg', ".heic"]]
    
    # 2. Handle First/Last Logic
    first_file = next((f for f in all_files if f.name == FIRST_FILE), None)
    last_file = next((f for f in all_files if f.name == LAST_FILE), None)
    middle_files = [f for f in all_files if f.name not in [FIRST_FILE, LAST_FILE]]
    
    ordered_inputs = []
    if first_file: ordered_inputs.append(first_file)
    ordered_inputs.extend(middle_files)
    if last_file: ordered_inputs.append(last_file)

    # 3. Calculate Durations
    music_len = get_duration(AUDIO_FILE)
    video_paths = [f for f in ordered_inputs if (f.suffix.lower() == ".mov")|(f.suffix.lower() == ".mp4")]
    picture_paths = [f for f in ordered_inputs if (f.suffix.lower() == ".heic")|(f.suffix.lower() == ".jpg")]
    
    total_video_time = sum(get_duration(f) for f in video_paths)
    
    if len(picture_paths) > 0:
        # Dynamic duration: (Music Time - Video Time) / Number of Photos
        img_duration = (music_len - total_video_time) / len(picture_paths)
        # Ensure duration isn't negative or ridiculously small
        img_duration = max(img_duration, 0.5) 
    else:
        img_duration = 5

    print(f"Music: {music_len:.2f}s | Videos: {total_video_time:.2f}s")
    print(f"Calculated Image Duration: {img_duration:.2f}s per photo")

    # 4. Prepare JPGs and Command
    final_input_paths = []
    cmd = ["ffmpeg", "-y"]
    
    for f in ordered_inputs:
        if f.suffix.lower() == ".heic":
            target = TEMP_DIR / f"{f.stem}.jpg"
            if not target.exists():
                Image.open(f).save(target, "JPEG")
            cmd.extend(["-loop", "1", "-t", str(img_duration), "-i", str(target)])
            final_input_paths.append(target)
        else:
            cmd.extend(["-i", str(f)])
            final_input_paths.append(f)
            
    # Add Audio (No loop needed since we calculated the duration to match)
    cmd.extend(["-i", AUDIO_FILE])
    
    # 5. Build Filters
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

    subprocess.run(cmd)
    shutil.rmtree(TEMP_DIR)
    print(f"Success! Movie synced to music length.")

if __name__ == "__main__":
    create_movie()