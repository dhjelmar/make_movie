# Media Compiler

A streamlined Python utility to merge iPhone `.mov` videos and `.heic` photos into a single stabilized 1080p MP4. Designed to be run via `uv` for zero-config dependency management.

## Usage

### File structure

```

- make_movie.py              # main script

- input
  - background_audio.mp3     # audio track

  - pictures_and_movie_clips folder containing
    - video files (*.mov, *.mp4)
    - photo files (*.jpg, *.heic)

- output
  - mymovie.mp4
  - pyproject.toml = setup file created when execute make_movie.py

```

### Execution

Run the script using uv. This will automatically handle the installation of Pillow and pillow-heif in a temporary isolated environment:

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

  - dependencies added to the source file

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

  - if execute the script or if separately create pyproject.toml file, can create and retain virtual environment (.venv) for use in vscode if use 

    `uv sync --no-install-project`


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
  