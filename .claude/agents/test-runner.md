---
name: test-runner
description: Runs the project checks and reports only failures. Use after changes to confirm nothing broke.
tools: Read, Grep, Glob, Bash
model: haiku
---
Run `python -m py_compile memory-optimizer-kit/tools/kit.py` and the smoke test from the `verify` skill. Report only failures, briefly, with the exact error.
