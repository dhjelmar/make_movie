# Media Compiler

Creates mp4 movie using FFmpeg from mov, mp4, jpg, and heic files. Designed to be run via `uv` for zero-config dependency management.

## Usage

Input:
  - background_audio.mp3
  - image and/or movie files

Input Options:
  - Supply list of image and/or movie files in files_order.txt file.
  - Supply image and/or movie files in pictures_and_movie_clips folder.

Output:
  - mymovie.mp4

Execution:
- Run the script using uv. This automatically installs dependencies in a temporary virtual environment.

  `uv run make_movie.py`

## Requirements

- **FFmpeg**: Must be installed and accessible in your system's PATH.

  `
  sudo apt update && sudo apt install ffmpeg -y   
  `

- **uv**: The Python package manager/runner.

  - install uv
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

## Notes

  - dependencies added to the source file for use by uv

    ```
    # /// script
    # requires-python = ">=3.11"
    # dependencies = [
    #     "pathlib",
    #     "pillow",
    #     "pillow-heif",
    #     "ipykernel",
    # ]
    # ///
    ```

  - if execute the script, it will create pyproject.toml file. The pyproject.toml file can create and retain the virtual environment (.venv) in the project folder for use in vscode with the following

    `uv sync --no-install-project`

  - alternately can create a minimal pyproject.toml file with

    `uv sync --bare`

  - to sync between `pyproject.toml` and versions in `uv.lock`:

    `
    uv sync
    `

  - Or to update the packages and `uv.lock` (test before committing)

    `
    uv sync --upgrade
    `
  