#!/bin/bash

set -o pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set the parent directory to search in
parent_directory="${script_dir}/.."

# Loop through all directories with a 'pyproject.toml' file
find "$parent_directory" -type f -name "pyproject.toml" | while read -r toml_file; do
    # Extract the directory path
    directory_path=$(realpath "$(dirname "$toml_file")")

    echo "Checking directory: $directory_path"

    # Change into the directory
    cd "$directory_path" || continue

    # Extract version using the 'poetry version' command and a regex for semver
    version=$(poetry version | awk '{print $2}' | grep -Eo "^[0-9]+\.[0-9]+\.[0-9]+-alpha[0-9]+$")

    # If the version matches the desired pattern, perform the operations
    if [[ $version ]]; then
        # Extract base version (without -alpha part)
        base_version=${version%-alpha*}

        echo "Processing $directory_path with version $version"

        poetry version "$base_version"
        poetry lock
        poetry publish --build
    fi

    # Change back to the original directory to continue searching
    cd - > /dev/null  # Suppress output
done
