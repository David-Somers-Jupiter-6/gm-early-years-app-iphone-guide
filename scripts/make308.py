"""Guide 3.08 (from 3.07). David, 20 Nov: "Add to Home Screen" helper in Troubleshooting > GM Early Years App issues.
 - s4-gm list: new 2nd item "Put this guide on your Home Screen" -> a2hs
 - a2hs page (after inst-7-tip, before s4-activation): numbered steps with pictures of the Safari buttons.
   The guide picks what to show (classes on <html> set by a small script):
     ah-home  - opened from the Home Screen already -> green "already on your Home Screen" box only
     ah-file  - not the website (downloaded copy / Claude app preview) -> "open the guide website in Safari" box
     ah-old   - Safari 18 or earlier (Share button in the toolbar) -> 3 steps; otherwise iOS 26 steps (••• > Share > Add)
   Without JavaScript the iOS 26 steps show, with a line for older iPhones.
 - Back/Next chain, Troubleshooting "Page N of 41", Contents counters "N / 81"
usage: python3 make308.py v3.07.html v3.08.html"""
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

LIVE = 'https://david-somers-jupiter-6.github.io/gm-early-years-app-iphone-guide/'
CHEV = '<span class="tc-c"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
PHONE_PLUS = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M12 9v6M9 12h6"/></svg>'
# pictures of the Safari buttons (drawn, iOS style)
I_MORE = '<span class="ah-b ah-round" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22"><circle cx="6" cy="12" r="1.9" fill="currentColor"/><circle cx="12" cy="12" r="1.9" fill="currentColor"/><circle cx="18" cy="12" r="1.9" fill="currentColor"/></svg></span>'
I_SHARE = '<span class="ah-b" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 8.5H6.5A1.5 1.5 0 005 10v9.5A1.5 1.5 0 006.5 21h11a1.5 1.5 0 001.5-1.5V10a1.5 1.5 0 00-1.5-1.5H16"/><path d="M12 14V3M8.5 6.5L12 3l3.5 3.5"/></svg></span>'
I_ADDHS = '<span class="ah-b" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="3.5" width="17" height="17" rx="4"/><path d="M12 8v8M8 12h8"/></svg></span>'
I_ADD = '<span class="ah-b ah-add" aria-hidden="true">Add</span>'
def row(n, text, icon):
    return '<li><span class="ah-n" aria-hidden="true">%d</span><span class="ah-t">%s</span>%s</li>' % (n, text, icon)

NEW = ('<section class="screen" id="a2hs" data-sec="Section 6 · Troubleshooting" data-title="Put this guide on your Home Screen" aria-label="Put this guide on your Home Screen">\n'
  '<div class="scroll">\n'
  '<div class="pbox gm-icon"><span class="gm-eyi" aria-hidden="true">' + PHONE_PLUS.replace('width="24" height="24"', 'width="22" height="22"') + '</span><h2 class="h2" tabindex="-1">Add to Home Screen</h2></div>\n'
  '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Section 6 · Troubleshooting</span><span class="pos">Page X of 41</span></div></div>\n'
  '<p class="info-lead ah-lead">Put this guide on your Home Screen. It then opens with one tap, like an app, even without a signal.</p>\n'
  '<div class="ah-done" role="status"><span class="ah-tick" aria-hidden="true">✓</span><p><strong>This guide is on your Home Screen.</strong> You are using it now, so there is nothing more to do.</p></div>\n'
  '<div class="tip ah-safari"><span class="k">Open the guide in Safari first</span><p>Open the guide website in <strong>Safari</strong> on your iPhone, then come back to this page.</p>'
  '<a class="btn ah-open" href="' + LIVE + '" target="_blank" rel="noopener">Open the guide in Safari</a></div>\n'
  '<div class="ah-steps">\n'
  '<p class="jr-k">In Safari</p>\n'
  '<ol class="ah-list ah-new" aria-label="Steps for iPhones with iOS 26 or later">' +
    row(1, 'Tap the <strong>More</strong> button next to the address bar', I_MORE) +
    row(2, 'Tap <strong>Share</strong>', I_SHARE) +
    row(3, 'Tap <strong>Add to Home Screen</strong>', I_ADDHS) +
    row(4, 'Leave <strong>Open as Web App</strong> on, then tap <strong>Add</strong>', I_ADD) + '</ol>\n'
  '<ol class="ah-list ah-oldl" aria-label="Steps for older iPhones">' +
    row(1, 'Tap the <strong>Share</strong> button at the bottom of the screen', I_SHARE) +
    row(2, 'Scroll down and tap <strong>Add to Home Screen</strong>', I_ADDHS) +
    row(3, 'Tap <strong>Add</strong>', I_ADD) + '</ol>\n'
  '<p class="ah-note">The name and the icon are filled in for you.<span class="ah-alt"> No <strong>More</strong> button? Tap <strong>Share</strong> at the bottom of the screen instead.</span></p>\n'
  '</div>\n'
  '</div>\n')
