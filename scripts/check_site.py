#!/usr/bin/env python3
"""Check the published site: local links resolve, required pages exist, and no secrets leak.

Usage: python3 scripts/check_site.py [--live]
  --live  also request every https://maquert.github.io/ URL in the README and site pages.
"""
import re, sys, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://maquert.github.io/mhjaso_public/"
REQUIRED = ["index.html", "turnera/index.html", "turnera/support/index.html", "turnera/privacy/index.html", "assets/styles.css"]
ALLOWED_EMAILS = {"miguel.hernandezjaso@gmail.com"}
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY|Bearer\s+[A-Za-z0-9._-]{20,})")

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links = []; self.title = ""; self._t = False; self.h1 = 0; self.lang = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if tag == "h1": self.h1 += 1
        if tag == "title": self._t = True
        for k in ("href", "src"):
            if k in a: self.links.append(a[k])
    def handle_endtag(self, tag):
        if tag == "title": self._t = False
    def handle_data(self, d):
        if self._t: self.title += d

def target(page, link):
    path = (page.parent / link.split("#")[0].split("?")[0]).resolve()
    return path / "index.html" if path.is_dir() else path

errors = []
for r in REQUIRED:
    if not (ROOT / r).exists(): errors.append(f"missing required file {r}")

live = set()
pages = [p for p in ROOT.rglob("*.html") if "design" not in p.relative_to(ROOT).parts and ".git" not in p.parts]
for page in pages:
    rel = page.relative_to(ROOT)
    text = page.read_text()
    p = Links(); p.feed(text)
    if p.lang != "en": errors.append(f"{rel}: missing lang=en")
    if p.h1 != 1: errors.append(f"{rel}: expected one h1, found {p.h1}")
    if not p.title.strip(): errors.append(f"{rel}: empty title")
    for l in p.links:
        if l.startswith(("mailto:", "#")): continue
        if l.startswith("http"):
            live.add(l); continue
        if not target(page, l).exists(): errors.append(f"{rel}: broken link {l}")
    for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
        if e not in ALLOWED_EMAILS: errors.append(f"{rel}: unexpected email {e}")

for f in [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".html", ".md", ".css"} and ".git" not in p.parts]:
    if SECRET.search(f.read_text(errors="ignore")): errors.append(f"{f.relative_to(ROOT)}: possible secret")

readme = (ROOT / "README.md").read_text()
live |= set(re.findall(r"\]\((https://[^)\s]+)\)", readme))
for l in re.findall(r'src="([^"]+)"', readme):
    if not (ROOT / l).exists(): errors.append(f"README.md: missing image {l}")
for l in re.findall(r"\]\((?!https?:)([^)\s#]+)\)", readme):
    if not (ROOT / l).exists(): errors.append(f"README.md: broken local link {l}")

if "--live" in sys.argv:
    for url in sorted(u for u in live if u.startswith(("https://maquert.github.io/", "https://github.com/Maquert/"))):
        try:
            code = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "site-check"}), timeout=20).status
        except Exception as e:
            code = str(e)
        if code != 200: errors.append(f"live {url}: {code}")

print("\n".join(errors) if errors else f"OK: {len(pages)} pages, {len(live)} external links{' (live-checked)' if '--live' in sys.argv else ''}")
sys.exit(1 if errors else 0)
