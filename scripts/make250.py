"""Guide 2.50 (from 2.49).
1. Your Health Visiting team (both copies): every address can be tapped. It opens a map in the
   team card, with a Contact details / Map switch. A note under the card says how to see the map
   and how to call.
2. Checklist Information 2 of 2 (Who can sign in?): new wording; yellow box for the partner line.
usage: python3 make250.py v2.49.html v2.50.html
"""
import re, sys, html
from urllib.parse import quote_plus
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)

def page(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S)
    assert m, pid
    return m

ADDR = re.compile(r'<div class="hv-addr">(<svg[^>]*>.*?</svg>)<span>(.*?)</span></div>', re.S)
CARD = re.compile(r'<div class="hv-card (hv-c-([A-Za-z]+)-(\d+))">\n(<h3>.*?</h3>)\n(.*?)\n</div>\n(?=<div class="hv-card|</div>)', re.S)

def do_hv(pid, sel):
    """sel: the prefix of that page's select ids (hvs on #hv, hv on #s5-hv)"""
    global s
    m = page(pid); b = m.group(0); n = 0
    def card(cm):
        nonlocal n
        cls, loc, idx, h3, body = cm.groups()
        am = ADDR.search(body); assert am, cls
        svg, addr = am.groups()
        q = quote_plus(html.unescape(addr))
        key = 'hvv-%s-%s-%s' % (sel, loc, idx)
        det = body[:am.start()] + ('<label class="hv-addr" for="%s-m">%s<span>%s</span></label>' % (key, svg, addr)) + body[am.end():]
        n += 1
        return ('<div class="hv-card %s">\n%s\n'
                '<input type="radio" class="hv-v hv-v-c" name="%s" id="%s-c" checked>'
                '<input type="radio" class="hv-v hv-v-m" name="%s" id="%s-m">\n'
                '<div class="hv-seg"><label for="%s-c">Contact details</label><label for="%s-m">Map</label></div>\n'
                '<div class="hv-det">\n%s\n</div>\n'
                '<div class="hv-map"><div class="hv-mapbox"><iframe title="Map showing %s" data-map="https://maps.google.com/maps?q=%s&amp;z=15&amp;output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe>'
                '<p class="hv-map-off">Tap <strong>Open in Maps</strong> to see this address on a map.</p></div>'
                '<a class="hv-open" href="https://maps.apple.com/?q=%s" target="_blank" rel="noopener">Open in Maps<svg aria-hidden="true" viewBox="0 0 20 20" width="15" height="15"><path d="M8 4H4v12h12v-4M11 4h5v5M16 4l-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a></div>\n'
                '</div>\n') % (cls, h3, key, key, key, key, key, key, det, addr, q, q)
    b2 = CARD.sub(card, b)
    assert n == 23, (pid, n)
    tips = ('<div class="hv-tips"><p>To view on a map, tap the address.</p>'
            '<p>To call, tap the contact number.</p></div>\n')
    # the tips go straight after the card list (.hv-cards): find its closing tag by counting divs
    st = b2.find('<div class="hv-cards"'); assert st > 0 and b2.count('<div class="hv-cards"') == 1
    depth = 0
    for t in re.finditer(r'<div\b|</div>', b2[st:]):
        depth += 1 if t.group(0) == '<div' else -1
        if depth == 0:
            end = st + t.end(); break
    assert b2[end] == '\n'; end += 1
    b2 = b2[:end] + tips + b2[end:]
    s = s[:m.start()] + b2 + s[m.end():]
    return n

print('cards', do_hv('hv', 'hvs'), do_hv('s5-hv', 'hv'))

# the tips show only while a team card is shown
show = []
for pid, sel in (('hv', 'hvs'), ('s5-hv', 'hv')):
    for loc in ('Bury', 'Rochdale', 'Stockport'):
        show.append('#%s:has(#%s-loc option[value="%s"]:checked):has(#%s-team-%s option:not([value=""]):checked) .hv-tips'
                    % (pid, sel, loc, sel, loc))
