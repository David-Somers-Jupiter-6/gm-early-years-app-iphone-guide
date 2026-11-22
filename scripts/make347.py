"""Guide 3.47 (from trial 3.46) – TRIAL. David, 22 Nov: delete question 3 ("Is this you?"). The Troubleshooter now
has 6 questions: after "Who has access?" comes "NHS login account". The start page list, steppers, question
numbers, Your results and the page code are updated to match.
usage: python3 make347.py v3.46.html v3.47.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>\n?' % re.escape(pid), s, re.S); assert m, pid; return m
def put(pid, new):
    global s
    m = page(pid); s = s[:m.start()] + new + s[m.end():]

# 1. remove the page
m = page('ts1c'); s = s[:m.start()] + s[m.end():]
# 2. links around it
rep('<a class="nav-btn nav-next go-yes" href="#ts1c">', '<a class="nav-btn nav-next go-yes" href="#ts2">')
rep('<a class="nav-btn nav-next go-no" href="#ts1c">', '<a class="nav-btn nav-next go-no" href="#ts2">')
blk = page('ts2').group(0); assert blk.count('<a class="nav-btn nav-back" href="#ts1c">') == 1
put('ts2', blk.replace('<a class="nav-btn nav-back" href="#ts1c">', '<a class="nav-btn nav-back" href="#ts1b">'))
# 3. Your results: remove the "Account holder" row
blk = page('tsum').group(0)
blk2, n = re.subn(r'<li class="r3">.*?</li>', '', blk, count=1, flags=re.S); assert n == 1 and 'ts1c' not in blk2
put('tsum', blk2)
# 4. JavaScript lists
for a in ("['ts1','ts1b','ts1c','ts2','ts3','ts4','ts5']", "['ts1','ts1b','ts1c','ts2','ts3','ts4','ts5','tsum']"):
    s = s.replace(a, a.replace("'ts1c',", ''))
# 5. CSS
css_end = s.index('</style>'); css, rest = s[:css_end], s[css_end:]
css = css.replace(',#ts1c,', ',').replace(',#ts1c)', ')').replace('(#ts1c,', '(')
def fix(mm):
    sel, body = mm.group(1), mm.group(2)
    if 'ts1c' not in sel: return mm.group(0)
    if sel.count(':has(') >= 2:
        sel = sel.replace(':has(#ts1c .ans-yes:checked)', '')
        if 'ts1c' not in sel: return sel + '{' + body + '}'
    assert ',' not in re.sub(r'\([^()]*\)', '', sel), sel   # single selector: drop the whole rule
    return ''
css = re.sub(r'([^{}]*)\{([^{}]*)\}', fix, css)
assert 'ts1c' not in css
s = css + rest
assert 'ts1c' not in s, [s[m.start()-80:m.end()+20] for m in re.finditer('ts1c', s)][:3]
# 6. numbering: 6 questions
Q = ['ts1', 'ts1b', 'ts2', 'ts3', 'ts4', 'ts5']
def stepper(cur):
    return '<div class="stepper chk-steps" aria-hidden="true">' + ''.join(
        '<span class="%s">%d</span>' % ('c cur' if i == cur else '', i) for i in range(1, 7)) + '</div>'
for i, pid in enumerate(Q, 1):
    blk = page(pid).group(0)
    blk, n = re.subn(r'<div class="stepper chk-steps" aria-hidden="true">.*?</div>', stepper(i), blk, count=1, flags=re.S); assert n == 1
    blk = re.sub(r'<span class="tp-n" aria-hidden="true">\d</span>', '<span class="tp-n" aria-hidden="true">%d</span>' % i, blk)
    blk = re.sub(r'Question \d of 7', 'Question %d of 6' % i, blk)
    blk = re.sub(r'aria-label="Troubleshooter question \d of 7"', 'aria-label="Troubleshooter question %d of 6"' % i, blk)
    assert ' of 7' not in blk, pid
    put(pid, blk)
blk = page('tsum').group(0)
blk, n = re.subn(r'<div class="stepper chk-steps" aria-hidden="true">.*?</div>', stepper(0), blk, count=1, flags=re.S); assert n == 1
put('tsum', blk)
# start page
blk = page('ts').group(0)
blk = blk.replace('Answer <strong>7 quick questions</strong>', 'Answer <strong>6 quick questions</strong>')
blk, n = re.subn(r'<li><span aria-hidden="true">3</span>Is this you\?</li>', '', blk); assert n == 1
k = iter(range(1, 7))
blk = re.sub(r'<li><span aria-hidden="true">\d</span>', lambda mm: '<li><span aria-hidden="true">%d</span>' % next(k), blk)
assert '6 quick questions' in blk
put('ts', blk)
# 7. Section 6 numbering and whole-guide counters
k = iter(range(1, 100)); s, n = re.subn(r'<span class="pos">Page \d+ of 50</span>', lambda mm: '<span class="pos">Page %d of 49</span>' % next(k), s); assert n == 49, n
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[:4] == ['cover', 'intro', 'contents', 'how'] and ids[-1] == 'search'; T = len(ids) - 1
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    nb = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    nb = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', nb)
    if nb != blk: put(pid, nb)
rep('Carer role v3.46', 'Carer role v3.47'); rep('Version 3.46 iPhone', 'Version 3.47 iPhone')
rep('>3.46 – REVIEW DRAFT', '>3.47 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.46</span>', '<span class="cv-ver">Version 3.47</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.42</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.46</span>', '<div class="rr"><span class="rv">3.47</span><span class="rd">22 Nov 2026</span><p>Troubleshooter: question 3 (Is this you?) removed; 6 questions</p></div>\n<div class="rr"><span class="rv">3.46</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, T)
