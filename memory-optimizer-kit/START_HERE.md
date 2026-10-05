# Memory Optimizer Kit - how to use (3 steps, no coding)

**Want it ON BY DEFAULT for every task (no pasting)? Read `DEFAULT_ON.md` first.**

**What it does**
- *Model & effort prompter*: for each new task it tells you which model and reasoning effort to pick (light / standard / deep / max) and why.
- *Memory optimizer*: keeps a short memory file (profile, projects, decisions, log). Old items move to an archive and only relevant ones come back, so every task starts with a small, focused context.
- *Delivery pipeline*: every task runs the same staged plan: Clarify > Map > Split > Do > Verify > Summarize.

## In ChatGPT
1. Start a new chat (Data analysis / Python must be on). Upload `memory-optimizer-kit.zip`.
2. Paste the text from `BOOTSTRAP_PROMPT.txt` and replace `<TYPE YOUR TASK HERE>`.
3. It unzips itself, reads `AGENTS.md`, and handles the task. At the end download the updated zip it gives you and use that one next time (this is how memory survives between chats).
Optional: create a Custom GPT, paste `GPT_INSTRUCTIONS.md` into Instructions, and put the zip in Knowledge so you only type the task.

## In Codex (CLI / cloud / IDE)
1. Unzip into your project (or its own folder). Codex reads `AGENTS.md` automatically.
2. Just describe your task. Memory is saved in the folder and persists, no export needed.

## Tune it
- Model names differ per account: edit `config/models.json` (one small file).
- Memory size limit: `context_budget_chars` in the same file.

## Commands (the AI runs these for you)
`python tools/kit.py task "..."` | `route "..."` | `remember Section "fact"` | `done ID "result"` | `compress` | `status` | `export`

Note: the advisor suggests a model/effort; ChatGPT cannot switch its own model mid-chat, so you pick it in the model menu. Codex lets you set both with `/model`.
