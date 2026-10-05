# Make it the DEFAULT (no pasting per task)

## ChatGPT - 2 ways (pick one)
**A. Every chat, automatically (easiest):** ChatGPT > Settings > Personalization > Custom instructions.
Paste the block below into "How would you like ChatGPT to respond?". It now applies to every new chat/task.
This works even without the zip (no Python needed).

**B. Project / Custom GPT (adds saved memory):** Create a Project (or Custom GPT). Paste the same block into its Instructions and add `memory-optimizer-kit.zip` to Project files / Knowledge. Every chat inside it auto-starts with the kit. Download the updated zip from the end of a chat and replace the file when you want to keep new memory.

### Block to paste (default-on)
```
For EVERY new task, automatically, without being asked:
1. Start with ONE line: "Recommended: <model> / <effort> because <reason>."
   Router: simple/short/low-risk -> light model, minimal-low effort. Normal multi-step work or coding -> standard, medium. Big, risky, multi-file, production, money, legal, security -> deep/max, high effort. Raise effort before switching to a bigger model.
2. Work in stages: Clarify (max 3 questions, only if blocked) > Map needed context only > Split into small stages > Do > Verify > Summarize.
3. Keep memory lean: remember only durable facts (my profile, projects, decisions). Never repeat memory back, never store secrets. Summarize old context instead of re-reading it.
4. If memory-optimizer-kit.zip is available, unzip it with Python, read AGENTS.md and use tools/kit.py (task / remember / done). At the end run `kit.py export` and give me the updated zip.
5. I am not a coder: simple words, do the work yourself, say what you verified and what you did not.
```

## Codex - global default
Copy the kit's `AGENTS.md` to `~/.codex/AGENTS.md` (applies to every project and task). Copy the `tools/`, `config/`, `memory/` folders to `~/.codex/memory-kit/` and change the paths in that AGENTS.md from `tools/kit.py` to `~/.codex/memory-kit/tools/kit.py`.
For one project only, just unzip the kit into the project: Codex reads its `AGENTS.md` automatically.

## Skill version (Codex / Claude Code)
Copy `skills/task-optimizer/` into `~/.codex/skills/` or `~/.claude/skills/`. Its description tells the agent to run it at the start of EVERY task. Edit the `tools/kit.py` path inside SKILL.md if you put the kit somewhere else.
