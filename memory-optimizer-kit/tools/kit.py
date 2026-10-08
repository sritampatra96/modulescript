#!/usr/bin/env python3
"""Memory optimizer + model/effort router. Standard library only (works in ChatGPT's Python sandbox and Codex).

Commands (run from the kit folder):
  python tools/kit.py task "describe the new task"     # ONE command per new task: route + context + plan
  python tools/kit.py route "describe the task"        # just model + effort advice
  python tools/kit.py remember "Section" "fact"        # save a fact (Profile/Projects/Decisions/Log)
  python tools/kit.py done TASK_ID "one-line result"   # close a task, log it, compress memory
  python tools/kit.py compress                         # shrink memory to budget
  python tools/kit.py status                           # memory size + recent tasks
  python tools/kit.py export                           # make a fresh zip with updated memory
"""
import json, re, sys, zipfile, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM, ARC, LOG = ROOT / "memory/MEMORY.md", ROOT / "memory/ARCHIVE.md", ROOT / "memory/TASK_LOG.md"
CFG = json.loads((ROOT / "config/models.json").read_text())

# ---------- router ----------
SIGNALS = {  # keyword -> (gravity points, kind)
    "coding": (r"\b(code|bug|fix|function|script|api|app|website|refactor|test|deploy|repo|python|javascript|sql|build|implement|debug|error|crash)\b", 1),
    "architecture": (r"\b(architecture|design system|migrate|migration|redesign|scal|from scratch|multi[- ]?file|whole project|end[- ]to[- ]end)\b", 2),
    "risk": (r"\b(production|delete|payment|security|auth|password|legal|medical|financial|tax|contract|irreversible|customer data)\b", 2),
    "research": (r"\b(research|compare|analy[sz]e|investigate|literature|market|strategy|evaluate|audit)\b", 1),
    "writing": (r"\b(write|essay|article|report|email|post|story|summar|rewrite|translate|proofread)\b", 0),
    "simple": (r"\b(quick|simple|small(?! business)|tiny|rename|typo|one[- ]line|just|short|reword|format)\b", -1),
}

def route(task: str) -> dict:
    t = task.lower()
    hits = {k: bool(re.search(p, t)) for k, (p, _) in SIGNALS.items()}
    g = 2 + sum(SIGNALS[k][1] for k, h in hits.items() if h)
    words = len(task.split())
    g += 1 if words > 60 else 0
    g += 1 if words > 200 else 0
    g += 1 if len(re.findall(r"\b(and then|then|also|after that|step|stage|first|second|finally)\b", t)) >= 3 else 0
    if words < 10 and not hits["risk"]:
        g = min(g, 3)  # short, low-risk asks rarely need max effort
    g = max(1, min(5, g))
    coding = hits["coding"] or hits["architecture"]
    tier = {1: "light", 2: "light", 3: "standard", 4: "deep", 5: "max"}[g]
    if hits["research"] and not hits["simple"]:
        g = max(g, 3)  # research/analysis is never a trivial ask
    if g == 2 and (hits["research"] or coding) and not hits["simple"]:
        tier = "standard"
    spec = CFG["tiers"][tier]
    effort = spec["efforts"][0] if g <= 2 else spec["efforts"][-1] if g >= 4 else spec["efforts"][min(1, len(spec["efforts"]) - 1)]
    kind = "coding" if coding else "research" if hits["research"] else "writing" if hits["writing"] else "general"
    return {"gravity": g, "kind": kind, "tier": tier,
            "model": spec["coding_model"] if coding else spec["model"], "effort": effort,
            "reason": f"gravity {g}/5 from {', '.join(k for k, h in hits.items() if h) or 'no strong signals'}; {words} words",
            "tip": "Start one tier lower if the first answer is fine; escalate effort (not model) first if it is wrong."}

# ---------- memory ----------
def read(p): return p.read_text() if p.exists() else ""

def remember(section: str, fact: str):
    text, head = read(MEM), f"## {section}"
    if head not in text:
        text = text.rstrip() + f"\n\n{head}\n"
    stamp = dt.date.today().isoformat()
    line = f"- [{stamp}] {fact.strip()}"
    parts = re.split(r"(?m)^(?=## )", text)
    parts = [p.rstrip() + f"\n{line}\n\n" if p.startswith(head) else p for p in parts]
    MEM.write_text("".join(parts).rstrip() + "\n")