nav = re.search(r'<nav class="bnav".*?</nav>', page('inst-7-tip').group(0), re.S).group(0)
nav = nav.replace('class="nav-btn nav-back" href="#inst-7"', 'class="nav-btn nav-back" href="#inst-7-tip"').replace('class="nav-btn nav-next" href="#s4-activation"', 'class="nav-btn nav-next" href="#s4-activation"')
NEW += nav + '\n</section>\n'
in_page('inst-7-tip', 'class="nav-btn nav-next" href="#s4-activation"', 'class="nav-btn nav-next" href="#a2hs"')
in_page('s4-activation', 'class="nav-btn nav-back" href="#inst-7-tip"', 'class="nav-btn nav-back" href="#a2hs"')
m = page('s4-activation'); s = s[:m.start()] + NEW + s[m.start():]
in_page('s4-gm', '<span class="tr-t">Activation Link issues</span>',
        '<span class="tr-t">Activation Link issues</span>', 1)
act = re.search(r'<a class="tr" href="#s4-activation">', page('s4-gm').group(0)).group(0)
in_page('s4-gm', act, '<a class="tr" href="#a2hs"><span class="tr-i">' + PHONE_PLUS + '</span><span class="tr-t">Add to Home Screen</span>' + CHEV + '</a>' + act)

# numbering
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
tr = [i for i in ids if 'data-sec="Section 6 · Troubleshooting"' in page(i).group(0)[:300]]
assert len(tr) == 41, len(tr)
for n, pid in enumerate(tr, 1):
    blk = page(pid).group(0); new = re.sub(r'<span class="pos">Page (?:\d+|X) of (?:40|41)</span>', f'<span class="pos">Page {n} of 41</span>', blk, count=1)
    assert new != blk, pid; m = page(pid); s = s[:m.start()] + new + s[m.end():]
assert ids[-1] == 'search'; T = len(ids) - 1; assert T == 81, T
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    new = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    new = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', new)
    if new != blk: m = page(pid); s = s[:m.start()] + new + s[m.end():]
assert not re.search(r'of 80\)|/ 80</span>|Page X of', s)
for a, b in zip(ids, ids[1:]):
    if a in ('inst-7-tip', 'a2hs'):
        na = re.search(r'class="nav-btn nav-next[^"]*" href="#([^"]+)"', page(a).group(0)).group(1)
        bb = re.search(r'class="nav-btn nav-back" href="#([^"]+)"', page(b).group(0)).group(1)
        assert na == b and bb == a, (a, b, na, bb)

