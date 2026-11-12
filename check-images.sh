#!/usr/bin/env bash
# Run from the repository root:  bash tools/check-images.sh
# Lists every image the README points to and tells you if the file is missing
# or if its name could cause trouble on GitHub (spaces, capital letters).
set -u
bad=0
for p in $(grep -oE '\]\((assets|screenshots)/[^)]+\)|src="(assets|screenshots)/[^"]+"' README.md \
           | sed -E 's/^\]\(//; s/\)$//; s/^src="//; s/"$//' | sort -u); do
  if [ -f "$p" ]; then
    echo "OK       $p"
  else
    echo "MISSING  $p"; bad=1
  fi
  case "$p" in *[A-Z]*|*" "*) echo "WARNING  $p has capitals or spaces (GitHub paths are case-sensitive)"; bad=1;; esac
done
[ $bad -eq 0 ] && echo && echo "All images found. Safe to push." || { echo; echo "Fix the lines above before you push."; exit 1; }
