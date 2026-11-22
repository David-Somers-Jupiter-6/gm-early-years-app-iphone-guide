"""Guide 3.32 (from trial 3.31) – LIVE. David, 22 Nov: put the Troubleshooter live; put Contents (with Search) back
after the Introduction so the next step is clear; review the Troubleshooter so each thing it must find out is a
separate, clearly asked question.
 - Route: Cover -> Introduction -> Contents (Search in its title box) -> How this guide works. Contents moves to
   after the Introduction (Welcome pages: Cover 1, Introduction 2, Contents 3).
 - Questions 4 and 5 now ask about the child's mother or primary carer, like questions 1–3:
   Q4 "NHS login account" / "They need their own NHS login" / "Does the child's mother or primary carer have an NHS
      login account?"
   Q5 "Can the child's mother or primary carer sign in to NHS login?"
 - Includes everything from trials 3.23–3.31 (Troubleshooter, section badge position, quicker taps, results badge).
usage: python3 make332.py v3.31.html v3.32.html"""
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

def edit(pid, a, b):
    global s
    m = page(pid); blk = m.group(0); assert blk.count(a) == 1, (pid, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

def info(pid, new_inner):
    global s
    m = page(pid); blk = m.group(0)
    blk, n = re.subn(r'(<div class="ts-info"><h3 class="h3 ts-sub"><span class="vh">[^<]*</span>).*?(</div>\n<div class="ts-qa">)',
                     lambda g: g.group(1) + new_inner + g.group(2), blk, count=1, flags=re.S)
    assert n == 1, pid; s = s[:m.start()] + blk + s[m.end():]

def answers(pid, ask, yes, no, yes_h, no_h):
    m = page(pid); blk = m.group(0)
    blk = re.sub(r'(<p class="q-ask" id="ask-%s">)[^<]*(</p>)' % pid, r'\g<1>%s\2' % ask, blk)
    blk = re.sub(r'(class="ans ans-yes" name="ans-%s"/><span class="rc" aria-hidden="true"></span><span>)[^<]*' % pid, r'\g<1>%s' % yes, blk)
    blk = re.sub(r'(class="ans ans-no" name="ans-%s"/><span class="rc" aria-hidden="true"></span><span>)[^<]*' % pid, r'\g<1>%s' % no, blk)
    blk = re.sub(r'(<p class="ok-h">)[^<]*', r'\g<1>%s' % yes_h, blk)
    blk = re.sub(r'(<div class="stop-head"><svg.*?</svg><h3>)[^<]*', lambda g: g.group(1) + no_h, blk, flags=re.S)
    globals()['s'] = s[:m.start()] + blk + s[m.end():]


def retitle(pid, old, new):
    global s
    m = page(pid); blk = m.group(0)
    for a in ['data-title="Troubleshooter · %s"' % old, '</span>%s</h2>' % old]:
        assert blk.count(a) == 1, (pid, a); blk = blk.replace(a, a.replace(old, new))
    s = s[:m.start()] + blk + s[m.end():]
    m = page('ts'); blk = m.group(0); a = '</span>%s</li>' % old
    assert blk.count(a) == 1, ('ts list', old); s = s[:m.start()] + blk.replace(a, '</span>%s</li>' % new) + s[m.end():]


def nav(pid, which, to):
    global s
    m = page(pid)
    blk, k = re.subn(r'(<a class="nav-btn nav-%s[^"]*" href="#)[^"]+(")' % which, r'\g<1>%s\2' % to, m.group(0))
    assert k >= 1, (pid, which); s = s[:m.start()] + blk + s[m.end():]

# 1. Contents after the Introduction
m = page('contents'); blk = m.group(0); s = s[:m.start()] + s[m.end():]
m = page('intro'); s = s[:m.end()] + blk + s[m.end():]
nav('intro', 'next', 'contents'); nav('contents', 'back', 'intro'); nav('contents', 'next', 'how'); nav('how', 'back', 'contents')
m = page('cover'); assert 'nav-start" href="#intro"' in m.group(0)
for pid, n in (('intro', 2), ('contents', 3)):
    m = page(pid); blk = re.sub(r'<span class="pos">Page \d of 3</span>', '<span class="pos">Page %d of 3</span>' % n, m.group(0), count=1)
    s = s[:m.start()] + blk + s[m.end():]

# 2. Questions 4 and 5 about the child's mother or primary carer
m = page('ts2'); blk = m.group(0)
for a, b in [('data-title="Troubleshooter · Do you have NHS login?"', 'data-title="Troubleshooter · NHS login account"'),
             ('</span>Do you have NHS login?</h2>', '</span>NHS login account</h2>')]:
    assert blk.count(a) == 1, a; blk = blk.replace(a, b)
s = s[:m.start()] + blk + s[m.end():]
m = page('ts'); blk = m.group(0); a = '</span>Do you have NHS login?</li>'; assert blk.count(a) == 1
s = s[:m.start()] + blk.replace(a, '</span>NHS login account</li>') + s[m.end():]
info('ts2', 'They need their own NHS login</h3><p class="q-why">The GM Early Years App uses an <strong>NHS login</strong> account to sign in.</p>')
answers('ts2', 'Does the child’s mother or primary carer have an NHS login account?', 'Yes, they have NHS login', 'No, or I’m not sure', 'They have NHS login', 'They need NHS login first')
answers('ts3', 'Can the child’s mother or primary carer sign in to NHS login?', 'Yes, they can sign in', 'No, they cannot sign in', 'They can sign in to NHS login', 'NHS login needs to work first')
m = page('tsum'); blk = m.group(0)
for a, b in [('You have NHS login', 'They have NHS login'), ('You do not have NHS login yet', 'They do not have NHS login yet'),
             ('<p class="sum-s">You can sign in</p>', '<p class="sum-s">They can sign in</p>'), ('You cannot sign in yet', 'They cannot sign in yet')]:
    assert blk.count(a) == 1, a; blk = blk.replace(a, b)
s = s[:m.start()] + blk + s[m.end():]

# counters by position
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[:4] == ['cover', 'intro', 'contents', 'how'] and ids[-1] == 'search'; T = len(ids) - 1
def put(pid, new):
    global s
    m = page(pid); s = s[:m.start()] + new + s[m.end():]
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: put(pid, new)

rep('Carer role v3.31', 'Carer role v3.32'); rep('Version 3.31 iPhone', 'Version 3.32 iPhone')
rep('>3.31 – REVIEW DRAFT', '>3.32 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.31</span>', '<span class="cv-ver">Version 3.32</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.27</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.31</span>', '<div class="rr"><span class="rv">3.32</span><span class="rd">22 Nov 2026</span><p>Troubleshooter live; Contents after the Introduction; questions 4 and 5 about the mother or primary carer</p></div>\n<div class="rr"><span class="rv">3.31</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, T)
