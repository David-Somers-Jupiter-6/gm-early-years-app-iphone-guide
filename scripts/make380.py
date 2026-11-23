"""Guide 3.80 (from 3.79) – TRIAL. Fix: the Signing in pages lost their slim progress lights (shown as numbered
circles again), screenshot sizing, "Tap to enlarge" position and title box height after 3.77 renumbered the sections,
because 20 style rules picked out Signing in by its label 'Section 5' (now Support). Those rules now use a
permanent marker on the Signing in pages (data-signin), so renumbering or renaming sections cannot break them,
and the Support pages no longer pick them up.
Also: Support menu order NHS login account help, GM Early Years App help, Still need help?, Troubleshooter.
usage: python3 make380.py v3.79.html v3.80.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
n = s.count('[data-sec^="Section 5"]'); assert n == 20, n
s = s.replace('[data-sec^="Section 5"]', '[data-signin]')
s, k = re.subn(r'(<section class="screen[^"]*" id="[^"]+" data-sec="Section 4 · Signing in")', r'\1 data-signin=""', s)
assert k == 18, k
# Support menu order (David): NHS login account help, GM Early Years App help, Still need help?, Troubleshooter
m = re.search(r'(<nav aria-label="Support contents" class="tc-list">)(.*?)(</nav>)', s, re.S)
cards = re.findall(r'<a class="tc[^"]*"[^>]*href="#[^"]+".*?</a>', m.group(2), re.S)
assert ''.join(cards) == m.group(2), 'unexpected menu markup'
byhref = {re.search(r'href="#([^"]+)"', c).group(1): c for c in cards}
assert set(byhref) == {'ts', 's4-nhs', 's4-gm', 's4-help'}, byhref.keys()
s = s[:m.start(2)] + ''.join(byhref[h] for h in ['s4-nhs', 's4-gm', 's4-help', 'ts']) + s[m.end(2):]
rep('Carer role v3.79', 'Carer role v3.80'); rep('Version 3.79 iPhone', 'Version 3.80 iPhone')
rep('>3.79 – REVIEW DRAFT', '>3.80 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.79</span>', '<span class="cv-ver">Version 3.80</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.75</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.79</span>', '<div class="rr"><span class="rv">3.80</span><span class="rd">23 Nov 2026</span><p>Signing in: progress lights and screenshot layout restored</p></div>\n<div class="rr"><span class="rv">3.79</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
