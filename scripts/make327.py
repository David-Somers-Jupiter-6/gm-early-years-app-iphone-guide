"""Guide 3.27 (from 3.25) – TRIAL (/preview/ only) mock-up. David, 21 Nov:
 1. Introduction as a short conversation: the reader's words on the right, the guide's replies on the left (with
    the App icon), each on its own line, appearing one after the other. Tip heading kept.
 2. Section badges: a little smaller (36 px) and lower, so the number sits level with the title's last line.
 3. Troubleshooter questions: a subheading that states the answer first (e.g. "The child's mother or primary
    carer"), then the explanation, each point on its own line; "Tap an answer, then tap Next" always shown
    (except on the very shortest screen, the iPhone SE in Safari, where there is no room for it).
 4. Troubleshooter questions keep everything in the same place from page to page: the explanation area and the
    question are given the same height on all five pages (worked out on the phone), so the question and the
    Yes / No answers do not jump about.
 5. Do your details match?: the example preview is a clear "try this" card: "See an example" with a tap prompt
    bar across the bottom, and a gentle glow the first time.
 6. Your results: a badge in the title box shows the outcome like a traffic light: green tick when everything is
    ready, amber "!" when something needs sorting, grey while questions are unanswered. The title box keeps the
    guide's colours.
 Answer messages on the Troubleshooter are one line, with shorter wording where they wrapped. The checklist's
    three-line minimum for each explanation paragraph is switched off here (it made one-line sentences take three
    lines). Question 2 and 4 explanations are shorter, and question 4 asks "Are your details the same in both?";
    question 4 (with its example) now sets the height for all five pages (the Next button already lights up), and on the shorter screens
    the Introduction's second-screen tip becomes one line ("A family member's phone, a computer or a printed copy.") (a new second tier, .fit-opt2, that goes only if a page still does
    not fit once the optional extras have gone).
 7. Taps feel quicker: buttons, answers, cards and links show a pressed state the moment they are touched
    (iOS Safari only shows :active when the page listens for touches), and pages fade in faster.
usage: python3 make327.py v3.25.html v3.27.html"""
import re, sys, base64
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

ICON = base64.b64encode(open(__file__.rsplit('/', 1)[0] + '/assets/app-icon-88.png', 'rb').read()).decode()
PERSON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8.5" r="3.8"/><path d="M4.8 20c.9-3.9 3.7-6 7.2-6s6.3 2.1 7.2 6"/></svg>'

# 1. Introduction conversation
AV = '<span class="cb-av" aria-hidden="true"><img src="data:image/png;base64,' + ICON + '" alt="" width="30" height="30"/></span>'
ME = '<span class="cb-av cb-me" aria-hidden="true">' + PERSON + '</span>'
CHAT = ('<div class="chat" role="group" aria-label="Introduction">'
        f'<div class="cb cb-you">{ME}<p><span class="vh">You: </span>I’m having trouble signing in to the GM Early Years App.</p></div>'
        f'<div class="cb cb-guide">{AV}<p><span class="vh">Guide: </span><strong>You are not alone, and it is not your fault.</strong></p></div>'
        f'<div class="cb cb-you">{ME}<p><span class="vh">You: </span>I have tried before, and it did not work.</p></div>'
        f'<div class="cb cb-guide">{AV}<p><span class="vh">Guide: </span>It usually comes down to one small detail. We will find it together, <strong>one step at a time</strong>.</p></div>'
        '</div>')
edit('intro', '<h3 class="h3">Tip: read the guide on a second screen</h3>\n<ul class="iv">',
     '<div class="iv-short" aria-hidden="true"><p class="iv-sh">Tip: read the guide on a second screen</p><p class="iv-sp">A family member’s phone, a computer or a printed copy.</p></div>\n'
     '<h3 class="h3 fit-opt2">Tip: read the guide on a second screen</h3>\n<ul class="iv fit-opt2">')
edit('intro', '<p class="lead iv-lead">Having trouble signing in to the GM Early Years App? <strong>You are not alone, and it is not your fault.</strong></p>\n'
              '<p class="iv-calm">If you have tried before and it did not work, it usually comes down to one small detail. This guide will help you find it, one step at a time.</p>',
     CHAT)