CSS = '''/* 3.08 Add to Home Screen helper (Troubleshooting > GM Early Years App issues) */
#app #a2hs .ah-lead{margin-bottom:12px}
#app #a2hs .ah-list{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-radius:14px;background:var(--surface);overflow:hidden}
#app #a2hs .ah-list li{display:flex;align-items:center;gap:10px;margin:0;padding:8px 10px;min-height:52px}
#app #a2hs .ah-list li+li{border-top:1px solid var(--line)}
#app #a2hs .ah-n{flex:0 0 28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#6c155c,#d01545);color:#fff;font:700 15px/1 var(--font-head)}
#app #a2hs .ah-t{flex:1;min-width:0;font-size:17px;line-height:1.3;color:var(--ink)}
#app #a2hs .jr-k{margin:0 0 6px;font:700 13px/1.2 var(--font-head);letter-spacing:.06em;text-transform:uppercase;color:var(--sub)}
#app #a2hs .ah-b{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;gap:6px;min-width:40px;height:36px;padding:0 8px;border-radius:10px;background:#f2f2f7;color:#007aff;border:1px solid #d9d9e0;font:600 14px/1 -apple-system,system-ui,sans-serif}
#app #a2hs .ah-round{border-radius:50%;width:40px;padding:0}
#app #a2hs .ah-add{background:#007aff;color:#fff;border-color:#007aff;font-size:15px;padding:0 14px}
#app #a2hs .ah-note{margin:10px 0 0;font-size:15px;line-height:1.4;color:var(--sub)}
#app #a2hs .ah-done{display:none;align-items:flex-start;gap:12px;margin-top:4px;padding:12px 14px;border-radius:var(--r);background:#e8f5ee;border-left:5px solid #00843d}
#app #a2hs .ah-done p{font-size:17px;line-height:1.45;color:var(--ink);margin:0}
#app #a2hs .ah-tick{flex:0 0 28px;height:28px;border-radius:50%;background:#00843d;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}
#app #a2hs .ah-safari{display:none;margin-top:4px}
#app #a2hs .ah-open{display:block;text-align:center}
#app #a2hs .ah-oldl{display:none}
html.ah-old #app #a2hs .ah-oldl{display:block}
html.ah-old #app #a2hs .ah-new,html.ah-old #app #a2hs .ah-alt{display:none}
html.ah-home #app #a2hs .ah-done{display:flex}
html.ah-home #app #a2hs :is(.ah-steps,.ah-safari,.ah-lead){display:none}
html.ah-file:not(.ah-home) #app #a2hs .ah-safari{display:block}
html.ah-file:not(.ah-home) #app #a2hs .ah-steps{display:none}
@media screen and (prefers-color-scheme:dark){#app #a2hs .ah-b{background:#2c2c2e;border-color:#3a3a3c;color:#0a84ff}#app #a2hs .ah-add{background:#0a84ff;color:#fff}#app #a2hs .ah-done{background:#12301f}}
@media screen and (max-height:700px){#app #a2hs .ah-list li{min-height:46px;padding:6px 10px}#app #a2hs .ah-b{height:32px}#app #a2hs .ah-round{width:36px}}
@media screen and (max-height:600px){#app #a2hs .ah-lead{margin-bottom:8px}#app #a2hs .ah-list li{min-height:42px;padding:4px 10px}#app #a2hs .ah-note{margin-top:6px}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
JS = '''
/* 3.08 Add to Home Screen helper: what to show */
(function(){
  var h=document.documentElement, ua=navigator.userAgent||'';
  try{ if((window.matchMedia&&window.matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true) h.classList.add('ah-home'); }catch(e){}
  if(location.protocol!=='https:') h.classList.add('ah-file');
  var v=ua.match(/Version\\/(\\d+)/); if(v&&+v[1]<26) h.classList.add('ah-old');
})();
'''
i = s.rfind('</script>'); s = s[:i] + JS + s[i:]

rep('Carer role v3.07', 'Carer role v3.08'); rep('Version 3.07 iPhone', 'Version 3.08 iPhone')
rep('<div>Version 3.07</div>', '<div>Version 3.08</div>'); rep('>3.07 – REVIEW DRAFT', '>3.08 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.05</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.07</span>', '<div class="rr"><span class="rv">3.08</span><span class="rd">20 Nov 2026</span><p>Add to Home Screen helper in GM Early Years App issues</p></div>\n<div class="rr"><span class="rv">3.07</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
