#!/bin/bash
set -e

echo "=== Markdown lint ==="
markdownlint-cli2 'Gen1/**/*.md' 'templates/**/*.md' 'prompts/**/*.md' 'examples/**/*.md' '*.md'

echo "=== Link check ==="
lychee --no-progress 'Gen1/**/*.md' 'templates/**/*.md' 'prompts/**/*.md' 'examples/**/*.md' '*.md'
