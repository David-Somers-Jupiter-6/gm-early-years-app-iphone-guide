"""Guide 3.46 (from trial 3.45) – TRIAL. David, 22 Nov:
 - help page "Only the child's mother or primary carer can access" renamed "Only the account holder can access"
   (title, GM Early Years App help card, question 2's No message link);
 - on that page, What to do ends "ask your Health Visiting team" (was "ask the team"), with the Find your Health
   Visiting team button; the "Still stuck? Get help" bar is removed.
usage: python3 make346.py v3.45.html v3.46.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    assert blk.count(a) == 1, (pid, a[:80]); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
OLD, NEW = 'Only the child’s mother or primary carer can access', 'Only the account holder can access'
for a in ('data-title="%s"', 'aria-label="%s"', '<h2 class="h2" tabindex="-1">%s</h2>'):
    edit('s4-2', a % OLD, a % NEW)
edit('s4-gm', '<b>%s</b>' % OLD, '<b>%s</b>' % NEW)
edit('ts1b', '<a class="msg-link" href="#s4-2">%s</a>' % OLD, '<a class="msg-link" href="#s4-2">%s</a>' % NEW)
edit('s4-2', 'If the account is for the wrong person, ask the team.</p>', 'If the account is for the wrong person, ask your Health Visiting team.</p>')
m = re.search(r'<section class="screen" id="s4-2".*?</section>', s, re.S); blk = m.group(0)
blk2, n = re.subn(r'<div class="stuck"><b>Still stuck\?</b><a class="stuck-a" href="#s4-help">.*?</a></div>\n', '', blk, flags=re.S)
assert n == 1; s = s[:m.start()] + blk2 + s[m.end():]
assert OLD not in s
rep('Carer role v3.45', 'Carer role v3.46'); rep('Version 3.45 iPhone', 'Version 3.46 iPhone')
rep('>3.45 – REVIEW DRAFT', '>3.46 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.45</span>', '<span class="cv-ver">Version 3.46</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.41</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.45</span>', '<div class="rr"><span class="rv">3.46</span><span class="rd">22 Nov 2026</span><p>Only the account holder can access (renamed); no Still stuck bar</p></div>\n<div class="rr"><span class="rv">3.45</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
