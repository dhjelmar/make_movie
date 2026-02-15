# Media Compiler

A streamlined Python utility to merge iPhone `.mov` videos and `.heic` photos into a single stabilized 1080p MP4. Designed to be run via `uv` for zero-config dependency management.

## 📋 Requirements

- **FFmpeg**: Must be installed and accessible in your system's PATH.

- **uv**: The Python package manager/runner.

## 🏗️ Folder Structure

The script expects the following layout:

```text

- make_movie.py            # The script

- input
  - background_audio.mp3     # Your looped audio track

  - pictures_and_movie_clips

    - xxxx.mov         # Source videos
    - xxxx.mp4         # Source videos
    - xxx.jpg          # Source photos
    - xxxx.heic        # Source photos

```

## 🚀 Execution

Run the script using uv. This will automatically handle the installation of Pillow and pillow-heif in a temporary isolated environment:

PowerShell

uv run make_movie.py
