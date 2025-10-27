#!/bin/bash

# Backup current branch
git branch backup-expand-messages

# Expand short commit messages to be more natural (4+ words)
git filter-branch -f --msg-filter '
sed "s/^Initial commit$/Initial project setup and structure/;
     s/^Added technical indicators$/Added technical indicator calculations/;
     s/^Added cross-asset features$/Added cross-asset correlation features/;
     s/^Added config utilities$/Added configuration and utility functions/;
     s/^Added baseline models$/Added baseline ML model implementations/;
     s/^Added ensemble learning$/Added ensemble learning model framework/;
     s/^Added unit tests$/Added comprehensive unit test suite/;
     s/^Added setup files$/Added project setup and configuration/;
     s/^Added Makefile$/Added Makefile for build automation/;
     s/^Updated README$/Updated README with project details/;
     s/^Added CI workflow$/Added continuous integration testing workflow/"
' -- --all

echo "✅ Expanded short commit messages!"
echo "📝 Review with: git log --format='%s'"
echo "⚠️  To push: git push origin main --force"
