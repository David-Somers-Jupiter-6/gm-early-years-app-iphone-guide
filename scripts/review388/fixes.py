"""3.88 fixes chosen by David from the problems-and-fixes doc (25 Nov 2026): 4, 5, 6, 7, 9, 10, 11.
usage: fixes.py src out
 4  Step 15 (You are signed in): the right-hand button is Finish and goes back to the cover; a closing line says
    "You can close this guide now" in the green box (the screenshot already shows My details), and one line for
    notifications and where to find help later.
 5  One set of counting words for carers in the title boxes: Stage, Step and Question.
    How this guide works: "Section 1" -> "Before you start"; Sign-in check: "Section 3" -> "Stage 1 of 3 · What you need";
    Signing in: "Part N of 3 · X" -> "Step N of 15 · X". (data-sec stays as it is: the navigation and Search use it.)
 6  Cannot get into your email: on iPhone SE in Safari the "Lost access to your email" button keeps its side padding.
 7  Your results: the "Sign-in check" label lines up with the right edge of the progress bar.
 9  Sign-in check questions: "Please tap an answer, then tap Next." shows in the space kept for the reply until an
    answer is tapped (the reply then takes its place, so nothing moves); the separate hint line above the answers goes.
    Tapping Next without an answer still highlights it in blue. iPhone SE in Safari (under 560 px high) keeps the 3.87
    behaviour: the reply space is below the bottom bar there, so the hint shows only when Next is tapped.
10  "No" replies: a round amber "!" icon in place of the red STOP sign.
11  Set up NHS login and Cannot sign in: the main link is the same solid button inside "What to do" as on the other
    NHS login help pages."""
import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:100], s.count(x)); s = s.replace(x, y)
def section(pid):
    i = s.index(f'<section class="screen" id="{pid}"'); j = s.index('</section>', i); return i, j
def in_section(pid, x, y, n=1):
    global s
    i, j = section(pid); sec = s[i:j]
    assert sec.count(x) == n, (pid, x[:100], sec.count(x)); s = s[:i] + sec.replace(x, y) + s[j:]

# 4. a proper ending on step 15
in_section('step-15', '<em>Well done – that’s everything. Your <strong>My details</strong> screen is open.</em>',
           '<em>Well done – that’s everything. You can close this guide now.</em>')
in_section('step-15', '<p>If your iPhone asks about notifications, either choice is fine. It does not affect signing in.</p>',
           '<p class="s15-end">Asked about notifications? Either choice is fine. Need help later? Tap <strong>Contents</strong>, then <strong>Support</strong>.</p>')
in_section('step-15', '<a class="nav-btn nav-next" href="#s4"><span>Next</span>',
           '<a class="nav-btn nav-next nav-finish" href="#cover" aria-label="Finish – back to the start of the guide"><span>Finish</span>')

# 5. Stage, Step and Question only
in_section('how', '<div class="kicker tb-loc">Section 1</div>', '<div class="kicker tb-loc">Before you start</div>')
in_section('ts', '<div class="kicker tb-loc">Section 3</div>', '<div class="kicker tb-loc">Stage 1 of 3 · What you need</div>')
for n in range(1, 16):
    i, j = section(f'step-{n}'); sec = s[i:j]
    m = re.findall(r'<div class="kicker part">Part \d of 3 · ([^<]+)</div>', sec); assert len(m) == 1, (n, m)
    sec = re.sub(r'<div class="kicker part">Part \d of 3 · ([^<]+)</div>', lambda k: f'<div class="kicker part">Step {n} of 15 · {k.group(1)}</div>', sec)
    s = s[:i] + sec + s[j:]

# 10. amber "!" in place of the STOP sign
stop = re.findall(r'<svg class="stop-ico"[^>]*>.*?</svg>', s, re.S); assert len(stop) == 4, len(stop)
calm = ('<svg class="stop-ico" aria-hidden="true" viewBox="0 0 40 40" width="28" height="28"><circle cx="20" cy="20" r="19" fill="#b45309"/>'
        '<rect x="17.8" y="8.5" width="4.4" height="15.5" rx="2.2" fill="#fff"/><circle cx="20" cy="30.2" r="2.8" fill="#fff"/></svg>')
s = re.sub(r'<svg class="stop-ico"[^>]*>.*?</svg>', calm, s, flags=re.S)

# 11. main help link inside "What to do"
for pid in ['s4-setup', 's4-cannot']:
    i, j = section(pid); sec = s[i:j]
    m = re.search(r'(<p class="abc-k">What to do</p><p>[^<]*</p>)(</div></div></div>\n)(<div class="hv-card sp-card abc-links">.*?</a></div>)\n', sec, re.S)
    assert m, pid
    sec = sec.replace(m.group(0), m.group(1) + m.group(3) + m.group(2))
    s = s[:i] + sec + s[j:]

css = '''
/* 3.88 (4) step 15: closing line */
#app #step-15 .s15-end{font-weight:400}
/* 3.88 (6) email help button keeps its side padding on short screens */
#app #s4-email .abc-row .abc-links .abc-btn{padding-left:12px!important;padding-right:12px!important}
/* 3.88 (7) results label lines up with the progress bar */
#app #tsum .pbox .kicker.tb-loc{right:16px!important}
/* 3.88 (9) the answer hint sits in the reply space until an answer is tapped */
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .q-hint{display:none!important}
@media (min-height:560px){
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5):not(:has(.ans:checked)) .ts-replies>.need-ans{visibility:visible!important}
}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5):not(.nudge):not(:has(.nudge-t:checked)) .ts-replies>.need-ans{background:rgba(120,135,155,.12)!important;border-left-color:transparent!important;animation:none!important}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
