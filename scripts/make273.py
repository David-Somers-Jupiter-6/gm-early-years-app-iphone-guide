"""Guide 2.73 (from 2.70, live). Title boxes: band + page icon in the GM Early Years App colours
(David, 17 Nov, from the "App band + icon" mockups, version A - no faded blocks).
- Every title box is the app colour: plum to crimson from the ABC app logo (#6c155c -> #d01545), with a
  dark plum band (#45093c) reading "GM Early Years App | <section>" and the ABC app icon.
- NHS login pages are NOT in the app colours: NHS blue box (#005eb8 -> #0b4f9c) with the dark NHS blue band
  (#003087) reading "NHS login | ..." and the NHS mark, like the NHS login account issues pages (2.70, unchanged).
  NHS login pages: s4-cannot-4, s4-signin, Steps A-H and their tips, s5-2.
- Question, step and tip pages: the band shows the section and the position ("Checklist | Question 1 of 4"),
  replacing the small label above the title; the progress bar sits under the band.
- Other pages: a page icon in a white circle, bottom right. The large faded page numbers and the small NHS logo
  in title boxes are no longer shown (the band carries the NHS login name).
- Contents keeps its short title box (with Search), now in the app colour.
- Screens <=600 px tall (iPhone SE in Safari): slimmer band, no icon, so every page still fits.
Band text is aria-hidden, so Search and screen readers are unaffected.
usage: python3 make273.py v2.70.html v2.73.html
"""
import re, sys, base64, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
b64 = lambda f: 'data:image/png;base64,' + base64.b64encode(open(os.path.join(here, f), 'rb').read()).decode()
ABC, MARK = b64('abc_round.png'), b64('nhsmark_white.png')
I = {
 'info':'<circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="7.6" r="1.4" fill="currentColor"/><path d="M12 10.8v6.2" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>',
 'people':'<circle cx="8.5" cy="8" r="3.3" fill="currentColor"/><path d="M2.5 19.5c.5-3.6 2.9-5.6 6-5.6s5.5 2 6 5.6z" fill="currentColor"/><circle cx="16.5" cy="9" r="2.7" fill="currentColor" opacity=".75"/><path d="M15.2 13.8c3.2-.2 5.6 1.6 6.3 5.2h-4.6" fill="currentColor" opacity=".75"/>',
 'clip':'<rect x="5" y="4" width="14" height="17.5" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="8.5" y="2.5" width="7" height="3.5" rx="1" fill="currentColor"/><path d="M8.5 13l2.4 2.4 4.6-5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
 'signin':'<path d="M13 4h5a2 2 0 012 2v12a2 2 0 01-2 2h-5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M3.5 12h11M10.5 7.5L15 12l-4.5 4.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
 'wrench':'<path d="M20.5 6.5a5 5 0 01-6.6 6.2L7 19.6a2 2 0 01-2.8-2.8l6.9-6.9A5 5 0 0117.5 3.5l-3 3 .6 2.4 2.4.6z" fill="currentColor"/>',
 'link':'<path d="M10 14a4.5 4.5 0 006.4 0l3-3a4.5 4.5 0 00-6.4-6.4l-1.2 1.2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M14 10a4.5 4.5 0 00-6.4 0l-3 3a4.5 4.5 0 006.4 6.4l1.2-1.2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
 'list':'<circle cx="5" cy="6.5" r="1.6" fill="currentColor"/><circle cx="5" cy="12" r="1.6" fill="currentColor"/><circle cx="5" cy="17.5" r="1.6" fill="currentColor"/><path d="M9.5 6.5h10M9.5 12h10M9.5 17.5h10" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
 'neq':'<rect x="2.5" y="6" width="8" height="12" rx="1.5" fill="currentColor"/><rect x="13.5" y="6" width="8" height="12" rx="1.5" fill="none" stroke="currentColor" stroke-width="2"/>',
 'help':'<circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9.3 9.3a2.8 2.8 0 015.4 1c0 1.9-2.7 2.3-2.7 4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="17.6" r="1.3" fill="currentColor"/>',
 'headset':'<path d="M4 13v-1a8 8 0 0116 0v1" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="12.5" width="4.5" height="7" rx="1.6" fill="currentColor"/><rect x="16.5" y="12.5" width="4.5" height="7" rx="1.6" fill="currentColor"/><path d="M19 19.5c0 1.5-2 2.5-5 2.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
 'phone':'<path d="M6.6 3.5l2.7-.5 1.8 4.4-2.1 1.6a12 12 0 006 6l1.6-2.1 4.4 1.8-.5 2.7a2 2 0 01-2 1.6A15.5 15.5 0 015 5.5a2 2 0 011.6-2z" fill="currentColor"/>',
 'mail':'<rect x="2.5" y="5" width="19" height="14" rx="2" fill="currentColor"/><path d="M3.5 6.5l8.5 6.3 8.5-6.3" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/>',
 'a11y':'<circle cx="12" cy="4.6" r="2" fill="currentColor"/><path d="M4.5 8.2l7.5 1.6 7.5-1.6M12 9.8v4.7M12 14.5l-3.3 6M12 14.5l3.3 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
 'book':'<path d="M4 4.5h6a2 2 0 012 2V20a2 2 0 00-2-2H4zM20 4.5h-6a2 2 0 00-2 2V20a2 2 0 012-2h6z" fill="currentColor"/>',
 'map':'<path d="M9 4L3.5 6v14L9 18l6 2 5.5-2V4L15 6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 4v14M15 6v14" stroke="currentColor" stroke-width="2"/>',
 'doc':'<path d="M6 2.5h8l4.5 4.5v14a1 1 0 01-1 1H6a1 1 0 01-1-1v-17.5a1 1 0 011-1z" fill="currentColor"/><path d="M14 2.5V7h4.5" fill="none" stroke="#fff" stroke-width="1.5"/><path d="M8 12h8M8 15.5h8M8 19h5" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>',
 'clock':'<circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 6.8V12l3.6 2.2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
 'search':'<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M15.5 15.5l5 5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
}
ICON = {'intro':'info','hv':'people','s2':'clip','s3':'signin','s4':'wrench','s4-cannot-4':'signin','s4-signin':'signin',
        's4-activation':'link','s4-activation-2':'link','s4-reasons':'list','s4-problems':'neq','s4-1b':'people','s4-2':'people',
        's4-help':'help','s5':'headset','s5-hv':'phone','s5-2':'headset','s5-gmdp':'mail','a11y':'a11y','s6':'book','how':'map',
        'doc-control':'doc','revisions':'clock','search':'search'}
