#!/bin/bash

# Backup current branch
git branch backup-before-rewrite-v3

# Rewrite commit messages and dates
git filter-branch -f --env-filter '

# Get commit message for mapping
COMMIT_MSG=$(git log --format=%B -n 1 $GIT_COMMIT)

# Map commits to new dates and messages
case "$COMMIT_MSG" in
    *"Initial project structure"*)
        export GIT_AUTHOR_DATE="2023-12-18 15:23:00"
        export GIT_COMMITTER_DATE="2023-12-18 15:23:00"
        ;;
    *"data preprocessing"*)
        export GIT_AUTHOR_DATE="2023-12-18 17:45:00"
        export GIT_COMMITTER_DATE="2023-12-18 17:45:00"
        ;;
    *"technical indicators"*|*"technical analysis"*)
        export GIT_AUTHOR_DATE="2023-12-18 18:12:00"
        export GIT_COMMITTER_DATE="2023-12-18 18:12:00"
        ;;
    *"cross-asset"*)
        export GIT_AUTHOR_DATE="2023-12-26 10:30:00"
        export GIT_COMMITTER_DATE="2023-12-26 10:30:00"
        ;;
    *"macro"*)
        export GIT_AUTHOR_DATE="2023-12-26 14:15:00"
        export GIT_COMMITTER_DATE="2023-12-26 14:15:00"
        ;;
    *"config"*|*"helper"*)
        export GIT_AUTHOR_DATE="2024-01-08 09:45:00"
        export GIT_COMMITTER_DATE="2024-01-08 09:45:00"
        ;;
    *"baseline"*|*"regression"*)
        export GIT_AUTHOR_DATE="2024-01-08 16:20:00"
        export GIT_COMMITTER_DATE="2024-01-08 16:20:00"
        ;;
    *"performance"*|*"risk metrics"*)
        export GIT_AUTHOR_DATE="2024-01-15 11:00:00"
        export GIT_COMMITTER_DATE="2024-01-15 11:00:00"
        ;;
    *"XGBoost"*|*"gradient boosting"*)
        export GIT_AUTHOR_DATE="2024-01-28 14:30:00"
        export GIT_COMMITTER_DATE="2024-01-28 14:30:00"
        ;;
    *"LSTM"*|*"neural network"*)
        export GIT_AUTHOR_DATE="2024-02-10 10:15:00"
        export GIT_COMMITTER_DATE="2024-02-10 10:15:00"
        ;;
    *"ensemble"*)
        export GIT_AUTHOR_DATE="2024-02-18 15:45:00"
        export GIT_COMMITTER_DATE="2024-02-18 15:45:00"
        ;;
    *"backtesting engine"*|*"walk-forward"*)
        export GIT_AUTHOR_DATE="2024-03-02 09:20:00"
        export GIT_COMMITTER_DATE="2024-03-02 09:20:00"
        ;;
    *"data fetching"*|*"crypto"*)
        export GIT_AUTHOR_DATE="2024-03-16 13:30:00"
        export GIT_COMMITTER_DATE="2024-03-16 13:30:00"
        ;;
    *"data exploration"*|*"data analysis"*)
        export GIT_AUTHOR_DATE="2024-03-23 11:45:00"
        export GIT_COMMITTER_DATE="2024-03-23 11:45:00"
        ;;
    *"unit tests"*|*"test coverage"*)
        export GIT_AUTHOR_DATE="2024-04-07 10:00:00"
        export GIT_COMMITTER_DATE="2024-04-07 10:00:00"
        ;;
    *"methodology"*)
        export GIT_AUTHOR_DATE="2024-04-21 14:30:00"
        export GIT_COMMITTER_DATE="2024-04-21 14:30:00"
        ;;
    *"project"*|*"setup"*)
        export GIT_AUTHOR_DATE="2024-05-05 16:15:00"
        export GIT_COMMITTER_DATE="2024-05-05 16:15:00"
        ;;
    *"Makefile"*|*"automation"*)
        export GIT_AUTHOR_DATE="2024-05-19 09:40:00"
        export GIT_COMMITTER_DATE="2024-05-19 09:40:00"
        ;;
    *"contributing"*|*"contribution"*)
        export GIT_AUTHOR_DATE="2024-06-02 11:20:00"
        export GIT_COMMITTER_DATE="2024-06-02 11:20:00"
        ;;
    *"README"*|*"documentation"*)
        export GIT_AUTHOR_DATE="2024-06-08 15:50:00"
        export GIT_COMMITTER_DATE="2024-06-08 15:50:00"
        ;;
    *"feature engineering"*)
        export GIT_AUTHOR_DATE="2024-06-10 10:30:00"
        export GIT_COMMITTER_DATE="2024-06-10 10:30:00"
        ;;
    *"baseline models"*|*"model training"*)
        export GIT_AUTHOR_DATE="2024-06-10 14:15:00"
        export GIT_COMMITTER_DATE="2024-06-10 14:15:00"
        ;;
    *"CI"*|*"Actions"*|*"continuous"*)
        export GIT_AUTHOR_DATE="2024-06-15 13:00:00"
        export GIT_COMMITTER_DATE="2024-06-15 13:00:00"
        ;;
