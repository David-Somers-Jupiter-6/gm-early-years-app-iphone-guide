"""Guide 3.30 (from 3.29) – TRIAL (/preview/ only) mock-up. David, 22 Nov: "create mock-ups and improve where needed;
check other questions so that page, question and responses line up". The suggestions from 3.29, built:
 1. A new question 3, "Is this you?" – "Are you the child's mother or primary carer?" – so a partner who answered
    "that is clear" is still found. The Troubleshooter now has seven questions.
 2. Kinder "not sure" on questions 1 and 2 (they check understanding, not a problem): a blue "That is OK" message,
    an amber light instead of red, and on the results "Read more" with a blue "i" instead of a red cross.
 3. Question 5 (Can you use NHS login?): the Tip becomes an action – "Try signing in on the NHS website, then come
    back" with a button that opens the NHS website's log in page in a new tab (same NHS login details).
 4. Answer messages in one style: "That is clear", "You have NHS login", "You can sign in to NHS login" ...
 5. The Checklist questions (c1–c4) also keep the question and answers in the same place on every page (they
    moved on the iPhone SE); the alignment code now handles both sets of questions.
 Page ids: ts1, ts1b, ts1c, ts2, ts3, ts4 (details, with the example), ts5 (link).
usage: python3 make330.py v3.29.html v3.30.html"""
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

t4 = page('ts4').group(0)
NAV = t4[t4.index('<input type="radio" class="nudge-t"'):t4.index('</section>')]
STOP = re.search(r'<svg class="stop-ico".*?</svg>', t4, re.S).group(0)
EX = t4[t4.index('<input type="checkbox" class="ex-t"'):t4.index('</label></div>') + len('</label>')]
OLD = ['ts1', 'ts1b', 'ts2', 'ts3', 'ts4', 'ts5']
IDS = ['ts1', 'ts1b', 'ts1c', 'ts2', 'ts3', 'ts4', 'ts5']
N = len(IDS)
SYS = {'app': ('ts-sys-app', 'GM Early Years App'), 'nhs': ('ts-sys-nhs', 'NHS login'), 'both': ('ts-sys-both', 'NHS login and the App')}

def nav(pid, back, nxt):
    n = NAV.replace('nw-ts4', 'nw-' + pid).replace('href="#ts3"', 'href="#%s"' % back).replace('href="#ts5"', 'href="#%s"' % nxt)
    assert n.count('href="#%s"' % nxt) == 2 and n.count('href="#%s"' % back) == 1, pid
    return n

def stepper(k):
    return '<div class="stepper chk-steps" aria-hidden="true">' + ''.join(
        '<span class="c cur">%d</span>' % (i + 1) if i == k else '<span class="">%d</span>' % (i + 1) for i in range(N)) + '</div>'