# 3. Troubleshooter questions: subheading first, points on their own lines; 4. aligned areas
INFO = {
 'ts1': ('The child’s mother or primary carer',
         ['Your Health Visiting team sets up a GM Early Years App account for the child’s mother or primary carer.',
          'We call this person the <strong>account holder</strong>.']),
 'ts2': ('Only the account holder',
         ['They sign in with their <strong>own NHS login</strong>.',
          'A partner or relative <strong>cannot</strong> sign in.']),
 'ts3': ('With your NHS login details',
         ['You will sign in to the App with your NHS login <strong>email address</strong> and <strong>password</strong>.']),
 'ts4': ('Exactly the same details in both',
         ['Your <strong>email address</strong> and <strong>mobile number</strong> must match.']),
 'ts5': ('Sent to your mobile by text',
         ['Your Health Visiting team sends the <strong>Activation Link</strong> to the mobile number on your App account.']),
}
for pid, (sub, paras) in INFO.items():
    m = page(pid); blk = m.group(0)
    a = blk.index('<p class="q-why">'); b = blk.index('<p class="q-ask"')
    extra = blk[blk.index('</p>', a) + 4:b].strip()
    info = ('<div class="ts-info"><h3 class="h3 ts-sub">' + sub + '</h3>' + ''.join('<p class="q-why">%s</p>' % p for p in paras)
            + (('\n' + extra) if extra else '') + '</div>\n')
    c = blk.index('<p class="q-hint')
    ask = blk[b:c]
    blk = blk[:a] + info + '<div class="ts-qa">' + ask.strip() + '</div>\n' + blk[c:]
    blk = blk.replace('<p class="q-hint fit-opt" id="hint-%s">' % pid, '<p class="q-hint" id="hint-%s">' % pid)
    s = s[:m.start()] + blk + s[m.end():]

# 3c. shorter answer and message wording so each fits on one line on the smaller iPhones
for pid, a, b in [
    ('ts1', '<span>No, I am a partner or another family member</span>', '<span>No, I am a partner or relative</span>'),
    ('ts1', '<h3>Only the account holder can sign in</h3>', '<h3>Only the account holder</h3>'),
    ('ts2', '<h3>You need your own NHS login first</h3>', '<h3>You need your own NHS login</h3>'),
    ('ts3', '<span>No, I cannot sign in to my NHS login</span>', '<span>No, I cannot sign in to it</span>'),
    ('ts3', '<h3>You need to be able to sign in to NHS login</h3>', '<h3>NHS login needs to work first</h3>'),
    ('ts5', '<span>No, I have not received an Activation Link</span>', '<span>No, it has not arrived</span>'),
    ('ts4', '<span>No, they are different, or I’m not sure</span>', '<span>No, or I’m not sure</span>'),
    ('ts5', '<h3>Your Activation Link has not arrived</h3>', '<h3>Your link has not arrived</h3>')]:
    edit(pid, a, b)

edit('ts4', '<p class="q-ask" id="ask-ts4">Are your email address and mobile number the same in both?</p>', '<p class="q-ask" id="ask-ts4">Are your details the same in both?</p>')

# 5. example card
edit('ts4', '<span class="ex-tap"><svg aria-hidden="true" viewBox="0 0 20 20" width="16" height="16"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12.6 12.6L17 17M8.5 6v5M6 8.5h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Tap to see an example</span>',
     '<span class="ex-tap"><svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11V5.5a1.5 1.5 0 013 0V10m0-1.5a1.5 1.5 0 013 0V11m0-1a1.5 1.5 0 013 0v4.5c0 3.6-2.4 6.5-6 6.5-2.6 0-4-1.2-5.4-3.2L4.4 14a1.5 1.5 0 012.4-1.8L9 15"/></svg><span>See an example</span><span class="ex-tap-s">Tap here</span></span>')

# 6. results badge (traffic light)
edit('tsum', '<span class="tp-n" aria-hidden="true">✓</span><h2 tabindex="-1">Your results</h2>',
     '<span aria-hidden="true" class="sec-b res-b"><span class="rb-ok">✓</span><span class="rb-no">!</span><span class="rb-un">–</span></span><h2 tabindex="-1">Your results</h2>')
edit('tsum', '<div class="pbox has-n">', '<div class="pbox has-n has-sb">')

TS = ['ts1', 'ts2', 'ts3', 'ts4', 'ts5']
ALL = ''.join(':has(#%s .ans-yes:checked)' % t for t in TS)
res = [f'body{ALL} #tsum .res-b{{background:#00703c!important;color:#fff!important}}', f'body{ALL} #tsum .res-b .rb-ok{{display:block}}', f'body{ALL} #tsum .res-b .rb-un{{display:none}}']
for t in TS:
    res += [f'body:has(#{t} .ans-no:checked) #tsum .res-b{{background:#ffb81c!important;color:#1d2b36!important}}',
            f'body:has(#{t} .ans-no:checked) #tsum .res-b .rb-no{{display:block}}',
            f'body:has(#{t} .ans-no:checked) #tsum .res-b .rb-un{{display:none}}']

