#!/bin/bash

# Backup current branch
git branch backup-dates-fix

# Rewrite only dates, keeping current messages
git filter-branch -f --env-filter '
COMMIT_MSG=$(git log --format=%s -n 1 $GIT_COMMIT)

case "$COMMIT_MSG" in
    "Initial commit")
        export GIT_AUTHOR_DATE="2023-12-18 15:23:00"
        export GIT_COMMITTER_DATE="2023-12-18 15:23:00"
        ;;
    "Added data preprocessing utils")
        export GIT_AUTHOR_DATE="2023-12-18 17:45:00"
        export GIT_COMMITTER_DATE="2023-12-18 17:45:00"
        ;;
    "Added technical indicators")
        export GIT_AUTHOR_DATE="2023-12-18 18:12:00"
        export GIT_COMMITTER_DATE="2023-12-18 18:12:00"
        ;;
    "Added cross-asset features")
        export GIT_AUTHOR_DATE="2023-12-26 10:30:00"
        export GIT_COMMITTER_DATE="2023-12-26 10:30:00"
        ;;
    "Added macro feature engineering")
        export GIT_AUTHOR_DATE="2023-12-26 14:15:00"
        export GIT_COMMITTER_DATE="2023-12-26 14:15:00"
        ;;
    "Added config utilities")
        export GIT_AUTHOR_DATE="2024-01-08 09:45:00"
        export GIT_COMMITTER_DATE="2024-01-08 09:45:00"
        ;;
    "Added baseline models")
        export GIT_AUTHOR_DATE="2024-01-08 16:20:00"
        export GIT_COMMITTER_DATE="2024-01-08 16:20:00"
        ;;
    "Added backtesting metrics")
        export GIT_AUTHOR_DATE="2024-01-15 11:00:00"
        export GIT_COMMITTER_DATE="2024-01-15 11:00:00"
        ;;
    "Implemented XGBoost model")
        export GIT_AUTHOR_DATE="2024-01-28 14:30:00"
        export GIT_COMMITTER_DATE="2024-01-28 14:30:00"
        ;;
    "Implemented LSTM model")
        export GIT_AUTHOR_DATE="2024-02-10 10:15:00"
        export GIT_COMMITTER_DATE="2024-02-10 10:15:00"
        ;;
    "Added ensemble learning")
        export GIT_AUTHOR_DATE="2024-02-18 15:45:00"
        export GIT_COMMITTER_DATE="2024-02-18 15:45:00"
        ;;
    "Implemented backtesting engine")
        export GIT_AUTHOR_DATE="2024-03-02 09:20:00"
        export GIT_COMMITTER_DATE="2024-03-02 09:20:00"
        ;;
    "Enhanced crypto data fetching")
        export GIT_AUTHOR_DATE="2024-03-16 13:30:00"
        export GIT_COMMITTER_DATE="2024-03-16 13:30:00"
        ;;
    "Added data exploration notebook")
        export GIT_AUTHOR_DATE="2024-03-23 11:45:00"
        export GIT_COMMITTER_DATE="2024-03-23 11:45:00"
        ;;
    "Added unit tests")
        export GIT_AUTHOR_DATE="2024-04-07 10:00:00"
        export GIT_COMMITTER_DATE="2024-04-07 10:00:00"
        ;;
    "Added methodology documentation")
        export GIT_AUTHOR_DATE="2024-04-21 14:30:00"
        export GIT_COMMITTER_DATE="2024-04-21 14:30:00"
        ;;
    "Added setup files")
        export GIT_AUTHOR_DATE="2024-05-05 16:15:00"
        export GIT_COMMITTER_DATE="2024-05-05 16:15:00"
        ;;
    "Added Makefile")
        export GIT_AUTHOR_DATE="2024-05-19 09:40:00"
        export GIT_COMMITTER_DATE="2024-05-19 09:40:00"
        ;;
    "Added contributing guidelines")
        export GIT_AUTHOR_DATE="2024-06-02 11:20:00"
        export GIT_COMMITTER_DATE="2024-06-02 11:20:00"
        ;;
    "Updated README")
        export GIT_AUTHOR_DATE="2024-06-08 15:50:00"
        export GIT_COMMITTER_DATE="2024-06-08 15:50:00"
        ;;
    "Added feature engineering notebook")
        export GIT_AUTHOR_DATE="2024-06-10 10:30:00"
        export GIT_COMMITTER_DATE="2024-06-10 10:30:00"
        ;;
    "Added model training notebook")
        export GIT_AUTHOR_DATE="2024-06-10 14:15:00"
        export GIT_COMMITTER_DATE="2024-06-10 14:15:00"
        ;;
    "Added CI workflow")
        export GIT_AUTHOR_DATE="2024-06-15 13:00:00"
        export GIT_COMMITTER_DATE="2024-06-15 13:00:00"
        ;;
esac
' -- --all

echo "✅ Dates fixed! Review with: git log --date=format:'%Y-%m-%d %H:%M' --pretty=format:'%ad - %s'"
echo "⚠️  To push: git push origin main --force"
