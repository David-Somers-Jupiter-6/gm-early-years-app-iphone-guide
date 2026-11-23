"""Guide 3.65 (from trial 3.64) – TRIAL. David, 23 Nov, question 1 (About your account):
 - the Who can help window is removed (the question window keeps its place);
 - the No reply (blue) now ends with "Who can help: Your Health Visiting team" in place of its link
   (the results page still links to the help page). Yes reply (green) unchanged.
 - question windows on questions 1-4 slightly tighter so the reply fits (answer buttons 48 px, above Apple's 44).
usage: python3 make365.py v3.64.html v3.65.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def in_sec(i, a, b, n=1):
    global s
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (i, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
in_sec('ts1', '<div class="abc-row"><span class="abc-ic ic-who who-nhs" aria-hidden="true"></span><div><p class="abc-k">Who can help</p><p><strong>Your Health Visiting team</strong></p></div></div>', '')
in_sec('ts1', ' See <a class="msg-link" href="#s4-who">Who will be set up with an account</a> for more information.</p></div>',
       '</p><p class="ok-more ts-help"><span class="abc-ic ic-who who-nhs ts-hi" aria-hidden="true"></span><span>Who can help: <strong>Your Health Visiting team</strong></span></p></div>')
CSS = '''/* 3.65 question 1: Who can help shown in the No reply */
#app #ts1 .ans-msg>p.ok-more.ts-help{display:flex!important;align-items:center;gap:8px;margin-top:5px!important;padding-top:5px;border-top:1px solid rgba(0,94,184,.2)}
/* question windows a little tighter (same on questions 1-4, so nothing moves between them) */
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask{margin-top:6px!important;padding:5px 10px 8px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask .ts-ask-k{margin:0 0 2px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask .q-hint{margin:4px 0 6px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask .ans-msg{margin-top:8px!important;padding-top:7px!important;padding-bottom:7px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask .radio{min-height:48px!important;padding-top:9px!important;padding-bottom:9px!important}
#app #ts1 .ts-help .ts-hi{position:static!important;flex:0 0 24px;width:24px!important;height:24px!important;border-radius:6px}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.64', 'Carer role v3.65'); rep('Version 3.64 iPhone', 'Version 3.65 iPhone')
rep('>3.64 – REVIEW DRAFT', '>3.65 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.64</span>', '<span class="cv-ver">Version 3.65</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.60</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.64</span>', '<div class="rr"><span class="rv">3.65</span><span class="rd">23 Nov 2026</span><p>Question 1: Who can help moved into the No reply</p></div>\n<div class="rr"><span class="rv">3.64</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
