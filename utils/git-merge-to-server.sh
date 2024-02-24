#!/bin/sh
# @desc Initialize python venv
# @changed 2024.02.24, 14:31

TARGET_SERVER_BRANCH="server"

test -f "./utils/config.sh" && . "./utils/config.sh"
test -f "./utils/config-local.sh" && . "./utils/config-local.sh"

git update-index --refresh

GIT_CHANGES=`git diff-index HEAD --`

if [ "$GIT_CHANGES" != "" ] && [[ ! "$*" =~ .*--allow-uncommited-changes.* ]]; then
  echo "The project has uncommited changes. Please commit them before merging."
  exit 1
fi

CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

echo "Trying to merge current branch '$CURRENT_BRANCH' into the '$TARGET_SERVER_BRANCH'..."

git checkout $TARGET_SERVER_BRANCH \
  && git pull && \
  git rebase $CURRENT_BRANCH && \
  git push && \
  git checkout $CURRENT_BRANCH && \
  echo Ok
