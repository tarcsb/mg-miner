#!/bin/bash

# Variables
REPO_URL="git@github.com:tarcsb/mg-miner.git"

# Remove the existing origin if it exists
git remote remove origin 2>/dev/null

# Add the new origin
git remote add origin $REPO_URL

# Stage all files for the initial commit
git add .

# Commit the changes while bypassing pre-commit hooks
SKIP=all git commit -m "Initial commit: project setup with core functionality, configuration, and documentation"

# Push the commit to the new origin
git push -u origin main

echo "Repository initialized and pushed to $REPO_URL"

