"""Guide 2.53 (from 2.52).
1. Home Screen app: web app manifest, icons and iPhone tags; a service worker keeps a copy of the
   guide so it opens without a signal (website only; a downloaded copy is unchanged).
2. Search: a Search page (id search) opened from a Search button in the Contents title box.
   It searches the titles and words of every page; results scroll inside the page.
3. Dark Mode: follows the iPhone's Light/Dark setting (screen only; printing stays light).
usage: python3 make253.py v2.52.html v2.53.html
"""
import re, sys, colorsys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cssparse import parse
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def page(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S)
    assert m, pid
    return m

def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# ---------------------------------------------------------------- 1. Home Screen app
rep('<meta name="theme-color" content="#0f4c8a"/>',
    '<meta name="theme-color" content="#0f4c8a"/>\n'
    '<meta name="color-scheme" content="light dark"/>\n'
    '<link rel="manifest" href="manifest.webmanifest"/>\n'
    '<link rel="apple-touch-icon" href="icons/icon-180.png"/>\n'
    '<meta name="apple-mobile-web-app-capable" content="yes"/>\n'
    '<meta name="mobile-web-app-capable" content="yes"/>\n'
    '<meta name="apple-mobile-web-app-title" content="EY App Guide"/>\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="default"/>')

# ---------------------------------------------------------------- 2. Search
SEARCH_ICON = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2.2"/>'
               '<path d="M12.6 12.6 17 17" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>')
# Search button in the Contents title box (in place of the hidden decorative mark)
edit('contents', '<span class="tp-n" aria-hidden="true">≡</span>',
     '<a class="tp-search" href="#search" aria-label="Search this guide">' + SEARCH_ICON + '<span>Search</span></a>')

nav_r = re.search(r'<nav class="bnav".*?</nav>', page('revisions').group(0), re.S).group(0)
nav_s = nav_r.replace('class="nav-btn nav-back" href="#doc-control"', 'class="nav-btn nav-back" href="#contents" data-hist=""', 1)
nav_s = re.sub(r'class="nav-btn nav-next off" href="#revisions"', 'class="nav-btn nav-next off" href="#search"', nav_s)
nav_s = re.sub(r'aria-label="Contents \(page \d+ of \d+\)"', 'aria-label="Contents"', nav_s)
nav_s = re.sub(r'<span class="count">[^<]*</span>', '<span class="count">Search</span>', nav_s)
assert 'data-hist' in nav_s and 'href="#search"' in nav_s
search = ('<section class="screen" id="search" data-sec="Search" data-title="Search this guide" aria-label="Search this guide">\n'
          '<div class="scroll">\n'
          '<div class="pbox"><h2 class="h2" tabindex="-1">Search this guide</h2></div>\n'
          '<div class="strip" aria-hidden="true"><div class="strip-row"><span>Search</span><span class="pos">All pages</span></div></div>\n'
          '<form class="srch-form" role="search" action="#search">'
          '<label class="srch-vh" for="srch-q">Search this guide</label>'
          '<span class="srch-ico">' + SEARCH_ICON + '</span>'
          '<input id="srch-q" class="srch-q" type="search" placeholder="For example: password" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" enterkeyhint="search"/>'
          '</form>\n'
          '<p class="srch-status" id="srch-status" role="status" aria-live="polite">Type a word, such as <strong>password</strong>, <strong>email</strong> or <strong>link</strong>.</p>\n'
          '<ol class="srch-res" id="srch-res" aria-label="Search results"></ol>\n'
          '<p class="srch-nojs">Search needs JavaScript, which is turned off. Please use <a href="#contents">Contents</a> to find a page.</p>\n'
          '</div>\n' + nav_s + '\n</section>\n')
m = page('revisions')
s = s[:m.end()] + '\n\n' + search + s[m.end():]

# the Contents counter (page N of 72) leaves the Search page out
ids = [i for i in re.findall(r'<section class="screen[^"]*" id="([^"]+)"', s) if i != 'search']
total = len(ids); assert total == 72, total
out = []; last = 0; k = 0
for mm in re.finditer(r'<section class="screen[^"]*" id="([^"]+)".*?</section>', s, re.S):
    if mm.group(1) == 'search': continue
    blk = mm.group(0); k += 1
    blk = re.sub(r'<span class="count">\d+ / \d+</span>', '<span class="count">%d / %d</span>' % (k, total), blk)
    blk = re.sub(r'aria-label="Contents \(page \d+ of \d+\)"', 'aria-label="Contents (page %d of %d)"' % (k, total), blk)
    out.append(s[last:mm.start()]); out.append(blk); last = mm.end()