def qpage(k, title, system, sub, paras, ask, yes, no, yes_h, no_h, soft=False, extra=''):
    pid = IDS[k]; back = IDS[k - 1] if k else 'ts'; nxt = IDS[k + 1] if k < N - 1 else 'tsum'
    cls, name = SYS[system]
    body = ''.join('<p class="q-why">%s</p>' % p for p in paras)
    if soft:
        no_msg = f'<div class="ans-msg msg-no ok soft" role="status"><span class="ok-ico" aria-hidden="true">i</span><p class="ok-h">{no_h}</p></div>'
    else:
        no_msg = f'<div class="ans-msg msg-no amber stop-msg" role="status"><div class="stop-head">{STOP}<h3>{no_h}</h3></div><p>Tap <strong>Next</strong> to continue.</p></div>'
    return f'''<section class="screen" id="{pid}" data-sec="Section 6 · Troubleshooting" data-title="Troubleshooter · {title}" aria-label="Troubleshooter question {k+1} of {N}">
<div class="scroll">
<div class="pbox has-n">{stepper(k)}<span class="tp-n" aria-hidden="true">{k+1}</span><div class="kicker part">Question {k+1} of {N}</div><h2 id="ts-q{k+1}" tabindex="-1"><span class="vh">Question {k+1} of {N}: </span>{title}</h2></div>
<div class="strip" aria-hidden="true"><div class="strip-row"><span class="ts-sys {cls}">{name}</span><span class="pos">Page X of 50</span></div></div>
<div class="ts-info"><h3 class="h3 ts-sub"><span class="vh">{name}: </span>{sub}</h3>{body}{extra}</div>
<div class="ts-qa"><p class="q-ask" id="ask-{pid}">{ask}</p></div>
<p class="q-hint" id="hint-{pid}">Tap an answer, then tap <strong>Next</strong>.</p>
<div class="radios" role="radiogroup" aria-labelledby="ask-{pid}" aria-describedby="hint-{pid}">
<label class="radio"><input type="radio" class="ans ans-yes" name="ans-{pid}"/><span class="rc" aria-hidden="true"></span><span>{yes}</span></label>
<label class="radio"><input type="radio" class="ans ans-no" name="ans-{pid}"/><span class="rc" aria-hidden="true"></span><span>{no}</span></label>
</div>
<p class="need-ans" role="status" aria-live="polite"><span class="ni" aria-hidden="true">i</span><span>Please tap an answer, then tap <strong>Next</strong>.</span></p>
<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">{yes_h}</p></div>
{no_msg}
</div>
{nav(pid, back, nxt)}</section>
'''

TIP_I = '<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.6 10.8c.6.5 1 1.2 1.1 2.2h5c.1-1 .5-1.7 1.1-2.2A6 6 0 0012 3z"/></svg>'
EXT = '<svg aria-hidden="true" viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 3h6v6M17 3l-8 8M15 12v4a1 1 0 01-1 1H4a1 1 0 01-1-1V6a1 1 0 011-1h4"/></svg>'
TRY = ('\n<div class="ts-tip"><span class="ts-tip-i">' + TIP_I + '</span><div><p><strong>Not sure?</strong> Try it on the NHS website.</p>'
       '<a class="ts-try" href="https://www.nhs.uk/nhs-app/account/" target="_blank" rel="noopener">Try signing in' + EXT + '<span class="vh"> (opens the NHS website in a new tab)</span></a></div></div>')

Q = [
 ('Who is the account for?', 'app', 'The child’s mother or primary carer',
  ['Your Health Visiting team sets up the GM Early Years App account for the <strong>child’s mother or primary carer</strong>.'],
  'Is it clear that the account is for the child’s mother or primary carer?', 'Yes, that is clear', 'No, I’m not sure',
  'That is clear', 'That is OK. We will help.', True),
 ('Who can sign in?', 'app', 'Only the child’s mother or primary carer',
  ['A partner or relative <strong>cannot</strong> sign in for them.', 'In this guide, we call this person the <strong>account holder</strong>.'],
  'Is it clear that only the child’s mother or primary carer can sign in?', 'Yes, that is clear', 'No, I’m not sure',
  'That is clear', 'That is OK. We will help.', True),
 ('Is this you?', 'app', 'The person signing in',
  ['Answer for <strong>yourself</strong>, the person who will sign in to the App.'],
  'Are you the child’s mother or primary carer?', 'Yes, that is me', 'No, I am a partner or relative',
  'You are the account holder', 'Only they can sign in', False),
 ('Do you have NHS login?', 'nhs', 'You need an NHS login account',
  ['The GM Early Years App uses an <strong>NHS login</strong> account to sign you in.'],
  'Do you have an NHS login account?', 'Yes, I have NHS login', 'No, or I’m not sure',
  'You have NHS login', 'You need NHS login first', False),
 ('Can you use NHS login?', 'nhs', 'Can you access NHS login?',
  ['You sign in to NHS login with your <strong>email address</strong> and <strong>password</strong>.'],
  'Can you sign in to your NHS login account?', 'Yes, I can sign in', 'No, I cannot sign in',
  'You can sign in to NHS login', 'NHS login needs to work first', False),
 ('Do your details match?', 'both', 'Exactly the same in both',
  ['Your <strong>email address</strong> and <strong>mobile number</strong> must be the same in NHS login and the App.'],
  'Are your details the same in both?', 'Yes, my details are the same', 'No, or I’m not sure',
  'Your details match', 'Your details need to match', False),
 ('Has your link arrived?', 'app', 'Sent to you by text message',
  ['Your Health Visiting team sends an <strong>Activation Link</strong> by text to the mobile number on your App account.'],
  'Have you received your Activation Link?', 'Yes, I have it', 'No, it has not arrived',
  'You have your Activation Link', 'Your link has not arrived', False),
]
NEW = ''.join(qpage(k, *q, extra=(('\n' + EX) if k == 5 else TRY if k == 4 else '')) for k, q in enumerate(Q))
for pid in OLD:
    m = page(pid); s = s[:m.start()] + s[m.end():]
