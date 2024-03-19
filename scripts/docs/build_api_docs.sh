#!/bin/bash

directory="../.."
current_directory=$(pwd)
docs_page_directory="$directory/docs/pages/api-docs"

rm -r $docs_page_directory/*

find "$directory" -type f \( -name "pydoc-markdown.yml" -o -name "pydoc-markdown.yaml" \) -print0 | while IFS= read -r -d $'\0' file; do
    folder=$(dirname "$file")
    echo "Processing folder: $folder"
    cd "$folder" || exit
    pydoc-markdown
    cd "$current_directory"
done

find "$docs_page_directory" -type f -name "__init__.md" -exec rm -f {} \;

create_meta() {
    local dir="$1"
    local meta_file="${dir}/_meta.json"

    # Start JSON
    echo "{" > "$meta_file"

    local entries=()
    for entry in "$dir"/*; do
        # Skip _meta.json itself
        if [[ "$entry" == *_meta.json ]]; then
            continue
        fi

        # Get basename for entry
        local base_entry=$(basename "$entry")
        if [[ -d "$entry" ]]; then
            # If entry is a directory, strip possible trailing slashes
            base_entry="${base_entry%/}"
            entries+=("    \"$base_entry\": \"$base_entry\"")
        else
            # If entry is a file, remove its extension
            base_entry="${base_entry%.*}"
            entries+=("    \"$base_entry\": \"$base_entry\"")
        fi
    done

    # Join entries with commas and newlines, then append to meta_file
    IFS=",\n"
    echo "${entries[*]}" >> "$meta_file"
    unset IFS

    # End JSON
    echo "}" >> "$meta_file"
}

traverse_dirs() {
    local dir="$1"
    create_meta "$dir"
    for subdir in "$dir"/*; do
        if [[ -d "$subdir" && "$subdir" != *"_meta.json" ]]; then
            traverse_dirs "$subdir"
        fi
    done
}

traverse_dirs "$docs_page_directory"
