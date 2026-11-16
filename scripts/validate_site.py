#!/usr/bin/env python3
"""Validate the GM Early Years App iPhone guide before it is published."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'index.html').read_text(encoding='utf-8')
version = re.search(r'<title>[^<]*\bv(\d+\.\d+)', html)
version = version.group(1) if version else None
pages = re.findall(r'<section class="screen[^"]*" id="([^"]+)"', html)
ids = set(re.findall(r'\bid="([^"]+)"', html))
targets = set(re.findall(r'href="#([^"]+)"', html))
images = re.findall(r'<img\b[^>]*>', html)
external = set(re.findall(r'href="(https?://[^"]+)"', html))
release = ROOT / 'releases' / f'GM_Early_Years_App_iPhone_v{version}.html'

checks = {
    'HTML doctype': html.lstrip().lower().startswith('<!doctype html>'),
    'language set to en-GB': '<html lang="en-GB">' in html,
    'mobile viewport': 'name="viewport"' in html and 'width=device-width' in html,
    'version found in title': version is not None,
    'version shown on cover and document control': version is not None and html.count(f'Version {version}') >= 2,
    'guide pages present (60 or more)': len(pages) >= 60,
    'page ids are unique': len(pages) == len(set(pages)),
    'cover, contents and the four sections present': {'cover', 'contents', 's2', 's3', 's4', 's5'} <= set(pages),
    'every internal link has a target': targets <= ids,
    'every image has alt text': all('alt=' in i for i in images),
    'external links use HTTPS': all(u.startswith('https://') for u in external),
    'external links go to NHS login or Apple Maps only': all(re.match(r'https://((help|settings)\.login\.nhs\.uk|maps\.apple\.com)(/|$)', u) for u in external),
    'team maps load from Google Maps only, and only when opened': all(u.startswith('https://maps.google.com/maps?') for u in re.findall(r'data-map="([^"]+)"', html)) and not re.search(r'<iframe[^>]+\ssrc=', html, re.I),
    'self-contained: no external stylesheets': not re.search(r'<link[^>]+rel=["\']stylesheet', html, re.I),
    'self-contained: no remote JavaScript': not re.search(r'<script[^>]+src=', html, re.I),
    'self-contained: no remote images or fonts': not re.search(r'(src=|url\()["\']?https?://', html, re.I),
    'published guide matches the archived release': release.is_file() and release.read_bytes() == (ROOT / 'index.html').read_bytes(),
    '404 page present': (ROOT / '404.html').is_file(),
    '.nojekyll present': (ROOT / '.nojekyll').is_file(),
    'file size under 5 MB': (ROOT / 'index.html').stat().st_size < 5_000_000,
}
for name, ok in checks.items():
    print(('PASS ' if ok else 'FAIL ') + name)
print(f'Guide version {version}, {len(pages)} pages, {len(images)} images, {len(external)} external links.')
assert all(checks.values()), 'Guide validation failed'
print(f'All {len(checks)} checks passed.')
