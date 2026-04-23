#!/bin/bash
cd "$(dirname "$0")"

# Initialize git
git init
echo "# Sphinx build output
_build/
_ext/__pycache__/

# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~" > .gitignore

git add -A
git commit -m "Initial commit: Apache Cookbook 4e, converted from AsciiDoc 3e to Sphinx/RST"

echo ""
echo "=== Git repo initialized ==="
git log --oneline
