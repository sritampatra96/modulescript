---
name: fix-issue
description: Read a GitHub issue, reproduce it, fix it, run checks, and commit. Use when the user gives an issue number to fix.
argument-hint: [issue-number]
disable-model-invocation: true
---
Fix issue $ARGUMENTS:
1. Read the issue with the GitHub tools.
2. Reproduce it (a failing check or script first).
3. Make the smallest fix; re-run the check.
4. Run the `verify` skill, then commit with a clear message.
