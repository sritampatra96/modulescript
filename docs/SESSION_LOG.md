# Session log: building the Memory Optimizer Kit

Summary of the work and decisions in this build session (not a verbatim transcript).

## Request
A Codex- and GPT-friendly memory usage optimization tool plus a best-model-and-effort prompter, deliverable as a zip that ChatGPT/Codex can accept, set itself up from, and run on every new task.

## What was built
| Piece | Purpose |
|---|---|
| `tools/kit.py` | Router (gravity 1-5 -> tier, model, effort), memory (`remember`, deterministic `compress`, archive recall), pipeline (`task`, `done`), `export` to re-zip |
| `config/models.json` | Editable model table and memory budget |
| `AGENTS.md` | Codex reads it automatically; defines the per-task protocol |
| `GPT_INSTRUCTIONS.md`, `BOOTSTRAP_PROMPT.txt` | ChatGPT setup from the uploaded zip |
| `DEFAULT_ON.md` | Always-on setup: ChatGPT Custom instructions, Project/Custom GPT, Codex global `AGENTS.md` |
| `skills/task-optimizer/` | Same protocol as a skill that fires on every new task |

## Decisions
- Standard library Python only, so it runs in ChatGPT's sandbox and Codex.
- Memory compression is rule-based (no AI calls, no cost).
- ChatGPT cannot keep files between chats, so `kit.py export` produces an updated zip to re-upload.
- The advisor recommends; ChatGPT cannot switch its own model, the user picks it in the menu.

## Testing
Clean-unzip run: 6 sample tasks through the router, full task flow, 40-note compression, archive recall, export. Found and fixed one bug: "small business" was read as an easy-task signal, and research tasks could rate as trivial.

## History
- PR 1: kit, docs, default-on setup.
- PR 2: router fix (research tasks never trivial).
- PR 3: `task-optimizer` skill.
- Next change: README and this log.

## Not verified
Not run inside ChatGPT or Codex themselves; model names are examples.
