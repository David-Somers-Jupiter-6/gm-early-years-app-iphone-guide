"""Guide 2.94 (from 2.93). David, 19 Nov - both mockups approved:
 1. Section 8 Contact & support start page: "Who to contact depends on the problem:" then three cards with logos
    (Your Health Visiting team / NHS login Support team / GMDP Support Team), each saying what it is "For:";
    Accessibility as a quieter line underneath. Logos embedded once in the styles.
 2. Checklist summary: a headline banner at the top - "N things to sort out first" (amber), "Not quite finished"
    (neutral) or "You are ready to sign in" (green, with a Go to Signing in button); problems as red cards with a
    solid Get help button; ticked items as one quiet line. Still works without JavaScript (the script only fills in N).
usage: python3 make294.py v2.93.html v2.94.html
"""
import re, sys, base64
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
def b64(p): return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
HERE = __file__.rsplit('/', 1)[0]
NHS = b64(HERE + '/nhsmark_white.png'); ABC = b64(HERE + '/abc_round_64.png')
CHEV = ('<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" '
        'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
TICK = ('<svg viewBox="0 0 20 20" width="14" height="14" aria-hidden="true"><path d="M4.5 10.4l3.6 3.5 7.4-7.6" fill="none" '
        'stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')
WARN = ('<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><path d="M10 5.5v5.2M10 14.2v.3" fill="none" '
        'stroke="currentColor" stroke-width="2.8" stroke-linecap="round"/></svg>')

# 1. Contact & support: who to contact for what
s5 = page('s5').group(0)
old = re.search(r'<p class="lead">Choose who to contact for help:</p>\n<nav aria-label="Contact and support" class="toc toc-sm">.*?</nav>', s5, re.S).group(0)
def card(cls, href, name, forwhat):
    return ('<a class="wc %s" href="#%s"><span class="wc-tile" aria-hidden="true"></span><span class="wc-t"><b>%s</b>'
            '<span class="wc-f"><em>For:</em> %s</span></span><span class="wc-c">%s</span></a>' % (cls, href, name, forwhat, CHEV))
NEW = ('<p class="wc-lead">Who to contact depends on the problem:</p>\n<nav aria-label="Who to contact" class="wc-list">'
       + card('wc-hv', 's5-hv', 'Your Health Visiting team', 'your App account – your details and Activation Link')
       + card('wc-nhs', 's5-2', 'NHS login Support team', 'your NHS login – setting up, signing in, security codes')
       + card('wc-gm', 's5-gmdp', 'GMDP Support Team', 'problems with the App itself, once NHS login works')
       + '<a class="wc-a11y" href="#a11y"><span>Large print, easy-read and other formats</span>' + CHEV + '</a></nav>')
edit('s5', old, NEW)

# 2. Checklist summary
edit('sum', '<p class="sum-intro">If any item below has a red cross, tap <strong>Get help</strong> next to it to find out what to do.</p>',
     '<div class="sum-msg sum-no sm-ban sm-amber" role="status"><span class="sm-bi">' + WARN + '</span><span><b><span class="sm-cnt">Some things</span> to sort out first</b>'
     '<small>Tap <strong>Get help</strong> on each one.</small></span></div>\n'
     '<div class="sum-msg sum-un sm-ban sm-grey" role="status"><span class="sm-bi">' + WARN + '</span><span><b>Not quite finished</b>'
     '<small>Tap <strong>Answer</strong> next to any item with a dash.</small></span></div>\n'
     '<div class="sum-msg sum-ok sm-ban sm-green" role="status"><span class="sm-bi">' + TICK + '</span><span><b>You are ready to sign in</b>'
     '<small>All four checks are done.</small></span></div>')
edit('sum', '<div class="sum-msg sum-ok ans-msg ok"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">You are ready to sign in</p><p>You have completed the checklist. Select <strong>Next</strong> to start signing in.</p></div>\n'
     '<div class="sum-msg sum-un tip"><span class="k">Not quite finished</span><p>Select <strong>Answer</strong> next to any item with a dash.</p></div>',
     '<a class="sm-go" href="#s3"><span>Go to Signing in</span>' + CHEV + '</a>')
# the script fills in the number ("2 things") - without it the banner says "Some things"
rep('/* keep earlier checklist answers coloured on later checklist pages */',
    "function sumCount(){ var n=0; ['c1','c2','c3','c4'].forEach(function(id){ var p=byId[id]; if(p&&p.querySelector('.ans-no:checked')) n++; });\n"
    "    var e=d.querySelector('#sum .sm-cnt'); if(e&&n) e.textContent=(n===1?'1 thing':n+' things'); }\n"
    "  /* keep earlier checklist answers coloured on later checklist pages */")
rep('function paintDots(){', 'function paintDots(){ sumCount();')

CSS = '''/* 2.94 Contact & support: who to contact for what */
#app #s5 .wc-lead{font-size:17px;line-height:1.4;color:var(--ink);margin:0 0 10px}
#app #s5 .wc-list{display:block}
#app #s5 .wc{display:flex;align-items:center;gap:12px;margin:0 0 8px;padding:10px;border:1px solid var(--line);border-left-width:5px;border-radius:14px;background:var(--surface);text-decoration:none!important;box-shadow:0 1px 2px rgba(0,48,135,.08)}
#app #s5 .wc-hv,#app #s5 .wc-nhs{border-left-color:#005eb8}#app #s5 .wc-gm{border-left-color:#c0174e}
#app #s5 .wc-tile{flex:0 0 44px;height:44px;border-radius:10px}
#app #s5 :is(.wc-hv,.wc-nhs) .wc-tile{background:#005eb8 url(%s) center/34px auto no-repeat}
#app #s5 .wc-gm .wc-tile{background:url(%s) center/30px 30px no-repeat,linear-gradient(135deg,#6c155c,#d01545)}
#app #s5 .wc-t{flex:1;min-width:0}
#app #s5 .wc-t b{display:block;font-family:var(--font-head);font-weight:700;font-size:17px;line-height:1.25;color:var(--ink)}
#app #s5 .wc-f{display:block;font-size:15px;line-height:1.3;color:var(--sub);margin-top:2px;font-weight:400!important}
#app #s5 .wc-f em{font-style:normal;font-weight:700;color:var(--ink)}
#app #s5 .wc-c{flex:0 0 auto;color:var(--accent2);display:flex}
#app #s5 .wc:active{background:var(--accentSoft)}
#app #s5 .wc-a11y{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:4px;padding:8px 4px;border-top:1px solid var(--line);color:var(--accent2);font-weight:700;font-size:16px;text-decoration:none!important}
@media screen and (max-height:600px){#app #s5 .wc{padding:8px 10px;margin-bottom:6px}#app #s5 .wc-lead{margin-bottom:8px}}
@media screen and (max-width:369px){#app #s5 .wc{gap:10px;padding:8px}#app #s5 .wc-tile{flex-basis:36px;height:36px;border-radius:9px}
 #app #s5 :is(.wc-hv,.wc-nhs) .wc-tile{background-size:28px auto}#app #s5 .wc-gm .wc-tile{background-size:24px 24px,auto}#app #s5 .wc-t b{font-size:16px}#app #s5 .wc-f{font-size:14px}}
/* 2.94 checklist summary: banner at the top, problems as red cards, ticked items as one quiet line */
#app #sum .sm-ban{align-items:center;gap:12px;margin:0 0 10px!important;padding:11px 14px!important;border-radius:14px}
#app #sum .sm-ban.sum-msg{display:none}
#app #sum .sm-amber{background:var(--amberBg,#fff7dc);border:1px solid #e0b400}
#app #sum .sm-grey{background:var(--surface);border:1px solid var(--line)}
#app #sum .sm-green{background:#e6f4ec;border:1px solid #00703c}
#app #sum .sm-bi{flex:0 0 30px;width:30px;height:30px;border-radius:50%%;display:flex;align-items:center;justify-content:center;color:#fff}
#app #sum .sm-amber .sm-bi{background:#b26b00}#app #sum .sm-grey .sm-bi{background:#4c6272}#app #sum .sm-green .sm-bi{background:#00703c}
#app #sum .sm-ban b{display:block;font-family:var(--font-head);font-weight:700;font-size:18px;line-height:1.25;color:var(--ink)}
#app #sum .sm-ban small{display:block;font-size:16px!important;line-height:1.35;color:var(--ink)}
#app #sum .sum-list{border-top:0}
#app #sum .sum-list li{border-bottom:0}
#app #sum .st-yes{gap:10px;padding:8px 4px!important;border-bottom:1px solid var(--line)}
#app #sum .st-yes .sum-ico{flex-basis:24px;width:24px;height:24px;font-size:13px}
#app #sum .st-yes .sum-l{font-family:inherit;font-weight:400;color:var(--sub)}
#app #sum .st-yes .sum-s{display:none}
#app #sum .st-no{margin:4px 0;padding:6px 8px 6px 10px!important;border:1px solid #e3a5a0;border-left:5px solid #c0392b;border-radius:12px;background:#fdf1f0}
#app #sum .st-no .sum-s{color:#5c3330}
#app #sum .st-no .sum-help{background:#005eb8;border-color:#005eb8;color:#fff}
#app #sum .st-un{padding:8px 4px!important;border-bottom:1px solid var(--line)}
#app #sum .sm-go{display:none;align-items:center;justify-content:center;gap:6px;margin-top:14px;min-height:46px;border-radius:999px;background:#005eb8;color:#fff!important;font-family:var(--font-head);font-weight:700;font-size:17px;text-decoration:none!important}
body:has(#c1 .ans-yes:checked):has(#c2 .ans-yes:checked):has(#c3 .ans-yes:checked):has(#c4 .ans-yes:checked) #app #sum .sm-go{display:flex}
body:has(#c1 .ans-yes:checked):has(#c2 .ans-yes:checked):has(#c3 .ans-yes:checked):has(#c4 .ans-yes:checked) #app #sum .sum-ok,
body:has(#c1 .ans-no:checked) #app #sum .sum-no,body:has(#c2 .ans-no:checked) #app #sum .sum-no,body:has(#c3 .ans-no:checked) #app #sum .sum-no,body:has(#c4 .ans-no:checked) #app #sum .sum-no{display:flex}
body:not(:has(#c1 .ans:checked)) #app #sum .sum-un,body:not(:has(#c2 .ans:checked)) #app #sum .sum-un,body:not(:has(#c3 .ans:checked)) #app #sum .sum-un,body:not(:has(#c4 .ans:checked)) #app #sum .sum-un{display:flex}
body:has(#c1 .ans-no:checked) #app #sum .sum-un,body:has(#c2 .ans-no:checked) #app #sum .sum-un,body:has(#c3 .ans-no:checked) #app #sum .sum-un,body:has(#c4 .ans-no:checked) #app #sum .sum-un{display:none}
@media screen and (max-height:700px),screen and (max-width:369px){#app #sum .sm-ban small{display:none}#app #sum .sm-ban{padding:9px 12px!important;margin-bottom:8px!important}#app #sum .st-yes,#app #sum .st-un{padding:6px 4px!important}#app #sum .st-no .sum-help{padding:5px 9px}}
@media screen and (max-height:600px),screen and (max-width:369px){#app #sum .sm-ban small{display:none}#app #sum .sm-ban b{font-size:17px}#app #sum .sm-bi{flex-basis:26px;width:26px;height:26px}#app #sum .st-no{gap:9px}#app #sum .st-no .sum-ico{flex-basis:24px;width:24px;height:24px;font-size:13px}#app #sum .sm-go{margin-top:10px}}
@media screen and (max-width:369px){#app #sum .st-no .sum-l{font-size:16px}#app #sum .st-no .sum-help{font-size:14px;padding:4px 7px 4px 9px}#app #sum .st-no{padding:5px 6px 5px 8px!important}}
@media print {#app #sum .sm-go{display:none!important}}
''' % (NHS, ABC)
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v2.93', 'Carer role v2.94'); rep('Version 2.93 iPhone', 'Version 2.94 iPhone')
rep('<div>Version 2.93</div>', '<div>Version 2.94</div>'); rep('>2.93 – REVIEW DRAFT', '>2.94 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.91</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.93</span>', '<div class="rr"><span class="rv">2.94</span><span class="rd">19 Nov 2026</span><p>Contact & support cards; Checklist summary headline and problem cards</p></div>\n<div class="rr"><span class="rv">2.93</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
