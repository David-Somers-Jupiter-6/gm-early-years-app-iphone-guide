"""3.83: light/dark legibility and Apple text sizes in menus. usage: polish.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
# wording: section numbers in text go stale
rep('go to <a href="#s3">Section 5 · Signing in</a>.', 'go to <a href="#s3">Signing in</a>.')
rep('(see <a href="#s5-2">Section 6 · Contacts</a>)', '(see <a href="#s5-2">Contacts</a>)', 2)
rep('Contact details for every team are in Section 6, Contacts.', 'Contact details for every team are in Contacts.')
rep('<div class="tip nav-tip" role="note"><p>The stage you are on is shown at the top of each page', '<div class="tip nav-tip fit-opt" role="note"><p>The stage you are on is shown at the top of each page')
# Contacts' copy of the team finder uses the same words as Section 2
m = re.search(r'<section class="screen[^"]*" id="s5-hv".*?</section>', s, re.S); blk = m.group(0)
blk2 = blk.replace('Locality</label>', 'Area</label>').replace('<option value="">Choose a locality first</option>', '<option value="">Choose an area first</option>')
assert blk2 != blk; s = s[:m.start()] + blk2 + s[m.end():]
css = '''
/* 3.83 Dark Mode: the Troubleshooter information box was light with light text */
@media (prefers-color-scheme:dark){
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-info .abc-row{background:#16283b!important;border-color:#6aaeea!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-info .abc-k{color:#9ccaf2!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-help .th-k{color:#bcd6ef!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) :is(.ans-msg,.ts-noreply,.ts-stop,.ts-help) a{color:#9ccaf2!important}
}
/* 3.83 small labels on the coloured title boxes: full white for legibility */
#app .screen .pbox .kicker,#app .screen .pbox .kicker.part{color:#fff!important}
#app .screen .stg-t{color:#fff!important}
/* 3.83 Apple text sizes in menus (Title 1 28 / Title 2 22 / Title 3 20 / Headline 17 / Callout 16 / Subheadline 15 / Footnote 13 / Caption 12, 11) */
#app .screen .stg-t{font-size:12px!important}
@media screen and (max-width:369px){#app .screen .stg-t{font-size:11px!important}}
#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b{font-size:22px!important}
@media screen and (max-height:600px),screen and (max-width:369px){#app .screen:not(#contents) :is(.pbox,.tp-body).has-sb>.sec-b{font-size:20px!important}}
#app #s4 .tc-t>b{font-size:17px!important}
#app #s4-gm .tc-t>b{font-size:16px!important}
#app :is(#s4,#s4-gm) .tc-s{font-size:15px!important}
#app :is(#s4,#s4-gm) .tc-w{font-size:15px!important}
#app :is(#s4-nhs,#s4-gm) .tr-t{font-size:17px!important}
#app #s3 .jr b,#app #s3 .jr strong{font-size:15px!important}
#app #contents .toc-tile{font-size:15px}
#app #contents.tight .toc-tile{font-size:13px}
#app #contents.tight .toc-st{font-size:11px!important}
#app #cover .cv-k,#app #cover .cv-k span,#app #cover .cv-ver{font-size:12px!important}
#app #cover h1{font-size:28px!important}
#app #cover .cv-sub{font-size:17px!important}
#app #cover .cv-st{font-size:15px!important}
#app #cover .cv-fam .cv-fl{font-size:15px!important}
#app #cover .cv-c{font-size:13px!important}
/* 3.83 a Next that waits for an answer stays readable (dark grey text on light grey in Light Mode) */
@media (prefers-color-scheme:light){#app .bnav .nav-next.go-wait.off{background:#dfe5ec!important;border-color:#c9d2dc!important;color:#4e5d6c!important}#app .bnav .nav-next.go-wait.off span,#app .bnav .nav-next.go-wait.off svg{color:#4e5d6c!important}}
/* 3.83 short screens (Safari): keep every row on screen, still on Apple sizes */
@media screen and (max-height:700px){
#app #s4-gm .tc-t>b{font-size:15px!important;line-height:1.2!important}
#app #s4-gm .tc-s{font-size:13px!important;line-height:1.25!important;margin-top:1px!important}
#app #s4-gm .tc{padding-top:4px!important;padding-bottom:4px!important;min-height:44px!important;margin-bottom:5px!important}
#app #tsum .sum-l{font-size:15px!important;line-height:1.2!important}
#app #tsum .sum-list>li{padding-top:3px!important;padding-bottom:3px!important}
#app #tsum .sm-ban{padding-top:6px!important;padding-bottom:6px!important}
}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
