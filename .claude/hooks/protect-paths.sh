#!/bin/bash
# Blocks edits to secret files. Exit 2 = block and tell Claude why.
f=$(python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
case "$f" in
  *.env|*.env.*|*/secrets/*|*.pem|*.key)
    echo "Blocked: $f looks like a secrets file." >&2
    exit 2;;
esac
exit 0
