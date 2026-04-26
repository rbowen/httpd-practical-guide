#!/bin/bash
# Set up (or update) the git remote and push to GitHub.
# Run this on matrim after syncing with sync-files.sh.
#
# First time: sets remote and pushes
# Subsequent: just commits and pushes

cd "$(dirname "$0")"

REMOTE="git@github.com:rbowen/httpd-practical-guide.git"

# Check if remote is already set correctly
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null)

if [ -z "$CURRENT_REMOTE" ]; then
    echo "Adding remote origin..."
    git remote add origin "$REMOTE"
elif [ "$CURRENT_REMOTE" != "$REMOTE" ]; then
    echo "Updating remote origin from $CURRENT_REMOTE to $REMOTE..."
    git remote set-url origin "$REMOTE"
else
    echo "Remote already set to $REMOTE"
fi

# Stage, commit, push
git add -A
git commit -m "${1:-Update from working copy}"
git branch -M main
git push -u origin main

echo ""
echo "Done! Repo at: https://github.com/rbowen/httpd-practical-guide"