s = ''.join(out) + s[last:]

css_search = '''/* 2.53 Search: button in the Contents title box, and the Search page */
#contents .tp-body{display:flex;align-items:center}
.tp-search{position:absolute;right:10px;top:50%;transform:translateY(-50%);z-index:2;display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 14px 0 11px;border-radius:18px;background:#fff;color:var(--accent2);font:700 15px/1 var(--font-body);text-decoration:none;box-shadow:0 1px 3px rgba(0,0,0,.18)}
.tp-search::before{content:"";position:absolute;inset:-6px -4px}
.tp-search:focus-visible{outline:3px solid #ffd23f;outline-offset:2px}
#search .scroll{display:flex;flex-direction:column}
.srch-form{position:relative;margin:2px 0 8px}
.srch-vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.srch-ico{position:absolute;left:13px;top:50%;transform:translateY(-50%);color:var(--sub);display:flex;pointer-events:none}
.srch-q{box-sizing:border-box;width:100%;height:46px;padding:0 12px 0 40px;border:1.5px solid var(--accent);border-radius:12px;background:#fff;color:var(--ink);font:400 17px/1.2 var(--font-body);-webkit-appearance:none;appearance:none}
.srch-q::placeholder{color:var(--sub);opacity:1}
.srch-q:focus{outline:3px solid #ffd23f;outline-offset:1px}
.srch-q::-webkit-search-cancel-button{-webkit-appearance:none;appearance:none;height:18px;width:18px;border-radius:50%;background:var(--sub) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M6 6l6 6M12 6l-6 6' stroke='white' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center/18px no-repeat;cursor:pointer}
.srch-status{margin:0 0 6px;font-size:15px;line-height:1.4;color:var(--sub)}
.srch-res{list-style:none;margin:0;padding:0;overflow-y:auto;-webkit-overflow-scrolling:touch;min-height:0;border-top:1px solid var(--line)}
.srch-row{display:block;padding:9px 2px 10px;border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none;min-height:44px}
.srch-row:focus-visible{outline:3px solid var(--ink);outline-offset:-3px;border-radius:6px}
.srch-t{display:block;font-weight:700;font-size:17px;line-height:1.3;color:var(--accent2)}
.srch-s{display:block;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--sub);margin-top:2px}
.srch-x{display:block;font-size:15px;font-weight:400;line-height:1.4;color:var(--ink);margin-top:3px}
.srch-row mark{background:#ffe680;color:#16314f;border-radius:3px;padding:0 1px}
.srch-nojs{display:none;font-size:17px}
html:not(.jsnav) #search .srch-form,html:not(.jsnav) #search .srch-status,html:not(.jsnav) #search .srch-res{display:none}
html:not(.jsnav) #search .srch-nojs{display:block}
'''
rep('@media print{', css_search + '@media print{')
rep('@media print{', '@media print{\n  #search{display:none!important}\n  .tp-search{display:none!important}')

