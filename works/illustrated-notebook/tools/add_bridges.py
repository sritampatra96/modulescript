#!/usr/bin/env python3
"""Insert 'Next' bridge cards between sections of an Illustrated Notebook PDF.

Where a new section starts at the top of a page, a full bridge page is inserted before it.
Where it starts mid-page, that page is split at the section header: the top part keeps the
end of the previous section and the bridge card fills the space below; the new section moves
to the top of the next page. Footers are renumbered.

Usage: add_bridges.py ref.pdf out.pdf   (prints the old->new page map as JSON on stdout)
Then: interlink_pdf.py out.pdf Thermodynamics_Illustrated_Notebook_interlinked.pdf
ref.pdf is the plain notebook (no interlinks): reference/Thermodynamics_Illustrated_Notebook.pdf,
in commit 103ca72 (`git show 103ca72:works/illustrated-notebook/reference/Thermodynamics_Illustrated_Notebook.pdf`).
Needs: pikepdf, reportlab, and the Comic Neue TTFs next to this script.
"""
import io, json, sys, textwrap
import pikepdf
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

HERE = __file__.rsplit("/", 1)[0]
pdfmetrics.registerFont(TTFont("CN", f"{HERE}/ComicNeue-400.ttf"))
pdfmetrics.registerFont(TTFont("CNB", f"{HERE}/ComicNeue-700.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

W, H = 594.96, 841.92
PAPER, LINE, MARGIN = HexColor("#fff9ed"), HexColor("#efe7d4"), HexColor("#f4b3b2")
NAVY, RED, YEL, YELB, TEAL = HexColor("#22305a"), HexColor("#d64030"), HexColor("#fff1a8"), HexColor("#c9a300"), HexColor("#2f7f7a")
PX0, PX1, PY0, PY1 = 42, 552, 46, 798          # paper box (pdf coords)

# (page, header top in top-down pts or None if section starts at top, to-number, to-title, hook)
BRIDGES = [
 (6, 313, "02", "Work Done by a Gas", "Heating is one way to raise U. But squeeze a bicycle pump with the nozzle blocked and the nozzle gets hot, with no flame at all. So pushing on a gas also changes its internal energy. How exactly does a gas give or receive energy by pushing?"),
 (10, None, "03", "The First Law", "We now have two ways to change a gas's internal energy: heating it (Q) and doing work (W). And Problem 2 showed that W depends on the path. So how do Q, W and the change in internal energy fit together?"),
 (15, None, "04", "Entropy", "The First Law says energy is conserved, but not which direction a process goes. Heat flows from hot to cold, never the reverse by itself. To describe this direction we need a new quantity: entropy."),
 (20, None, "05", "Calculating Entropy", "So far entropy is only 'more or less disorder'. Physics needs numbers: when heat flows into something, by exactly how much does its entropy change?"),
 (26, None, "06", "The Second Law", "Look back at Problems 5, 6 and 7: every time, the total entropy went up. Clausius and Kelvin turned this pattern into one of the strongest laws in physics."),
 (29, 155, "07", "Thermodynamic Processes", "The Second Law tells us what is impossible. To build what IS possible, like engines and fridges, we need to know exactly how a gas behaves in each kind of change. There are four standard ones."),
 (39, None, "08", "Heat Engines", "Problem 11 was a full cycle: heat in, work out, heat thrown away, back to the start. That is exactly what every engine does, from Watt's steam engine to a car."),
 (43, 172, "09", "The Carnot Cycle", "Our cycle in Problem 11 reached 20%. A car engine reaches about 30%. So what is the best any engine could ever do? A French engineer answered that in 1824."),
 (49, None, "10", "Maxwell's Demon & Heat Death", "Carnot's limit rests on one rule: total entropy never decreases. Two famous ideas push that rule to the extreme, one at the scale of molecules and one at the scale of the universe."),
]


def paper(c, y0=PY0, y1=PY1):
    c.setFillColor(PAPER); c.rect(PX0, y0, PX1 - PX0, y1 - y0, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.setLineWidth(0.5)
    y = y1 - 24
    while y > y0 + 4:
        c.line(PX0, y, PX1, y); y -= 24
    c.setStrokeColor(MARGIN); c.setLineWidth(1.4); c.line(PX0 + 1.5, y0, PX0 + 1.5, y1)


def card(c, top, bottom, num, title, hook):
    """Bridge card between y=top and y=bottom (pdf coords)."""
    x0, x1 = 64, 532
    lines = textwrap.wrap(hook, 52)
    h = min(top - bottom, 140 + len(lines) * 22)
    y1 = top - min((top - bottom - h) / 2, 160); y0 = y1 - h
    c.setFillColor(YEL); c.setStrokeColor(YELB); c.setLineWidth(2)
    c.roundRect(x0, y0, x1 - x0, h, 14, stroke=1, fill=1)
    c.setFillColor(YELB); c.setFont("CNB", 10)
    c.drawString(x0 + 20, y1 - 26, "B R I D G E   T O   S E C T I O N   " + num)
    # badge
    c.setFillColor(HexColor("#ffd6e2")); c.setStrokeColor(RED); c.setLineWidth(1.6)
    c.circle(x0 + 38, y1 - 62, 17, stroke=1, fill=1)
    c.setFillColor(RED); c.setFont("CNB", 12); c.drawCentredString(x0 + 38, y1 - 66, num)
    c.setFillColor(NAVY); c.setFont("CNB", 22); c.drawString(x0 + 66, y1 - 70, title.upper())
    c.setStrokeColor(YELB); c.setDash(4, 4); c.setLineWidth(1); c.line(x0 + 20, y1 - 92, x1 - 20, y1 - 92); c.setDash()
    c.setFillColor(TEAL); c.setFont("DVB", 13); c.drawString(x0 + 20, y1 - 118, "NEXT ▶")
    c.setFillColor(HexColor("#3a2f00")); c.setFont("CN", 15)
    y = y1 - 118
    for ln in textwrap.wrap(hook, 52):
        c.drawString(x0 + 92, y, ln); y -= 22
    return y


def overlay_pdf(draw):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H)); draw(c); c.save(); buf.seek(0)
    return pikepdf.open(buf)


def footer(c, n, total):
    c.setFillColorRGB(1, 1, 1); c.rect(150, 8, 300, 26, stroke=0, fill=1)
    c.setFillColor(HexColor("#6b8a96")); c.setFont("Helvetica", 6.5)
    c.drawCentredString(W / 2, 19, f"THERMODYNAMICS · IBDP HL  |  {n} / {total}")


def main(src, dst):
    ref = pikepdf.open(src)
    out = pikepdf.new()
    bridges = {b[0]: b for b in BRIDGES}
    plan = []                      # list of (kind, data)
    pmap = {}
    for i in range(len(ref.pages)):
        p = i + 1
        b = bridges.get(p)
        if b and b[1] is None:
            plan.append(("bridge", b)); plan.append(("orig", p))
        elif b:
            plan.append(("splitA", (p, b))); plan.append(("splitB", (p, b)))
        else:
            plan.append(("orig", p))
    total = len(plan)
    for k, (kind, d) in enumerate(plan, 1):
        if kind == "orig":
            pmap[d] = k
        elif kind == "splitB":
            pmap.setdefault(d[0], k)  # section header page
    # section pages = page carrying header
    for k, (kind, d) in enumerate(plan, 1):
        if kind == "splitA":
            pmap[f"{d[0]}A"] = k

    for k, (kind, d) in enumerate(plan, 1):
        if kind == "orig":
            out.pages.append(ref.pages[d - 1])
            ov = overlay_pdf(lambda c: footer(c, k, total))
            pg = out.pages[-1]; pg.add_overlay(ov.pages[0])
        elif kind == "bridge":
            _, _, num, title, hook = d
            def draw(c):
                paper(c); card(c, PY1 - 40, PY0 + 60, num, title, hook); footer(c, k, total)
            ov = overlay_pdf(draw); out.pages.append(ov.pages[0])
        else:
            p, (_, ytop, num, title, hook) = d
            cut = H - (ytop - 30)            # pdf y of the cut line
            src_page = ref.pages[p - 1]
            blank = overlay_pdf(lambda c: (c.setFillColorRGB(1, 1, 1), c.rect(0, 0, 1, 1, stroke=0, fill=1))); out.pages.append(blank.pages[0]); pg = out.pages[-1]
            if kind == "splitA":
                bg = overlay_pdf(lambda c: (paper(c, PY0, cut), card(c, cut - 14, PY0 + 50, num, title, hook), footer(c, k, total)))
                pg.add_overlay(bg.pages[0])
                pg.add_overlay(src_page, pikepdf.Rectangle(0, 0, W, H))
                # clip: hide everything of the original below the cut by re-drawing bridge area on top
                top_layer = overlay_pdf(lambda c: (c.setFillColorRGB(1, 1, 1), c.rect(0, 0, W, cut, stroke=0, fill=1),
                                                   paper(c, PY0, cut), card(c, cut - 14, PY0 + 50, num, title, hook), footer(c, k, total)))
                pg.add_overlay(top_layer.pages[0])
            else:
                dy = (H - 56) - cut
                bgp = overlay_pdf(lambda c: (c.setFillColorRGB(1, 1, 1), c.rect(0, 0, W, H, stroke=0, fill=1), paper(c)))
                pg.add_underlay(bgp.pages[0])
                pg.add_overlay(src_page, pikepdf.Rectangle(0, dy, W, H + dy))
                # cover what slid above the paper top and the old footer region
                cover = overlay_pdf(lambda c: (c.setFillColorRGB(1, 1, 1), c.rect(0, PY1, W, H - PY1, stroke=0, fill=1), paper(c, H - 58, PY1),
                                               paper(c, PY0, PY0 + dy + 4) if dy > 0 else None,
                                               footer(c, k, total)))
                pg.add_overlay(cover.pages[0])
    out.save(dst)
    sections = {b[2]: pmap[b[0]] for b in BRIDGES}
    print(json.dumps({"total": total, "map": {str(a): b for a, b in pmap.items()}, "sections": sections}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
