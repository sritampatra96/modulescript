#!/usr/bin/env python3
"""One-time installer: puts the Claude Code Setup Playbook on YOUR computer.

Run from inside this repo:   python scripts/install_local_setup.py
Safe to re-run. Existing files are backed up as <name>.bak, never lost.
Standard library only.
"""
import shutil, sys, json, time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOME = Path.home() / ".claude"

PERSONAL_CLAUDE_MD = """# About me
- I am not a coder. Use simple language and do the setup/implementation yourself.
- Do not ask permission for routine steps. Confirm only before irreversible or outward actions
  (deleting, overwriting, sending, publishing, pushing).
- For long or serious work, remind me to use my pinned project "Claude Memory Usage Optimiser".
- Be honest about what you verified and what you did not.
- Plan first for anything big; verify before saying done; summarize in plain words.
"""

PERSONAL_SETTINGS = {
    "$schema": "https://json-schema.org/claude-code-settings.json",
    "permissions": {
        "deny": [
            "Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)",
            "Bash(git push --force *)", "Bash(rm -rf *)",
        ]
    },
}

def backup_write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") == text:
            print(f"  same   {path}"); return
        shutil.copy2(path, path.with_name(path.name + f".{int(time.time())}.bak"))
    path.write_text(text, encoding="utf-8"); print(f"  wrote  {path}")

def copy_tree(src: Path, dst: Path):
    if not src.exists(): return
    for f in src.rglob("*"):
        if f.is_file() and "__pycache__" not in f.parts:
            backup_write(dst / f.relative_to(src), f.read_text(encoding="utf-8"))

def main():
    print("Personal setup ->", HOME)
    backup_write(HOME / "CLAUDE.md", PERSONAL_CLAUDE_MD)

    sp = HOME / "settings.json"
    cur = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
    cur.setdefault("$schema", PERSONAL_SETTINGS["$schema"])
    deny = cur.setdefault("permissions", {}).setdefault("deny", [])
    for rule in PERSONAL_SETTINGS["permissions"]["deny"]:
        if rule not in deny: deny.append(rule)
    backup_write(sp, json.dumps(cur, indent=2) + "\n")

    # personal skills + agents (task-optimizer needs the kit path, so keep it per-project)
    for name in ("plan-feature", "fix-issue", "commit"):
        copy_tree(REPO / ".claude/skills" / name, HOME / "skills" / name)
    copy_tree(REPO / ".claude/agents", HOME / "agents")

    print("\nDone. Project setup (CLAUDE.md, .claude/, hook) already lives in this repo.")
    print("Next: open a terminal in this repo, run `claude`, then type /doctor and /context.")

if __name__ == "__main__":
    sys.exit(main())
