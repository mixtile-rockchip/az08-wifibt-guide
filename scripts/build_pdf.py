#!/usr/bin/env python3
"""Build one PDF per language from mkdocs.yml.

mkdocs-static-i18n builds every language in one run, and print-site then emits
a single /print_page/ for all of them, so each language gets its own build here:
that language as the only (default) one, print-site added, screen-only theme
features dropped. The print page is served locally and printed with headless
Chromium to <out>/<name>-<LANG>.pdf, followed by the BT RF Test Commands manual
as an appendix. A JSON manifest describing what the PDF contains is written
next to each build for scripts/check_pdf.py.
"""
import argparse, functools, http.server, json, os, subprocess, sys, threading
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter
from pypdf.generic import NameObject, TextStringObject

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
# toc.integrate removes the secondary sidebar that print-site copies its TOC from.
SCREEN_ONLY_FEATURES = {"toc.integrate", "content.code.copy"}
TOC_TITLES = {"en": "Contents", "zh": "目录"}
# Vendor manual appended after the guide; links to it jump to the appendix instead.
APPENDIX_PDF = ROOT / "docs" / "assets" / "BT-RF-Test-Commands-for-Linux-v0.9.pdf"
APPENDIX = {
    "en": ("Appendix · BT RF Test Commands for Linux (v0.9)",
           "Ampak / Cypress Bluetooth RF test command reference (v0.9). The full manual follows."),
    "zh": ("附录 · BT RF Test Commands for Linux (v0.9)",
           "Ampak / Cypress 蓝牙射频测试命令参考手册（v0.9）。完整手册见后续页面。"),
}
# A4 width minus the left/right @page margins in pdf.css (14 mm each), in CSS px.
PRINT_WIDTH_PX = round((210 - 2 * 14) / 25.4 * 96)

COLLECT_JS = """() => {
  document.querySelectorAll('a.headerlink').forEach(e => e.remove());
  const root = document.querySelector('#print-site-page') || document.body;
  const vis = e => e.offsetParent !== null;
  const text = e => e.textContent.replace(/\\s+/g, ' ').trim();
  return {
    headings: [...root.querySelectorAll('h1, h2')].filter(vis).map(text),
    toc: [...root.querySelectorAll('#print-page-toc a')].map(text).filter(Boolean),
    admonitions: [...root.querySelectorAll('.admonition-title')].filter(vis).map(text),
    // bold one-line labels ("**2.4G 11b**") that introduce the block below them
    labels: [...root.querySelectorAll('p')].filter(p => vis(p) && p.children.length === 1 && p.firstElementChild.localName === 'strong' && text(p) === text(p.firstElementChild)).map(text),
    images: [...root.querySelectorAll('img')].filter(vis).map(i => ({
      src: i.getAttribute('src'),
      width: i.getBoundingClientRect().width,
      box: i.parentElement.getBoundingClientRect().width,
      loaded: i.complete && i.naturalWidth > 0,
    })),
    code: [...root.querySelectorAll('pre')].filter(vis).map(p => ({
      lines: p.textContent.split('\\n').map(l => l.trimEnd()).filter(Boolean),
      clipped: p.scrollWidth > p.clientWidth + 1,
    })),
    internal_links: [...root.querySelectorAll('a[href^="#"]')].filter(vis).length,
    // lead-ins whose block is an image: the lead-in is then the last text on its page
    image_leadins: [...root.querySelectorAll('.pdf-keep')].filter(k => k.lastElementChild.querySelector('img')).map(k => text(k.firstElementChild)),
    // print-site rewrites ids with a plain text replace; a heading id such as "2" turns <h2> into <hxxx-2>
    unknown_tags: [...new Set([...root.querySelectorAll('*')].map(e => e.localName).filter(n => n.includes('-')))],
  };
}"""

