"""3.82 review: Search page and Contents (search button; option B groups sections by stage). usage: search_contents.py src out A|B"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read(); V = sys.argv[3] if len(sys.argv) > 3 else 'A'
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % re.escape(i), s, re.S); assert m, i; return m
def rin(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
ICON = re.search(r'<img class="cv-icon" alt="GM Early Years App" src="(data:[^"]+)"', s).group(1)
MAG = '<svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M13 13l4.5 4.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
MIC = '<svg viewBox="0 0 20 20" width="17" height="17" aria-hidden="true"><rect x="7" y="2.5" width="6" height="10" rx="3" fill="currentColor"/><path d="M4.5 9.5a5.5 5.5 0 0 0 11 0M10 15v2.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'

# ---------- Search page ----------
rin('search', '<div class="pbox"><h2 class="h2" tabindex="-1">Search this guide</h2></div>',
    '<div class="pbox has-sb"><span aria-hidden="true" class="sec-b sr-app"></span><h2 class="h2" tabindex="-1">Search this guide</h2></div>')
rin('search', '<a class="srch-tp" href="#hv">Contact your HV team</a>', '<a class="srch-tp" href="#hv">Contact your Health Visiting team</a>')
rin('search', '<a class="nav-btn nav-next off" href="#search" aria-disabled="true" tabindex="-1">', '<a class="nav-btn nav-next off sr-nonext" href="#search" aria-hidden="true" tabindex="-1">')
# results: no sideways movement; swipe does not leave Search
rep("stage.addEventListener('touchstart',function(e){ if(e.touches.length!==1||zoomOpen()){on=false;return;}",
    "stage.addEventListener('touchstart',function(e){ if(e.touches.length!==1||zoomOpen()||(cur&&cur.id==='search')){on=false;return;}")
# snippets: leave out the title box (its title is shown already) and end labels with a full stop
rep(".srch-form,iframe,.go-wait,h2.h2,select,.hv-seg,.hv-map,.hv-tips'),function(x){ x.parentNode.removeChild(x); });",
    ".srch-form,iframe,.go-wait,h2.h2,select,.hv-seg,.hv-map,.hv-tips,.pbox,.tp-card'),function(x){ x.parentNode.removeChild(x); });\n"
    "      [].forEach.call(c.querySelectorAll('h3,h4,.k,dt,.abc-k'),function(x){ var t=(x.textContent||'').trim(); if(t&&!/[.!?:…]$/.test(t)) x.appendChild(d.createTextNode('.')); });")

# ---------- Contents: search button ----------
m = sec('contents').group(0)
old = re.search(r'<a class="tp-search" href="#search" aria-label="Search this guide">.*?</a>', m, re.S).group(0)
rin('contents', old, '<div class="tps"><a class="tps-go" href="#search" aria-label="Search this guide"><span class="tps-i">%s</span><span>Search</span></a>'
    '<a class="tps-mic" href="#search" aria-label="Search by speaking"><span class="tps-mb">%s</span></a></div>' % (MAG, MIC))
rep("if(e.target.closest&&e.target.closest('#cover .cv-mic')) mic.click();", "if(e.target.closest&&e.target.closest('#cover .cv-mic, #contents .tps-mic')) mic.click();")

css = '''
#app #search .scroll,#app #search .srch-res{overflow-x:hidden!important;overscroll-behavior-x:none}
#app #search .srch-res{touch-action:pan-y}
#app #search .sr-nonext{visibility:hidden}
#app #search .pbox.has-sb>.sec-b.sr-app{width:46px!important;height:46px!important;bottom:12px!important;border-radius:12px!important;box-shadow:0 4px 12px rgba(0,0,0,.3)!important;background:#fff url(ICON) center/cover no-repeat!important;border:2.5px solid #fff;box-sizing:border-box}
#app #contents .tps{position:absolute;right:10px;top:50%;transform:translateY(-50%);z-index:2;display:flex;align-items:center;height:44px;padding:0 4px 0 4px;border-radius:22px;background:#fff;box-shadow:0 2px 6px rgba(16,40,70,.22),0 0 0 2px rgba(255,255,255,.55)}
#app #contents .tps a{display:flex;align-items:center;text-decoration:none;-webkit-tap-highlight-color:transparent;touch-action:manipulation}
#app #contents .tps-go{gap:8px;height:44px;padding:0 6px 0 2px;color:#1f3a47;font:700 16px/1 var(--font-body)}
#app #contents .tps-i{width:32px;height:32px;border-radius:9px;background:#7d8a66;color:#fff;display:flex;align-items:center;justify-content:center}
#app #contents .tps-mic{height:44px;padding:0 2px 0 4px;border-left:1px solid #e2e7ea}
#app #contents .tps-mb{width:32px;height:32px;border-radius:50%;background:#d5573b;color:#fff;display:flex;align-items:center;justify-content:center;margin-left:6px}
#app #contents .tps-go:active .tps-i{background:#66724f}#app #contents .tps-mic:active .tps-mb{background:#b5432a}
@media (prefers-color-scheme:dark){#app #contents .tps{background:#1c2b33;box-shadow:0 2px 6px rgba(0,0,0,.4),0 0 0 2px rgba(255,255,255,.18)}#app #contents .tps-go{color:#fff}#app #contents .tps-mic{border-left-color:#34454f}}
'''

# ---------- Contents B: more informative layout ----------
if V == 'B':
    m = sec('contents').group(0)
    def row(h):
        mm = re.search(r'<a class="toc-row[^"]*" href="#%s".*?</a>' % re.escape(h), m, re.S); return mm.group(0)
    def tile(h, label):
        r = row(h); gb = re.search(r'<span class="gb"[^>]*>.*?</span>', r, re.S).group(0)
        cur = ' aria-current="page"' if 'aria-current' in r else ''
        return '<a class="toc-tile" href="#%s"%s>%s<span>%s</span></a>' % (h, cur, gb, label)
    def withsub(h, sub):
        r = row(h)
        return re.sub(r'(<span class="tt">)([^<]*)(</span>)', r'\1\2<small class="toc-sub toc-opt">%s</small>\3' % sub, r, count=1)
    def hdr(t): return '<p class="toc-st">%s</p>' % t
    nav_old = re.search(r'<nav aria-label="Contents" class="toc toc-grp">.*?</nav>', m, re.S).group(0)
    nav_new = ('<nav aria-label="Contents" class="toc toc-grp toc-b">\n'
        '<div class="toc-g toc-tiles">' + tile('cover', 'Cover page') + tile('intro', 'Introduction') + tile('contents', 'Contents') + '</div>\n'
        '<div class="toc-g">' + row('how') + '</div>\n'
        + hdr('Stage 1 · What you need') + '<div class="toc-g">' + row('hv') + '\n' + row('ts') + '</div>\n'
        + hdr('Stage 2 · How to sign in') + '<div class="toc-g">' + row('s3') + '</div>\n'
        + hdr('Stage 3 · Who can help') + '<div class="toc-g">' + row('s4') + '\n' + row('s5') + '</div>\n'
        '<div class="toc-g">' + row('a11y') + '\n' + row('s6') + '</div>\n</nav>')
    rin('contents', nav_old, nav_new)
    css += '''
#app #contents .toc-tiles{display:grid!important;grid-template-columns:repeat(3,1fr);gap:0}
#app #contents .toc-tile{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:50px;padding:4px 4px;text-decoration:none;color:var(--ink);font:700 14px/1.15 var(--font-body);text-align:center}
#app #contents .toc-tile+.toc-tile{border-left:1px solid var(--line)}
#app #contents .toc-tile .gb{width:27px;height:27px;border-radius:50%;background:var(--accentSoft);border:1.5px solid var(--accent);color:var(--accent2);font:700 15px/1 var(--font-head);display:flex;align-items:center;justify-content:center;box-sizing:border-box}
#app #contents .toc-tile[aria-current="page"] .gb{background:var(--accent);color:#fff}
#app #contents .toc-tile[aria-current="page"]{color:var(--accent2)}
#app #contents .toc-st{margin:7px 2px 3px;font:700 12px/1.2 var(--font-head);letter-spacing:.08em;text-transform:uppercase;color:var(--sub)}
#app #contents .toc-b .toc-g{margin-top:0}
#app #contents .toc-b .toc-g+.toc-g{margin-top:6px}
#app #contents.tight .toc-b .toc-g+.toc-g{margin-top:4px}
#app #contents.tight .toc-b .toc-g{border-radius:14px!important;border-top:1px solid var(--line)}
#app #contents.tight .toc-st{margin:4px 2px 2px;font-size:11.5px}
#app #contents.tight .toc-tile{min-height:50px;padding:5px 4px;gap:3px;font-size:13px}
#app #contents.tight .toc-tile .gb{width:26px;height:26px;font-size:13px}
#app #contents.tight .toc-b .toc-sub.toc-opt{display:none}
'''
css += '#app #contents.tight .toc-sub{font-size:13px;line-height:1.15;margin-top:0}\n'
css = css.replace('ICON', ICON)
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok', V)
