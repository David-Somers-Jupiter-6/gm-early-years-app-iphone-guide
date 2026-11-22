"""Guide 3.31 (from 3.30) – TRIAL (/preview/ only). David, 22 Nov: focus on who can ACCESS the account.
 Q1 question: "Is it clear that the GM Early Years App account is for the child's mother or primary carer?"
 Q2 title "Who can access the account?", subheading "Account access", "Only the child's mother or primary carer can
    access the account that has been set up for them." / "In this guide, we call this person the account holder." /
    "Is it clear that only the child's mother or primary carer can access the account?"
 Q5 title "Can you access NHS login?", subheading "Used to sign in to the App", "NHS login is used to access the GM
    Early Years App account." (Tip and Try signing in kept) / "Can the child's mother or primary carer sign in to
    their NHS login account?"
usage: python3 make331.py v3.30.html v3.31.html"""
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

answers('ts1', 'Is it clear who the GM Early Years App account is for?', 'Yes, that is clear', 'No, I’m not sure', 'That is clear', 'That is OK. We will help.')

retitle('ts1b', 'Who can sign in?', 'Who has access?')
info('ts1b', 'Account access</h3><p class="q-why">Only the <strong>child’s mother or primary carer</strong> can access the account that has been set up for them.</p>'
             '<p class="q-why">In this guide, we call this person the <strong>account holder</strong>.</p>')
answers('ts1b', 'Is it clear only the child’s mother or primary carer can access it?', 'Yes, that is clear', 'No, I’m not sure', 'That is clear', 'That is OK. We will help.')

retitle('ts3', 'Can you use NHS login?', 'NHS login access')
m = page('ts3'); blk = m.group(0)
blk2 = re.sub(r'(<h3 class="h3 ts-sub"><span class="vh">[^<]*</span>)[^<]*</h3><p class="q-why">.*?</p>',
              lambda g: g.group(1) + 'Used to sign in to the App</h3><p class="q-why"><strong>NHS login</strong> is used to access the GM Early Years App account.</p>', blk, count=1, flags=re.S)
assert blk2 != blk; s = s[:m.start()] + blk2 + s[m.end():]
answers('ts3', 'Can the mother or primary carer sign in to NHS login?', 'Yes, they can sign in', 'No, they cannot sign in', 'They can sign in to NHS login', 'NHS login needs to work first')

m = page('tsum'); blk = m.group(0)
assert blk.count('<p class="sum-l">Who can sign in</p>') == 3
blk = blk.replace('<p class="sum-l">Who can sign in</p>', '<p class="sum-l">Who has access</p>').replace('Read who can sign in', 'Read who can access the account')
s = s[:m.start()] + blk + s[m.end():]

rep('Carer role v3.30', 'Carer role v3.31'); rep('Version 3.30 iPhone', 'Version 3.31 iPhone')
rep('>3.30 – REVIEW DRAFT', '>3.31 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.30</span>', '<span class="cv-ver">Version 3.31</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.26</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.30</span>', '<div class="rr"><span class="rv">3.31</span><span class="rd">22 Nov 2026</span><p>Troubleshooter: who can access the account; Can you access NHS login?</p></div>\n<div class="rr"><span class="rv">3.30</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