css = '''/* 2.50 team cards: tap the address for a map; Contact details / Map switch; how-to note under the card */
.hv-v{position:absolute;width:1px;height:1px;margin:0;opacity:0;pointer-events:none}
.hv-seg{display:none;margin:6px 0 8px;padding:2px;border:1.5px solid #a9c7e6;border-radius:11px;background:#fff}
.hv-seg label{flex:1 1 50%;display:flex;align-items:center;justify-content:center;min-height:34px;padding:4px 6px;border-radius:8px;font-weight:700;font-size:15px;line-height:1.2;color:var(--accent);cursor:pointer;-webkit-tap-highlight-color:transparent}
.hv-v-c:checked~.hv-seg label:first-child,.hv-v-m:checked~.hv-seg label:last-child{background:var(--accent);color:#fff}
.hv-v:focus-visible~.hv-seg{outline:3px solid #ffd23f;outline-offset:1px}
label.hv-addr{cursor:pointer;-webkit-tap-highlight-color:rgba(15,76,138,.12)}
label.hv-addr span{color:var(--accent);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
.hv-map{display:none}
.hv-v-m:checked~.hv-det{display:none}
.hv-v-m:checked~.hv-map{display:block}
.hv-v-m:checked~.hv-seg{display:flex}
.hv-mapbox{position:relative;height:var(--maph,clamp(140px,calc(100dvh - 470px),240px));border-radius:10px;overflow:hidden;background:#e4ecf5;border:1px solid #c9d8ea}
.hv-mapbox::before{content:"Loading map\\2026";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:15px;color:var(--sub)}
.hv-mapbox iframe{position:relative;display:block;width:100%;height:100%;border:0}
.hv-mapbox iframe:not([src]){display:none}
.hv-map-off{display:none;position:relative;margin:0;padding:0 16px;height:100%;align-items:center;justify-content:center;text-align:center;font-size:15px;line-height:1.4;color:var(--ink);background:#e4ecf5}
.hv-mapbox:has(iframe:not([src])) .hv-map-off{display:flex}
.hv-mapbox:has(iframe:not([src]))::before{content:none}
.hv-open{display:inline-flex;align-items:center;gap:6px;min-height:36px;margin-top:4px;font-weight:700;font-size:15px;color:var(--accent);text-decoration:underline;text-underline-offset:3px}
.hv-tips{display:none;margin-top:14px}
.hv-tips p{font-size:15px;line-height:1.4;color:var(--sub);margin:0}
''' + ',\n'.join(show) + '''{display:block}
.hv-cards:has(.hv-v-m:checked)+.hv-tips{display:none!important}
#hv .hv-card:has(.hv-v-m:checked) h3,#s5-hv .hv-card:has(.hv-v-m:checked) h3{margin-bottom:2px!important}
@media (max-height:700px){ .hv-tips{margin-top:10px} }
@media (max-width:369px){ .hv-tips{margin-top:4px} .hv-tips p{line-height:1.33} }
'''
rep('@media print{', css + '@media print{')
pcss = '''
  .hv-seg,.hv-map,.hv-tips,.hv-v{display:none!important}
  .hv-det{display:block!important}
  label.hv-addr span{color:inherit!important;text-decoration:none!important}'''
rep('@media print{', '@media print{' + pcss)

# map: load the map only when it is first opened; a new team choice shows contact details again
js = '''
/* 2.50 team cards: the map loads the first time it is opened and fills the space left on the screen;
   choosing a team starts on contact details */
(function(){
  var d=document, probe=null;
  function visH(){
    var H=window.innerHeight;
    try{
      if(!probe){ probe=d.createElement('div'); probe.setAttribute('aria-hidden','true'); probe.style.cssText='position:fixed;top:0;left:0;width:0;height:100dvh;visibility:hidden;pointer-events:none'; d.body.appendChild(probe); }
      var ph=probe.getBoundingClientRect().height; if(ph>200) H=Math.min(H,ph);
      var vv=window.visualViewport; if(vv&&vv.height>200&&Math.abs((vv.scale||1)-1)<0.01) H=Math.min(H,vv.height);
    }catch(e){}
    return Math.floor(H);
  }
  function fitMap(){
    var r=d.querySelector('.screen.on .hv-v-m:checked'); if(!r) return;
    var card=r.closest('.hv-card'); if(!card||card.offsetParent===null) return;
    var se=d.scrollingElement||d.documentElement;
    card.style.setProperty('--maph','260px');
    var over=se.scrollHeight-visH();
    if(over>0) card.style.setProperty('--maph',Math.max(130,260-over-2)+'px');
  }
  window.addEventListener('resize',function(){ setTimeout(fitMap,80); });
  if(window.visualViewport){ try{ window.visualViewport.addEventListener('resize',function(){ setTimeout(fitMap,80); }); }catch(e){} }
  d.addEventListener('change',function(e){
    var t=e.target; if(!t||!t.classList) return;
    if(t.classList.contains('hv-v-m')&&t.checked){
      var f=t.closest('.hv-card').querySelector('iframe[data-map]');
      if(f&&!f.getAttribute('src')) f.setAttribute('src',f.getAttribute('data-map'));
      fitMap();
    }
    if(t.tagName==='SELECT'&&t.closest('.hv-find')){
      [].forEach.call(t.closest('.screen').querySelectorAll('.hv-v-c'),function(r){ r.checked=true; });
    }
  });
})();
'''
rep('})();\n</script>\n\n</body>', '})();\n' + js + '</script>\n\n</body>')

# 2. Information 2 of 2
m = page('ci2'); b = m.group(0)
old = ('<p class="info-lead">Only the <strong>account holder</strong> can sign in to the GM Early Years App account. A partner or another family member cannot sign in to the account.</p>\n'
       '<div class="tip info-q"><p>To sign in, the account holder uses the same <strong>email address</strong> and <strong>password</strong> as their own NHS login account.</p></div>\n')
new = ('<p class="info-lead ci2-p">Only the <strong>account holder</strong> (the child\'s mother or primary carer) can sign in to their GM Early Years App account.</p>\n'
       '<p class="info-lead ci2-p">To sign in, the account holder uses the same <strong>email address</strong> and <strong>password</strong> as their own NHS login account.</p>\n'
       '<div class="amber info-q ci2-amber"><p>A partner or another family member cannot sign in to the account.</p></div>\n')
assert b.count(old) == 1
s = s[:m.start()] + b.replace(old, new) + s[m.end():]
rep('@media print{', '#ci2 .ci2-p{margin-bottom:10px}\n#ci2 .ci2-amber{margin-top:4px;margin-bottom:14px}\n@media print{')

# version
rep('Carer role v2.49', 'Carer role v2.50'); rep('Version 2.49 iPhone', 'Version 2.50 iPhone')
rep('<div>Version 2.49</div>', '<div>Version 2.50</div>'); rep('>2.49 – REVIEW DRAFT', '>2.50 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.47</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.49</span>', '<div class="rr"><span class="rv">2.50</span><span class="rd">16 Nov 2026</span><p>Team addresses open a map; new wording on Who can sign in?</p></div>\n<div class="rr"><span class="rv">2.49</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst)
