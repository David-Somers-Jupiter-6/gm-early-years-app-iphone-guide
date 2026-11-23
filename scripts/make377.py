"""Guide 3.77 (from trial 3.76) – TRIAL. David, 23 Nov – new structure:
 Contents: Cover page, Introduction, 1 How this guide works | 2 Contact your Health Visiting team (own band) |
 3 Troubleshooter (own band) | 4 Signing in to the GM Early Years App | 5 Troubleshooting, 6 Contact & support |
 Accessibility, About this guide.
 - Section 3 About your account (acct, nhs) and Section 4 Checklist (s2, c1-c4, sum) removed (the Troubleshooter
   replaces them), with their script references;
 - the Troubleshooter (ts, ts1, ts1b, ts2-ts5, tsum) moves straight after Contact your Health Visiting team as Section 3;
 - Signing in becomes Section 4, Troubleshooting 5, Contact & support 6 (labels, badges, aria labels, in-text mentions);
 - Back / Next: hv -> ts, ts Back -> hv, Signing in Back -> Troubleshooter results;
 - "Return to the checklist" (Activation Link: When you have your link) now returns to the Troubleshooter, question 6;
 - How this guide works roadmap step 1 mentions the Troubleshooter's 6 questions;
 - every page counter (Page N of M, Contents N / T) recomputed.
usage: python3 make377.py v3.76.html v3.77.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
SEC = re.compile(r'<section class="screen[^"]*" id="([^"]+)".*?</section>\n?', re.S)
def blocks():
    return [(m.group(1), m.start(), m.end()) for m in SEC.finditer(s)]
def get(i):
    for k, a, b in blocks():
        if k == i: return a, b
    raise KeyError(i)
def edit(i, f):
    global s
    a, b = get(i); s = s[:a] + f(s[a:b]) + s[b:]
def in_sec(i, old, new, n=1):
    def f(blk):
        assert blk.count(old) == n, (i, old[:80], blk.count(old)); return blk.replace(old, new)
    edit(i, f)

# 1 remove Sections 3 and 4
for i in ['acct', 'nhs', 's2', 'c1', 'c2', 'c3', 'c4', 'sum']:
    a, b = get(i); s = s[:a] + s[b:]
# 2 move the Troubleshooter after hv
ids = [k for k, a, b in blocks()]
TS = ['ts', 'ts1', 'ts1b', 'ts2', 'ts3', 'ts4', 'ts5', 'tsum']
i0 = ids.index('ts'); assert ids[i0:i0 + 8] == TS, ids[i0:i0 + 8]
a, _ = get('ts'); _, b = get('tsum'); block = s[a:b]; s = s[:a] + s[b:]
_, hv_end = get('hv'); s = s[:hv_end] + block + s[hv_end:]
# 3 navigation
in_sec('hv', '<a class="nav-btn nav-next" href="#acct">', '<a class="nav-btn nav-next" href="#ts">')
in_sec('ts', '<a class="nav-btn nav-back" href="#s4">', '<a class="nav-btn nav-back" href="#hv">')
in_sec('s3', '<a class="nav-btn nav-back" href="#sum">', '<a class="nav-btn nav-back" href="#tsum">')
in_sec('s4-activation-2', '<h3>Return to the checklist</h3>', '<h3>Return to the Troubleshooter</h3>')
in_sec('s4-activation-2', '<p><a href="#s2">Checklist</a> — answer <a href="#c4">question 4</a>, then follow the <a href="#s3">sign-in instructions</a>.</p>',
       '<p><a href="#ts">Troubleshooter</a> — answer <a href="#ts5">question 6</a>, then follow the <a href="#s3">sign-in instructions</a>.</p>')
# 4 section numbers (labels, badges, aria labels) – order matters
for i in TS:
    edit(i, lambda blk: blk.replace('Section 6 · Troubleshooting', 'Section 3 · Troubleshooter'))
order = [k for k, a, b in blocks()]
def section_of(i):
    a, b = get(i); m = re.search(r'data-sec="([^"]*)"', s[a:b]); return m.group(1) if m else ''
for i in order:
    sec = section_of(i)
    if sec == 'Section 5 · Signing in':
        edit(i, lambda blk: blk.replace('Section 5 · Signing in', 'Section 4 · Signing in'))
for i in order:
    if section_of(i) == 'Section 6 · Troubleshooting':
        edit(i, lambda blk: blk.replace('Section 6 · Troubleshooting', 'Section 5 · Troubleshooting'))
for i in order:
    if section_of(i) == 'Section 7 · Contact &amp; support':
        edit(i, lambda blk: blk.replace('Section 7 · Contact &amp; support', 'Section 6 · Contact &amp; support'))
in_sec('s3', 'aria-label="Section 5"', 'aria-label="Section 4"')
in_sec('s4', 'aria-label="Section 6: Troubleshooting"', 'aria-label="Section 5: Troubleshooting"')
in_sec('s4', '<span aria-hidden="true" class="sec-b">6</span>', '<span aria-hidden="true" class="sec-b">5</span>')
in_sec('s4', '<span class="tp-n" aria-hidden="true">6</span>', '<span class="tp-n" aria-hidden="true">5</span>')
in_sec('s5', 'aria-label="Section 7"', 'aria-label="Section 6"')
in_sec('s5', '<span aria-hidden="true" class="sec-b">7</span>', '<span aria-hidden="true" class="sec-b">6</span>')
in_sec('s5', '<span class="tp-n" aria-hidden="true">7</span>', '<span class="tp-n" aria-hidden="true">6</span>')
in_sec('ts', 'aria-label="Troubleshooter"', 'aria-label="Section 3: Troubleshooter"')
# in-text mentions of Section 7 (body only)
body_start = s.index('<body'); head, body = s[:body_start], s[body_start:]
parts = re.split(r'(<script.*?</script>|<style.*?</style>)', body, flags=re.S)
for n in range(0, len(parts), 2):
    parts[n] = parts[n].replace('Section 7, Contact &amp; support', 'Section 6, Contact &amp; support').replace('Section 7 · Contact &amp; support', 'Section 6 · Contact &amp; support')
s = head + ''.join(parts)
leftover = [m.group(0) for m in re.finditer(r'Section 7[^<]{0,30}', re.sub(r'<script.*?</script>|<style.*?</style>', '', s[s.index('<body'):], flags=re.S))]
assert not leftover, leftover
# 5 Contents
a, b = get('contents'); blk = s[a:b]
toc = re.search(r'<nav aria-label="Contents" class="toc toc-grp">.*?</nav>', blk, re.S).group(0)
rows = dict(re.findall(r'(<a class="toc-row[^"]*" href="#([^"]+)">.*?</a>)', toc, re.S)[i][::-1] for i in range(len(re.findall(r'<a class="toc-row', toc))))
def row(h): return rows[h]
ts_row = row('s4').replace('href="#s4"', 'href="#ts"').replace('<span class="gb">6</span>', '<span class="gb">3</span>').replace('<span class="tt">Troubleshooting</span>', '<span class="tt">Troubleshooter</span>')
s3_row = row('s3').replace('<span class="gb">5</span>', '<span class="gb">4</span>')
s4_row = row('s4').replace('<span class="gb">6</span>', '<span class="gb">5</span>')
s5_row = row('s5').replace('<span class="gb">7</span>', '<span class="gb">6</span>')
new_toc = ('<nav aria-label="Contents" class="toc toc-grp">\n'
           '<div class="toc-g">' + row('cover') + '\n' + row('intro') + '\n' + row('how') + '</div>\n'
           '<div class="toc-g">' + row('hv') + '</div>\n'
           '<div class="toc-g">' + ts_row + '</div>\n'
           '<div class="toc-g">' + s3_row + '</div>\n'
           '<div class="toc-g">' + s4_row + '\n' + s5_row + '</div>\n'
           '<div class="toc-g">' + row('a11y') + '\n' + row('s6') + '</div>\n</nav>')
s = s[:a] + blk.replace(toc, new_toc) + s[b:]
# 6 How this guide works roadmap
in_sec('how', '<strong>Check what you need:</strong> your Health Visiting team, your account, and 4 quick Yes or No questions',
       '<strong>Check what you need:</strong> your Health Visiting team, then the Troubleshooter’s 6 quick Yes or No questions')
# 7 script references to the removed pages
rep("    if(cur&&cur.id==='s2'&&a.getAttribute('href')==='#c1') resetChecklist(['c1','c2','c3','c4']);\n", '')
rep("[['sum',['c1','c2','c3','c4']],['tsum',['ts1','ts1b','ts2','ts3','ts4','ts5']]]", "[['tsum',['ts1','ts1b','ts2','ts3','ts4','ts5']]]")
rep("var orders=[['c1','c2','c3','c4','sum'],['ts1','ts1b','ts2','ts3','ts4','ts5','tsum']];", "var orders=[['ts1','ts1b','ts2','ts3','ts4','ts5','tsum']];")
rep("var CHQ=['c1','c2','c3','c4'];", "var CHQ=[];")
# 8 page counters
order = [k for k, a, b in blocks()]
pages = [k for k in order if k != 'search']; T = len(pages)
groups = {}
for k in pages: groups.setdefault(section_of(k), []).append(k)
for k in pages:
    g = groups[section_of(k)]; n = g.index(k) + 1; idx = pages.index(k) + 1
    def f(blk, n=n, m=len(g), idx=idx):
        blk = re.sub(r'<span class="pos">Page \d+ of \d+</span>', '<span class="pos">Page %d of %d</span>' % (n, m), blk)
        blk = re.sub(r'<span class="count">\d+ / \d+</span>', '<span class="count">%d / %d</span>' % (idx, T), blk)
        blk = re.sub(r'\(page \d+ of \d+\)', '(page %d of %d)' % (idx, T), blk)
        return blk
    edit(k, f)
# 9 version
rep('Carer role v3.76', 'Carer role v3.77'); rep('Version 3.76 iPhone', 'Version 3.77 iPhone')
rep('>3.76 – REVIEW DRAFT', '>3.77 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.76</span>', '<span class="cv-ver">Version 3.77</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.72</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.76</span>', '<div class="rr"><span class="rv">3.77</span><span class="rd">23 Nov 2026</span><p>New structure: the Troubleshooter is Section 3; About your account and the Checklist removed</p></div>\n<div class="rr"><span class="rv">3.76</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, '| pages', T, '| sections', {k: len(v) for k, v in groups.items()})