# Pair each bold label ("**2.4G 11b**") or "…:" lead-in with the block it introduces, so a
# page break cannot fall between them. CSS break-after: avoid is not honoured before images.
KEEP_JS = """() => {
  for (const p of document.querySelectorAll('#print-site-page p')) {
    const next = p.nextElementSibling;
    const t = p.textContent.trim();
    const label = p.children.length === 1 && p.firstElementChild.localName === 'strong'
      && t === p.firstElementChild.textContent.trim();
    if (!next || !(label || /[:：]$/.test(t))) continue;
    const keep = document.createElement('div');
    keep.className = 'pdf-keep';
    p.before(keep);
    keep.append(p, next);
  }
}"""

# Divider page for the appendix, listed in the TOC; links to the manual point at it.
APPENDIX_JS = """([title, text, file]) => {
  const section = document.createElement('section');
  section.className = 'print-page pdf-appendix';
  section.id = 'appendix';
  const h1 = document.createElement('h1');
  h1.id = 'appendix-title';
  h1.textContent = title;
  const p = document.createElement('p');
  p.textContent = text;
  section.append(h1, p);
  [...document.querySelectorAll('section.print-page')].pop().after(section);
  const toc = document.querySelector('#print-page-toc ul');
  if (toc) {
    const li = document.createElement('li');
    li.className = 'md-nav__item';
    const a = document.createElement('a');
    a.className = 'md-nav__link';
    a.href = '#appendix';
    a.textContent = title;
    li.append(a);
    toc.append(li);
  }
  for (const a of document.querySelectorAll('a[href]'))
    if (new URL(a.href, location.href).pathname.endsWith('/' + file)) a.setAttribute('href', '#appendix');
}"""

# Rendered links that leave the print page (other pages, assets), as local paths.
# Hidden ones (the .pdf-download line) never reach the PDF.
LOCAL_LINKS_JS = """() => [...new Set([...document.querySelectorAll('a[href]')]
  .filter(a => a.offsetParent !== null)
  .map(a => new URL(a.href, location.href))
  .filter(u => u.origin === location.origin && u.pathname !== location.pathname)
  .map(u => u.pathname))]"""

REWRITE_JS = """mapping => {
  for (const a of document.querySelectorAll('a[href]')) {
    const u = new URL(a.href, location.href);
    if (u.origin === location.origin && u.pathname in mapping)
      a.href = mapping[u.pathname] + u.search + u.hash;
  }
}"""


class _ConfigLoader(yaml.SafeLoader):
    """Reads mkdocs.yml without resolving !!python tags (MkDocs resolves them via INHERIT)."""


_ConfigLoader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def load_base(base):
    return yaml.load(base.read_text(), Loader=_ConfigLoader)


def lang_config(base, lang):
    """Config overlay for one language; everything else is inherited from mkdocs.yml."""
    cfg = load_base(base)
    i18n = next(p["i18n"] for p in cfg["plugins"] if isinstance(p, dict) and "i18n" in p)
    chosen = next(l for l in i18n["languages"] if l["locale"] == lang)
    theme = {"features": [f for f in cfg["theme"].get("features", []) if f not in SCREEN_ONLY_FEATURES]}
    if not chosen.get("default"):
        theme["language"] = lang
    overlay = {
        "INHERIT": str(base),
        "docs_dir": str(base.parent / cfg.get("docs_dir", "docs")),
        "theme": theme,
        "extra_css": cfg.get("extra_css", []) + ["stylesheets/pdf.css"],
        "plugins": [
            {"i18n": {**i18n, "languages": [{**chosen, "default": True, "build": True}]}},
            {"print-site": {
                "add_to_navigation": False,
                "add_cover_page": True,
                "add_table_of_contents": True,
                "toc_title": TOC_TITLES.get(lang, "Contents"),
                "enumerate_headings": False,
                "add_full_urls": False,
                "print_page_title": "",
            }},
        ],
    }
    if chosen.get("site_name"):
        overlay["site_name"] = chosen["site_name"]
    return overlay


