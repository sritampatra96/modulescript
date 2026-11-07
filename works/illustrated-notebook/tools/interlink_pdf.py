#!/usr/bin/env python3
"""Add interlinks to an Illustrated Notebook PDF without changing its original pages.

Adds: (1) a clickable CONTENTS panel on page 1, (2) a Back / Contents / Next strip on every page,
(3) PDF bookmarks. Needs: pypdf, reportlab.

Usage: interlink_pdf.py in.pdf out.pdf
Edit SECTIONS / PROBLEMS / ARTIFACTS below for a new module (page numbers are 1-based).
"""
import io, sys
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import RectangleObject, NameObject, ArrayObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

NAVY, RED, YELLOW, PINK, CREAM = "#1d3a7a", "#d64030", "#f2c230", "#ffd6e2", "#fff6d6"

# (number label, title, first page)
SECTIONS = [
    ("00", "Introduction: What is Heat?", 2), ("01", "Internal Energy", 3), ("02", "Work Done by a Gas", 7),
    ("03", "The First Law", 12), ("04", "Entropy", 18), ("05", "Calculating Entropy", 24),
    ("06", "The Second Law", 31), ("07", "Thermodynamic Processes", 35), ("08", "Heat Engines", 46),
    ("09", "The Carnot Cycle", 51), ("10", "Maxwell's Demon, Heat Death", 58),
]
PROBLEMS = [5, 9, 14, 15, 21, 25, 29, 33, 38, 41, 43, 49, 55]   # worked problems 1..13
ARTIFACTS = [3, 15, 27, 42, 56]                                   # interactive artifacts 1..5
MODULE = "THERMODYNAMICS"


def section_index(page):
    idx = 0
    for i, (_, _, p) in enumerate(SECTIONS):
        if page >= p:
            idx = i
    return idx


