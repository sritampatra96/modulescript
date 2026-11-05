# Project: modulescript
A tool to add a script for any module. Also holds the Memory Optimizer Kit (a model/effort advisor, auto-compressing memory and staged task pipeline).

## Commands
- Start a task: `python memory-optimizer-kit/tools/kit.py task "<request>"`
- Finish a task: `python memory-optimizer-kit/tools/kit.py done <TASK_ID> "<result>"`
- Save a fact: `python memory-optimizer-kit/tools/kit.py remember <Profile|Projects|Decisions|Log> "<fact>"`

## Conventions
- The owner is not a coder: use simple language and do setup/implementation yourself.
- Python standard library only (no new dependencies).
- Model names live in `memory-optimizer-kit/config/models.json`.
- Never store secrets or API keys in memory files.

## Workflow
- Plan first for anything touching more than 2 files.
- Run the `task-optimizer` skill at the start of each new task.
- Small commits, one logical change each.

## Gotchas
- `memory-optimizer-kit.zip` mirrors the `memory-optimizer-kit/` folder; rebuild it after changing the folder.

## More context
- Build history: @docs/SESSION_LOG.md
