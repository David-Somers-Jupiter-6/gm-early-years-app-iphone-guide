"""Guide 3.12 (from trial 3.11) – LIVE. David, 20 Nov: make all trial improvements live, with the new cover
"C3·6 All GMCA" (from the cover mock-ups in GMCA colours):
 - Solid GMCA slate logo band: GMCA logo (left) and Greater Manchester – Doing Digital Differently (right), nothing behind them
   (the old blue header on the cover is no longer shown)
 - Photo, then a white panel that overlaps it, with a faint hexagon pattern (GMCA device) and the large App icon as a badge
 - "For parents and carers" + Version, "GM Early Years App", "Help signing in to your account on an iPhone"
 - Three choices on a white card with square icons in GMCA colours (slate / vermilion / green):
   Start the guide (Contents), Help with a problem (Troubleshooting), Search
 - "For families in Bury · Rochdale · Stockport" (gives way on small screens if needed)
 - Start button in GMCA slate (no pulse)
 - Dark Mode: slate panel with light text
usage: python3 make312.py v3.11.html v3.12.html"""
import re, sys, math, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
ICON = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'app-icon-cover.png'), 'rb').read()).decode()

def hexnet(w, h, r=22):
    out = []; dx = r * math.sqrt(3); dy = r * 1.5; y = 0; row = 0
    while y < h + r:
        x = dx / 2 if row % 2 else 0
        while x < w + dx:
            out.append('<polygon points="%s"/>' % ' '.join('%.1f,%.1f' % (x + r * math.cos(math.radians(60 * k - 30)), y + r * math.sin(math.radians(60 * k - 30))) for k in range(6)))
            x += dx
        y += dy; row += 1
    return '<svg class="cv-net" width="%d" height="%d" viewBox="0 0 %d %d" aria-hidden="true" focusable="false">%s</svg>' % (w, h, w, h, ''.join(out))
CHEV = '<svg class="cv-ch" viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_PLAY = '<svg viewBox="0 0 20 20" width="14" height="14" aria-hidden="true"><path d="M6 4l10 6-10 6z" fill="currentColor"/></svg>'
I_Q = '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9.2 9.2a2.8 2.8 0 115 1.8c-1 .8-2.2 1.3-2.2 2.8M12 17.6h.01"/></svg>'
I_S = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/></svg>'

m = re.search(r'<section class="screen cover" id="cover".*?</section>', s, re.S); blk = m.group(0)
photo = re.search(r'<img class="cover-img"[^>]*>', blk).group(0)
ddd = re.search(r'<img class="cover-logo"[^>]*>', blk).group(0).replace('class="cover-logo"', 'class="cv-ddd"')
a = blk.index('<div class="scroll">'); b = blk.index('<nav class="bnav"')
new_scroll = ('<div class="scroll">\n'
  '<div class="cv-band"><div aria-label="GMCA: Greater Manchester Combined Authority" class="cv-gmca" role="img"><div class="w">GMCA</div>'
  '<div class="s"><div>Greater</div><div>Manchester</div><div>Combined</div><div>Authority</div></div></div>' + ddd + '</div>\n'
  '<div class="cover-photo">' + photo + '</div>\n'
  '<div class="cv-sheet">\n<div class="cv-netw" aria-hidden="true">' + hexnet(250, 220) + '</div>\n'
  '<img class="cv-icon" alt="GM Early Years App" src="' + ICON + '" width="76" height="76"/>\n'
  '<p class="cv-k"><span>For parents and carers</span><span class="cv-ver">Version 3.12</span></p>\n'
  '<h1 tabindex="-1">GM Early Years App</h1>\n'
  '<p class="cv-sub">Help signing in to your account on an iPhone</p>\n'
  '<nav class="cv-rows" aria-label="Quick links">'
  '<a href="#contents"><span class="cv-ai cv-a1">' + I_PLAY + '</span><span class="cv-t">Start the guide</span>' + CHEV + '</a>'
  '<a href="#s4"><span class="cv-ai cv-a2">' + I_Q + '</span><span class="cv-t">Help with a problem</span>' + CHEV + '</a>'
  '<a href="#search"><span class="cv-ai cv-a3">' + I_S + '</span><span class="cv-t">Search</span>' + CHEV + '</a></nav>\n'
  '<p class="cv-fam fit-opt"><span class="cv-fl">For families in</span><span class="cv-c">Bury</span><span class="cv-c">Rochdale</span><span class="cv-c">Stockport</span></p>\n'
  '</div>\n</div>\n')
blk = blk[:a] + new_scroll + blk[b:]
s = s[:m.start()] + blk + s[m.end():]

