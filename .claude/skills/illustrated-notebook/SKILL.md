---
name: illustrated-notebook
description: Use when the user asks to build a new module/topic in the "Illustrated Notebook" style (the Thermodynamics notebook format): story-first narration, hand-drawn notebook look, equation boxes, worked problems with solutions, and interactive artifacts. Also use when asked to convert lesson scripts into that style.
---

# Illustrated Notebook (house style)

The user is not a coder: do the building yourself, simple language.

1. Read `works/illustrated-notebook/STYLE_GUIDE.md` (look, page anatomy, narration voice, problem rules, checklist).
2. Copy `works/illustrated-notebook/template.html` to `works/<module-name>/<module-name>.html` and fill it in. Keep the CSS tokens and component classes as they are.
3. Build in this order: cover and stat strip, intro hook, numbered sections (figure, rule in words, equation box, symbols, examiner tip), worked problems (new, slightly harder, full solutions), one interactive artifact per 2-3 sections reusing a worked problem's numbers, closing summary, Bonus Trivia, Question Sources Note.
4. Verify: open in Chromium (Playwright is installed), check the slider/toys work, check phone width and print, and check artifact numbers match the solutions.
5. The original reference PDF is `works/illustrated-notebook/reference/Thermodynamics_Illustrated_Notebook.pdf`. Never edit or delete it.
6. Publish as an Artifact only if the user asks to share.