def compress():
    """Deterministic, no AI needed: move oldest Log lines to ARCHIVE, then trim long lines."""
    text, budget, keep = read(MEM), CFG["context_budget_chars"], CFG["archive_keep_recent_log"]
    m = re.search(r"(?ms)^## Log\n(.*?)(?=^## |\Z)", text)
    if m:
        lines = [l for l in m.group(1).splitlines() if l.startswith("- ")]
        old = lines[:-keep] if len(lines) > keep else []
        while len(text) > budget and len(lines) > 3 and not old:
            old, lines = lines[:1], lines[1:]
        if old:
            ARC.write_text(read(ARC).rstrip() + "\n" + "\n".join(old) + "\n")
            new_body = "(newest at bottom; old items are auto-moved to ARCHIVE.md)\n" + "\n".join(l for l in lines if l not in old) + "\n\n"
            text = text[:m.start(1)] + new_body + text[m.end(1):]
    text = "\n".join(l if len(l) < 240 else l[:237] + "..." for l in text.splitlines()) + "\n"
    MEM.write_text(text)
    return len(text)

def relevant_archive(task: str, limit=6):
    words = {w for w in re.findall(r"[a-z]{4,}", task.lower())}
    scored = [(len(words & set(re.findall(r"[a-z]{4,}", l.lower()))), l) for l in read(ARC).splitlines() if l.startswith("- ")]
    return [l for s, l in sorted(scored, reverse=True)[:limit] if s]

# ---------- task pipeline ----------
STAGES = ["1. CLARIFY - restate the goal; ask at most 3 questions only if truly blocked, else assume and say so",
          "2. MAP - list the files/info/context needed; ignore everything else",
          "3. SPLIT - break into small stages, each with a clear 'done' check",
          "4. DO - run one stage at a time; keep notes short",
          "5. VERIFY - test / re-read against the goal; fix before reporting",
          "6. SUMMARIZE - plain-language result, then run: python tools/kit.py done <TASK_ID> \"result\""]

def new_task(desc: str):
    r = route(desc)
    tid = dt.datetime.now().strftime("T%Y%m%d-%H%M%S")
    ctx = read(MEM)
    arch = relevant_archive(desc)
    pack = ctx + ("\n## Relevant older memory\n" + "\n".join(arch) + "\n" if arch else "")
    depth = "Think briefly; answer directly." if r["gravity"] <= 2 else "Plan first, work in stages, verify before answering." if r["gravity"] <= 4 else "Think carefully, double-check assumptions, verify every stage, flag risks."
    prompt = f"""# TASK {tid}
## Goal
{desc}

## Recommended setup
Model: {r['model']}   Reasoning effort: {r['effort']}   (gravity {r['gravity']}/5, {r['kind']})
Why: {r['reason']}
If your current model/effort differs, tell the user once, in one line, and continue anyway.

## How to work ({depth})
""" + "\n".join(STAGES) + f"""

## Context (use only what is relevant; do not repeat it back)
{pack}
## Rules
- Simple language. User is not a coder: do the setup/implementation yourself.
- Do not ask permission for routine steps. Confirm only before irreversible/outward actions.
- Be honest about what was verified and what was not.
"""
    (ROOT / "tasks" / f"{tid}.md").write_text(prompt)
    with LOG.open("a") as f:
        f.write(f"- {tid} OPEN [{r['tier']}/{r['effort']}] {desc[:120]}\n")
    print(prompt)

def done(tid: str, result: str):
    with LOG.open("a") as f:
        f.write(f"- {tid} DONE {result}\n")
    remember("Log", f"{tid}: {result}")
    print(f"closed {tid}; memory now {compress()} chars")

def status():
    print(f"memory: {len(read(MEM))}/{CFG['context_budget_chars']} chars, archive: {len(read(ARC))} chars")
    print("\n".join(read(LOG).splitlines()[-8:]))

def export():
    out = ROOT.parent / "memory-optimizer-kit.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(ROOT.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p, Path(ROOT.name) / p.relative_to(ROOT))
    print(f"saved {out}  <- download this and upload it next time to keep your memory")

if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0] if a else ""
    if cmd == "route" and len(a) > 1: print(json.dumps(route(" ".join(a[1:])), indent=2))
    elif cmd == "task" and len(a) > 1: new_task(" ".join(a[1:]))
    elif cmd == "remember" and len(a) >= 3: remember(a[1], " ".join(a[2:]))
    elif cmd == "done" and len(a) >= 3: done(a[1], " ".join(a[2:]))
    elif cmd == "compress": print("memory now", compress(), "chars")
    elif cmd == "status": status()
    elif cmd == "export": export()
    else: print(__doc__)
