---
name: task-optimizer
description: Use at the start of EVERY new task, however small, before doing any work. Picks the best model and reasoning effort, loads only the relevant memory, runs the staged plan (Clarify, Map, Split, Do, Verify, Summarize), and saves what is worth remembering when the task ends.
---

# Task Optimizer (runs on every new task)

The user is not a coder: simple language, do the setup and implementation yourself.

## 1. Start (always, before working)
Run: `python memory-optimizer-kit/tools/kit.py task "<the user's request in their words>"`
- It prints the recommended model + reasoning effort, a small context pack from memory, and a staged plan.
- Tell the user ONE line: "Recommended: <model> / <effort> because <reason>." If the current setting differs, say so once, then continue.
- If the task is a follow-up in the same conversation, do not rerun it; reuse the open task.

## 2. Work the stages
CLARIFY (max 3 questions, only if truly blocked, else assume and say so) > MAP (only the context needed) > SPLIT (small stages, each with a done-check) > DO (one stage at a time) > VERIFY (test or re-read against the goal) > SUMMARIZE.
Raise reasoning effort before switching to a bigger model. Confirm only before irreversible or outward actions.

## 3. Finish (always)
- Save durable facts: `python memory-optimizer-kit/tools/kit.py remember <Profile|Projects|Decisions|Log> "fact"`
- Close: `python memory-optimizer-kit/tools/kit.py done <TASK_ID> "one-line result"` (logs it and compresses memory).
- Final answer: result, what you verified, what you did not.

## Rules
- Never store secrets, passwords or API keys in memory. Never paste memory back to the user.
- Model names live in config/models.json; edit them if the user's account differs.
