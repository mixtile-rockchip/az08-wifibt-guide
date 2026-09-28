#!/usr/bin/env python3
"""Quality gate for the PDFs written by scripts/build_pdf.py.

Checks each build/pdf-<lang>.json manifest against its PDF and exits non-zero
on any failure. Needs poppler-utils (pdffonts, pdftotext, pdfimages) and pypdf.
"""
import json, os, re, subprocess, sys
from pathlib import Path

from pypdf import PdfReader
from pypdf.generic import Destination

ROOT = Path(__file__).resolve().parent.parent
CJK = re.compile(r"[一-鿿]")
# Chinese punctuation that must never start a line.
NO_LINE_START = "，。、；：？！）」』》"
# Code lines up to this length fit the A4 code width without wrapping.
FITS_ON_ONE_LINE = 80
# Height of the tallest heading line (h1) in pt.
HEADING_HEIGHT_PT = 30
BOTTOM_MARGIN_PT = 18 / 25.4 * 72
FOOTER = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def page_words(pdf):
    """Per page: (top y from the top edge, text) of every word."""
    xml = run("pdftotext", "-bbox", pdf, "-")
    return [[(float(m.group(1)), m.group(2)) for m in re.finditer(r'<word xMin="[^"]+" yMin="([^"]+)"[^>]*>([^<]*)</word>', page)]
            for page in xml.split("<page ")[1:]]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def check(manifest):
    pdf, lang = manifest["pdf"], manifest["lang"]
    fails = []
    fail = fails.append
    reader = PdfReader(pdf)
    pages = [run("pdftotext", "-layout", "-f", str(i), "-l", str(i), pdf, "-") for i in range(1, len(reader.pages) + 1)]
    text = "\n".join(pages)
    lines = [norm(l) for l in text.splitlines()]
    flat = re.sub(r"\s+", "", text)

    # fonts: every font embedded and a Noto family; the Chinese PDF must carry Noto Sans CJK
    fonts, unembedded = set(), set()
    for row in run("pdffonts", pdf).splitlines()[2:]:
        cols = row.split()
        fonts.add(cols[0].split("+", 1)[-1])
        if cols[-5] != "yes":
            unembedded.add(cols[0].split("+", 1)[-1])
    for name in sorted(unembedded):
        fail(f"font not embedded: {name}")
    for name in sorted(f for f in fonts if not f.startswith("Noto")):
        fail(f"fallback font used: {name}")
    if lang == "zh" and not any("CJK" in f for f in fonts):
        fail("no Noto Sans CJK font in the Chinese PDF")

    # language of the content
    cjk = len(CJK.findall(text))
    if lang == "zh" and cjk < 500:
        fail(f"Chinese PDF has only {cjk} CJK characters")
    if lang == "en" and cjk > 0.02 * len(flat):
        fail(f"English PDF has {cjk} CJK characters")

    # markup the print page mangled
    for tag in manifest["unknown_tags"]:
        fail(f"unknown element <{tag}> in the print page")

    # table of contents
    toc_page = next((p for p in pages[:4] if manifest["toc_title"] in p), None)
    if toc_page is None:
        fail(f"TOC title {manifest['toc_title']!r} not found in the first pages")
    elif not manifest["toc"]:
        fail("TOC is empty")
    else:
        for entry in manifest["toc"]:
            if re.sub(r"\s+", "", entry) not in re.sub(r"\s+", "", toc_page):
                fail(f"TOC entry missing: {entry}")

    # bookmarks
    outline = []
    stack = list(reader.outline)
    while stack:
        item = stack.pop(0)
        if isinstance(item, list):
            stack[:0] = item
        else:
            outline.append(item)
    titles = [norm(o.title) for o in outline]
    for h in manifest["headings"]:
        if norm(h) not in titles:
            fail(f"bookmark missing for heading: {h}")
    for t in titles:
        half = len(t) // 2
        if half and len(t) % 2 == 0 and t[:half] == t[half:]:
            fail(f"bookmark title doubled: {t}")

    # links: internal ones jump to a real page, none point at the local build server
    internal = 0
    for page in reader.pages:
        for annot in page.get("/Annots") or []:
            a = annot.get_object()
            if a.get("/Subtype") != "/Link":
                continue
            action = a.get("/A")
            uri = action.get_object().get("/URI") if action else None
            if uri is not None:
                if re.search(r"127\.0\.0\.1|localhost|file:", str(uri)):
                    fail(f"link to the local build: {uri}")
                elif str(uri).startswith(manifest["site_url"]):
                    rel = str(uri)[len(manifest["site_url"]):].split("#")[0]
                    target = ROOT / "site" / rel
                    if not (target.is_file() or (target / "index.html").is_file()):
                        fail(f"link into the website has no target in site/: {uri}")
                continue
            dest = a.get("/Dest") or (action.get_object().get("/D") if action else None)
            if dest is None:
                continue
            internal += 1
            try:
                target = reader.named_destinations.get(str(dest)) if not isinstance(dest, list) else dest
                if target is None:
                    fail(f"internal link to unknown destination {dest}")
            except Exception as e:  # noqa: BLE001
                fail(f"cannot resolve internal link {dest}: {e}")
    if internal < manifest["internal_links"]:
        fail(f"{internal} internal links in PDF, {manifest['internal_links']} in HTML")

    # images: all loaded, none wider than the text column, all present in the PDF
    for img in manifest["images"]:
        if not img["loaded"]:
            fail(f"image not loaded: {img['src']}")
        if img["width"] > img["box"] + 1:
            fail(f"image wider than the page: {img['src']}")
    embedded = len(run("pdfimages", "-list", pdf).splitlines()[2:])
    if embedded < len(manifest["images"]):
        fail(f"{embedded} images in PDF, {len(manifest['images'])} in HTML")

    # code blocks: nothing clipped, short lines never wrapped, long lines complete
    if not manifest["code"]:
        fail("no code blocks found")
    for block in manifest["code"]:
        if block["clipped"]:
            fail(f"code block clipped: {block['lines'][0][:60]}")
        for line in block["lines"]:
            if len(line) <= FITS_ON_ONE_LINE:
                if not any(norm(line) in l for l in lines):
                    fail(f"code line wrapped or missing: {line}")
            elif re.sub(r"\s+", "", line) not in flat:
                fail(f"long code line incomplete: {line[:60]}…")

    # admonitions
    for title in manifest["admonitions"]:
        if norm(title) not in text:
            fail(f"admonition title missing: {title}")

    # blank pages (the footer page number does not count as content)
    page_images = [len(run("pdfimages", "-list", "-f", str(i), "-l", str(i), pdf).splitlines()[2:])
                   for i in range(1, len(pages) + 1)]
    for i, p in enumerate(pages, 1):
        body = [l for l in p.splitlines() if l.strip() and not FOOTER.match(l)]
        if not body and not page_images[i - 1]:
            fail(f"page {i} is blank")

    # headings stranded at the bottom of a page: nothing but the footer below them
    words = page_words(pdf)
    for o in outline:
        if not (isinstance(o, Destination) and o.get("/Top") is not None and o.title):
            continue
        n = reader.get_destination_page_number(o)
        height = float(reader.pages[n].mediabox.height)
        heading_bottom = height - float(o["/Top"]) + HEADING_HEIGHT_PT
        below = [w for w in words[n] if w[0] > heading_bottom and not FOOTER.match(w[1])]
        if not below and heading_bottom < height - BOTTOM_MARGIN_PT:
            fail(f"heading alone at the bottom of page {n + 1}: {o.title}")

    # bold labels and "…:" lead-ins left as the last line of a page
    labels = {norm(l) for l in manifest["labels"]}
    image_leadins = {norm(l) for l in manifest["image_leadins"]}
    for i, p in enumerate(pages, 1):
        body = [norm(l) for l in p.splitlines() if l.strip() and not FOOTER.match(l)]
        if not body or i == len(pages):
            continue
        if body[-1] in image_leadins and page_images[i - 1]:
            continue  # the image it introduces is below it on the same page
        if body[-1] in labels:
            fail(f"label alone at the bottom of page {i}: {body[-1]}")
        elif body[-1].endswith((":", "：")):
            fail(f"lead-in separated from what it introduces, page {i}: {body[-1]}")

    # Chinese line breaking
    if lang == "zh":
        for l in lines:
            if l and l[0] in NO_LINE_START:
                fail(f"line starts with closing punctuation: {l[:40]}")

    summary = (f"{Path(pdf).name}: {len(reader.pages)} pages, fonts {sorted(fonts)}, "
               f"{len(outline)} bookmarks, {internal} internal links, {len(manifest['images'])} images, "
               f"{sum(len(b['lines']) for b in manifest['code'])} code lines, {len(manifest['admonitions'])} admonitions")
    return summary, fails


def main():
    manifests = sorted((ROOT / "build").glob("pdf-*.json"))
    if not manifests:
        print("no build/pdf-*.json manifests; run scripts/build_pdf.py first", file=sys.stderr)
        return 1
    bad = 0
    for m in manifests:
        summary, fails = check(json.loads(m.read_text()))
        print(("FAIL " if fails else "PASS ") + summary)
        for f in fails:
            print(f"::error::{f}" if "GITHUB_ACTIONS" in os.environ else f"  - {f}")
        bad += bool(fails)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
