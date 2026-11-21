"""Guide 3.23 (from 3.22) – TRIAL (/preview/ only). David, 21 Nov: a Troubleshooter at the top of Troubleshooting
that brings together About your account, Your account details and the Checklist, in the checklist format (one
question per page, Yes / No, the progress LEDs, a summary at the end). If it works better, it can later replace
Sections 3 and 4.
 - Troubleshooting menu: new first card "Troubleshooter" in the App colours, "Find out what is stopping you".
   The "Help from" lines on the cards give way when the menu would not fit (smaller iPhones).
 - ts    Troubleshooter (start page): 5 quick questions, Begin.
 - ts1   Who has the account?      Are you the child's mother or primary carer?        No -> A partner is signing in
 - ts2   Who can sign in?          Do you have your own NHS login account?              No -> Set up NHS login
 - ts3   Can you use NHS login?    Can you sign in to your NHS login account?           No -> Cannot sign in
 - ts4   Do your details match?    with the account details example: a small preview,
                                   tap to see the whole example                         No -> Details do not match
 - ts5   Has your link arrived?    Have you received an Activation Link?                No -> Activation Link issues
 - tsum  Your results: a tick or a Get help button for each; all Yes -> Next to Signing in; any No -> Done.
 Asking about NHS login and matching details here means the Checklist questions are not asked twice.
 Begin starts with a clean set of answers (Checklist answers are kept, and the other way round).
usage: python3 make323.py v3.22.html v3.23.html"""
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

TS = ['ts1', 'ts2', 'ts3', 'ts4', 'ts5']
c2 = page('c2').group(0)
NAV_Q = c2[c2.index('<input type="radio" class="nudge-t"'):c2.index('</section>')]
STOP_SVG = re.search(r'<svg class="stop-ico".*?</svg>', c2, re.S).group(0)
ARROW_N = '<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def nav_q(pid, back, nxt):
    n = NAV_Q.replace('nw-c2', 'nw-' + pid).replace('href="#c1"', 'href="#%s"' % back).replace('href="#c3"', 'href="#%s"' % nxt)
    assert n.count('href="#%s"' % nxt) == 2, pid
    return n

def stepper(k):
    return '<div class="stepper chk-steps" aria-hidden="true">' + ''.join(
        '<span class="c cur">%d</span>' % (i + 1) if i == k else '<span class="">%d</span>' % (i + 1) for i in range(5)) + '</div>'

def question(k, title, why, ask, yes, no, yes_h, no_h, extra=''):
    pid = TS[k]; nxt = TS[k + 1] if k < 4 else 'tsum'; back = TS[k - 1] if k else 'ts'
    after = 'continue to question %d' % (k + 2) if k < 4 else 'see your results'
    after_no = 'continue' if k < 4 else 'see your results'  # kept short so the page fits
    return f'''<section class="screen" id="{pid}" data-sec="Section 6 · Troubleshooting" data-title="Troubleshooter · {title}" aria-label="Troubleshooter question {k+1} of 5">
<div class="scroll">
<div class="pbox has-n">{stepper(k)}<span class="tp-n" aria-hidden="true">{k+1}</span><div class="kicker part">Question {k+1} of 5</div><h2 id="ts-q{k+1}" tabindex="-1"><span class="vh">Question {k+1} of 5: </span>{title}</h2></div>
<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · Troubleshooting</span><span class="pos">Page X of 48</span></div></div>
<p class="q-why">{why}</p>
{extra}<p class="q-ask" id="ask-{pid}">{ask}</p>
<p class="q-hint fit-opt" id="hint-{pid}">Tap an answer, then tap <strong>Next</strong>.</p>
<div class="radios" role="radiogroup" aria-labelledby="ask-{pid}" aria-describedby="hint-{pid}">
<label class="radio"><input type="radio" class="ans ans-yes" name="ans-{pid}"/><span class="rc" aria-hidden="true"></span><span>{yes}</span></label>
<label class="radio"><input type="radio" class="ans ans-no" name="ans-{pid}"/><span class="rc" aria-hidden="true"></span><span>{no}</span></label>
</div>
<p class="need-ans" role="status" aria-live="polite"><span class="ni" aria-hidden="true">i</span><span>Please tap an answer, then tap <strong>Next</strong>.</span></p>
<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">{yes_h}</p><p>Tap <strong>Next</strong> to {after}.</p></div>
<div class="ans-msg msg-no amber stop-msg" role="status"><div class="stop-head">{STOP_SVG}<h3>{no_h}</h3></div><p>Tap <strong>Next</strong> to {after_no}.</p></div>
</div>
{nav_q(pid, back, nxt)}</section>
'''