def build(src, dst):
    r = PdfReader(src)
    n = len(r.pages)
    W, H = float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height)
    links = []  # (page_index, rect(x0,y0,x1,y1), target_page_index)

    def overlay(pno):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(W, H))
        if pno == 1:
            draw_contents(c, links)
        draw_strip(c, pno, links)
        c.save()
        buf.seek(0)
        return PdfReader(buf).pages[0]

    def pill(c, x, y, w, h, fill, stroke, text, size=8, color=NAVY, bold=True):
        c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(1.2)
        c.roundRect(x, y, w, h, h / 2, fill=1, stroke=1)
        c.setFillColor(color); c.setFont("DVB" if bold else "DV", size)
        c.drawCentredString(x + w / 2, y + h / 2 - size * 0.35, text)

    def draw_strip(c, pno, links):
        si = section_index(pno)
        y, h = 28, 14
        c.setFillColor(CREAM); c.setStrokeColor("#9db8dd"); c.setLineWidth(0.8); c.setDash(3, 2)
        c.line(60, y + h + 1, W - 38, y + h + 1); c.setDash()
        # back
        if si > 0:
            lab = f"◀ Back: {SECTIONS[si-1][1]}"
            w = min(190, pdfmetrics.stringWidth(lab, "DVB", 7.5) + 16)
            pill(c, 62, y, w, h, "white", NAVY, lab, 7.5)
            links.append((pno - 1, (62, y, 62 + w, y + h), SECTIONS[si - 1][2] - 1))
        # contents
        pill(c, W / 2 - 38, y, 76, h, YELLOW, NAVY, "≡ Contents", 7.5)
        links.append((pno - 1, (W / 2 - 38, y, W / 2 + 38, y + h), 0))
        # next
        if si < len(SECTIONS) - 1:
            lab = f"Next: {SECTIONS[si+1][1]} ▶"
            w = min(190, pdfmetrics.stringWidth(lab, "DVB", 7.5) + 16)
            pill(c, W - 40 - w, y, w, h, "white", NAVY, lab, 7.5)
            links.append((pno - 1, (W - 40 - w, y, W - 40, y + h), SECTIONS[si + 1][2] - 1))

    def draw_contents(c, links):
        x0, x1 = 62, W - 38
        py, ph = 54, 196                      # panel bottom and height (blank lower half of the cover)
        c.setFillColor(CREAM); c.setStrokeColor(NAVY); c.setLineWidth(2)
        c.roundRect(x0, py, x1 - x0, ph, 12, fill=1, stroke=1)
        c.setFillColor(RED); c.setFont("DVB", 7.5)
        c.drawString(x0 + 14, py + ph - 16, "CONTENTS  \u00B7  CLICK ANY ITEM TO JUMP")
        colw = (x1 - x0 - 28) / 2
        for i, (num, title, pg) in enumerate(SECTIONS):
            col, row = divmod(i, 6)
            x = x0 + 14 + col * colw
            y = py + ph - 34 - row * 15.5
            c.setFillColor(PINK); c.setStrokeColor(RED); c.setLineWidth(1)
            c.circle(x + 7, y + 3.5, 7, fill=1, stroke=1)
            c.setFillColor(RED); c.setFont("DVB", 6); c.drawCentredString(x + 7, y + 1.5, num)
            c.setFillColor(NAVY); c.setFont("DVB", 8.5)
            c.drawString(x + 20, y, title)
            c.setFont("DV", 7); c.setFillColor("#667")
            c.drawRightString(x + colw - 16, y, f"p.{pg}")
            links.append((0, (x, y - 4, x + colw - 10, y + 11), pg - 1))
        ry = py + 36 + 8
        c.setFillColor(RED); c.setFont("DVB", 7); c.drawString(x0 + 14, ry + 17, "WORKED PROBLEMS")
        for i, pg in enumerate(PROBLEMS):
            x = x0 + 14 + i * 28
            pill(c, x, ry, 24, 13, "#fff1a8", "#c9a300", str(i + 1), 7.5)
            links.append((0, (x, ry, x + 24, ry + 13), pg - 1))
        ay = py + 8
        c.setFillColor(RED); c.setFont("DVB", 7); c.drawString(x0 + 14, ay + 17, "INTERACTIVE ARTIFACTS")
        for i, pg in enumerate(ARTIFACTS):
            x = x0 + 14 + i * 28
            pill(c, x, ay, 24, 13, "#e4f4e4", "#2e7d32", str(i + 1), 7.5)
            links.append((0, (x, ay, x + 24, ay + 13), pg - 1))
        c.setFillColor("#667"); c.setFont("DV", 6.5)
        c.drawString(x0 + 14 + 5 * 28 + 4, ay + 3, "(the live versions run in the HTML edition)")

    w = PdfWriter()
    for i, page in enumerate(r.pages):
        page.merge_page(overlay(i + 1))
        w.add_page(page)
    for pi, rect, tgt in links:
        ann = Link(rect=RectangleObject(rect), border=[0, 0, 0], target_page_index=0)
        ann[NameObject("/Dest")] = ArrayObject([w.pages[tgt].indirect_reference, NameObject("/Fit")])  # real page reference
        ref = w._add_object(ann)
        pg = w.pages[pi]
        if "/Annots" not in pg:
            pg[NameObject("/Annots")] = ArrayObject()
        pg["/Annots"].append(ref)
    # bookmarks
    root = w.add_outline_item(f"{MODULE}: Contents", 0)
    for i, (num, title, pg) in enumerate(SECTIONS):
        sec = w.add_outline_item(f"{num}  {title}", pg - 1)
        nxt = SECTIONS[i + 1][2] if i + 1 < len(SECTIONS) else n + 1
        for k, p in enumerate(PROBLEMS):
            if pg <= p < nxt:
                w.add_outline_item(f"Worked problem {k+1}", p - 1, parent=sec)
        for k, p in enumerate(ARTIFACTS):
            if pg <= p < nxt:
                w.add_outline_item(f"Interactive artifact {k+1}", p - 1, parent=sec)
    w.add_metadata({"/Title": f"{MODULE}: Illustrated Notebook (interlinked)"})
    w.page_mode = "/UseOutlines"
    with open(dst, "wb") as f:
        w.write(f)
    print("wrote", dst, "pages", n, "links", len(links))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
