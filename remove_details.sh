#!/bin/bash

# Backup current branch
git branch backup-remove-details

# Remove all commit message bodies, keep only subject lines
git filter-branch -f --msg-filter '
    # Get only the first line (subject) and remove everything else
    head -n 1
' -- --all

echo "✅ Removed all commit body details!"
echo "📝 Review with: git log --format='%s'"
echo "⚠️  To push: git push origin main --force"