CSS = """/* 3.27 mock-ups */
/* 1. Introduction conversation */
#app #intro .chat{display:flex;flex-direction:column;gap:8px;margin:2px 0 14px}
#app #intro .cb{display:flex;align-items:flex-end;gap:8px;opacity:0}
#app #intro.on .cb{animation:cbIn .4s ease-out forwards}
#app #intro.on .cb:nth-child(2){animation-delay:.45s}
#app #intro.on .cb:nth-child(3){animation-delay:.9s}
#app #intro.on .cb:nth-child(4){animation-delay:1.35s}
@keyframes cbIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){#app #intro .cb,#app #intro.on .cb{opacity:1;animation:none}}
#app #intro .cb p{margin:0;padding:9px 13px;border-radius:16px;font-size:17px;line-height:1.38;max-width:82%}
#app #intro .cb-you{flex-direction:row-reverse}
#app #intro .cb-you p{background:#dfe8f1;color:var(--ink);border-bottom-right-radius:5px}
#app #intro .cb-guide p{background:var(--surface);color:var(--ink);border:1px solid var(--line);border-bottom-left-radius:5px;box-shadow:0 1px 3px rgba(20,40,60,.08)}
#app #intro .cb-av{flex:0 0 30px;width:30px;height:30px;border-radius:8px;overflow:hidden;display:grid;place-items:center}
#app #intro .cb-av img{width:30px;height:30px;display:block}
#app #intro .cb-me{border-radius:50%;background:#c9d6e2;color:#33475b}
@media screen and (max-height:700px){#app #intro .chat{gap:6px;margin-bottom:10px}#app #intro .cb p{font-size:16px;padding:7px 11px}}
@media screen and (max-height:600px){#app #intro .chat{gap:4px;margin:0 0 8px}#app #intro .cb p{padding:5px 10px;line-height:1.32}#app #intro .cb-av{flex-basis:26px;width:26px;height:26px}#app #intro .cb-av img{width:26px;height:26px}}
@media (prefers-color-scheme:dark){#app #intro .cb-you p{background:#2b3b4c}#app #intro .cb-me{background:#3a4d61;color:#dfe8f1}}
#app #intro .iv-short{display:none}
#app #intro.tighter .iv-short{display:block}
#app #intro .iv-sh{margin:0 0 2px;font:800 18px/1.25 var(--font-head);color:var(--ink)}
#app #intro .iv-sp{margin:0;font-size:16px;line-height:1.35;color:var(--ink)}
/* 2. section badges level with the title's last line */
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b{width:36px;height:36px;bottom:13px;font-size:19px}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b.sec-i{font-size:21px}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b.sec-app,#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b.sec-app img{width:38px;height:38px}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b.sec-app{bottom:12px;border-radius:10px}
/* 3./4. Troubleshooter questions */
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-sub{margin:0 0 4px;font-size:19px;line-height:1.3;color:var(--ink)}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-info .q-why{min-height:0!important;margin:0 0 6px!important}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-info{box-sizing:border-box}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-qa{display:flex;flex-direction:column;justify-content:flex-start;box-sizing:border-box;padding-top:6px}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-qa .q-ask{margin-top:4px}
@media screen and (max-height:700px){#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-sub{font-size:18px;margin-bottom:2px}#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-info .q-why{margin-bottom:4px!important}}
@media screen and (max-height:640px){#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-qa .q-ask{margin-top:0}#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-info>.q-why:last-child{margin-bottom:0!important}#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-info>.ex-full+*{margin:0}}
/* 3b. compact answer messages on the Troubleshooter (the Next button already lights up) */
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ans-msg>p:not(.ok-h){display:none}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ans-msg.amber{margin-top:8px!important;padding:8px 12px!important}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ans-msg.ok{margin-top:8px!important;padding-top:8px!important;padding-bottom:8px!important}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .stop-head{margin:0!important}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .stop-ico{flex-basis:28px;width:28px;height:28px}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .stop-head h3{font-size:17px}
#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ok-h{margin:0}
@media screen and (max-height:600px){#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-info .q-why{font-size:16px;line-height:1.35}#app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .ts-sub{font-size:17px}
  /* iPhone SE in Safari only: no room for the hint line (tapping Next without an answer still says what to do) */
  #app :is(#ts1,#ts2,#ts3,#ts4,#ts5) .q-hint{display:none}}
/* second tier: only if a page still does not fit once the optional extras have gone */
#app .screen.tighter .fit-opt2{display:none!important}
/* 5. example card */
#app #ts4 .ex-peek{height:98px;margin-bottom:10px;border:2px solid #005eb8;box-shadow:0 2px 8px rgba(0,94,184,.15)}
@media screen and (max-height:680px){#app #ts4 .ex-peek{height:84px;margin-bottom:8px}}
@media screen and (max-height:600px){#app #ts4 .ex-peek{height:76px}}
#app #ts4 .ex-peek::after{bottom:34px;height:30px}
#app #ts4 .ex-tap{left:0;right:0;bottom:0;border-radius:0;justify-content:flex-start;gap:8px;padding:7px 12px;font-size:16px}
#app #ts4 .ex-tap-s{margin-left:auto;font-weight:600;opacity:.9}
#app #ts4.on .ex-peek{animation:exGlow 1.6s ease-out .6s 2}
@keyframes exGlow{0%{box-shadow:0 0 0 0 rgba(0,94,184,.45)}70%{box-shadow:0 0 0 10px rgba(0,94,184,0)}100%{box-shadow:0 2px 8px rgba(0,94,184,.15)}}
@media (prefers-reduced-motion:reduce){#app #ts4.on .ex-peek{animation:none}}
#app #ts4 .ex-peek:active{transform:scale(.985)}
/* 6. results badge */
#app #tsum .res-b{background:#e3e7ea!important;color:#55626b!important;font:800 20px/1 var(--font-head)}
#app #tsum .res-b>span{display:none}
#app #tsum .res-b .rb-un{display:block}
""" + '\n'.join(res) + """
/* 7. pressed state the moment a button is touched; faster page fade */
#app :is(.nav-btn,.radio,.tc,.toc-row,.tr,.sum-help,.cv-rows a,.ex-peek,.srch-mic,.btn){-webkit-tap-highlight-color:transparent;touch-action:manipulation}
#app :is(.nav-btn,.tc,.toc-row,.tr,.sum-help,.cv-rows a):active{transform:scale(.97);filter:brightness(.94);transition:transform 60ms,filter 60ms}
#app .radio:active{background:rgba(0,94,184,.08)}
.screen.on{animation-duration:.12s!important}
"""
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:')
_css = s[:s.index('@media print{')]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# 4. JS: same heights for the explanation and question areas on all five questions; 7. touch listener
rep("  d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')) paintDots();",
    """  /* 3.27 Troubleshooter: give the explanation and question areas the same height on all five pages */
  var TSQ=['ts1','ts2','ts3','ts4','ts5'];
  function tsAlign(){ if(!cur||TSQ.indexOf(cur.id)<0) return;
    var ps=TSQ.map(function(id){ return byId[id]; }).filter(Boolean), w=cur.getBoundingClientRect().width, saved=[];
    ps.forEach(function(p,i){ [].forEach.call(p.querySelectorAll('.ts-info,.ts-qa'),function(e){ e.style.minHeight=''; });
      saved[i]=p.getAttribute('style'); if(p!==cur) p.style.cssText+=';display:flex!important;position:absolute;visibility:hidden;left:0;top:0;width:'+w+'px'; });
    ['.ts-info','.ts-qa'].forEach(function(c){ var m=0;
      ps.forEach(function(p){ var e=p.querySelector(c); if(e) m=Math.max(m,e.getBoundingClientRect().height); });
      ps.forEach(function(p){ var e=p.querySelector(c); if(e) e.style.minHeight=Math.ceil(m)+'px'; }); });
    ps.forEach(function(p,i){ if(p===cur) return; if(saved[i]===null) p.removeAttribute('style'); else p.setAttribute('style',saved[i]); });
  }
  d.addEventListener('touchstart',function(){},{passive:true});
  d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')) paintDots();""")
