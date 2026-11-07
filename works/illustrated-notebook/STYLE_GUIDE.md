# Illustrated Notebook: Style Guide

Captured from **Thermodynamics: Heat. Work. Change.** (IBDP Physics HL, "The Illustrated Notebook", 50 pages, Dr. Soumya Ranjan Senapati).
The original is saved in `reference/Thermodynamics_Illustrated_Notebook.pdf`. Use this guide plus `template.html` for every new module.

## 1. The big idea
A module is a **teaching script turned into a hand-drawn science notebook**: story first, then the rule, then the maths, then practice, with small interactive toys along the way. It reads like a good teacher talking, not like a textbook.

## 2. Page and look
| Element | Rule |
|---|---|
| Paper | Warm cream (`#fdf8ea`) with faint blue ruled lines and a thin red margin line on the left. |
| Fonts | Rounded, friendly "comic-notebook" face for everything (Comic Neue / Comic Sans MS). Equations in italic serif/math style. Small letter-spaced caps for labels. |
| Colours | Navy `#1d3a7a` (headings, text), Red `#d64030` (accents, labels, the second line of the title), Yellow `#f2c230` (highlights, card top bars), Green `#2e7d32` (equations, worked solutions), Soft blue `#eaf3fd` (physics-model panels). |
| Cards | Cream fill, 2px navy border, rounded corners, a soft offset shadow. |
| Footer | `MODULE NAME · COURSE | page / total` in small grey. |
| Print | The HTML has print CSS. Worked solutions are expanded when printed. A PDF companion has static illustrations. |

## 3. Page anatomy (in order)
1. **Cover**
   - Small red letter-spaced kicker: `IBDP PHYSICS HL · THE ILLUSTRATED NOTEBOOK`.
   - Huge navy title ending in a full stop (`THERMODYNAMICS.`), then a red three-word tagline (`Heat. Work. Change.`) with a yellow underline.
   - One-line subtitle, then "Demo Script, Draft for approval", then author name.
   - One hero illustration in a framed card.
   - **Stat strip** of four numbers: source pages, worked problems, figures redrawn, interactive artifacts.
   - Yellow dashed **"About this illustrated edition"** box that states what is kept (narration, data, solutions, trivia), the flow of topics, and the print and PDF notes.
