---
name: verify
description: Check the work is correct before committing. Use before every commit or when asked to verify.
---
1. `python -m py_compile memory-optimizer-kit/tools/kit.py`
2. `python memory-optimizer-kit/tools/kit.py task "verify smoke test"` runs without error.
3. Re-read the diff against the user's goal; report what was and was not checked.