m = page('ts'); s = s[:m.end()] + NEW + s[m.end():]
assert s.count('id="ts-ex"') == 1

# start page
m = page('ts'); blk = m.group(0)
blk = blk.replace('Answer <strong>6 quick questions</strong>', 'Answer <strong>7 quick questions</strong>')
blk = re.sub(r'<ol class="cq">.*?</ol>', '<ol class="cq">' + ''.join('<li><span aria-hidden="true">%d</span>%s</li>' % (i + 1, q[0]) for i, q in enumerate(Q)) + '</ol>', blk, flags=re.S)
blk = blk.replace('It takes about a minute.', 'It takes a minute or two.')
assert '7 quick questions' in blk
s = s[:m.start()] + blk + s[m.end():]

# results
m = page('tsum'); blk = m.group(0)
CHEV = re.search(r'Get help(<svg.*?</svg>)</a>', blk, re.S).group(1)
ROWS = [('Who the account is for', 'That is clear', 'Read who the account is for', 'acct', True),
        ('Who can sign in', 'That is clear', 'Read who can sign in', 's4-2', True),
        ('Account holder', 'You are the account holder', 'Only they can sign in', 's4-2', False),
        ('NHS login account', 'You have NHS login', 'You do not have NHS login yet', 's4-setup', False),
        ('Signing in to NHS login', 'You can sign in', 'You cannot sign in yet', 's4-cannot', False),
        ('Account details', 'Your details match', 'Your details may not match', 's4-problems', False),
        ('Activation Link', 'You have your Activation Link', 'Your link has not arrived', 's4-activation', False)]
def li(k, l, y, n, h, soft):
    ico = '<span class="sum-ico n soft" aria-hidden="true">i</span>' if soft else '<span class="sum-ico n" aria-hidden="true">✗</span>'
    btn = ('Read more' if soft else 'Get help')
    return (f'<li class="r{k+1}"><div class="st st-yes"><span class="sum-ico y" aria-hidden="true">✓</span><div class="sum-t"><p class="sum-l">{l}</p><p class="sum-s">{y}</p></div></div>'
            f'<div class="st st-no{" soft" if soft else ""}">{ico}<div class="sum-t"><p class="sum-l">{l}</p><p class="sum-s">{n}</p></div><a class="sum-help" href="#{h}">{btn}{CHEV}</a></div>'
            f'<div class="st st-un"><span class="sum-ico u" aria-hidden="true">–</span><div class="sum-t"><p class="sum-l">{l}</p><p class="sum-s">Not answered yet</p></div><a class="sum-help" href="#{IDS[k]}">Answer{CHEV}</a></div></li>')