js_search = r'''
/* 2.53 Search: looks through the titles and words of every page */
(function(){
  var d=document, pg=d.getElementById('search'); if(!pg) return;
  var q=d.getElementById('srch-q'), res=d.getElementById('srch-res'), st=d.getElementById('srch-status'), form=pg.querySelector('.srch-form');
  var index=null, probe=null, timer=0;
  var STOP={'the':1,'a':1,'an':1,'to':1,'my':1,'i':1,'of':1,'and':1,'in':1,'on':1,'is':1,'for':1,'how':1,'do':1,'can':1,'what':1,'it':1,'me':1,'with':1,'am':1};
  function norm(t){ return (t||'').toLowerCase().replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/\s+/g,' ').trim(); }
  function build(){
    index=[];
    [].forEach.call(d.querySelectorAll('.stage>.screen'),function(s){
      if(s.id==='search'||s.id==='cover') return;
      var sc=s.querySelector('.scroll'); if(!sc) return;
      var c=sc.cloneNode(true);
      [].forEach.call(c.querySelectorAll('.strip,svg,script,style,[aria-hidden="true"],.srch-form,iframe,.go-wait,h2.h2,select,.hv-seg,.hv-map,.hv-tips'),function(x){ x.parentNode.removeChild(x); });
      /* keep a space between blocks, so words from two lines do not run together */
      [].forEach.call(c.querySelectorAll('p,div,li,h1,h2,h3,h4,label,a,br,td,th,dt,dd,small,span,strong'),function(x){ if(x.parentNode) x.parentNode.insertBefore(d.createTextNode(' '),x.nextSibling); });
      var text=(c.textContent||'').replace(/\s+/g,' ').replace(/\s+([.,;:!?)’'])/g,'$1').replace(/([(‘])\s+/g,'$1').trim();
      var title=s.getAttribute('data-title')||'', sec=s.getAttribute('data-sec')||'';
      index.push({id:s.id,title:title,sec:sec,text:text,nt:norm(text),ntitle:norm(title)});
    });
  }
  function words(v){ var w=norm(v).replace(/[^a-z0-9@.'\- ]/g,' ').split(' ').filter(function(x){ return x.length>0; });
    var k=w.filter(function(x){ return !STOP[x]; }); return (k.length?k:w).filter(function(x){ return x.length>1||/\d/.test(x); }); }
  function count(h,n){ var c=0,i=h.indexOf(n); while(i>=0&&c<6){ c++; i=h.indexOf(n,i+n.length); } return c; }
  function snippet(e,ws){
    var at=-1,len=0; ws.forEach(function(w){ var i=e.nt.indexOf(w); if(i>=0&&(at<0||i<at)){ at=i; len=w.length; } });
    if(at<0) return e.text.slice(0,110)+(e.text.length>110?'…':'');
    var a=Math.max(0,at-45), b=Math.min(e.text.length,at+len+80);
    while(a>0&&e.text[a-1]!==' '&&at-a<60) a--; while(b<e.text.length&&e.text[b]!==' '&&b-at<140) b++;
    return (a>0?'…':'')+e.text.slice(a,b).trim()+(b<e.text.length?'…':'');
  }
  function mark(el,txt,ws){
    var lt=norm(txt).length===txt.length?norm(txt):txt.toLowerCase(), pos=0, hits=[];
    ws.forEach(function(w){ var i=lt.indexOf(w); while(i>=0){ hits.push([i,i+w.length]); i=lt.indexOf(w,i+w.length); } });
    hits.sort(function(x,y){ return x[0]-y[0]; });
    hits.forEach(function(h){ if(h[0]<pos) return; el.appendChild(d.createTextNode(txt.slice(pos,h[0]))); var m=d.createElement('mark'); m.textContent=txt.slice(h[0],h[1]); el.appendChild(m); pos=h[1]; });
    el.appendChild(d.createTextNode(txt.slice(pos)));
  }
  function visH(){
    var H=window.innerHeight;
    try{
      if(!probe){ probe=d.createElement('div'); probe.setAttribute('aria-hidden','true'); probe.style.cssText='position:fixed;top:0;left:0;width:0;height:100dvh;visibility:hidden;pointer-events:none'; d.body.appendChild(probe); }
      var ph=probe.getBoundingClientRect().height; if(ph>200) H=Math.min(H,ph);
      var vv=window.visualViewport; if(vv&&vv.height>200&&Math.abs((vv.scale||1)-1)<0.01) H=Math.min(H,vv.height);
    }catch(e){}
    return Math.floor(H);
  }
  /* the results list scrolls inside the page, so the page itself never needs scrolling */
  function fitRes(){
    if(!pg.classList.contains('on')) return;
    var se=d.scrollingElement||d.documentElement;
    res.style.maxHeight='none';
    var h=res.getBoundingClientRect().height, over=se.scrollHeight-visH();
    if(over>0) res.style.maxHeight=Math.max(96,Math.floor(h-over-2))+'px';
  }
  function run(){
    if(!index) build();
    var v=q.value, ws=words(v);
    while(res.firstChild) res.removeChild(res.firstChild);
    if(!ws.length){ st.innerHTML='Type a word, such as <strong>password</strong>, <strong>email</strong> or <strong>link</strong>.'; fitRes(); return; }
    var found=[];
    index.forEach(function(e){
      var ok=true, score=0;
      ws.forEach(function(w){ var t=count(e.ntitle,w), x=count(e.nt,w); if(!t&&!x) ok=false; score+=t*20+Math.min(x,5); });
      if(ok) found.push({e:e,score:score});
    });
    found.sort(function(a,b){ return b.score-a.score; });
    found.slice(0,40).forEach(function(f){
      var e=f.e, li=d.createElement('li'), a=d.createElement('a');
      a.className='srch-row'; a.href='#'+e.id;
      var t=d.createElement('span'); t.className='srch-t'; mark(t,e.title,ws);
      var sc=d.createElement('span'); sc.className='srch-s'; sc.textContent=e.sec;
      var x=d.createElement('span'); x.className='srch-x'; mark(x,snippet(e,ws),ws);
      a.appendChild(t); a.appendChild(sc); a.appendChild(x); li.appendChild(a); res.appendChild(li);
    });
    st.textContent=found.length?(found.length===1?'1 page found.':found.length+' pages found.')+' Tap a page to open it.'
                               :'No pages found for “'+v.trim()+'”. Try another word, or use Contents.';
    res.scrollTop=0; fitRes();
  }
  q.addEventListener('input',function(){ clearTimeout(timer); timer=setTimeout(run,120); });
  form.addEventListener('submit',function(e){ e.preventDefault(); run(); try{ q.blur(); }catch(x){} });
  window.addEventListener('resize',function(){ setTimeout(fitRes,80); });
  if(window.visualViewport){ try{ window.visualViewport.addEventListener('resize',function(){ setTimeout(fitRes,80); }); }catch(e){} }
  new MutationObserver(function(){ if(pg.classList.contains('on')){ if(!index) build(); setTimeout(fitRes,90); } }).observe(pg,{attributes:true,attributeFilter:['class']});
})();

/* 2.53 Home Screen app: keep a copy of the guide on the iPhone so it opens without a signal (website only) */
if('serviceWorker' in navigator && location.protocol==='https:'){
  window.addEventListener('load',function(){ navigator.serviceWorker.register('sw.js').catch(function(){}); });
}
'''
rep('})();\n</script>\n\n</body>', '})();\n' + js_search + '</script>\n\n</body>')