NHS_PAGES = {'s4-cannot-4', 's4-signin', 's5-2'} | {'step-' + c for c in 'abcdefgh'} | {'step-%s-tip' % c for c in 'bcdefgh'}
SHORT = {'Welcome':'Welcome','Section 1':'Health Visiting team','Section 2':'Checklist','Section 3':'Signing in',
         'Section 4':'Troubleshooting','Section 5':'Contact &amp; support','Section 6':'About this guide','Search':'Search'}
done = []
for m in list(re.finditer(r'<section class="screen" id="([^"]+)" data-sec="([^"]*)"', s))[::-1]:
    pid, sec = m.group(1), m.group(2)
    if pid in ('contents',): continue
    end = s.find('</section>', m.start()); blk = s[m.start():end]
    t = re.search(r'<div class="(pbox[^"]*|tp-body)">', blk)
    if not t or 'nhs-band' in t.group(1): continue
    short = next(v for k, v in SHORT.items() if sec.startswith(k))
    kick = re.search(r'<div class="kicker[^"]*">([^<]*)</div>', blk)
    nhs = pid in NHS_PAGES
    if kick:
        left, right = ('NHS login', re.sub(r'^NHS login · ', '', kick.group(1))) if nhs else (short, kick.group(1).replace(' · GM Early Years App', ' · App'))
    elif 'class="stepper' in blk[:blk.find('</h2>')]:
        left, right = short, 'Summary'
    else:
        left, right = ('NHS login', short) if nhs else ('GM Early Years App', short)
    logo = '<i class="eym"></i>' if nhs else '<img class="eyl" alt="" src="@@ABC@@">'
    band = '<div class="eyb%s" aria-hidden="true">%s<b%s>%s</b><span>%s</span></div>' % (' eyb-nhs' if nhs else '', logo, ' class="eyn"' if left == 'GM Early Years App' else '', left, right)
    icon = ''
    if not kick and 'class="stepper' not in blk[:blk.find('</h2>')]:
        assert pid in ICON, pid
        icon = '<span class="eyi" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22">%s</svg></span>' % I[ICON[pid]]
    cls = t.group(1) + ' eyx' + (' eyx-nhs' if nhs else '')
    newtag = '<div class="%s">' % cls + band + icon
    blk = blk[:t.start()] + newtag + blk[t.end():]
    s = s[:m.start()] + blk + s[end:]
    done.append(pid)