blk = re.sub(r'<ul class="sum-list">.*?</ul>', '<ul class="sum-list">\n' + ''.join(li(k, *r) for k, r in enumerate(ROWS)) + '\n</ul>', blk, flags=re.S)
blk = re.sub(r'<div class="stepper chk-steps" aria-hidden="true">.*?</div>', '<div class="stepper chk-steps" aria-hidden="true">' + ''.join('<span class="">%d</span>' % (i + 1) for i in range(N)) + '</div>', blk, count=1, flags=re.S)
blk = blk.replace('All six checks are done.', 'All seven checks are done.')
s = s[:m.start()] + blk + s[m.end():]

# ---- CSS lists and the results logic
n1 = s.count('#ts1,#ts1b,#ts2,'); assert n1 >= 10, n1
s = s.replace('#ts1,#ts1b,#ts2,', '#ts1,#ts1b,#ts1c,#ts2,')
s = re.sub(r'\n(?:body:has\(#ts(?:1b|[1-5]) [^\n]*|body:not\(:has\(#ts(?:1b|[1-5]) [^\n]*|body:has\(#ts1 \.ans-yes:checked\):has[^\n]*)(?=\n)', '', s)
assert 'body:has(#ts5 .ans-no:checked)' not in s and 'body:has(#ts1b .ans-no:checked)' not in s
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
# amber light (not red) for "not sure" on the two understanding questions
for i, t in ((1, 'ts1'), (2, 'ts1b')):
    L.append(f'body:has(#{t} .ans-no:checked) #app .chk-steps span:nth-child({i}).bad{{background:#ffb81c!important;border-color:#ffb81c!important;color:#1d2b36!important}}')
CSS = """/* 3.30 Troubleshooter: seven questions; kinder "not sure"; try signing in */
""" + '\n'.join(L) + """
#app .ans-msg.ok.soft{background:#e8f1fb;border-left-color:#005eb8}
#app .ans-msg.ok.soft .ok-ico{background:#005eb8;font-family:Georgia,serif;font-style:italic}
#app .ans-msg.ok.soft .ok-h{color:#003d78}
#app #tsum .sum-ico.soft{background:#005eb8!important;color:#fff!important;font-family:Georgia,serif;font-style:italic}
#app #tsum .st-no.soft{border-color:#b7d2ee!important;background:#f3f8fd!important}
@media (prefers-color-scheme:dark){#app .ans-msg.ok.soft{background:#1d3046}#app .ans-msg.ok.soft .ok-h{color:#bcd9ff}#app #tsum .st-no.soft{background:#18293b!important;border-color:#2c4a6b!important}}
#app #ts3 .ts-tip{display:flex;gap:8px;align-items:flex-start;margin:6px 0 0;padding:8px 12px;border-radius:12px;background:#e8f1fb;border-left:4px solid #005eb8;color:var(--ink)}
#app #ts3 .ts-tip p{margin:0 0 6px;font-size:16px;line-height:1.35}
#app #ts3 .ts-tip-i{flex:0 0 20px;color:#005eb8;margin-top:1px}
#app #ts3 .ts-try{display:inline-flex;align-items:center;gap:6px;min-height:38px;padding:6px 14px;border-radius:999px;background:#005eb8;color:#fff;font:700 15px/1.2 var(--font-body);text-decoration:none}
#app #ts3 .ts-try:active{transform:scale(.97);filter:brightness(.94)}
@media (prefers-color-scheme:dark){#app #ts3 .ts-tip{background:#1d3046}#app #ts3 .ts-tip-i{color:#7fb8ff}}
@media screen and (max-height:600px){#app :is(#c1,#c2,#c3,#c4) .ans-msg{margin-top:6px!important}#app :is(#c1,#c2,#c3,#c4) .q-ask{margin-top:8px!important}}
@media screen and (max-height:640px){#app #ts3 .ts-tip{padding:6px 10px}#app #ts3 .ts-tip p{margin-bottom:4px;font-size:15px}#app #ts3 .ts-try{min-height:34px;padding:4px 12px}}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}')

# ---- JS: lists, and align the Checklist questions too
n2 = s.count("'ts1','ts1b','ts2','ts3','ts4','ts5'"); assert n2 == 4, n2
s = s.replace("'ts1','ts1b','ts2','ts3','ts4','ts5'", "'ts1','ts1b','ts1c','ts2','ts3','ts4','ts5'")
old_align = s[s.index('  function tsAlign(){'):s.index("  d.addEventListener('touchstart'")]
new_align = """  var CHQ=['c1','c2','c3','c4'];
  function tsAlign(){ var grp=TSQ.indexOf(cur&&cur.id)>=0?[TSQ,['.ts-info','.ts-qa']]:CHQ.indexOf(cur&&cur.id)>=0?[CHQ,['.q-why','.q-ask']]:null; if(!grp) return;
    var ps=grp[0].map(function(id){ return byId[id]; }).filter(Boolean), w=cur.getBoundingClientRect().width, saved=[];
    ps.forEach(function(p,i){ grp[1].forEach(function(c){ var e=p.querySelector(c); if(e) e.style.removeProperty('min-height'); });
      saved[i]=p.getAttribute('style'); if(p!==cur) p.style.cssText+=';display:flex!important;position:absolute;visibility:hidden;left:0;top:0;width:'+w+'px'; });
    grp[1].forEach(function(c){ var m=0;
      ps.forEach(function(p){ var e=p.querySelector(c); if(e) m=Math.max(m,e.getBoundingClientRect().height); });
      ps.forEach(function(p){ var e=p.querySelector(c); if(e) e.style.setProperty('min-height',Math.ceil(m)+'px','important'); }); });
    ps.forEach(function(p,i){ if(p===cur) return; if(saved[i]===null) p.removeAttribute('style'); else p.setAttribute('style',saved[i]); });
  }
