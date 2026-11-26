#!/usr/bin/env python3
"""Validate the Simple guide (simple/ live and simple/preview/ trial) before it is published."""
from pathlib import Path
import re, json

ROOT = Path(__file__).resolve().parents[1]
ok_all = True
for rel, trial in (('simple/index.html', False), ('simple/preview/index.html', True)):
    f = ROOT / rel
    html = f.read_text(encoding='utf-8')
    version = re.search(r'<span class="cv-ver">Version (\d+\.\d+)</span>', html)
    version = version.group(1) if version else None
    pages = re.findall(r'<section class="screen[^"]*" id="([^"]+)"', html)
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    targets = set(re.findall(r'href="#([^"]+)"', html)) | set(re.findall(r'data-open="([^"]+)"', html)) - {''}
    images = re.findall(r'<img\b[^>]*>', html)
    external = set(re.findall(r'href="(https?://[^"]+)"', html)) | set(re.findall(r'"m":\s*"(https?://[^"]+)"', html))
    release = ROOT / 'releases' / f'GM_Early_Years_App_Simple_Guide_v{version}.html'
    folder = f.parent
    icons = '../../icons/' if trial else '../icons/'
    checks = {
        'HTML doctype': html.lstrip().lower().startswith('<!doctype html>'),
        'language set to en-GB': '<html lang="en-GB">' in html,
        'mobile viewport': 'name="viewport"' in html and 'width=device-width' in html,
        'version found on the cover': version is not None,
        'all pages present (cover, Before you start, steps 1 to N, help, contacts, accessibility)': (lambda steps: steps >= 7 and set(pages) == {'cover', 'before', 'help', 'contacts', 'a11y'} | {f'step-{i}' for i in range(1, steps + 1)})(len([x for x in pages if x.startswith('step-')])),
        'page ids are unique': len(pages) == len(set(pages)),
        'every internal link has a target': targets <= ids,
        'every image has alt text': all('alt=' in i for i in images),
        'external links use HTTPS': all(u.startswith('https://') for u in external),
        'external links go to NHS login or Apple Maps only': all(re.match(r'https://((help|settings)\.login\.nhs\.uk|maps\.apple\.com)(/|$)', u) for u in external),
        'self-contained: no external stylesheets, scripts, images or fonts': not re.search(r'<link[^>]+rel=["\']stylesheet|<script[^>]+src=|(src=|url\()["\']?https?://', html, re.I),
        'Home Screen: manifest and iPhone icon linked': 'rel="manifest" href="manifest.webmanifest"' in html and f'rel="apple-touch-icon" href="{icons}icon-180.png"' in html,
        'Home Screen: manifest present and valid': (folder / 'manifest.webmanifest').is_file() and json.loads((folder / 'manifest.webmanifest').read_text(encoding='utf-8'))['start_url'] == './',
        'file size under 2 MB': f.stat().st_size < 2_000_000,
    }
    if trial:
        live = (ROOT / 'simple/index.html').read_text(encoding='utf-8')
        checks['trial version is the same as, or newer than, live'] = tuple(map(int, version.split('.'))) >= tuple(map(int, re.search(r'cv-ver">Version (\d+\.\d+)', live).group(1).split('.')))
    else:
        checks['published simple guide matches the archived release'] = release.is_file() and release.read_bytes() == f.read_bytes()
        checks['offline worker cache named for this version'] = f"'ey-simple-v{version}'" in (folder / 'sw.js').read_text(encoding='utf-8')
    print(f'== {rel}: Simple guide version {version}, {len(pages)} pages, {len(images)} images, {len(external)} external links')
    for name, ok in checks.items():
        print(('PASS ' if ok else 'FAIL ') + name)
        ok_all &= ok
assert ok_all, 'Simple guide validation failed'
print('All Simple guide checks passed.')
