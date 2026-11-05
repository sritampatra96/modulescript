---
name: commit
description: Run checks, then write a conventional commit message from the diff and commit. Use when the user says commit.
disable-model-invocation: true
allowed-tools: Bash(git status) Bash(git diff *) Bash(git add *) Bash(git commit *)
---
1. Run the `verify` skill; stop if it fails.
2. Look at `git diff` and write a conventional message (feat/fix/docs/chore: short summary).
3. One logical change per commit.
