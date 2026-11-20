"""Guide 3.10 (from 3.09) – TRIAL (/preview/). David, 20 Nov: a calmer, fresher guide for frustrated carers.
Seven improvements, everywhere they apply:
 1 Gentler "The issue" icon: soft blue-grey "i" (was amber "!"), no amber background
 2 A reassuring first line on every Troubleshooting help page (one line; hidden on iPhone SE size to keep the page on one screen)
 3 More breathing space: light grey pages with white cards and soft shadows (light mode; Dark Mode unchanged)
 4 "You're on track": "Part 1 done", "Part 2 done – nearly there", and a clear "You're signed in" finish
 5 "Still stuck?" bar at the bottom of every help page, going to whoever can help next
   (NHS login pages: NHS login Support – it replaces the second "Contact NHS login Support" button; HV pages: Still need help?)
 6 One wording style: "Tap" (no more "Select ... then select Next")
 7 Shorter text (GMDP note, Introduction, Checklist start, some help text)
Best-possible front of the guide (cover to the end of the Checklist):
 - Cover: "Help signing in to your account on an iPhone", a calm line, and quick links: Help with a problem / Search
 - Contents: one white card, grouped by stage with small gaps
 - Introduction: shorter, "You are not alone", second-screen tip as three icon rows, "Need help now?" link
 - Run through the Checklist: the four questions listed up front ("It takes about a minute")
usage: python3 make310.py v3.09.html v3.10.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def in_page(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0); assert blk.count(a) == n, (pid, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
def set_body(pid, new):  # replace everything between the strip and the end of .scroll
    global s
    m = page(pid); blk = m.group(0)
    a = blk.index('</div></div>\n', blk.index('<div class="strip"')) + len('</div></div>\n')
    b = blk.rindex('</div>\n<nav class="bnav"')
    s = s[:m.start()] + blk[:a] + new + blk[b:] + s[m.end():]

CHECK = '<svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M4.5 10.5l3.5 3.5 7.5-8" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EXT = '<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><path d="M11 3.5h5.5V9M16.5 3.5L9 11M14 12v3.5a1 1 0 01-1 1H4.5a1 1 0 01-1-1V7a1 1 0 011-1H8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ico(path, w=20):
    return '<svg viewBox="0 0 24 24" width="%d" height="%d" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (w, w, path)

# ---------- 1 gentler issue icon ----------
n = s.count('<span class="abc-ic ic-issue" aria-hidden="true">!</span>'); assert n >= 10, n
s = s.replace('<span class="abc-ic ic-issue" aria-hidden="true">!</span>', '<span class="abc-ic ic-issue" aria-hidden="true">i</span>')

# ---------- 7 shorter text ----------
n = s.count('(The GMDP Support team cannot assist with NHS login account issues, as they do not have access to NHS login accounts.)'); assert n == 8, n
s = s.replace('(The GMDP Support team cannot assist with NHS login account issues, as they do not have access to NHS login accounts.)', 'GMDP Support cannot see NHS login accounts.')
in_page('s4-pw', 'Reset your password using the NHS login guide. If that does not work, contact NHS login Support.', 'Reset your password using the NHS login guide.')

# ---------- 2 reassuring first line + 5 Still stuck? ----------
NHS_CONTACT = 'https://help.login.nhs.uk/contact'
HELP = {  # page: (calm line, kind)
    's4-setup': ('Here is how to get started.', 'nhs'),
    's4-cannot': ('This is common, and it can be fixed.', 'nhs'),
    's4-pw': ('This is common, and easy to fix.', 'nhs'),
    's4-code': ('This is common, and it can be fixed.', 'nhs'),
    's4-email': ('There is a way round this.', 'nhs'),
    's4-mobile': ('Your number can be updated.', 'nhs'),
    's4-name': ('Your name can be updated.', 'nhs'),
    's4-activation': ('A new link can be sent to you.', 'hv'),
    's4-problems': ('Your team can put this right.', 'hv'),
    's4-1b': ('Your team can put this right.', 'hv'),
    's4-2': ('Here is what to do instead.', 'hv'),
    's4-help': ('You are not on your own.', None),
}
for pid, (calm, kind) in HELP.items():
    m = page(pid); blk = m.group(0)
    assert blk.count('<div class="abc">') == 1, pid
    blk = blk.replace('<div class="abc">', '<p class="calm"><span aria-hidden="true">' + CHECK + '</span>' + calm + '</p>\n<div class="abc">')
    if kind == 'nhs':
        c = re.search(r'<a class="sp-link abc-btn" href="%s"[^>]*>.*?</a>' % re.escape(NHS_CONTACT), blk, re.S)
        if c: blk = blk.replace(c.group(0), '')
        blk = blk.replace('<div class="hv-card sp-card abc-links"></div>', '')
        bar = ('<div class="stuck"><b>Still stuck?</b><a class="stuck-a" href="%s" rel="noopener" target="_blank">Contact NHS login %s</a></div>\n' % (NHS_CONTACT, EXT))
    elif kind == 'hv':
        bar = '<div class="stuck"><b>Still stuck?</b><a class="stuck-a" href="#s4-help">Get help %s</a></div>\n' % ARROW
    else:
        bar = ''
    i = blk.rindex('</div>\n<nav class="bnav"'); blk = blk[:i] + bar + blk[i:]
    s = s[:m.start()] + blk + s[m.end():]

# ---------- 6 one wording style: Tap ----------
for a, b in [('Select one option, then select <strong>Next</strong>.', 'Tap an answer, then tap <strong>Next</strong>.'),
             ('Please choose an answer, then select <strong>Next</strong>.', 'Please tap an answer, then tap <strong>Next</strong>.'),
             ('Select <strong>Next</strong> below to continue.', 'Tap <strong>Next</strong> to continue.')]:
    s = s.replace(a, b)
s = re.sub(r'Select <strong>Next</strong> to', 'Tap <strong>Next</strong> to', s)
s = re.sub(r'Select Next to', 'Tap Next to', s)
body = re.sub(r'<style.*?</style>|<script.*?</script>|<select.*?</select>', '', s, flags=re.S)
left = re.findall(r'.{30}\b[Ss]elect\b.{30}', body)
assert not left, left

# ---------- 4 on track ----------
in_page('step-4', '<div class="step-body">\n', '<div class="step-body">\n<p class="ontrack"><span aria-hidden="true">' + CHECK + '</span>Part 1 done. Next, sign in to NHS login.</p>\n')
in_page('step-10', '<div class="step-body">\n', '<div class="step-body">\n<p class="ontrack"><span aria-hidden="true">' + CHECK + '</span>Part 2 done – nearly there.</p>\n')
in_page('step-15', '<p>The <strong>My details</strong> screen opens. You are now signed in to your Carer account.</p>',
        '<div class="ontrack big" role="status"><span aria-hidden="true">' + CHECK + '</span><b>You’re signed in</b><em>Well done – that’s everything. Your <strong>My details</strong> screen is open.</em></div>')

# ---------- cover ----------
m = page('cover'); blk = m.group(0)
old_panel = re.search(r'<div class="cover-panel">.*?</div>\n', blk, re.S).group(0)
new_panel = ('<div class="cover-panel">\n<span class="pill">For parents and carers</span>\n<h1 tabindex="-1">GM Early Years App</h1>\n'
             '<p class="sub">Help signing in to your account on an iPhone</p>\n'
             '<p class="cv-calm">We will take you through it, one step at a time.</p>\n'
             '<nav class="cv-quick" aria-label="Quick links"><a class="cv-q" href="#s4">' + ico('<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 114 2c-.9.6-1.5 1.1-1.5 2.2M12 17h.01"/>', 18) +
             'Help with a problem</a><a class="cv-q" href="#search">' + ico('<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>', 18) + 'Search</a></nav>\n</div>\n')
blk = blk.replace(old_panel, new_panel)
s = s[:m.start()] + blk + s[m.end():]

# ---------- contents: grouped ----------
toc = re.search(r'<nav aria-label="Contents" class="toc">.*?</nav>', s, re.S).group(0)
def grp(ids):
    rows = [re.search(r'<a class="toc-row[^"]*" href="#%s">.*?</a>' % i, toc, re.S).group(0) for i in ids]
    return '<div class="toc-g">' + '\n'.join(rows) + '</div>'
newtoc = ('<nav aria-label="Contents" class="toc toc-grp">\n' + grp(['cover', 'intro', 'how']) + '\n' + grp(['hv', 'acct', 's2']) + '\n' + grp(['s3']) + '\n' +
          grp(['s4', 's5']) + '\n' + grp(['s6', 'a11y']) + '\n</nav>')
assert newtoc.count('toc-row') == toc.count('toc-row') == 11
rep(toc, newtoc)

# ---------- introduction ----------
I_PHONE = ico('<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>')
I_PC = ico('<rect x="3" y="4.5" width="18" height="12" rx="1.8"/><path d="M8 20h8M12 16.5V20"/>')
I_PRINT = ico('<path d="M7 9V3.5h10V9"/><rect x="3.5" y="9" width="17" height="8" rx="2"/><path d="M7 14h10v6.5H7z"/>')
set_body('intro',
    '<p class="lead iv-lead">Having trouble signing in to the GM Early Years App? <strong>You are not alone.</strong> This guide shows you what is stopping you, and what to do next.</p>\n'
    '<h3 class="h3">Tip: read the guide on a second screen</h3>\n'
    '<ul class="iv"><li><span>' + I_PHONE + '</span>A family member’s phone</li><li><span>' + I_PC + '</span>A computer</li><li><span>' + I_PRINT + '</span>A printed copy</li></ul>\n'
    '<p class="iv-then">Then follow the steps on your own iPhone.</p>\n'
    '<a class="iv-help" href="#s4"><span>Need help now?</span><b>Go to Troubleshooting</b>' + ARROW + '</a>\n'
    '<div class="push" aria-hidden="true"></div>\n'
    '<div class="tip nav-tip" role="note"><p>Tap <strong>Next</strong> to continue.</p></div>\n')

# ---------- run through the checklist ----------
Q = ['Do you have NHS login?', 'Can you use NHS login?', 'Do your details match?', 'Has your Activation Link arrived?']
set_body('s2',
    '<p class="lead cq-lead">Before you sign in, answer <strong>4 quick questions</strong>. It takes about a minute, and helps you sign in first time.</p>\n'
    '<ol class="cq">' + ''.join('<li><span aria-hidden="true">%d</span>%s</li>' % (i + 1, q) for i, q in enumerate(Q)) + '</ol>\n'
    '<p class="cq-end">Answer <strong>Yes</strong> or <strong>No</strong>. At the end, you will see what to do next.</p>\n'
    '<p class="cq-tap">Tap <strong>Begin</strong> to start.</p>\n')


# ---------- fit: optional extras give way before anything needs scrolling ----------
OLD_FIT = """  function fit(){
    if(!cur) return; var c=cur.querySelector('.crop'); if(!c) return;
    var se=d.scrollingElement||root;
    cur.style.setProperty('--maxh','560px');
    var over=se.scrollHeight-visH();
    if(over>0){ var h=c.getBoundingClientRect().height; cur.style.setProperty('--maxh',Math.max(64,Math.floor(h-over-2))+'px'); }
  }"""
NEW_FIT = """  function fit(){
    if(!cur) return; var c=cur.querySelector('.crop'), se=d.scrollingElement||root;
    function shrink(){ if(!c) return; cur.style.setProperty('--maxh','560px'); var over=se.scrollHeight-visH();
      if(over>0){ var h=c.getBoundingClientRect().height; cur.style.setProperty('--maxh',Math.max(64,Math.floor(h-over-2))+'px'); } }
    /* 3.10: if the page still needs scrolling, the optional extras (reassuring line, "Part done" line, tips) give way */
    cur.classList.remove('tight'); shrink();
    if(se.scrollHeight-visH()>0&&cur.querySelector('.calm,.ontrack:not(.big),.fit-opt,.toc-grp')){ cur.classList.add('tight'); shrink(); }
  }"""
rep(OLD_FIT, NEW_FIT)
s = s.replace('<p class="iv-then">', '<p class="iv-then fit-opt">').replace('<p class="cq-tap">', '<p class="cq-tap fit-opt">')
in_page('intro', '<div class="tip nav-tip" role="note">', '<div class="tip nav-tip fit-opt" role="note">')
# Activation Link not received: shorter
in_page('s4-activation', 'You need an Activation Link to open the App sign-in page. It is sent to you by text message.', 'Your Activation Link opens the App sign-in page. It comes by text message.')
in_page('s4-activation', 'Ask them to check your account has the right name and mobile number, and to send a new link.', 'Ask them to check your name and mobile number, and send a new link.')

# ---------- CSS ----------
CSS = r'''/* 3.10 Calmer guide (trial): see make310.py */
/* 1 gentler issue icon */
#app .screen .abc-row:nth-child(1){border-left-color:#7c93ad!important;background:var(--surface)!important}
#app .screen .abc-ic.ic-issue{background:#7c93ad!important;font-family:Georgia,'Times New Roman',serif!important;font-style:italic;font-weight:700!important}
/* 2 reassuring first line */
#app .screen .calm{display:flex;align-items:center;gap:8px;margin:0 0 9px;font-size:17px;line-height:1.3;color:var(--ink)}
#app .screen .calm span{flex:0 0 24px;height:24px;border-radius:50%;background:#e3f2ea;color:#00703c;display:flex;align-items:center;justify-content:center}
/* 5 still stuck */
#app .screen:has(>.scroll .stuck) .scroll{display:flex;flex-direction:column}
#app .screen .stuck{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:4px 5px 4px 14px;border-radius:14px;background:var(--surface);border:1px solid var(--line)}
#app .screen .abc:has(+.stuck){margin-bottom:8px}
#app .screen .stuck b{font:700 16px/1.2 var(--font-head);color:var(--ink)}
#app .screen .stuck a.stuck-a{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 15px;border-radius:999px;background:linear-gradient(135deg,#6c155c,#d01545);color:#fff!important;font-weight:700;font-size:16px;text-decoration:none!important;white-space:nowrap}
/* 4 on track */
#app .screen .ontrack{display:flex;align-items:center;gap:9px;margin:0 0 10px;padding:7px 12px;border-radius:12px;background:#e8f5ee;color:#0b4f2c;font-size:16px;line-height:1.3;font-weight:600}
#app .screen .ontrack span{flex:0 0 24px;height:24px;border-radius:50%;background:#00843d;color:#fff;display:flex;align-items:center;justify-content:center}
#app .screen .ontrack.big{flex-direction:column;align-items:center;text-align:center;padding:14px 12px;font-size:17px;gap:6px}
#app .screen .ontrack.big span{flex-basis:auto;width:40px;height:40px}
#app .screen .ontrack.big span svg{width:24px;height:24px}
#app .screen .ontrack.big b{font:800 20px/1.2 var(--font-head);color:#0b4f2c}
#app .screen .ontrack.big em{font-style:normal;font-weight:500}
@media (prefers-color-scheme:dark){
  #app .screen .ontrack{background:#12301f;color:#cfeedd}
  #app .screen .ontrack.big b{color:#9ee0b8}
  #app .screen .ontrack strong{color:inherit!important}
  #app .screen .calm span{background:#12301f;color:#9ee0b8}
}
/* cover */
#app #cover .cover-panel{gap:9px}
#app #cover .pill{letter-spacing:.1em}
#app #cover .cv-calm{font-size:17px;line-height:1.35;opacity:.95;margin:0}
#app #cover .cv-quick{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
#app #cover .cv-q{display:inline-flex;align-items:center;gap:7px;min-height:44px;padding:0 15px;border-radius:999px;background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.75);color:#fff;font-weight:700;font-size:16px;text-decoration:none}
#app #cover .cv-q:active{background:rgba(255,255,255,.3)}
/* contents: grouped card */
#app #contents .toc.toc-grp{border-top:0;margin-top:2px;gap:6px}
#app #contents .toc-g{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:14px;background:var(--surface);padding:0 12px}
#app #contents .toc-g .toc-row:last-child{border-bottom:0}
/* introduction */
#app #intro .iv-lead,#app #s2 .cq-lead{color:var(--ink)!important}
#app #intro .iv-lead{margin-bottom:12px!important}
#app #intro .iv{list-style:none;margin:2px 0 0;padding:0;border:1px solid var(--line);border-radius:14px;background:var(--surface)}
#app #intro .iv li{display:flex;align-items:center;gap:11px;margin:0;padding:7px 12px;font-size:17px;line-height:1.3;color:var(--ink)}
#app #intro .iv li+li{border-top:1px solid var(--line)}
#app #intro .iv li>span{flex:0 0 32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;background:var(--accentSoft);color:var(--accent2)}
#app #intro .iv-then{margin:8px 0 0;font-size:17px;line-height:1.35;color:var(--ink)}
#app #intro .iv-help{display:flex;align-items:center;gap:8px;margin-top:12px;padding:10px 12px;border-radius:14px;border:1px solid var(--line);background:var(--surface);color:var(--ink);text-decoration:none;min-height:48px}
#app #intro .iv-help span{font-size:16px;color:var(--sub)}
#app #intro .iv-help b{flex:1;font-size:17px;color:var(--accent2)}
#app #intro .iv-help svg{color:var(--accent2)}
/* run through the checklist */
#app #s2 .cq-lead{margin-bottom:12px!important}
#app #s2 .cq{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-radius:14px;background:var(--surface)}
#app #s2 .cq li{display:flex;align-items:center;gap:11px;margin:0;padding:8px 12px;font:700 17px/1.3 var(--font-body);color:var(--ink)}
#app #s2 .cq li+li{border-top:1px solid var(--line)}
#app #s2 .cq li>span{flex:0 0 26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#6c155c,#d01545);color:#fff;font:700 14px/1 var(--font-head)}
#app #s2 .cq-end{margin:12px 0 0;font-size:17px;line-height:1.4;color:var(--ink)}
#app #s2 .cq-tap{margin:8px 0 0;font-size:17px;line-height:1.4;color:var(--sub)}
/* 3 breathing space: light grey pages, white cards (light mode only) */
@media (prefers-color-scheme:light){
  #app{--surface:#fff}
  #app .screen:not(#cover){background:#eef1f5}
  #app .screen .abc-row{border:0!important;border-left:5px solid!important;border-radius:14px!important;background:#fff!important;box-shadow:0 1px 2px rgba(16,40,70,.05),0 4px 14px rgba(16,40,70,.06)!important;margin-bottom:8px!important}
  #app .screen .abc-row:nth-child(1){border-left-color:#7c93ad!important}
  #app .screen .abc-row:nth-child(2){border-left-color:#005eb8!important}
  #app .screen .abc-row:nth-child(3){border-left-color:#00703c!important}
  #app .screen :is(.toc-g,.iv,.iv-help,.cq,.stuck,.nd,.tr-list,.ah-list,.tc){box-shadow:0 1px 2px rgba(16,40,70,.04),0 3px 10px rgba(16,40,70,.05)}
}
/* when a page would need scrolling, the extras give way (class set by fit()) */
#app .screen.tight :is(.calm,.ontrack:not(.big),.fit-opt){display:none!important}
#app #contents.tight .toc.toc-grp{gap:0}
#app #contents.tight .toc-g{border-radius:0;box-shadow:none}
#app #contents.tight .toc-g+.toc-g{border-top:1px solid #b9c6d3}
#app #contents.tight .toc-g:first-child{border-radius:14px 14px 0 0}
#app #contents.tight .toc-g:last-child{border-radius:0 0 14px 14px}
/* short screens (iPhone SE size): keep every page on one screen */
@media screen and (max-height:700px){
  #app #intro .iv li{padding:5px 12px}
  #app #intro .iv li>span{flex-basis:28px;height:28px}
  #app #intro .iv-help{margin-top:8px;min-height:44px;padding:6px 12px}
  #app #intro .iv-lead{margin-bottom:8px!important}
  #app #s2 .cq li{padding:6px 12px}
  #app #contents .toc.toc-grp{gap:4px}
  #app .screen .abc-row{margin-bottom:6px!important}
}
@media screen and (max-height:600px){
  #app .screen .calm{display:none}
  #app .screen .ontrack:not(.big){display:none}
  #app #intro .iv-then,#app #intro .nav-tip{display:none}
  #app #s2 .cq-tap{display:none}
  #app #cover .cv-calm{display:none}
  #app #contents .toc.toc-grp{gap:3px}
  #app #contents.tight .toc-row{min-height:32px!important;padding-top:1px!important;padding-bottom:1px!important}
  #app #contents.tight .toc-row .gb{flex-basis:26px;width:26px;height:26px;font-size:13px}
  #app #contents.tight .toc-row .gb svg{width:15px;height:15px}
}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

# version
rep('Carer role v3.09', 'Carer role v3.10'); rep('Version 3.09 iPhone', 'Version 3.10 iPhone')
rep('<div>Version 3.09</div>', '<div>Version 3.10</div>'); rep('>3.09 – REVIEW DRAFT', '>3.10 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.07</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.09</span>', '<div class="rr"><span class="rv">3.10</span><span class="rd">20 Nov 2026</span><p>Calmer design: gentler icons, reassurance, white cards, Still stuck?, Tap wording; new cover, Contents, Introduction and Checklist start</p></div>\n<div class="rr"><span class="rv">3.09</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
