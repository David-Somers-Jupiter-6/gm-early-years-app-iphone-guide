"""3.81 review: cover (version kept; area tags as soft labels, option A or B). usage: cover.py src out A|B"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read(); V = sys.argv[3]
def rep(a, b, n=1):
    global s
    m = re.search(r'<section class="screen cover".*?</section>', s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
PIN = '<svg viewBox="0 0 24 24" width="%d" height="%d" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" fill="currentColor"/><circle cx="12" cy="10" r="2.4" fill="#fff"/></svg>'
rep('<p class="cv-sub">Help signing in to your account on an iPhone</p>', '<p class="cv-sub">A guide to signing in on your iPhone</p>')
rep('<span class="cv-st">Step-by-step help to sign in</span>', '<span class="cv-st">One step at a time</span>')
rep('<a class="nav-btn nav-back off" href="#cover" aria-disabled="true" tabindex="-1">', '<a class="nav-btn nav-back off cv-noback" href="#cover" aria-hidden="true" tabindex="-1">')
if V == 'A':
    rep('<span class="cv-fl">For families in</span>', '<span class="cv-fl"><span class="cv-pin">%s</span>For families in</span>' % (PIN % (15, 15)))
else:
    for t in ['Bury', 'Rochdale', 'Stockport']:
        rep('<span class="cv-c">%s</span>' % t, '<span class="cv-c">%s%s</span>' % (PIN % (13, 13), t))
css = ('#app #cover .cv-noback{visibility:hidden}\n'
       '#app #cover .cv-c{border:0!important;box-shadow:none!important;background:#e6eef2!important;color:#1f4556!important;border-radius:7px!important;padding:3px 9px!important;cursor:default;pointer-events:none}\n'
       '#app #cover .cv-c svg{color:#c8102e;margin:0 2px -2px -3px}\n'
       + ('#app #cover .cv-c{padding:3px 7px!important;font-size:13px!important}#app #cover .cv-fam{gap:5px!important}#app #cover .cv-fl{font-size:14px}\n' if V=='B' else '') +
       
       '#app #cover .cv-pin{color:#c8102e;margin-right:4px;display:inline-block;vertical-align:-2px}#app #cover .cv-fl{display:inline-flex;align-items:center}\n'
       '@media (prefers-color-scheme:dark){#app #cover .cv-c{background:rgba(255,255,255,.12)!important;color:#fff!important}#app #cover .cv-c svg circle,#app #cover .cv-pin svg circle{fill:#1d2b33}}\n')
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok', V)
