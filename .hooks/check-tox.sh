#!/bin/bash

if [ $# == 0 ]; then
    echo "No branch name is given, so this script will be executed on all branches."
    tox
    exit $?
fi

# Get the current branch name
current_branch=$(git symbolic-ref --short HEAD)

# Loop through the input parameters (i.e., the list of branch names)
for branch in "$@"; do
    # Check if the current branch matches the current input parameter
    if [ "$current_branch" = "$branch" ]; then
        # If it does, execute the 'tox' command
        tox
        exit $?
    fi
done

# If the current branch does not match any of the input parameters, print a message
echo "Current branch '$current_branch' does not match any of the specified branch names: $*"
exit 0