rep("function check(){ refit();", "function check(){ tsAlign(); refit();")
rep("    if(se.scrollHeight-visH()>0&&cur.querySelector('.calm,.ontrack:not(.big),.fit-opt,.toc-grp')){ cur.classList.add('tight'); shrink(); }",
    "    cur.classList.remove('tighter');\n"
    "    if(se.scrollHeight-visH()>0&&cur.querySelector('.calm,.ontrack:not(.big),.fit-opt,.toc-grp')){ cur.classList.add('tight'); shrink(); }\n"
    "    if(se.scrollHeight-visH()>0&&cur.querySelector('.fit-opt2')){ cur.classList.add('tighter'); shrink(); }")
# re-fit when an answer is chosen (its message appears)
rep("  d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')) paintDots(); });",
    "  d.addEventListener('change',function(e){ if(e.target.classList&&e.target.classList.contains('ans')){ paintDots(); setTimeout(check,30); } });")

rep('Carer role v3.25', 'Carer role v3.27'); rep('Version 3.25 iPhone', 'Version 3.27 iPhone')
rep('>3.25 – REVIEW DRAFT', '>3.27 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.25</span>', '<span class="cv-ver">Version 3.27</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.21</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.25</span>', '<div class="rr"><span class="rv">3.27</span><span class="rd">21 Nov 2026</span><p>Mock-ups: Introduction conversation; Troubleshooter layout; results badge; quicker taps</p></div>\n<div class="rr"><span class="rv">3.25</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