CSS = '''/* 3.12 Cover "C3·6 All GMCA": slate logo band, photo, white panel with hexagons, App icon, three choices */
#app .hdr{display:none!important}
#app #cover .scroll{display:flex!important;flex-direction:column!important;padding:0!important;background:#fff}
#app #cover .cv-band{flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:60px;padding:8px 18px;background:#2d5161}
#app #cover .cv-gmca{display:flex;align-items:flex-start;gap:6px;color:#fff}
#app #cover .cv-gmca .w{font-family:'Hanken Grotesk',sans-serif;font-weight:600;font-size:26px;letter-spacing:.01em;line-height:.72}
#app #cover .cv-gmca .s{font-family:'Hanken Grotesk',sans-serif;font-size:6.5px;font-weight:600;line-height:1;letter-spacing:.03em;text-transform:uppercase}
#app #cover .cv-gmca .s div{border-bottom:1px solid currentColor;padding-bottom:2px;margin-bottom:1px;opacity:.85}
#app #cover .cv-gmca .s div:last-child{margin-bottom:0}
#app #cover .cv-ddd{display:block;width:118px;height:auto}
#app #cover .cover-photo{flex:1 1 0!important;height:auto!important;max-height:none!important;min-height:56px;background:#e8dccf}
#app #cover .cover-photo::after{display:none!important}
#app #cover .cover-photo .cover-img{object-position:22% 22%!important}
#app #cover .cv-sheet{flex:0 0 auto;position:relative;margin-top:-24px;background:#fff;border-radius:26px 26px 0 0;padding:16px 18px 12px;box-shadow:0 -10px 30px rgba(31,58,71,.16)}
#app #cover .cv-netw{position:absolute;inset:0;overflow:hidden;border-radius:26px 26px 0 0;pointer-events:none}
#app #cover .cv-net{position:absolute;right:-24px;top:-8px;fill:none;stroke:#2d5161;stroke-opacity:.1;stroke-width:1.1}
#app #cover .cv-sheet>*:not(.cv-netw):not(.cv-icon){position:relative}
#app #cover .cv-icon{position:absolute;right:18px;top:-40px;width:76px;height:76px;border-radius:20px;border:4px solid #fff;box-shadow:0 10px 22px rgba(31,58,71,.25);background:#fff;z-index:2}
#app #cover .cv-k{display:flex;gap:10px;align-items:baseline;margin:0;font:700 12.5px/1.3 var(--font-body);letter-spacing:.13em;text-transform:uppercase;color:#b5432a}
#app #cover .cv-ver{letter-spacing:.02em;text-transform:none;font-weight:600;color:#5d6b70}
#app #cover h1{margin:4px 0 4px;font:800 31px/1.04 Archivo,var(--font-head);letter-spacing:-.012em;color:#2d5161}
#app #cover .cv-sub{margin:0 0 12px;max-width:290px;font:600 17.5px/1.32 var(--font-body);color:#1f3a47;text-wrap:balance}
#app #cover .cv-rows{display:flex;flex-direction:column;border:1px solid #e0e5e8;border-radius:16px;overflow:hidden;background:#fff}
#app #cover .cv-rows a{display:flex;align-items:center;gap:12px;min-height:46px;padding:0 14px;font:700 17px/1.2 var(--font-body);color:#1f3a47;text-decoration:none}
#app #cover .cv-rows a+a{border-top:1px solid #e3e7ea}
#app #cover .cv-rows a:active{background:#f2f3f1}
#app #cover .cv-ai{flex:0 0 32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;color:#fff}
#app #cover .cv-a1{background:#2d5161}
#app #cover .cv-a2{background:#d5573b}
#app #cover .cv-a3{background:#7d8a66}
#app #cover .cv-t{flex:1}
#app #cover .cv-ch{color:#b5432a;flex:0 0 auto}
#app #cover .cv-fam{display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin:11px 0 0}
#app #cover .cv-fl{font:600 14px var(--font-body);color:#5d6b70;margin-right:2px}
#app #cover .cv-c{padding:4px 11px;border-radius:999px;background:#f2f3f1;border:1px solid #dfe3e6;color:#2d5161;font:700 13.5px var(--font-body)}
#app #cover .nav-start{background:#2d5161!important;border-color:#2d5161!important;color:#fff!important;box-shadow:0 2px 8px rgba(45,81,97,.3)!important;animation:none!important}
@media screen and (max-height:600px){
  #app #cover .cv-band{min-height:54px;padding:6px 16px}
  #app #cover .cv-sheet{padding:12px 16px 8px}
  #app #cover h1{font-size:28px;margin:2px 0}
  #app #cover .cv-sub{margin-bottom:8px;font-size:17px}
  #app #cover .cv-rows a{min-height:44px}
  #app #cover .cv-icon{width:64px;height:64px;top:-32px;border-radius:17px}
}
@media (prefers-color-scheme:dark){
  #app #cover .scroll{background:#16232a}
  #app #cover .cv-sheet{background:#1c2b33;box-shadow:0 -10px 30px rgba(0,0,0,.4)}
  #app #cover .cv-net{stroke:#ffffff;stroke-opacity:.07}
  #app #cover .cv-icon{border-color:#1c2b33;background:#1c2b33}
  #app #cover .cv-k{color:#f2b3a3}
  #app #cover .cv-ver{color:#b7c4ca}
  #app #cover h1{color:#fff}
  #app #cover .cv-sub{color:#dfe9ee}
  #app #cover .cv-rows{background:#24353e;border-color:#33464f}
  #app #cover .cv-rows a{color:#fff}
  #app #cover .cv-rows a+a{border-color:#33464f}
  #app #cover .cv-ch{color:#f2b3a3}
  #app #cover .cv-fl{color:#b7c4ca}
  #app #cover .cv-c{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.3);color:#fff}
  #app #cover .nav-start{background:#3a6a7f!important;border-color:#3a6a7f!important}
}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v3.11', 'Carer role v3.12'); rep('Version 3.11 iPhone', 'Version 3.12 iPhone')
rep('>3.11 – REVIEW DRAFT', '>3.12 – REVIEW DRAFT')
assert s.count('<div>Version 3.11</div>') == 0
old = re.search(r'<div class="rr"><span class="rv">3\.09</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.11</span>', '<div class="rr"><span class="rv">3.12</span><span class="rd">20 Nov 2026</span><p>New cover in GMCA colours; trial improvements (3.10, 3.11) made live</p></div>\n<div class="rr"><span class="rv">3.11</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
