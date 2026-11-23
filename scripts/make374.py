"""Guide 3.74 (from trial 3.73) – TRIAL. David, 23 Nov (title and explanation mock-ups approved):
Titles (also start page list, results page and data-title):
  1 Who is the account for?  2 Who can sign in to the account?  3 Do you have an NHS login account?
  4 Can you sign in to your NHS login account?  5 Are your details the same in both accounts?
  6 Has your Activation Link arrived?
Explanations: one information box with two short sections (questions 1, 2, 3, 4, 6); question 3 makes clear the
account holder must already have set up their own NHS login account; questions 3-4 say whose NHS login it must be.
The title box is the same size for one- and two-line titles, so nothing moves.
usage: python3 make374.py v3.73.html v3.74.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); assert m, i; return m
def in_sec(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:70], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
def card(rows):
    body = ''.join('<p class="abc-k%s">%s</p><p>%s</p>' % (' ts-k2' if n else '', k, t) for n, (k, t) in enumerate(rows))
    return '<div class="abc ts-card"><div class="abc-row"><span class="abc-ic ic-info" aria-hidden="true">i</span><div>%s</div></div></div>' % body
TITLES = [('ts1', '1', 'About your account', 'About your account', 'Who is the account for?'),
          ('ts1b', '2', 'Who will be able to access the account?', 'Who will be able to access the account?', 'Who can sign in to the account?'),
          ('ts2', '3', 'Do you have NHS login?', 'Do you have NHS login?', 'Do you have an NHS login account?'),
          ('ts3', '4', 'Can you sign in to NHS login?', 'Can you sign in to NHS login?', 'Can you sign in to your NHS login account?'),
          ('ts4', '5', 'Do your details match?', 'Account details', 'Are your details the same in both accounts?'),
          ('ts5', '6', 'Has your link arrived?', 'Activation Link', 'Has your Activation Link arrived?')]
for i, n, old, oldsum, new in TITLES:
    in_sec(i, '</span>%s</h2>' % old, '</span>%s</h2>' % new)
    rep('id="%s" data-sec="Section 6 · Troubleshooting" data-title="Troubleshooter · %s"' % (i, old), 'id="%s" data-sec="Section 6 · Troubleshooting" data-title="Troubleshooter · %s"' % (i, new))
    in_sec('ts', '<span aria-hidden="true">%s</span>%s</li>' % (n, old), '<span aria-hidden="true">%s</span>%s</li>' % (n, new))
    in_sec('tsum', '<p class="sum-l">%s</p>' % oldsum, '<p class="sum-l">%s</p>' % new, 3)
NEW = {
 'ts1': [('Who it is for', 'Your Health Visiting team sets up the account for the <strong>child’s mother or primary carer</strong>. We call this person the <strong>account holder</strong>.'),
         ('If it is for the wrong person', 'Your Health Visiting team can put it right.')],
 'ts1b': [('Who can access it', 'Only the <strong>account holder</strong> (the child’s mother or primary carer).'),
          ('How they sign in', 'With their own <strong>NHS login</strong>. Nobody else can sign in for them.')],
 'ts2': [('What you need', 'You need to have set up your own <strong>NHS login</strong> account. You use it to sign in to the GM Early Years App.'),
         ('Who must set it up', 'The <strong>account holder</strong> – the child’s mother or primary carer.')],
 'ts3': [('Signing in', 'You must be able to sign in to your own <strong>NHS login</strong> account to use the GM Early Years App.'),
         ('Whose NHS login', 'The <strong>account holder’s</strong> – the child’s mother or primary carer.')],
 'ts5': [('How it arrives', 'Your Health Visiting team sends an <strong>Activation Link</strong> by text to the mobile number on your GM Early Years App account.'),
         ('What it does', 'It opens the GM Early Years App sign-in page.')],
}
for i, rows in NEW.items():
    m = sec(i); b = m.group(0)
    old = re.search(r'<div class="ts-info">(.*?)</div>\n<div class="ts-ask">', b, re.S)
    b = b.replace(old.group(0), '<div class="ts-info">' + card(rows) + '</div>\n<div class="ts-ask">')
    s = s[:m.start()] + b + s[m.end():]
CSS = '/* 3.74 troubleshooter information box: second section under a thin line */\n#app .screen .ts-card p.abc-k.ts-k2{margin-top:8px!important;padding:8px 0 0 0!important;text-indent:0!important;border-top:1px solid rgba(0,94,184,.2)}\n'
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.73', 'Carer role v3.74'); rep('Version 3.73 iPhone', 'Version 3.74 iPhone')
rep('>3.73 – REVIEW DRAFT', '>3.74 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.73</span>', '<span class="cv-ver">Version 3.74</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.69</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.73</span>', '<div class="rr"><span class="rv">3.74</span><span class="rd">23 Nov 2026</span><p>Troubleshooter: clearer question titles and explanations</p></div>\n<div class="rr"><span class="rv">3.73</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