# --- the account details example (from Your account details), as a small preview that opens in full
nhs = page('nhs').group(0)
EXOUT = re.search(r'<ul class="ex-out">.*?</ul>', nhs, re.S).group(0)
EXW = re.search(r'<div class="exw".*?</div></div></div>', nhs, re.S).group(0)
assert EXW.count('class="exc ') == 2
ZOOM = '<svg aria-hidden="true" viewBox="0 0 20 20" width="16" height="16"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12.6 12.6L17 17M8.5 6v5M6 8.5h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
EXAMPLE = (f'<input type="checkbox" class="ex-t" id="ts-ex" aria-label="Show the whole example of matching details"/>'
           f'<label class="ex-peek" for="ts-ex"><span class="ex-pv" aria-hidden="true">{EXW.replace(" role=\"img\"", "")}</span>'
           f'<span class="ex-tap">{ZOOM}Tap to see an example</span></label>\n'
           f'<label class="ex-full" for="ts-ex"><span class="ex-box"><span class="ex-bh">Example: the same details in both</span>{EXW}{EXOUT}'
           f'<span class="ex-close">Tap anywhere to close</span></span></label>\n')

Q = [
    question(0, 'Who has the account?',
             'Your Health Visiting team sets up a GM Early Years App account for the <strong>child’s mother</strong> or <strong>primary carer</strong>. We call this person the <strong>account holder</strong>.',
             'Are you the child’s mother or primary carer?',
             'Yes, I am the account holder', 'No, I am a partner or another family member',
             'You are the account holder', 'Only the account holder can sign in'),
    question(1, 'Who can sign in?',
             'Only the <strong>account holder</strong> can sign in, with the <strong>email address</strong> and <strong>password</strong> of their own NHS login. A partner or family member <strong>cannot</strong> sign in to it.',
             'Do you have your own NHS login account?',
             'Yes, I have my own NHS login', 'No, I have not set up NHS login',
             'You have your own NHS login', 'You need your own NHS login first'),
    question(2, 'Can you use NHS login?',
             'You will sign in to the App with your NHS login <strong>email address</strong> and <strong>password</strong>.',
             'Can you sign in to your NHS login account?',
             'Yes, I can sign in to my NHS login', 'No, I cannot sign in to my NHS login',
             'You can sign in to NHS login', 'You need to be able to sign in to NHS login'),
    question(3, 'Do your details match?',
             'Your details must be <strong>exactly the same</strong> in <strong>NHS login</strong> and the <strong>GM Early Years App</strong>.',
             'Are your email address and mobile number the same in both?',
             'Yes, my details are the same', 'No, they are different, or I’m not sure',
             'Your details match', 'Your details need to match',
             extra=EXAMPLE),
    question(4, 'Has your link arrived?',
             'Your Health Visiting team sends the <strong>Activation Link</strong> by text message to the <strong>mobile number</strong> on your App account.',
             'Have you received an Activation Link?',
             'Yes, I have my Activation Link', 'No, I have not received an Activation Link',
             'You have your Activation Link', 'Your Activation Link has not arrived'),
]

# --- start page
s2 = page('s2').group(0)
NAV_S2 = s2[s2.index('<nav class="bnav"'):s2.index('</section>')]
nav_start = NAV_S2.replace('href="#nhs"', 'href="#s4"').replace('href="#c1"', 'href="#ts1"')
assert 'href="#ts1"' in nav_start
CLIP = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M8.5 12.5l2.2 2.2 4.8-4.8"/></svg>'
START = f'''<section class="screen" id="ts" data-sec="Section 6 · Troubleshooting" data-title="Troubleshooter" data-next="Begin" aria-label="Troubleshooter">
<div class="scroll">
<div class="pbox gm-icon"><span class="gm-eyi" aria-hidden="true">{CLIP}</span><h2 class="h2" tabindex="-1">Troubleshooter</h2></div>
<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · Troubleshooting</span><span class="pos">Page X of 48</span></div></div>
<p class="lead cq-lead">Answer <strong>5 quick questions</strong> about your account. At the end, you will see what is stopping you, and what to do next.</p>
<ol class="cq"><li><span aria-hidden="true">1</span>Who has the account?</li><li><span aria-hidden="true">2</span>Who can sign in?</li><li><span aria-hidden="true">3</span>Can you use NHS login?</li><li><span aria-hidden="true">4</span>Do your details match?</li><li><span aria-hidden="true">5</span>Has your link arrived?</li></ol>
<p class="cq-end">Answer <strong>Yes</strong> or <strong>No</strong>. It takes about a minute.</p>
</div>
{nav_start}</section>
'''