def public_urls(base, lang, paths, site_dir):
    """Map local print-build paths to public URLs, checked against the built website.

    Pages live under the language root (…/zh/…); shared files such as
    docs/assets/*.pdf exist only once, at the site root.
    """
    cfg = load_base(base)
    i18n = next(p["i18n"] for p in cfg["plugins"] if isinstance(p, dict) and "i18n" in p)
    default = next(l["locale"] for l in i18n["languages"] if l.get("default"))
    site_url = cfg["site_url"].rstrip("/") + "/"
    prefix = "" if lang == default else f"{lang}/"
    mapping = {}
    for path in paths:
        rel = path.lstrip("/")
        for candidate in (prefix + rel, rel):
            target = site_dir / candidate
            if target.is_file() or (target / "index.html").is_file():
                mapping[path] = site_url + candidate
                break
        else:
            raise SystemExit(f"{lang}: link {path} has no counterpart in {site_dir}; run `mkdocs build` first")
    return mapping


def finish_pdf(pdf, appendix):
    """Fix bookmark titles, then append the appendix PDF. Returns the guide's page count."""
    writer = PdfWriter(clone_from=str(pdf))
    guide_pages = len(writer.pages)
    # Chromium repeats the text of h1 bookmarks ("TitleTitle"); keep one copy.
    outlines = writer.root_object.get("/Outlines")
    stack = [outlines.get_object().get("/First")] if outlines else []
    while stack:
        ref = stack.pop()
        if ref is None:
            continue
        node = ref.get_object()
        title = str(node.get("/Title", ""))
        half = len(title) // 2
        if len(title) % 2 == 0 and half and title[:half] == title[half:]:
            node[NameObject("/Title")] = TextStringObject(title[:half])
        stack += [node.get("/First"), node.get("/Next")]
    writer.append(str(appendix), import_outline=False)
    writer.write(str(pdf))
    return guide_pages


def render(site_dir, out_pdf, public, appendix, chromium=None):
    handler = functools.partial(QuietHandler, directory=str(site_dir))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{httpd.server_port}/print_page/"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=chromium)
            page = browser.new_page(viewport={"width": PRINT_WIDTH_PX, "height": 1000})
            page.goto(url, wait_until="networkidle")
            page.emulate_media(media="print")
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.evaluate(KEEP_JS)
            page.evaluate(APPENDIX_JS, [*appendix, APPENDIX_PDF.name])
            manifest = page.evaluate(COLLECT_JS)
            page.evaluate(REWRITE_JS, public(page.evaluate(LOCAL_LINKS_JS)))
            page.pdf(path=str(out_pdf), format="A4", print_background=True,
                     prefer_css_page_size=True, outline=True, tagged=True)
            manifest["chromium"] = browser.version
            browser.close()
    finally:
        httpd.shutdown()
    return manifest


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="Focalcrest-RF-Test-Guide")
    ap.add_argument("--langs", default="en,zh")
    ap.add_argument("--out", default="site/pdf")
    a = ap.parse_args()
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(exist_ok=True)
    base_cfg = ROOT / "mkdocs.yml"
    for lang in a.langs.split(","):
        cfg_path = BUILD / f"mkdocs.pdf-{lang}.yml"
        site_dir = BUILD / f"pdf-{lang}"
        cfg_path.write_text(yaml.safe_dump(lang_config(base_cfg, lang), allow_unicode=True, sort_keys=False))
        subprocess.run(["mkdocs", "build", "--strict", "-q", "-f", str(cfg_path), "-d", str(site_dir)], check=True)
        pdf = out / f"{a.name}-{lang.upper()}.pdf"
        public = functools.partial(public_urls, base_cfg, lang, site_dir=ROOT / "site")
        manifest = render(site_dir, pdf, public, APPENDIX[lang], os.environ.get("CHROMIUM_EXE") or None)
        guide_pages = finish_pdf(pdf, APPENDIX_PDF)
        manifest.update(lang=lang, pdf=str(pdf), toc_title=TOC_TITLES.get(lang, "Contents"),
                        guide_pages=guide_pages, appendix_pdf=str(APPENDIX_PDF), appendix_title=APPENDIX[lang][0],
                        site_url=load_base(base_cfg)["site_url"].rstrip("/") + "/")
        (BUILD / f"pdf-{lang}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
        print(f"{pdf.relative_to(ROOT)}  {pdf.stat().st_size // 1024} KiB")


if __name__ == "__main__":
    sys.exit(main())
