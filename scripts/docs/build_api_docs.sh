#!/bin/bash

directory="../.."
current_directory=$(pwd)

find "$directory" -type f \( -name "pydoc-markdown.yml" -o -name "pydoc-markdown.yaml" \) -print0 | while IFS= read -r -d $'\0' file; do
    folder=$(dirname "$file")
    echo "Processing folder: $folder"
    cd "$folder" || exit
    pydoc-markdown
    cd "$current_directory"
done