assert len(done) == 63, len(done)
s = s.replace('@@ABC@@', ABC)
APP, NHS = 'linear-gradient(135deg,#6c155c 0%,#d01545 100%)', 'linear-gradient(135deg,#005eb8 0%,#0b4f9c 100%)'
CSS = '''/* 2.73 title boxes: band + page icon in the GM Early Years App colours; NHS login pages in NHS blue */
#app .screen .pbox.eyx,#app .screen .tp-card .tp-body.eyx,#app #contents .tp-card .tp-body{background:@@APP@@!important}
#app .screen .pbox.eyx-nhs,#app .screen .tp-card .tp-body.eyx-nhs{background:@@NHS@@!important}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx{position:relative!important;overflow:hidden!important;padding-top:38px!important}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper){padding-top:38px!important}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx{height:auto!important;max-height:none!important}
#app .screen[data-sec^="Section 3"]:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper):has(.kicker){min-height:128px!important}
@media (max-width:359px){#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper):has(.kicker){min-height:128px!important}}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyb{position:absolute!important;top:0;left:0;right:0;height:30px;background:#45093c;display:flex;align-items:center;gap:9px;padding:0 16px;color:rgba(255,255,255,.82);font:700 12px/1 var(--font-body);letter-spacing:.08em;text-transform:uppercase;z-index:2}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyb-nhs{background:#003087}
.eyx>.eyb .eyl{flex:0 0 18px;height:18px;width:18px;border-radius:4px;box-shadow:0 0 0 1px rgba(255,255,255,.7)}
.eyx>.eyb .eym{flex:0 0 32px;display:block;width:32px;height:13px;background:url(@@MARK@@) center/contain no-repeat}
.eyx>.eyb b{color:#fff;font-weight:700;text-transform:none;letter-spacing:.02em;font-size:13px;white-space:nowrap}
.eyx>.eyb span{border-left:1px solid rgba(255,255,255,.4);padding-left:9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx .kicker{display:none!important}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx .stepper{margin-bottom:8px!important}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyi{position:absolute!important;right:14px;bottom:14px;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:#fff;color:#a3124d;box-shadow:0 3px 8px rgba(0,0,0,.25);z-index:2}
#app .screen .eyx-nhs>.eyi{color:#005eb8}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(>.eyi) h2{max-width:calc(100% - 54px)!important;white-space:normal!important}
#app .screen:not(#contents) :is(.pbox,.tp-body).eyx .tp-n,#app .screen .tp-card .tp-n,#app .screen:not(#contents) :is(.pbox,.tp-body).eyx .nhsbadge,#app .screen .tp-card:has(.eyx)>.nhsbadge{display:none!important}
#app .screen .pbox.eyx.has-badge{padding-bottom:18px!important}
@media (max-width:369px){#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyb{font-size:11px;letter-spacing:.05em;gap:7px;padding:0 13px}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyb b.eyn{display:none}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyb b.eyn+span{border-left:0;padding-left:0}#app .screen .eyx>.eyb .eym{display:none}}
@media (max-width:369px) and (max-height:680px){#app .screen .q-why{min-height:0!important;margin-bottom:4px!important}#app .screen .q-ask{min-height:0!important}#app .screen .ans-msg{margin-top:6px!important;padding-top:6px!important;padding-bottom:6px!important}}
@media (max-height:600px){#app .screen:not(#contents) :is(.pbox,.tp-body).eyx{padding-top:28px!important;min-height:72px!important}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyb{height:22px;font-size:11px}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper){padding-top:8px!important;min-height:72px!important}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper):has(.kicker){min-height:72px!important}#app .screen[data-sec^="Section 3"]:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper):has(.kicker){min-height:72px!important}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper)>.eyb{display:none!important}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(.stepper) .kicker{display:block!important}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx>.eyi{display:none!important}#app .screen:not(#contents) :is(.pbox,.tp-body).eyx:has(>.eyi) h2{max-width:100%!important}}
'''.replace('@@APP@@', APP).replace('@@NHS@@', NHS).replace('@@MARK@@', MARK)
rep('@media print{', CSS + '@media print{')
rep('Carer role v2.70', 'Carer role v2.73'); rep('Version 2.70 iPhone', 'Version 2.73 iPhone')
rep('<div>Version 2.70</div>', '<div>Version 2.73</div>'); rep('>2.70 – REVIEW DRAFT', '>2.73 – REVIEW DRAFT')
for v in ('2.67', '2.68', '2.69'):
    old = re.search(r'<div class="rr"><span class="rv">%s</span>.*?</div>\n' % re.escape(v), s)
    if old and v != '2.69': s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.70</span>', '<div class="rr"><span class="rv">2.73</span><span class="rd">17 Nov 2026</span><p>Title boxes: band and page icon in the GM Early Years App colours; NHS login pages in NHS blue</p></div>\n<div class="rr"><span class="rv">2.70</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(done), 'title boxes')