# ---------------------------------------------------------------- 3. Dark Mode
def hx(c):
    c = c.lstrip('#')
    if len(c) == 3: c = ''.join(x * 2 for x in c)
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
def tohex(r, g, b): return '#%02x%02x%02x' % tuple(max(0, min(255, round(v * 255))) for v in (r, g, b))
def hls(c): return colorsys.rgb_to_hls(*c)
FIXED = {'#fff': '#111821', '#ffffff': '#111821'}
def keep_bright(h, l, s_): return s_ > 0.85 and 0.45 < l < 0.75     # yellows like the highlight stay as they are
def map_bg(c):
    if c in FIXED: return FIXED[c]
    h, l, s_ = hls(hx(c))
    if keep_bright(h, l, s_) or l < 0.62: return c
    if l >= 0.80: nl = 0.105 + (1 - l) * 0.55
    else: nl = 0.24
    return tohex(*colorsys.hls_to_rgb(h, nl, s_ * 0.45))
def map_text(c):
    h, l, s_ = hls(hx(c))
    if l <= 0.5: return tohex(*colorsys.hls_to_rgb(h, 0.90 - l * 0.35, min(1, s_ * 0.7)))
    return c
def map_border(c):
    h, l, s_ = hls(hx(c))
    if keep_bright(h, l, s_): return c
    if l >= 0.62: return tohex(*colorsys.hls_to_rgb(h, 0.30, s_ * 0.5))
    if l < 0.35: return tohex(*colorsys.hls_to_rgb(h, 0.75, s_ * 0.6))
    return c
