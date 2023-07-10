#!/bin/bash

# Get the absolute path of the script's directory
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set the parent directory to search in
parent_directory="${script_dir}/.."

# Find all directories containing "pyproject.toml" and loop through them
find "$parent_directory" -type f -name "pyproject.toml" | while read -r toml_file; do
    # Extract the directory path
    directory_path=$(dirname "$toml_file")
    directory_path=$(realpath "$directory_path")

    # Change to the directory
    cd "$directory_path"

    echo "Running poetry lock in $directory_path"

    # Remove existing poetry.lock file if it exists
    if [[ -e poetry.lock ]]; then
        rm -f poetry.lock
    fi

    # Execute "poetry lock"
    poetry lock

    # Move back to the parent directory
    cd "$parent_directory"
done
