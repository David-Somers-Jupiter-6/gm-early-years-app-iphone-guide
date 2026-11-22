"""Guide 3.29 (from 3.28) – TRIAL (/preview/ only) mock-up. David, 22 Nov: Troubleshooter questions 1–4 say exactly
who and what, so the reader does not have to put two and two together.
 Q1 Who is the account for?   "The child's mother or primary carer" / the HV team sets it up for them /
                              "Is it clear that the account is for the child's mother or primary carer?"
 Q2 Who can sign in?          "Only the child's mother or primary carer" / a partner or relative cannot sign in for
                              them / "In this guide, we call this person the account holder." /
                              "Is it clear that only the child's mother or primary carer can sign in?"
 Q3 Do you have NHS login?    "You need an NHS login account" / "The GM Early Years App uses an NHS login account to
                              sign you in." / "Do you have an NHS login account?"
 Q4 Can you use NHS login?    "Can you access your NHS login account?" / email address and password / a Tip box
                              "Check that you can sign in to NHS login first." / "Can you sign in to your NHS login account?"
 Results rows 1 and 2 follow (Not sure → About your account / A partner is signing in).
usage: python3 make329.py v3.28.html v3.29.html"""
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

info('ts1', 'The child’s mother or primary carer</h3><p class="q-why">Your Health Visiting team sets up the GM Early Years App account for the <strong>child’s mother or primary carer</strong>.</p>')
answers('ts1', 'Is it clear that the account is for the child’s mother or primary carer?', 'Yes, that is clear', 'No, I’m not sure',
        'Good, that is clear', 'Check who the account is for')

info('ts1b', 'Only the child’s mother or primary carer</h3><p class="q-why">A partner or relative <strong>cannot</strong> sign in for them.</p>'
             '<p class="q-why">In this guide, we call this person the <strong>account holder</strong>.</p>')
answers('ts1b', 'Is it clear that only the child’s mother or primary carer can sign in?', 'Yes, that is clear', 'No, I’m not sure',
        'Good, that is clear', 'Only they can sign in')

info('ts2', 'You need an NHS login account</h3><p class="q-why">The GM Early Years App uses an <strong>NHS login</strong> account to sign you in.</p>')
answers('ts2', 'Do you have an NHS login account?', 'Yes, I have NHS login', 'No, or I’m not sure', 'You have NHS login', 'You need NHS login first')

TIP = '<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.6 10.8c.6.5 1 1.2 1.1 2.2h5c.1-1 .5-1.7 1.1-2.2A6 6 0 0012 3z"/></svg>'
info('ts3', 'Can you access your NHS login account?</h3><p class="q-why">You sign in to NHS login with your <strong>email address</strong> and <strong>password</strong>.</p>'
            '<p class="ts-tip"><span class="ts-tip-i">' + TIP + '</span><span><strong>Tip:</strong> check that you can sign in to NHS login first.</span></p>')
answers('ts3', 'Can you sign in to your NHS login account?', 'Yes, I can sign in', 'No, I cannot sign in', 'You can sign in to NHS login', 'NHS login needs to work first')

# results rows 1 and 2
CHEV_RE = r'(Get help<svg.*?</svg></a>)'
m = page('tsum'); blk = m.group(0)
blk = re.sub(r'<li class="r1">.*?</li>', lambda g: g.group(0)
             .replace('<p class="sum-l">Account holder</p>', '<p class="sum-l">Who the account is for</p>')
             .replace('You are the account holder', 'That is clear').replace('Only the account holder can sign in', 'Not sure who the account is for')
             .replace('href="#s4-2">Get help', 'href="#acct">Get help'), blk, count=1, flags=re.S)
blk = re.sub(r'<li class="r2">.*?</li>', lambda g: g.group(0)
             .replace('<p class="sum-l">Your own NHS login</p>', '<p class="sum-l">Who can sign in</p>')
             .replace('You will use your own NHS login', 'That is clear').replace('Only your own NHS login works', 'Not sure who can sign in')
             .replace('href="#s4-1b">Get help', 'href="#s4-2">Get help'), blk, count=1, flags=re.S)
assert blk.count('Who the account is for') == 3 and blk.count('Who can sign in</p>') == 3 and 'href="#acct">Get help' in blk and blk.count('href="#s4-2">Get help') == 1
s = s[:m.start()] + blk + s[m.end():]

CSS = """/* 3.29 Troubleshooter tip box */
#app #ts3 .ts-tip{display:flex;gap:8px;align-items:flex-start;margin:6px 0 0;padding:8px 12px;border-radius:12px;background:#e8f1fb;border-left:4px solid #005eb8;color:var(--ink);font-size:16px;line-height:1.35}
#app #ts3 .ts-tip-i{flex:0 0 20px;color:#005eb8;margin-top:1px}
@media (prefers-color-scheme:dark){#app #ts3 .ts-tip{background:#1d3046}#app #ts3 .ts-tip-i{color:#7fb8ff}}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}')

rep('Carer role v3.28', 'Carer role v3.29'); rep('Version 3.28 iPhone', 'Version 3.29 iPhone')
rep('>3.28 – REVIEW DRAFT', '>3.29 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.28</span>', '<span class="cv-ver">Version 3.29</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.24</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.28</span>', '<div class="rr"><span class="rv">3.29</span><span class="rd">22 Nov 2026</span><p>Troubleshooter questions 1–4 say exactly who and what</p></div>\n<div class="rr"><span class="rv">3.28</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
