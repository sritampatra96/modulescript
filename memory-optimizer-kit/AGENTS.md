# Memory Optimizer Kit - standing instructions (Codex reads this file automatically)

You are working with a user who is NOT a coder. Use simple language. Do setup and implementation yourself.

## Run this protocol for EVERY new task, without being asked
1. Run: `python tools/kit.py task "<the user's request in their words>"`
   - It picks the best model + reasoning effort, builds a small context pack from `memory/`, and writes a staged plan to `tasks/`.
2. Tell the user ONE line: the recommended model + effort and why. If your current setting differs, say so once, then continue.
3. Follow the printed stages: CLARIFY > MAP > SPLIT > DO > VERIFY > SUMMARIZE. Work stage by stage; keep notes short.
4. Save anything worth remembering: `python tools/kit.py remember <Profile|Projects|Decisions|Log> "fact"`
5. Finish with: `python tools/kit.py done <TASK_ID> "one-line result"` (this logs and auto-compresses memory).
6. In the final answer give: result, what you verified, what you did not verify.

## Memory rules
- Read `memory/MEMORY.md` at the start of a session. Do not read ARCHIVE.md in full; the tool pulls only relevant lines.
- Never paste memory back to the user. Never store secrets, passwords, or API keys in memory.
- Prefer escalating reasoning effort before switching to a bigger model.
- Edit `config/models.json` if model names differ in the user's account.

## Skill
`skills/task-optimizer/SKILL.md` is this same protocol as a skill. Install it by copying the folder `skills/task-optimizer` into `~/.codex/skills/` (Codex) or `~/.claude/skills/` (Claude Code); it then runs on every new task.
