"""Guide 3.18 (from 3.17) – TRIAL (/preview/ only). David, 21 Nov: a calmer start. People reach this guide already
frustrated ("I've tried this and it doesn't work") and do not know where it is failing, so the guide leads them
gently through the questions instead of asking them to choose.
 - Start (cover button and "Start the guide") opens the Introduction, not Contents. Contents stays in the bottom bar.
 - Introduction: calm, reassuring words; "Need help now? Go to Troubleshooting" removed.
 - How this guide works: says what will happen (3 parts) instead of what the guide will "show you";
   "You do not need to work out what is wrong. This guide does that with you."
 - Your roadmap page removed (How this guide works now does its job): How this guide works → Contact your HV team.
   86 → 85 pages; Section 1 is 1 page.
usage: python3 make318.py v3.17.html v3.18.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>\n?' % re.escape(pid), s, re.S)
    assert m, pid
    return m

def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0); assert blk.count(a) == n, (pid, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

def nav(pid, which, to):
    global s
    m = page(pid)
    blk, k = re.subn(r'(<a class="nav-btn nav-%s[^"]*" href="#)[^"]+(")' % which, r'\g<1>%s\2' % to, m.group(0))
    assert k == 1, (pid, which); s = s[:m.start()] + blk + s[m.end():]

# 1. Start → Introduction
edit('cover', '<a class="nav-btn nav-next nav-start" href="#contents">', '<a class="nav-btn nav-next nav-start" href="#intro">')
edit('cover', '<nav class="cv-rows" aria-label="Quick links"><a href="#contents">', '<nav class="cv-rows" aria-label="Quick links"><a href="#intro">')
nav('intro', 'back', 'cover')

# 2. Introduction: calm words
edit('intro', '<p class="lead iv-lead">Having trouble signing in to the GM Early Years App? <strong>You are not alone.</strong> This guide shows you what is stopping you, and what to do next.</p>',
     '<p class="lead iv-lead">Having trouble signing in to the GM Early Years App? <strong>You are not alone, and it is not your fault.</strong></p>\n'
     '<p class="iv-calm">If you have tried before and it did not work, it usually comes down to one small detail. This guide will help you find it, one step at a time.</p>')
m = re.search(r'<a class="iv-help" href="#s4">.*?</a>\n', page('intro').group(0), re.S); assert m
edit('intro', m.group(0), '')
edit('intro', '<p>Tap <strong>Next</strong> to continue.</p>', '<p>Tap <strong>Next</strong> when you are ready.</p>')

# 3. How this guide works: what will happen
m = re.search(r'<p class="hw-p">Sometimes connecting.*?</ol>', page('how').group(0), re.S); assert m
edit('how', m.group(0),
     '<p class="hw-p"><strong>You do not need to work out what is wrong.</strong> This guide does that with you.</p>\n'
     '<p class="hw-p hw-will">Here is what will happen:</p>\n'
     '<ol class="hw-list">'
     '<li><span class="hw-n" aria-hidden="true">1</span><span><strong>Check what you need:</strong> your Health Visiting team, your account, and 4 quick Yes or No questions</span></li>'
     '<li><span class="hw-n" aria-hidden="true">2</span><span><strong>Sign in, one step at a time,</strong> with a picture of each screen</span></li>'
     '<li><span class="hw-n" aria-hidden="true">3</span><span><strong>Get the right help</strong> if something is not right: who to contact and what to do</span></li>'
     '</ol>')
nav('how', 'next', 'hv'); nav('hv', 'back', 'how')

# 4. remove Your roadmap
m = page('roadmap'); s = s[:m.start()] + s[m.end():]
assert 'href="#roadmap"' not in s, re.findall(r'.{80}href="#roadmap".{40}', s)[:3]

CSS = """/* 3.18 calmer Introduction */
#app #intro .iv-calm{font-size:17px;line-height:1.45;color:var(--ink);margin:0 0 14px}
@media screen and (max-height:600px){#app #intro .iv-calm{margin-bottom:10px;font-size:16px}}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# 5. counters
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[-1] == 'search'; T = len(ids) - 1; assert T == 85, T
edit('how', '<span class="pos">Page 1 of 2</span>', '<span class="pos">Page 1 of 1</span>')
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: m = page(pid); s = s[:m.start()] + new + s[m.end():]
assert '/ 86<' not in s and 'of 86)' not in s

rep('Carer role v3.17', 'Carer role v3.18'); rep('Version 3.17 iPhone', 'Version 3.18 iPhone')
rep('>3.17 – REVIEW DRAFT', '>3.18 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.17</span>', '<span class="cv-ver">Version 3.18</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.15</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.17</span>', '<div class="rr"><span class="rv">3.18</span><span class="rd">21 Nov 2026</span><p>Calmer start: Start opens the Introduction; How this guide works says what will happen</p></div>\n<div class="rr"><span class="rv">3.17</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, 'pages', T)