LIGHT_RGBA = re.compile(r'rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*([.\d]+)\s*\)')
HEX = re.compile(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b')
def kind(p):
    p = p.strip().lower()
    if p in ('background', 'background-color', 'background-image'): return 'bg'
    if p in ('color', 'fill', 'stroke', 'caret-color', 'text-decoration-color', '-webkit-text-fill-color'): return 'text'
    if p.startswith('border') or p.startswith('outline'): return 'border'
    return None
def lum(c): return hls(hx(c))[1]

css = s[s.index('<style'):s.index('</style>')]; css = css[css.index('>') + 1:]
dark = []   # (media, selector, decls)
for media, sel, decls in parse(css):
    if media and 'print' in media: continue
    if not sel or sel.startswith('@') or sel.startswith(':root') or 'from' == sel or 'to' == sel or re.match(r'^[\d.%, ]+$', sel): continue
    out = []; bg_kept_light = False; texts = []
    for decl in decls.split(';'):
        if ':' not in decl: continue
        p, v = decl.split(':', 1); k = kind(p)
        if not k: continue
        nv = v
        if k == 'bg':
            def f(m_):
                c = m_.group(0).lower(); n = map_bg(c)
                return n
            nv = HEX.sub(f, nv)
            nv = LIGHT_RGBA.sub(lambda m_: 'rgba(17,24,33,%s)' % m_.group(1), nv)
            nv = nv.replace('var(--accent)', 'var(--accentFill)').replace('var(--accent2)', 'var(--accent2Fill)')
            lits = HEX.findall(nv)
            if lits and all(lum(x) > 0.55 for x in lits): bg_kept_light = True
        elif k == 'text':
            texts.append((p, v))
            nv = HEX.sub(lambda m_: map_text(m_.group(0).lower()), nv)
        elif k == 'border':
            nv = HEX.sub(lambda m_: map_border(m_.group(0).lower()), nv)
        if nv != v: out.append('%s:%s' % (p.strip(), nv.strip()))
    if bg_kept_light:   # a bright background that stays bright keeps its dark text
        out = [o for o in out if kind(o.split(':', 1)[0]) != 'text']
        if not texts: out.append('color:#16314f')
        else: out += ['%s:%s' % (p.strip(), v.strip().replace('var(--ink)', '#16314f').replace('var(--sub)', '#54677d')) for p, v in texts]
    if out: dark.append((media, sel, ';'.join(out)))

DARK_ROOT = ''':root{color-scheme:dark;
  --ink:#e3eaf2; --sub:#a9b7c7; --accent:#6aaeea; --accent2:#9ccaf2; --accentSoft:#16283b;
  --surface:#151c24; --line:#2b3846; --headerBg:#0f4c8a; --headerSub:#bcd6ef; --hl:#ffd23f;
  --backdrop:#0a0f14; --dots:#3b4a5a; --amberBg:#33290c; --amberInk:#f3cf74;
  --accentFill:#1d6fb8; --accent2Fill:#0e4f86}'''
blocks = {}
for media, sel, decls in dark:
    blocks.setdefault(media, []).append('%s{%s}' % (sel, decls))
dcss = ['/* 2.53 Dark Mode: follows the iPhone setting. Made by make253.py from the light styles. */',
        '@media screen and (prefers-color-scheme:dark){\n' + DARK_ROOT + '\n' + '\n'.join(blocks.pop(None, [])) + '\n}']
for media, rules in blocks.items():
    parts = [p.strip() for p in media.split(',')]
    q = ', '.join('screen and (prefers-color-scheme:dark) and ' + (p[len('screen and '):] if p.startswith('screen and ') else p) for p in parts)
    dcss.append('@media %s{\n%s\n}' % (q, '\n'.join(rules)))
DARK_EXTRA = '''@media screen and (prefers-color-scheme:dark){
  .tp-search{background:#e3eaf2;color:#0e4f86}
  .srch-q{background:#0d141c}
  .srch-row mark{background:#ffd23f;color:#16314f}
  .shot img,.crop img{filter:brightness(.92)}
  .cover-bar{background:#0b1118;color:#e3eaf2;border-top:1px solid var(--line)}
  .cover-bar i{background:var(--accent)}
  .srch-q::-webkit-search-cancel-button{background:var(--sub) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M6 6l6 6M12 6l-6 6' stroke='%23111821' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center/18px no-repeat}
}'''
rep('@media print{', '\n'.join(dcss) + '\n' + DARK_EXTRA + '\n@media print{')
print('dark rules', len(dark))

# ---------------------------------------------------------------- version
rep('Carer role v2.52', 'Carer role v2.53'); rep('Version 2.52 iPhone', 'Version 2.53 iPhone')
rep('<div>Version 2.52</div>', '<div>Version 2.53</div>'); rep('>2.52 – REVIEW DRAFT', '>2.53 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.50</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.52</span>', '<div class="rr"><span class="rv">2.53</span><span class="rd">16 Nov 2026</span><p>Search; Dark Mode; works offline from the Home Screen</p></div>\n<div class="rr"><span class="rv">2.52</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst)
