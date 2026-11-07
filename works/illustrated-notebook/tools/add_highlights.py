#!/usr/bin/env python3
"""Draw yellow highlighter marks over key terms in a notebook PDF (first occurrence per section).

Usage: add_highlights.py in.pdf out.pdf
Pipeline: add_bridges.py -> add_highlights.py -> interlink_pdf.py
Section page ranges come from SECTIONS in interlink_pdf.py. Needs: pikepdf, reportlab, poppler (pdftotext).
"""
import io, re, subprocess, sys, html
import pikepdf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from interlink_pdf import SECTIONS

KEYWORDS = [
    "internal energy", "ideal gas", "kinetic energy", "potential energy", "work done", "p–V diagram",
    "area under", "state function", "First Law", "Second Law", "conservation of energy",
    "entropy", "disorder", "microstates", "microstate", "isolated system", "non-isolated",
    "reversible", "irreversible", "spontaneously", "Clausius", "Kelvin form", "heat pump",
    "isobaric", "isovolumetric", "isothermal", "adiabatic", "closed cycle", "heat engine",
    "hot reservoir", "cold reservoir", "efficiency", "Carnot cycle", "Carnot efficiency",
    "maximum theoretical efficiency", "Boltzmann", "kelvin", "latent heat", "probability",
    "heat death",
]
KW = sorted(([k.lower().split() for k in KEYWORDS]), key=len, reverse=True)
MARK = Color(1, 0.86, 0.2, alpha=0.6)


def norm(w):
    return re.sub(r"^[^\w–-]+|[^\w–-]+$", "", w.lower())


def section_of(page):
    idx = 0
    for i, (_, _, p) in enumerate(SECTIONS):
        if page >= p:
            idx = i
    return idx


def main(src, dst):
    bbox = subprocess.run(["pdftotext", "-bbox", src, "-"], capture_output=True, text=True).stdout
    pages = re.split(r"<page ", bbox)[1:]
    pdf = pikepdf.open(src)
    W = float(pdf.pages[0].mediabox[2]); H = float(pdf.pages[0].mediabox[3])
    used = {}
    count = 0
    keep = []
    for pno, ptxt in enumerate(pages, 1):
        if pno == 1:
            continue
        words = [(float(a), float(b), float(c), float(d), html.unescape(t)) for a, b, c, d, t in
                 re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', ptxt)]
        sec = section_of(pno); u = used.setdefault(sec, set())
        rects = []
        i = 0
        while i < len(words):
            hit = None
            for k in KW:
                n = len(k)
                if i + n <= len(words) and [norm(w[4]) for w in words[i:i + n]] == k:
                    hit = k; break
            if hit:
                key = " ".join(hit); n = len(hit)
                seg = words[i:i + n]
                same_line = all(abs(w[1] - seg[0][1]) < 3 for w in seg)
                body_size = all(7 <= (w[3] - w[1]) <= 15 for w in seg) and not any(w[4].isupper() and len(w[4]) > 2 for w in seg)
                if key not in u and same_line and body_size and words[i][3] < H - 40:
                    u.add(key)
                    rects.append((seg[0][0] - 1.5, min(w[1] for w in seg), seg[-1][2] + 1.5, max(w[3] for w in seg)))
                i += n
            else:
                i += 1
        if not rects:
            continue
        buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H)); c.setFillColor(MARK)
        for x0, y0, x1, y1 in rects:
            h = y1 - y0
            c.roundRect(x0, H - y1 + h * 0.08, x1 - x0, h * 0.8, 2, stroke=0, fill=1)
            c.setStrokeColor(Color(0.84, 0.25, 0.19, alpha=0.9)); c.setLineWidth(1.1)
            c.line(x0 + 1, H - y1 + h * 0.06, x1 - 1, H - y1 + h * 0.06)
        c.save(); buf.seek(0)
        ov = pikepdf.open(buf); keep.append(ov)
        pdf.pages[pno - 1].add_overlay(ov.pages[0])
        count += len(rects)
    pdf.save(dst)
    print("highlighted", count)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