# --- results page (from the checklist summary)
sm = page('sum').group(0)
CHEV = re.search(r'<a class="sum-help" href="#s4-setup">Get help(<svg.*?</svg>)</a>', sm, re.S).group(1)
def row(k, label, yes_s, no_s, help_id):
    return (f'<li class="r{k+1}"><div class="st st-yes"><span class="sum-ico y" aria-hidden="true">✓</span><div class="sum-t"><p class="sum-l">{label}</p><p class="sum-s">{yes_s}</p></div></div>'
            f'<div class="st st-no"><span class="sum-ico n" aria-hidden="true">✗</span><div class="sum-t"><p class="sum-l">{label}</p><p class="sum-s">{no_s}</p></div><a class="sum-help" href="#{help_id}">Get help{CHEV}</a></div>'
            f'<div class="st st-un"><span class="sum-ico u" aria-hidden="true">–</span><div class="sum-t"><p class="sum-l">{label}</p><p class="sum-s">Not answered yet</p></div><a class="sum-help" href="#{TS[k]}">Answer{CHEV}</a></div></li>')
ROWS = ''.join([row(0, 'Account holder', 'You are the account holder', 'Only the account holder can sign in', 's4-2'),
                row(1, 'NHS login account', 'You have your own NHS login', 'You do not have NHS login yet', 's4-setup'),
                row(2, 'Signing in to NHS login', 'You can sign in', 'You cannot sign in yet', 's4-cannot'),
                row(3, 'Account details', 'Your details match', 'Your details may not match', 's4-problems'),
                row(4, 'Activation Link', 'You have your Activation Link', 'Your link has not arrived', 's4-activation')])
body = sm[sm.index('<div class="sum-msg sum-no'):sm.index('<ul class="sum-list">')]
body = body.replace('All four checks are done.', 'All five checks are done.')
nav_sum = sm[sm.index('<input type="radio" class="nudge-t"'):sm.index('</section>')]
nav_sum = nav_sum.replace('nw-sum', 'nw-tsum').replace('href="#c4"', 'href="#ts5"')
nav_sum = nav_sum.replace(f'<a class="nav-btn nav-next go-no" href="#s3"><span>Next</span>{ARROW_N}</a>',
                          f'<a class="nav-btn nav-next go-no nav-done" href="#s4" aria-label="Done – back to Troubleshooting"><span>Done</span>{ARROW_N}</a>')
assert 'nav-done' in nav_sum and 'href="#ts5"' in nav_sum
RESULTS = f'''<section class="screen" id="tsum" data-sec="Section 6 · Troubleshooting" data-title="Troubleshooter results" aria-label="Troubleshooter results">
<div class="scroll">
<div class="pbox has-n"><div class="stepper chk-steps" aria-hidden="true"><span class="">1</span><span class="">2</span><span class="">3</span><span class="">4</span><span class="">5</span></div><span class="tp-n" aria-hidden="true">✓</span><h2 tabindex="-1">Your results</h2></div>
<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · Troubleshooting</span><span class="pos">Page X of 48</span></div></div>
{body}<ul class="sum-list">
{ROWS}
</ul>
</div>
{nav_sum}</section>
'''

# --- insert after the Troubleshooting menu
m = page('s4'); s = s[:m.end()] + START + ''.join(Q) + RESULTS + s[m.end():]
# menu card
m = page('s4'); blk = m.group(0)
card = ('<a class="tc tc-app tc-ts" href="#ts"><span class="tc-tile">' + CLIP.replace('width="22" height="22"', 'width="24" height="24"') + '</span>'
        '<span class="tc-t"><b>Troubleshooter</b><span class="tc-s">Find out what is stopping you</span></span>'
        '<span class="tc-c"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span></a>')
blk2 = blk.replace('<nav aria-label="Troubleshooting contents" class="tc-list">', '<nav aria-label="Troubleshooting contents" class="tc-list">' + card)
assert blk2 != blk
n_tw = blk2.count('<span class="tc-w">'); assert n_tw == 2, n_tw
blk2 = blk2.replace('<span class="tc-w">', '<span class="tc-w fit-opt">')  # "Help from" lines give way on short screens
s = s[:m.start()] + blk2 + s[m.end():]

