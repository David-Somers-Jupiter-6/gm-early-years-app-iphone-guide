"""Guide 3.28 (from 3.27) – TRIAL (/preview/ only) mock-up. David, 21 Nov:
 1. Introduction: back to the original (not the conversation), with "You are not alone, and it is not your fault."
    on its own line.
 2. Troubleshooter: six questions, in David's order (GM Early Years App account, who can sign in, NHS login account,
    NHS login sign in, details match, link arrived), with short titles that fit on one line. Which system each
    question is about (GM Early Years App / NHS login / both) shows in colour on the line under the title box,
    instead of in the title.
 3. Clearer wording on each question page: a subheading that gives the answer, two short plain sentences, then the
    question.
 New page ts1b (Who can sign in?); the old ts2 "Who can sign in?" becomes "Do you have NHS login?". Results have
 six rows. Page ids: ts1, ts1b, ts2, ts3, ts4 (details, with the example), ts5 (link).
usage: python3 make328.py v3.27.html v3.28.html  (reads v3.25 for the original Introduction)"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
s325 = open(src.replace('v3.27', 'v3.25'), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def page(pid, txt=None):
    t = s if txt is None else txt
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>\n?' % re.escape(pid), t, re.S)
    assert m, pid
    return m

# ---- 1. Introduction: original, with the reassurance on its own line
intro = page('intro', s325).group(0)
a = '<p class="lead iv-lead">Having trouble signing in to the GM Early Years App? <strong>You are not alone, and it is not your fault.</strong></p>'
assert intro.count(a) == 1
intro = intro.replace(a, '<p class="lead iv-lead">Having trouble signing in to the GM Early Years App?</p>\n<p class="iv-alone">You are not alone, and it is not your fault.</p>')
m = page('intro'); s = s[:m.start()] + intro + s[m.end():]

# ---- 2./3. Troubleshooter questions
t4 = page('ts4').group(0)
NAV = t4[t4.index('<input type="radio" class="nudge-t"'):t4.index('</section>')]
STOP = re.search(r'<svg class="stop-ico".*?</svg>', t4, re.S).group(0)
EX = t4[t4.index('<input type="checkbox" class="ex-t"'):t4.index('</label></div>') + len('</label>')]
IDS = ['ts1', 'ts1b', 'ts2', 'ts3', 'ts4', 'ts5']
SYS = {'app': ('ts-sys-app', 'GM Early Years App'), 'nhs': ('ts-sys-nhs', 'NHS login'), 'both': ('ts-sys-both', 'NHS login and the App')}

def nav(pid, back, nxt):
    n = re.sub(r'nw-ts4', 'nw-' + pid, NAV)
    n = n.replace('href="#ts3"', 'href="#%s"' % back).replace('href="#ts5"', 'href="#%s"' % nxt)
    assert n.count('href="#%s"' % nxt) == 2 and n.count('href="#%s"' % back) == 1, pid
    return n

def stepper(k):
    return '<div class="stepper chk-steps" aria-hidden="true">' + ''.join(
        '<span class="c cur">%d</span>' % (i + 1) if i == k else '<span class="">%d</span>' % (i + 1) for i in range(6)) + '</div>'

def qpage(k, title, system, sub, paras, ask, yes, no, yes_h, no_h, extra=''):
    pid = IDS[k]; back = IDS[k - 1] if k else 'ts'; nxt = IDS[k + 1] if k < 5 else 'tsum'
    cls, name = SYS[system]
    after = 'continue to question %d' % (k + 2) if k < 5 else 'see your results'
    body = ''.join('<p class="q-why">%s</p>' % p for p in paras)
    return f'''<section class="screen" id="{pid}" data-sec="Section 6 · Troubleshooting" data-title="Troubleshooter · {title}" aria-label="Troubleshooter question {k+1} of 6">
<div class="scroll">
<div class="pbox has-n">{stepper(k)}<span class="tp-n" aria-hidden="true">{k+1}</span><div class="kicker part">Question {k+1} of 6</div><h2 id="ts-q{k+1}" tabindex="-1"><span class="vh">Question {k+1} of 6: </span>{title}</h2></div>
<div class="strip" aria-hidden="true"><div class="strip-row"><span class="ts-sys {cls}">{name}</span><span class="pos">Page X of 49</span></div></div>
<div class="ts-info"><h3 class="h3 ts-sub"><span class="vh">{name}: </span>{sub}</h3>{body}{extra}</div>
<div class="ts-qa"><p class="q-ask" id="ask-{pid}">{ask}</p></div>
<p class="q-hint" id="hint-{pid}">Tap an answer, then tap <strong>Next</strong>.</p>
<div class="radios" role="radiogroup" aria-labelledby="ask-{pid}" aria-describedby="hint-{pid}">
<label class="radio"><input type="radio" class="ans ans-yes" name="ans-{pid}"/><span class="rc" aria-hidden="true"></span><span>{yes}</span></label>
<label class="radio"><input type="radio" class="ans ans-no" name="ans-{pid}"/><span class="rc" aria-hidden="true"></span><span>{no}</span></label>
</div>
<p class="need-ans" role="status" aria-live="polite"><span class="ni" aria-hidden="true">i</span><span>Please tap an answer, then tap <strong>Next</strong>.</span></p>
<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">{yes_h}</p><p>Tap <strong>Next</strong> to {after}.</p></div>
<div class="ans-msg msg-no amber stop-msg" role="status"><div class="stop-head">{STOP}<h3>{no_h}</h3></div><p>Tap <strong>Next</strong> to {'continue' if k < 5 else 'see your results'}.</p></div>
</div>
{nav(pid, back, nxt)}</section>
'''

Q = [
 ('Who is the account for?', 'app', 'The child’s mother or primary carer',
  ['Your Health Visiting team sets up the GM Early Years App account for the child’s mother or primary carer.',
   'In this guide, we call this person the <strong>account holder</strong>.'],
  'Are you the child’s mother or primary carer?', 'Yes, I am the account holder', 'No, I am a partner or relative',
  'You are the account holder', 'Only the account holder'),
 ('Who can sign in?', 'app', 'Only the account holder',
  ['They sign in with their <strong>own NHS login</strong>.',
   'A partner or relative <strong>cannot</strong> sign in for them.'],
  'Will you sign in with your own NHS login?', 'Yes, with my own NHS login', 'No, or I’m not sure',
  'You will use your own NHS login', 'Only your own NHS login works'),
 ('Do you have NHS login?', 'nhs', 'You need an NHS login account',
  ['NHS login is a free NHS account. You may already use it for the NHS App.',
   'The GM Early Years App uses it to sign you in.'],
  'Do you have an NHS login account?', 'Yes, I have NHS login', 'No, or I’m not sure',
  'You have NHS login', 'You need NHS login first'),
 ('Can you use NHS login?', 'nhs', 'With your email address and password',
  ['You sign in to the App with your NHS login <strong>email address</strong> and <strong>password</strong>.',
   'Check that they work in NHS login first.'],
  'Can you sign in to NHS login?', 'Yes, I can sign in', 'No, I cannot sign in',
  'You can sign in to NHS login', 'NHS login needs to work first'),
 ('Do your details match?', 'both', 'Exactly the same in both',
  ['Your <strong>email address</strong> and <strong>mobile number</strong> must be the same in NHS login and the App.'],
  'Are your details the same in both?', 'Yes, my details are the same', 'No, or I’m not sure',
  'Your details match', 'Your details need to match'),
 ('Has your link arrived?', 'app', 'Sent to you by text message',
  ['Your Health Visiting team sends an <strong>Activation Link</strong> by text to the mobile number on your App account.'],
  'Have you received your Activation Link?', 'Yes, I have it', 'No, it has not arrived',
  'You have your Activation Link', 'Your link has not arrived'),
]
NEW = ''.join(qpage(k, *q, extra=(('\n' + EX) if k == 4 else '')) for k, q in enumerate(Q))
for pid in ['ts1', 'ts2', 'ts3', 'ts4', 'ts5']:
    m = page(pid); s = s[:m.start()] + s[m.end():]
m = page('ts'); s = s[:m.end()] + NEW + s[m.end():]
assert s.count('id="ts-ex"') == 1

# start page
m = page('ts'); blk = m.group(0)
blk = blk.replace('Answer <strong>5 quick questions</strong>', 'Answer <strong>6 quick questions</strong>')
blk = re.sub(r'<ol class="cq">.*?</ol>', '<ol class="cq">' + ''.join('<li><span aria-hidden="true">%d</span>%s</li>' % (i + 1, q[0]) for i, q in enumerate(Q)) + '</ol>', blk, flags=re.S)
assert '6 quick questions' in blk
s = s[:m.start()] + blk + s[m.end():]

# results
m = page('tsum'); blk = m.group(0)
CHEV = re.search(r'Get help(<svg.*?</svg>)</a>', blk, re.S).group(1)
ROWS = [('Account holder', 'You are the account holder', 'Only the account holder can sign in', 's4-2'),
        ('Your own NHS login', 'You will use your own NHS login', 'Only your own NHS login works', 's4-1b'),
        ('NHS login account', 'You have NHS login', 'You do not have NHS login yet', 's4-setup'),
        ('Signing in to NHS login', 'You can sign in', 'You cannot sign in yet', 's4-cannot'),
        ('Account details', 'Your details match', 'Your details may not match', 's4-problems'),
        ('Activation Link', 'You have your Activation Link', 'Your link has not arrived', 's4-activation')]
lis = ''.join(f'<li class="r{k+1}"><div class="st st-yes"><span class="sum-ico y" aria-hidden="true">✓</span><div class="sum-t"><p class="sum-l">{l}</p><p class="sum-s">{y}</p></div></div>'
              f'<div class="st st-no"><span class="sum-ico n" aria-hidden="true">✗</span><div class="sum-t"><p class="sum-l">{l}</p><p class="sum-s">{n}</p></div><a class="sum-help" href="#{h}">Get help{CHEV}</a></div>'
              f'<div class="st st-un"><span class="sum-ico u" aria-hidden="true">–</span><div class="sum-t"><p class="sum-l">{l}</p><p class="sum-s">Not answered yet</p></div><a class="sum-help" href="#{IDS[k]}">Answer{CHEV}</a></div></li>'
              for k, (l, y, n, h) in enumerate(ROWS))
blk = re.sub(r'<ul class="sum-list">.*?</ul>', '<ul class="sum-list">\n' + lis + '\n</ul>', blk, flags=re.S)
blk = re.sub(r'<div class="stepper chk-steps" aria-hidden="true">.*?</div>', '<div class="stepper chk-steps" aria-hidden="true">' + ''.join('<span class="">%d</span>' % (i + 1) for i in range(6)) + '</div>', blk, count=1, flags=re.S)
blk = blk.replace('All five checks are done.', 'All six checks are done.')
s = s[:m.start()] + blk + s[m.end():]

# ---- CSS: include the new page; regenerate the results logic for six questions
n1 = s.count('#ts1,#ts2,'); assert n1 >= 10, n1
s = s.replace('#ts1,#ts2,', '#ts1,#ts1b,#ts2,')
before = len(s)
s = re.sub(r'\n(?:body:has\(#ts[1-5] [^\n]*|body:not\(:has\(#ts[1-5] [^\n]*|body:has\(#ts1 \.ans-yes:checked\):has[^\n]*)(?=\n)', '', s)
assert 'body:has(#ts5 .ans-no:checked)' not in s and len(s) < before
ALL = ''.join(':has(#%s .ans-yes:checked)' % t for t in IDS)
L = []
for k, t in enumerate(IDS, 1):
    L += [f'body:has(#{t} .ans-yes:checked) #tsum .r{k} .st-yes{{display:flex}}',
          f'body:has(#{t} .ans-no:checked) #tsum .r{k} .st-no{{display:flex}}',
          f'body:not(:has(#{t} .ans:checked)) #tsum .r{k} .st-un{{display:flex}}',
          f'body:has(#{t} .ans-no:checked) #app #tsum .sum-no{{display:flex}}',
          f'body:not(:has(#{t} .ans:checked)) #app #tsum .sum-un{{display:flex}}',
          f'body:has(#{t} .ans-no:checked) #tsum .go-yes{{display:none!important}}',
          f'body:has(#{t} .ans-no:checked) #tsum .go-no{{display:inline-flex!important}}']
for t in IDS:
    L += [f'body:has(#{t} .ans-no:checked) #app #tsum .sum-un{{display:none}}',
          f'body:has(#{t} .ans-no:checked) #tsum .res-b{{background:#ffb81c!important;color:#1d2b36!important}}',
          f'body:has(#{t} .ans-no:checked) #tsum .res-b .rb-no{{display:block}}',
          f'body:has(#{t} .ans-no:checked) #tsum .res-b .rb-un{{display:none}}']
L += [f'body{ALL} #app #tsum .sum-ok{{display:flex}}',
      f'body{ALL} #app #tsum .go-yes{{background:#00703c!important;border-color:#00703c!important;color:#fff}}',
      f'body{ALL} #tsum .res-b{{background:#00703c!important;color:#fff!important}}', f'body{ALL} #tsum .res-b .rb-ok{{display:block}}', f'body{ALL} #tsum .res-b .rb-un{{display:none}}']
CSS = """/* 3.28 Troubleshooter: six questions; which system each question is about; original Introduction */
""" + '\n'.join(L) + """
#app .strip .ts-sys{font-weight:800}
#app .strip .ts-sys-app{color:#a3124d}
#app .strip .ts-sys-nhs{color:#005eb8}
#app .strip .ts-sys-both{color:#4b2e83}
@media (prefers-color-scheme:dark){#app .strip .ts-sys-app{color:#ff8fb8}#app .strip .ts-sys-nhs{color:#7fb8ff}#app .strip .ts-sys-both{color:#c3a9ff}}
#app #intro .iv-alone{margin:0 0 12px;font:800 19px/1.35 var(--font-head);color:var(--ink)}
@media screen and (max-height:700px){#app #intro .iv-alone{font-size:18px;margin-bottom:8px}}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# ---- JS lists
n2 = s.count("'ts1','ts2','ts3','ts4','ts5'"); assert n2 == 4, n2
s = s.replace("'ts1','ts2','ts3','ts4','ts5'", "'ts1','ts1b','ts2','ts3','ts4','ts5'")

# ---- counters
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[-1] == 'search'; T = len(ids) - 1; assert T == 93, T
sec6 = [i for i in ids if 'data-sec="Section 6 · Troubleshooting"' in page(i).group(0)[:400]]
assert len(sec6) == 49 and sec6[:9] == ['s4', 'ts', 'ts1', 'ts1b', 'ts2', 'ts3', 'ts4', 'ts5', 'tsum'], sec6[:9]
def put(pid, new):
    global s
    m = page(pid); s = s[:m.start()] + new + s[m.end():]
for n, pid in enumerate(sec6, 1):
    blk = page(pid).group(0)
    new = re.sub(r'<span class="pos">Page (?:\d+|X) of (?:48|49)</span>', f'<span class="pos">Page {n} of 49</span>', blk, count=1)
    assert f'Page {n} of 49' in new, pid; put(pid, new)
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: put(pid, new)
assert 'Page X of' not in s

rep('Carer role v3.27', 'Carer role v3.28'); rep('Version 3.27 iPhone', 'Version 3.28 iPhone')
rep('>3.27 – REVIEW DRAFT', '>3.28 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.27</span>', '<span class="cv-ver">Version 3.28</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.23</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.27</span>', '<div class="rr"><span class="rv">3.28</span><span class="rd">21 Nov 2026</span><p>Troubleshooter: six questions, short titles, clearer wording; original Introduction</p></div>\n<div class="rr"><span class="rv">3.27</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, 'pages', T)