"""
s = s.replace(old_align, new_align)

# validator: allow the NHS website's log in page
v = open(__file__.rsplit('/', 1)[0] + '/validate_site.py', encoding='utf-8').read()
if 'www\\.nhs\\.uk' not in v:
    v2 = v.replace(r"(help|settings)\.login\.nhs\.uk|maps\.apple\.com", r"(help|settings)\.login\.nhs\.uk|www\.nhs\.uk/nhs-app/account/|maps\.apple\.com")
    v2 = v2.replace("'external links go to NHS login, Apple Maps, EASS or the guide website only'", "'external links go to NHS login, the NHS website log in page, Apple Maps, EASS or the guide website only'")
    assert v2 != v; open(__file__.rsplit('/', 1)[0] + '/validate_site.py', 'w', encoding='utf-8').write(v2)

# ---- counters
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[-1] == 'search'; T = len(ids) - 1; assert T == 94, T
sec6 = [i for i in ids if 'data-sec="Section 6 · Troubleshooting"' in page(i).group(0)[:400]]
assert len(sec6) == 50 and sec6[:10] == ['s4', 'ts'] + IDS + ['tsum'], sec6[:10]
def put(pid, new):
    global s
    m = page(pid); s = s[:m.start()] + new + s[m.end():]
for n, pid in enumerate(sec6, 1):
    blk = page(pid).group(0)
    new = re.sub(r'<span class="pos">Page (?:\d+|X) of (?:49|50)</span>', f'<span class="pos">Page {n} of 50</span>', blk, count=1)
    assert f'Page {n} of 50' in new, pid; put(pid, new)
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: put(pid, new)
assert 'Page X of' not in s

rep('Carer role v3.29', 'Carer role v3.30'); rep('Version 3.29 iPhone', 'Version 3.30 iPhone')
rep('>3.29 – REVIEW DRAFT', '>3.30 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.29</span>', '<span class="cv-ver">Version 3.30</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.25</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.29</span>', '<div class="rr"><span class="rv">3.30</span><span class="rd">22 Nov 2026</span><p>Troubleshooter: seven questions, kinder “not sure”, Try signing in; Checklist questions line up</p></div>\n<div class="rr"><span class="rv">3.29</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, 'pages', T)
