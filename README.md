# Media Compiler

A streamlined Python utility to merge iPhone `.mov` videos and `.heic` photos into a single stabilized 1080p MP4. Designed to be run via `uv` for zero-config dependency management.

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

  - set up a project

    - add dependencies to the source file, run script craete pyproject.tomlj, then, if want to create .venv, run `uv sync --no-install-project` 

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

    - other potential solution

      ```
      # https://blog.phle.dev/posts/python-setup-2024/

      # initialize project
      uv init . --package

      # Add dev dependencies:
      uv add --dev ipykernel
      
      # Add project dependencies
      uv add pathlib pillow pillow-heif
      ```

  - following structue is created
    - `pyproject.toml` file
    - `.venv/` local virtual environment
    - `uv.lock` file which records version of every dependency
    - `src/myapp/__init__.py` project structure

  - to sync between `pyproject.toml` and versions in `uv.lock`:

    `
    uv sync
    `

  - Or to update the packages and `uv.lock` (test before committing)

    `
    uv sync --upgrade
    `
  


## Folder Structure

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

## Execution

Run the script using uv. This will automatically handle the installation of Pillow and pillow-heif in a temporary isolated environment:

`uv run make_movie.py`