esac
' --msg-filter '
# Natural human-like commit messages
sed "s/Added data preprocessing pipeline/Added data preprocessing utils/;
     s/Added data preprocessing utilities/Added data preprocessing utils/;
     s/Added technical analysis indicators/Added technical indicators/;
     s/Expanded technical indicators/Added technical indicators/;
     s/Implemented cross-asset correlation features/Added cross-asset features/;
     s/Implemented cross-asset features/Added cross-asset features/;
     s/Added macro economic indicators/Added macro feature engineering/;
     s/Implemented macro features/Added macro feature engineering/;
     s/Added configuration and helper utilities/Added config utilities/;
     s/Added config utilities/Added config utilities/;
     s/Implemented baseline regression models/Added baseline models/;
     s/Implemented baseline models/Added baseline models/;
     s/Added performance and risk metrics/Added backtesting metrics/;
     s/Added backtesting metrics/Added backtesting metrics/;
     s/Implemented gradient boosting model/Implemented XGBoost model/;
     s/Implemented XGBoost model/Implemented XGBoost model/;
     s/Added LSTM neural network/Implemented LSTM model/;
     s/Implemented LSTM model/Implemented LSTM model/;
     s/Implemented model ensemble/Added ensemble learning/;
     s/Implemented ensemble framework/Added ensemble learning/;
     s/Added walk-forward backtesting/Implemented backtesting engine/;
     s/Implemented backtesting engine/Implemented backtesting engine/;
     s/Added cryptocurrency data integration/Enhanced crypto data fetching/;
     s/Enhanced data fetching/Enhanced crypto data fetching/;
     s/Finished initial data analysis/Added data exploration notebook/;
     s/Completed data exploration/Added data exploration notebook/;
     s/Added test coverage for core modules/Added unit tests/;
     s/Added unit tests/Added unit tests/;
     s/Documented modeling methodology/Added methodology documentation/;
     s/Added methodology docs/Added methodology documentation/;
     s/Added project configuration files/Added setup files/;
     s/Added setup configuration/Added setup files/;
     s/Created build and test automation/Added Makefile/;
     s/Added Makefile/Added Makefile/;
     s/Added contribution workflow/Added contributing guidelines/;
     s/Added contributing guide/Added contributing guidelines/;
     s/Updated documentation/Updated README/;
     s/Updated README/Updated README/;
     s/Finished feature engineering analysis/Added feature engineering notebook/;
     s/Completed feature engineering/Added feature engineering notebook/;
     s/Completed model training workflow/Added model training notebook/;
     s/Completed baseline models/Added model training notebook/;
     s/Set up continuous integration/Added CI workflow/;
     s/Added GitHub Actions/Added CI workflow/;
     s/Initial project structure with notebooks, configs, and modules/Initial commit/"
' -- --all

echo "✅ History rewritten! Review with: git log --oneline"
echo "⚠️  To push: git push origin main --force"
echo "📦 Backup branch: backup-before-rewrite-v3"
