#!/bin/sh

# Get absolute project root directory
CURRENT_DIR=$(pwd)

# Check if .git exists
GIT_DIR="$CURRENT_DIR/.git"
if [ ! -d "$GIT_DIR" ]; then
    echo "Not a git directory."
    exit 1
fi

# Check if pre-commit is already created
PRE_COMMIT_PATH="$GIT_DIR/hooks/pre-commit_test"
if [ -f "$PRE_COMMIT_PATH" ]; then
    echo "$PRE_COMMIT_PATH already exists."
    exit 1
fi

cp "$CURRENT_DIR/pre-commit.sample" "$PRE_COMMIT_PATH"