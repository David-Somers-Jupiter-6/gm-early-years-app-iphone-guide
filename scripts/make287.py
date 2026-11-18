"""Guide 2.87 (from 2.86). Section 3 · NHS login now opens with the key message (David, 18 Nov):
 the account holder's NHS login details must exactly match the details on their GM Early Years App account
 (given name, surname, NHS number, mobile phone number, email address), then leads them on:
 "Sign in to check your details" -> the NHS login sign-in steps.
 - The section start page (nhs) becomes "Before you sign in" (band "NHS login | Start here"):
   a diagram: NHS login | must match | GM Early Years App, with a tick on both sides of each of the five
   details (hints on mobile number and email address); then Same? You can sign in / Different? Contact your
   HV team; then the button. The "This section has two parts" list goes.
 - The separate Part a page (nhs-info) is removed; the sign-in start page band goes back to "Signing in".
 - Section 3 is 17 pages; the guide is 72 pages.
usage: python3 make287.py v2.86.html v2.87.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# 0. fix from 2.85: a duplicated "@media screen and (max-height:700px){" left a block open, so every rule after it
#    (the print styles, the switch fade on tall screens) only applied on screens up to 700 px tall
rep('@media screen and (max-height:700px){\n@media screen and (max-height:700px){\n', '@media screen and (max-height:700px){\n')

# 1. start page content: side-by-side diagram (option B) with a Yes / No ending (from option D)
TICK = ('<svg viewBox="0 0 20 20" width="12" height="12" aria-hidden="true"><path d="M4.5 10.4l3.6 3.5 7.4-7.6" '
        'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')
CROSS = ('<svg viewBox="0 0 20 20" width="12" height="12" aria-hidden="true"><path d="M5.5 5.5l9 9M14.5 5.5l-9 9" '
         'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>')
ITEMS = [('Given name', ''), ('Surname', ''), ('NHS number', ''),
         ('Mobile phone number', 'Gets your security codes'),
         ('Email address', 'Used to sign in to NHS login')]
rows = ''.join('<li class="mx-r"><span class="mx-t mx-tn">%s</span><span class="mx-l"><b>%s</b>%s</span><span class="mx-t mx-ta">%s</span></li>'
               % (TICK, a, ('<small>%s</small>' % b) if b else '', TICK) for a, b in ITEMS)
nhs = page('nhs').group(0)
ARROW = re.search(r'class="nav-btn nav-next" href="#nhs-info"><span>Next</span>(<svg.*?</svg>)</a>', nhs, re.S).group(1)
BODY = ('<p class="lead mx-lead">These details must be the <strong>same</strong> in both places:</p>\n'
        '<div class="mx" role="group" aria-label="Details that must match in NHS login and the GM Early Years App">'
        '<div class="mx-h" aria-hidden="true"><span class="mx-hn">NHS<br>login</span><span class="mx-he">must<br>match</span><span class="mx-ha">GM Early<br>Years App</span></div>'
        '<ul class="mx-list">' + rows + '</ul></div>\n'
        '<div class="mx-yn"><div class="mx-y"><span class="mx-i">' + TICK + '</span><span><b>Same?</b><small>You can sign in</small></span></div>'
        '<div class="mx-n"><span class="mx-i">' + CROSS + '</span><span><b>Different?</b><small><a href="#hv">Ask your HV team</a></small></span></div></div>\n'
        '<a class="match-go" href="#s4-signin"><span>Sign in to check your details</span>' + ARROW + '</a>')
old = re.search(r'<p class="lead">This section has two parts:</p>\n<nav aria-label="NHS login" class="toc toc-sm">.*?</nav>', nhs, re.S).group(0)
edit('nhs', old, BODY)
edit('nhs', '<b>NHS login</b><span>Overview</span>', '<b>NHS login</b><span>Start here</span>')
edit('nhs', '<h2 class="h2" tabindex="-1">NHS login</h2>', '<h2 class="h2" tabindex="-1">Before you sign in</h2>')
edit('nhs', 'data-title="NHS login"', 'data-title="Before you sign in to NHS login"')
edit('nhs', 'class="nav-btn nav-next" href="#nhs-info"', 'class="nav-btn nav-next" href="#s4-signin"')

# 2. remove the separate Part a page; sign-in start page follows straight on
m = page('nhs-info'); s = s[:m.start()] + s[m.end():].lstrip('\n')
edit('s4-signin', 'class="nav-btn nav-back" href="#nhs-info"', 'class="nav-btn nav-back" href="#nhs"')
edit('s4-signin', '<b>NHS login</b><span>Part b</span>', '<b>NHS login</b><span>Signing in</span>')
assert 'nhs-info' not in s

CSS = '''/* 2.87 Section 3 start page: details that must match (diagram) */
#nhs .mx-lead{color:var(--ink);margin-bottom:10px}
#app #nhs .mx{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--surface)}
#app #nhs .mx-h,#app #nhs .mx-r{display:grid;grid-template-columns:62px 1fr 62px;align-items:center}
#app #nhs .mx-h{text-align:center;font-family:var(--font-head);font-weight:700;font-size:12.5px;line-height:1.15;color:#fff;align-items:stretch}
#app #nhs .mx-hn{background:#005eb8;padding:5px 3px}#app #nhs .mx-ha{background:linear-gradient(135deg,#6c155c,#d01545);padding:5px 3px}
#app #nhs .mx-he{display:flex;align-items:center;justify-content:center;color:var(--sub);font-size:11.5px;letter-spacing:.07em;text-transform:uppercase}
#app #nhs .mx-list{list-style:none;margin:0;padding:0}
#app #nhs .mx-r{min-height:33px;border-top:1px solid var(--line);margin:0}
#app #nhs .mx-l{text-align:center;padding:3px 0}
#app #nhs .mx-l b{display:block;font-family:var(--font-head);font-weight:700;font-size:15.5px;line-height:1.25;color:var(--ink)}
#app #nhs .mx-l small{display:block;font-size:13.5px;line-height:1.2;color:var(--sub)}
#app #nhs .mx-t{justify-self:center;width:22px;height:22px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center}
#app #nhs .mx-tn{background:#005eb8}#app #nhs .mx-ta{background:#c0174e}
#app #nhs .mx-yn{display:flex;gap:8px;margin-top:10px}
#app #nhs .mx-yn>div{flex:1 1 auto}
#app #nhs .mx-yn>div{display:flex;align-items:center;gap:7px;border-radius:12px;padding:6px 8px;min-width:0}
#app #nhs .mx-y{background:#e6f4ec;border:1px solid #00703c}#app #nhs .mx-n{background:#fdeaea;border:1px solid #c0392b}
#app #nhs .mx-i{flex:0 0 20px;width:20px;height:20px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center}
#app #nhs .mx-y .mx-i{background:#00703c}#app #nhs .mx-n .mx-i{background:#c0392b}
#app #nhs .mx-yn b{display:block;font-family:var(--font-head);font-size:15px;line-height:1.2;color:#16314f}
#app #nhs .mx-yn small{display:block;font-size:14px;line-height:1.25;color:#33475b;white-space:nowrap}
#app #nhs .mx-yn small a{color:#9b1c1c;font-weight:700;font-size:inherit!important;line-height:inherit;text-underline-offset:2px}
.match-go{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;min-height:46px;padding:8px 18px;border-radius:999px;box-sizing:border-box;
  background:#005eb8;color:#fff!important;text-decoration:none!important;font-family:var(--font-head);font-weight:700;font-size:17px;line-height:1.2;
  box-shadow:0 2px 6px rgba(0,48,135,.25)}
.match-go svg{flex:0 0 auto;width:18px;height:18px}
.match-go:active{background:#003087}
.match-go:focus-visible{outline:3px solid var(--hl);outline-offset:2px}
@media screen and (max-height:640px){
#app #nhs .mx-r{min-height:31px}
.match-go{min-height:44px;margin-top:10px}
}
@media screen and (max-height:600px),screen and (max-width:369px){
#nhs .mx-lead{margin-bottom:8px}
#app #nhs .mx-h{font-size:12px}#app #nhs .mx-hn,#app #nhs .mx-ha{padding:4px 3px}
#app #nhs .mx-r{min-height:30px}#app #nhs .mx-l{padding:2px 0}
#app #nhs .mx-l b{font-size:15px}#app #nhs .mx-l small{font-size:13px}
#app #nhs .mx-t{width:20px;height:20px}
#app #nhs .mx-yn{margin-top:8px}#app #nhs .mx-yn>div{padding:5px 9px}
.match-go{margin-top:10px;min-height:42px;padding:6px 16px}
}
@media screen and (max-width:369px){
#app #nhs .mx-h,#app #nhs .mx-r{grid-template-columns:50px 1fr 50px}
#app #nhs .mx-h{font-size:11px}
#app #nhs .mx-yn{gap:6px}#app #nhs .mx-yn>div{gap:5px;padding:5px 6px}#app #nhs .mx-i{flex-basis:18px;width:18px;height:18px}#app #nhs .mx-yn b{font-size:14px}#app #nhs .mx-yn small{font-size:12.5px}
.match-go{font-size:16px;padding:6px 12px}
}
@media screen and (max-width:340px){#app #nhs .mx-yn .mx-i{display:none}}
@media print{.match-go{display:none}}
'''
rep('@media print{', CSS + '@media print{', 1)

# 3. renumber every page
order = [m.group(1) for m in re.finditer(r'<section class="screen(?: cover)?" id="([^"]+)"', s)]
order = [p for p in order if p != 'search']
total = len(order); assert total == 72, total
secs = {}
for pid in order:
    ds = re.search(r'data-sec="([^"]*)"', page(pid).group(0))
    secs.setdefault(ds.group(1) if ds else 'Welcome', []).append(pid)
for kk, pids in secs.items():
    for i, pid in enumerate(pids):
        pos = re.findall(r'<span class="pos">Page \d+ of \d+</span>', page(pid).group(0))
        if pos: edit(pid, pos[0], '<span class="pos">Page %d of %d</span>' % (i + 1, len(pids)))
for n2, pid in enumerate(order, 1):
    blk2 = page(pid).group(0)
    c2 = re.findall(r'<span class="count">\d+ / \d+</span>', blk2); assert len(c2) == 1, pid
    edit(pid, c2[0], '<span class="count">%d / %d</span>' % (n2, total))
    a2 = re.findall(r'aria-label="Contents \(page \d+ of \d+\)"', blk2)
    if a2: edit(pid, a2[0], 'aria-label="Contents (page %d of %d)"' % (n2, total))
for a, b in zip(order[3:], order[4:]):
    assert re.search(r'class="nav-btn nav-next[^"]*" href="#%s"' % b, page(a).group(0)), ('next', a, b)
    assert re.search(r'class="nav-btn nav-back" href="#%s"' % a, page(b).group(0)), ('back', b, a)
print('Section 3 pages:', len(secs['Section 3 · NHS login']))


# stylesheet must be balanced where new CSS goes in (guards against another unclosed block)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), ('unbalanced CSS before @media print', _css.count('{'), _css.count('}'))

rep('Carer role v2.86', 'Carer role v2.87'); rep('Version 2.86 iPhone', 'Version 2.87 iPhone')
rep('<div>Version 2.86</div>', '<div>Version 2.87</div>'); rep('>2.86 – REVIEW DRAFT', '>2.87 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.84</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.86</span>', '<div class="rr"><span class="rv">2.87</span><span class="rd">18 Nov 2026</span><p>NHS login starts with the details that must match, then leads into signing in</p></div>\n<div class="rr"><span class="rv">2.86</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
