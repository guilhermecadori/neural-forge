#!/usr/bin/env sh
# dvc-bootstrap.sh — initialize DVC in a neural-forge project following
# the conventions in docs/adr/0001-dvc-remote-strategy.md.
#
# Usage (from the monorepo root):
#   scripts/dvc-bootstrap.sh projects/<project-name>
#
# What it does:
#   1. Runs `dvc init` in the target project (idempotent).
#   2. Writes a committed .dvc/config declaring a 'local' remote whose URL
#      is the repo-relative path ../../../.dvc-store/<project-name>.
#      DVC resolves this relative to .dvc/config, so it works on every
#      clone and every CI runner with zero per-machine setup.
#   3. Creates the matching folder under .dvc-store/ at the monorepo root.

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

# Resolve the monorepo root as the directory containing this script's parent.
script_dir=$(cd "$(dirname "$0")" && pwd)
repo_root=$(cd "$script_dir/.." && pwd)

project_name=$(basename "$project_path")
store_path="$repo_root/.dvc-store/$project_name"
remote_url="../../../.dvc-store/$project_name"

echo "==> project:     $project_path"
echo "==> store path:  $store_path"
echo "==> remote url:  $remote_url  (resolved relative to .dvc/config)"

mkdir -p "$store_path"
# Preserve the folder even when empty so CI clones see the remote target.
: > "$store_path/.gitkeep"

cd "$project_path"

if [ ! -d .dvc ]; then
  dvc init
else
  echo "==> .dvc already exists, skipping 'dvc init'"
fi

# Committed config: declare the 'local' remote with a repo-relative URL.
# No config.local. No env vars. No credentials.
cat > .dvc/config <<EOF
[core]
    remote = local
['remote "local"']
    url = $remote_url
# The remote URL is repo-relative and resolved against this config file.
# See docs/adr/0001-dvc-remote-strategy.md for the rationale.
EOF

echo "==> done. Verify with:  (cd $project_path && dvc remote list)"