# --- styles: share the existing Checklist / summary / example styles with the new pages (in place, inside @media too)
def tr_sel(sel):
    out = []
    for p in sel.split(','):
        q = p
        if ':has(#c' not in q and 'body:' not in q:
            q = re.sub(r'#sum(?![\w-])', ':is(#sum,#tsum)', q)
            q = re.sub(r'#s2(?![\w-])', ':is(#s2,#ts)', q)
            q = re.sub(r'#c2(?![\w-])', ':is(#c2,#ts1,#ts2,#ts3,#ts4,#ts5)', q)
            if re.search(r'\.(exw|exc|ex-out|ex-i|ex-ok|ex-no)\b', q):
                q = re.sub(r'#nhs(?![\w-])', ':is(#nhs,#ts4)', q)
        out.append(q)
    return ','.join(out)
def fix_style(css):
    return re.sub(r'([^{}]+)\{([^{}]*)\}', lambda m: (tr_sel(m.group(1)) if not m.group(1).lstrip().startswith('@') else m.group(1)) + '{' + m.group(2) + '}', css)
s = re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + fix_style(m.group(2)) + m.group(3), s, flags=re.S)

ALL = ''.join(':has(#%s .ans-yes:checked)' % t for t in TS)
logic = []
for k, t in enumerate(TS, 1):
    logic += [f'body:has(#{t} .ans-yes:checked) #tsum .r{k} .st-yes{{display:flex}}',
              f'body:has(#{t} .ans-no:checked) #tsum .r{k} .st-no{{display:flex}}',
              f'body:not(:has(#{t} .ans:checked)) #tsum .r{k} .st-un{{display:flex}}',
              f'body:has(#{t} .ans-no:checked) #app #tsum .sum-no{{display:flex}}',
              f'body:not(:has(#{t} .ans:checked)) #app #tsum .sum-un{{display:flex}}',
              f'body:has(#{t} .ans-no:checked) #tsum .go-yes{{display:none!important}}',
              f'body:has(#{t} .ans-no:checked) #tsum .go-no{{display:inline-flex!important}}']
for k, t in enumerate(TS, 1):
    logic.append(f'body:has(#{t} .ans-no:checked) #app #tsum .sum-un{{display:none}}')
logic += [f'body{ALL} #app #tsum .sum-ok{{display:flex}}',
          f'body{ALL} #app #tsum .go-yes{{background:#00703c!important;border-color:#00703c!important;color:#fff}}']
