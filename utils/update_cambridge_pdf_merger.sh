#!/bin/bash
REPO_URL="https://github.com/definitelyna/Cambridge-PDF-Merger"
CLONE_DIR="Cambridge-PDF-Merger"

# Remove the existing directory if it exists
if [ -d "$CLONE_DIR" ]; then
    rm -rf "$CLONE_DIR"
fi

# Clone the latest commit of the repository
git clone --depth 1 "$REPO_URL" "$CLONE_DIR"
