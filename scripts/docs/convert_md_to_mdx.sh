#!/bin/bash

directory="../../docs"  # Replace with your desired directory path

find "$directory" -type f -name "*.md" -exec sh -c 'mv "$1" "${1%.md}.mdx"' _ {} \;
