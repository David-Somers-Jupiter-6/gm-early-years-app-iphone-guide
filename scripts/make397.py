"""Guide 3.97 (from 3.96) – Installing the App: "Tap Search" and "Search for the App" combined into one step (David, 28 Nov).
 - page inst-2 removed; inst-3 is now step 2 "Search for the App" (Tap Search chip, combined instruction, its screenshot kept)
 - 6 steps: inst-1, inst-3, inst-4, inst-5, inst-6, inst-7 (+ inst-7-tip); page ids kept so links still work
 - clip inst-3 rebuilt by scripts/assets/install/v397/build_clip_search.py; clip address ?v=3.97
 - Contents counters 77 -> 76, Support "Page N of 35" -> 34
usage: python3 make397.py v3.96.html v3.97.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
def sec(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>\n' % re.escape(pid), s, re.S); assert m, pid; return m

rep('content="Version 3.96. A screen-by-screen', 'content="Version 3.97. A screen-by-screen')
rep('>3.96 (iPhone edition)<', '>3.97 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.96</span>', '<span class="cv-ver">Version 3.97</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.91</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.96</span>', '<div class="rr"><span class="rv">3.97</span><span class="rd">28 Nov 2026</span><p>Installing the App: Tap Search and Search for the App combined (6 steps)</p></div>\n<div class="rr"><span class="rv">3.96</span>')
rep("return base()+n+'.mp4?v=3.96';", "return base()+n+'.mp4?v=3.97';")

# counters before the page goes: every page after inst-2 moves up one
secs = [(m.group(1), m.start(), m.end()) for m in re.finditer(r'<section class="screen[^"]*" id="([^"]+)".*?</section>', s, re.S)]
gone = [i for i, (pid, a, b) in enumerate(secs) if pid == 'inst-2'][0]
out, last = [], 0
for i, (pid, a, b) in enumerate(secs):
    blk = s[a:b]
    def cnt(m):
        n = int(m.group(1)); return f'{n - 1 if i > gone else n}'
    blk = re.sub(r'(?<=<span class="count">)(\d+)(?= / 77</span>)', cnt, blk).replace(' / 77</span>', ' / 76</span>')
    blk = re.sub(r'(?<=aria-label="Contents \(page )(\d+)(?= of 77\)")', cnt, blk).replace(' of 77)"', ' of 76)"')
    if 'data-sec="Section 5 · Support"' in blk:
        blk = re.sub(r'(?<=<span class="pos">Page )(\d+)(?= of 35</span>)', cnt, blk).replace(' of 35</span>', ' of 34</span>')
    out.append(s[last:a]); out.append(blk); last = b
out.append(s[last:]); s = ''.join(out)
assert ' / 77<' not in s and 'of 35</span>' not in s

# remove step 2 page and join the chain
m = sec('inst-2'); s = s[:m.start()] + s[m.end():]
m = sec('inst-1'); blk = m.group(0); assert blk.count('href="#inst-2"') == 1
s = s[:m.start()] + blk.replace('href="#inst-2"', 'href="#inst-3"') + s[m.end():]
m = sec('inst-3'); blk = m.group(0); assert blk.count('<a class="nav-btn nav-back" href="#inst-2">') == 1
blk = blk.replace('<a class="nav-btn nav-back" href="#inst-2">', '<a class="nav-btn nav-back" href="#inst-1">')
old_p = '<p>Tap the search box and type <strong>gm early years</strong>. Look for <strong>GM Early Years</strong> by Greater Manchester Early Years.</p>\n'
assert blk.count(old_p) == 1
blk = blk.replace(old_p, '<p>Tap <strong>Search</strong> at the bottom of the App Store. Tap the search box and type <strong>gm early years</strong>. '
                  'Look for <strong>GM Early Years</strong> by Greater Manchester Early Years.</p>\n'
                  '<div class="tap"><span class="lbl">Tap</span><span class="chip">Search</span></div>\n')
s = s[:m.start()] + blk + s[m.end():]

# renumber the steps: 7 -> 6
NEW = {'inst-1': 1, 'inst-3': 2, 'inst-4': 3, 'inst-5': 4, 'inst-6': 5, 'inst-7': 6}
def stepper(cur):
    return '<div class="stepper" aria-hidden="true">' + ''.join(
        '<span class="d">✓</span>' if i < cur else ('<span class="c">%d</span>' % i if i == cur else '<span class="">%d</span>' % i) for i in range(1, 7)) + '</div>'
for pid, n in list(NEW.items()) + [('inst-7-tip', 7)]:
    m = sec(pid); blk = m.group(0)
    blk, k = re.subn(r'<div class="stepper" aria-hidden="true">.*?</div>', stepper(n), blk, count=1, flags=re.S); assert k == 1, pid
    old = int(re.search(r'<span class="tp-n" aria-hidden="true">(\d)</span>', blk).group(1))
    shown = min(n, 6)
    blk = blk.replace(f'<span class="tp-n" aria-hidden="true">{old}</span>', f'<span class="tp-n" aria-hidden="true">{shown}</span>')
    blk = blk.replace(f'Step {old} of 7', f'Step {shown} of 6')
    blk = re.sub(r'data-title="Install step \d ·', f'data-title="Install step {shown} ·', blk)
    blk = re.sub(r'aria-label="Install step \d', f'aria-label="Install step {shown}', blk)
    assert not re.search(r'Step \d of 7\b', blk), pid
    s = s[:m.start()] + blk + s[m.end():]
rep('Install the GM Early Years App from the App Store in 7 steps.', 'Install the GM Early Years App from the App Store in 6 steps.')
assert 'id="inst-2"' not in s and '#inst-2"' not in s
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