2. **Section 00, Introduction:** a historical hook (a person, a year, a surprise), never a definition.
3. **Numbered sections** (`01`, `02`, ...) with a pink circle badge and a dashed blue rule above the heading.
4. **Closing section:** an "Extension" (a big-picture idea, e.g. Maxwell's demon and heat death), a one-paragraph summary of the module's laws, **Bonus Trivia** with a star, and a **Question Sources Note**.

## 3b. Interlinks (moving between sections)
Every module must be navigable. The template builds all of this automatically from the section headings:
- **Contents bar** pinned at the top: one numbered chip per section, the current section is highlighted in yellow, click any chip to jump there.
- **Bridge box** between every two sections: a blue dashed box with a one-line hook ("Next up: ...") and two buttons, `← Back: <previous section>` and `Go: <next section> →`. The hook comes from `data-bridge="..."` on the next section.
- **Back-to-top button** (↑) appears after scrolling down. Last bridge offers `↑ Contents`.
- **How to use:** give every section header `class="sec" id="sNN" data-bridge="one sentence that links the previous idea to this one"`. Write the bridge sentence like the notebook's own transitions ("Heat flows hot to cold, never the reverse. To describe this direction we need entropy.").
- Hidden when printing.

## 4. Building blocks
- **Figure card.** Label `FIGURE 03` in small caps, then the image, then a dashed divider, then the caption `Figure 3.` (bold) with a plain description, then a tiny italic note: *AI-generated notebook illustration · diagram geometry and question data define the physics.*
  - **Two-up figure:** a cartoon illustration on the left (coloured-pencil style, objects with faces and a thumbs-up, yellow "spark" lines) and a **PHYSICS MODEL** panel on the right (blue dashed box with a clean, labelled schematic).
  - Pure-diagram figures (p-V graphs, T-S rectangle) use thin axes, one coloured path per idea (rust red and teal), a soft shaded area, and the label placed inside the shape.
- **Equation box.** Centred equation in a rounded box with a green border and a green offset shadow. Under it, a plain list of symbols: `ΔU = change in internal energy (J)`, one per line, with units. Colour-code the same symbol across a module (e.g. Q red, ΔU purple, W blue).
- **Examiner tip.** Yellow dashed box, one or two sentences, always starts with `Examiner tip:`.
- **Concept chips.** Dashed rounded pills under a section title (`HEAT` `WORK` `INTERNAL ENERGY`) that show which ideas the section ties together.
- **Table.** Navy header row, white text, alternate rows light blue. Used for sign conventions and comparisons.
- **Worked problem card.**
  - Yellow top bar and a red letter-spaced label `WORKED PROBLEM 01 / 13`.
  - Big navy title: `Problem 1: The Helium Tank`.
  - A small source line with a book icon: `Tsokos (CUP, 3rd ed.) B.4 · topic · replaces SME: ...`.
  - A **Visual setup** panel (cartoon plus a QUESTION DATA & MODEL schematic).
  - The question with parts (a), (b), (c), (d).
  - A dashed divider, then a green `▾ Worked solution` that is collapsible on screen and open in print. Each part is solved in steps with units, and the last line states the physics lesson.
- **Interactive artifact.** Yellow card with a red label `INTERACTIVE ARTIFACT 01 · PARTICLE MODEL`, a punchy navy command title (`Turn up the temperature.`), a live drawing on the left, and on the right a slider, a big red number, and a **green dashed readout box** with 2 or 3 live values, then one sentence saying what to notice. Rule: one artifact per big idea, and it must reuse numbers from a worked problem.

## 5. Narration voice
- **Story first.** Open each topic with a person, a year and a scene (Rumford 1798, Joule's paddles, Clausius 1865). Then say what it means.
- **Plain words.** Short sentences. "In plain words: how disordered the system is."
- **Talk to the student.** "Keep that in your pocket, we'll use it again and again." "A beautifully simple rule." "Squeeze the gas and the molecules hit the walls more often."
- **Say the trap out loud.** Common errors become examiner tips or the "student says..." part of a question (e.g. doubling the Celsius number).
- **Link forward.** End a section with the question the next one answers ("Heat flows hot to cold, never the reverse. To describe this direction we need entropy.").
- **Summary line at the end.** "Energy is conserved (First Law); total entropy increases (Second Law); no engine can exceed Carnot."

## 6. Teaching sequence inside each section
Hook (story) → Illustration → Rule in words → Equation box and symbol list → Examiner tip → Graph or diagram reading → Worked problem → Interactive artifact → Bridge to the next section.

## 7. Problem-writing rules
- All questions are **new and slightly harder** than the source notes (IB Paper 2 / HL level), never copied.
- Every problem has a source line that says which book/section style it follows and what it replaces.
- Real objects and numbers (helium tank, boiling pot, power station at 840 K and 300 K). Always give units, always convert Celsius to kelvin explicitly.
- A problem usually ends with a **judgement** part ("advise the investor", "a student says...").
- Full worked solutions are always included.

## 8. Illustration rules
- Cartoon objects drawn as coloured pencil on lined paper: friendly faces, thumbs-up, yellow burst lines.
- Historical scenes are labelled illustrative reconstructions.
- The physics comes from the schematic panel, not the cartoon. Cartoon = memory hook, schematic = exact data.
- Image generation is done outside this repo. Until images exist, the template uses clean inline SVG placeholders.

## 9. Checklist before a module is "done"
- [ ] Cover with stat strip and About box
- [ ] Intro hook with a figure
- [ ] Every section has a number badge, a figure, an equation box with symbols, and an examiner tip
- [ ] Every problem has: source line, visual setup, question parts, worked solution
- [ ] At least one interactive artifact per 2 or 3 sections, each tied to a worked problem
- [ ] Every `.sec` has an `id` and a `data-bridge` sentence; contents bar and bridges tested
- [ ] Closing summary, Bonus Trivia, Question Sources Note
- [ ] Print preview checked (solutions expanded)
- [ ] Numbers in the artifacts match the worked solutions
