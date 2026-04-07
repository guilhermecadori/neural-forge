#!/usr/bin/env sh
# dvc-bootstrap.sh — initialize DVC in a neural-forge project following
# the conventions in docs/adr/0001-dvc-remote-strategy.md.
#
# Usage (from the monorepo root):
#   scripts/dvc-bootstrap.sh projects/<project-name>
#
# What it does:
#   1. Runs `dvc init` in the target project (idempotent).
#   2. Writes a committed .dvc/config that declares the 'onedrive' remote
#      as the default, with NO url (machine-specific paths live elsewhere).
#   3. Writes a git-ignored .dvc/config.local with the absolute OneDrive
#      path for this machine, derived from $ONEDRIVE_DVC or a sensible
#      Windows default.
#   4. Creates the corresponding folder on disk.
#
# Required environment:
#   ONEDRIVE_DVC   Optional. Absolute path to your personal DVCStore root.
#                  Defaults to "$OneDrive/DVCStore" if OneDrive is set,
#                  otherwise "C:/Users/$USER/OneDrive/DVCStore".

set -eu

if [ $# -ne 1 ]; then
  echo "usage: $0 <path-to-project>" >&2
  exit 2
fi

project_path=$1
if [ ! -d "$project_path" ]; then
  echo "error: '$project_path' is not a directory" >&2
  exit 1
fi

project_name=$(basename "$project_path")

# Resolve the DVCStore root.
if [ -n "${ONEDRIVE_DVC:-}" ]; then
  store_root=$ONEDRIVE_DVC
elif [ -n "${OneDrive:-}" ]; then
  store_root="$OneDrive/DVCStore"
elif [ -n "${OneDriveConsumer:-}" ]; then
  store_root="$OneDriveConsumer/DVCStore"
else
  store_root="C:/Users/${USER:-$USERNAME}/OneDrive/DVCStore"
fi

remote_path="$store_root/neural-forge/$project_name"

echo "==> project:     $project_path"
echo "==> remote path: $remote_path"

mkdir -p "$remote_path"

cd "$project_path"

if [ ! -d .dvc ]; then
  dvc init
else
  echo "==> .dvc already exists, skipping 'dvc init'"
fi

# Committed config: declare the remote and default, no URL.
cat > .dvc/config <<EOF
[core]
    remote = onedrive
# The 'onedrive' remote URL is intentionally not set here.
# It is a personal, machine-specific path defined in .dvc/config.local,
# which is git-ignored. See docs/adr/0001-dvc-remote-strategy.md
# in the monorepo root for the rationale and setup instructions.
EOF

# Machine-local config: the real absolute path.
cat > .dvc/config.local <<EOF
['remote "onedrive"']
    url = $remote_path
EOF

echo "==> done. Verify with:  (cd $project_path && dvc remote list)"