CSS = '/* 3.23 Troubleshooter (ts, ts1-ts5, tsum) */\n' + '\n'.join(logic) + '\n' + """#app #s4 .tc-ts .tc-tile{background:linear-gradient(135deg,#6c155c,#d01545)}
#app #s4 .tc-ts{border-left-color:#c0174e}
#app #ts .pbox.gm-icon>.gm-eyi{color:#fff}
#app #ts .cq-end{margin-top:12px}
.ex-t{position:absolute;width:1px;height:1px;opacity:0;margin:0;pointer-events:none}
#app #ts4 .q-why{margin-bottom:6px}
#app #ts4 .ex-peek{display:block;position:relative;height:72px;overflow:hidden;margin:0 0 8px;border:1px solid var(--line);border-radius:12px;background:var(--surface);cursor:pointer}
#app #ts4 .ex-pv{display:block;width:166.7%;transform:scale(.6);transform-origin:0 0;padding:6px;box-sizing:border-box;pointer-events:none}
#app #ts4 .ex-peek::after{content:"";position:absolute;left:0;right:0;bottom:0;height:46px;background:linear-gradient(rgba(255,255,255,0),var(--surface))}
#app #ts4 .ex-tap{position:absolute;right:8px;bottom:7px;z-index:1;display:inline-flex;align-items:center;gap:5px;padding:5px 10px;border-radius:999px;background:#005eb8;color:#fff;font:700 14px/1.2 var(--font-body)}
#app #ts4 .ex-t:focus-visible+.ex-peek{outline:3px solid #ffd23f;outline-offset:2px}
#app #ts4 .ex-full{display:none;position:fixed;inset:0;z-index:60;align-items:center;justify-content:center;padding:16px;background:rgba(9,20,30,.62);cursor:pointer}
#app #ts4:has(.ex-t:checked) .ex-full{display:flex}
#app #ts4 .ex-box{display:block;width:100%;max-width:430px;box-sizing:border-box;padding:14px;border-radius:16px;background:var(--surface,#fff);border:1px solid var(--line)}
#app #ts4 .ex-bh{display:block;margin:0 0 8px;font:700 17px/1.3 var(--font-head);color:var(--ink)}
#app #ts4 .ex-close{display:block;margin-top:12px;text-align:center;font-size:15px;color:var(--sub)}
#app #ts4 .ex-box .ex-out{margin-top:12px}
@media screen and (max-height:700px){#app #tsum .st-no .sum-s{display:none}}
@media screen and (max-width:369px){#app #s4.tight .tc .tc-s{display:none!important}}
@media screen and (max-height:600px){#app #ts4 .ex-peek{height:60px}#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .q-why{margin-bottom:6px}}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# --- script: LEDs, results count and a clean start for each run
m = re.search(r"  var order=\['c1','c2','c3','c4','sum'\];\n  function paintDots\(\)\{ sumCount\(\);\n(.*?)\n  \}\n", s, re.S)
assert m, 'paintDots'
inner = m.group(1)
s = s.replace(m.group(0),
              "  var orders=[['c1','c2','c3','c4','sum'],['ts1','ts2','ts3','ts4','ts5','tsum']];\n"
              "  function paintDots(){ sumCount(); orders.forEach(function(order){\n" + inner + "\n  }); }\n")
rep("""function sumCount(){ var n=0; ['c1','c2','c3','c4'].forEach(function(id){ var p=byId[id]; if(p&&p.querySelector('.ans-no:checked')) n++; });
    var e=d.querySelector('#sum .sm-cnt'); if(e&&n) e.textContent=(n===1?'1 thing':n+' things'); }""",
    """function sumCount(){ [['sum',['c1','c2','c3','c4']],['tsum',['ts1','ts2','ts3','ts4','ts5']]].forEach(function(g){ var n=0;
      g[1].forEach(function(id){ var p=byId[id]; if(p&&p.querySelector('.ans-no:checked')) n++; });
      var e=d.querySelector('#'+g[0]+' .sm-cnt'); if(e&&n) e.textContent=(n===1?'1 thing':n+' things'); }); }""")
rep("""function resetChecklist(){ [].forEach.call(d.querySelectorAll('.ans:checked'),function(r){ r.checked=false; });""",
    """function resetChecklist(ids){ ids.forEach(function(id){ var p=byId[id]; if(p) [].forEach.call(p.querySelectorAll('.ans:checked'),function(r){ r.checked=false; }); });""")
rep("""if(cur&&cur.id==='s2'&&a.getAttribute('href')==='#c1') resetChecklist();""",
    """if(cur&&cur.id==='s2'&&a.getAttribute('href')==='#c1') resetChecklist(['c1','c2','c3','c4']);
    if(cur&&cur.id==='ts'&&a.getAttribute('href')==='#ts1') resetChecklist(['ts1','ts2','ts3','ts4','ts5']);""")
assert s.count('resetChecklist(') == 3, s.count('resetChecklist(')

# --- page counters
ids = re.findall(r'<section class="screen(?: cover)?[^"]*" id="([^"]+)"', s)
assert ids[-1] == 'search'; T = len(ids) - 1; assert T == 92, T
sec6 = [i for i in ids if 'data-sec="Section 6 · Troubleshooting"' in page(i).group(0)[:400]]
assert len(sec6) == 48 and sec6[:8] == ['s4', 'ts', 'ts1', 'ts2', 'ts3', 'ts4', 'ts5', 'tsum'], sec6[:9]
def put(pid, new):
    global s
    m = page(pid); s = s[:m.start()] + new + s[m.end():]
for n, pid in enumerate(sec6, 1):
    blk = page(pid).group(0)
    new = re.sub(r'<span class="pos">Page (?:\d+|X) of (?:41|48)</span>', f'<span class="pos">Page {n} of 48</span>', blk, count=1)
    assert f'Page {n} of 48' in new, pid; put(pid, new)
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: put(pid, new)
assert 'Page X of' not in s

rep('Carer role v3.22', 'Carer role v3.23'); rep('Version 3.22 iPhone', 'Version 3.23 iPhone')
rep('>3.22 – REVIEW DRAFT', '>3.23 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.22</span>', '<span class="cv-ver">Version 3.23</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.18</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.22</span>', '<div class="rr"><span class="rv">3.23</span><span class="rd">21 Nov 2026</span><p>Troubleshooting: new Troubleshooter (5 questions and your results)</p></div>\n<div class="rr"><span class="rv">3.22</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, 'pages', T)
