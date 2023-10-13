#!/bin/bash

# Ensure the file supported_versions.txt exists
if [[ ! -f "./supported_versions.txt" ]]; then
    echo "Error: supported_versions.txt file not found!"
    exit 1
fi

spec_dir="./src/grai_source_openlineage/specs"

master_init_file="$spec_dir/__init__.py"
rm "$master_init_file"


declare -a supported_versions

# Read each line from the file
while IFS= read -r semver; do
    if [[ ! $semver =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Warning: Invalid semver format - $semver"
        continue
    fi
    echo "Processing version $semver"
    # Convert semver to url format
    url_version=$(echo "$semver" | tr '.' '-')

    # Create the URL
    url="https://openlineage.io/spec/$url_version/OpenLineage.json"

    # Convert semver to directory format
    dir_version=$(echo "$semver" | tr '.' '_')

    # Create the directory
    directory="$spec_dir/v$dir_version/"
    mkdir -p "$directory"

    error_message=$(wget -O "$directory/OpenLineage.json" "$url" 2>&1)

    # Check if the download was successful
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to download the spec file for version $semver"
        echo "Error Message: $error_message"
        exit
    fi

    cd "$directory" || exit
    error_message=$(poetry run datamodel-codegen --input OpenLineage.json --output models.py 2>&1)
    rm OpenLineage.json

    if [[ ! -f models.py ]]; then
        echo "Error: Failed to generate models.py for version $semver"
        echo "Error Message: $error_message"
        exit
    fi

    echo "from grai_source_openlineage.specs.v$dir_version import models" > __init__.py

    cd "$OLDPWD"
    echo "from grai_source_openlineage.specs import v$dir_version" >> "$master_init_file"

    supported_versions+=(v$semver)

done < <(sort -V supported_versions.txt)


versions_string="{\n"
for version in "${supported_versions[@]}"; do
    sanitized_version=$(echo "$version" | tr '.' '_')
    versions_string+="    \"$version\": $sanitized_version.models,\n"
done
versions_string="${versions_string%,}}"

echo "" >> "$master_init_file"
echo -e "SUPPORTED_VERSIONS = $versions_string" >> "$master_init_file"
