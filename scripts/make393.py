"""Guide 3.93 (from 3.92) – Installing the App: tapping a step's picture plays a short clip of that step,
then shows the highlighted screenshot (with Play again).
usage: python3 make393.py v3.92.html v3.93.html [--embed CLIPS_DIR]
  --embed puts the clips inside the file (for the copy shared in the chat); the website loads them from clips/."""
import re, sys, os, json, base64
src, dst = sys.argv[1], sys.argv[2]
embed = sys.argv[sys.argv.index('--embed') + 1] if '--embed' in sys.argv else None
s = open(src, encoding='utf-8').read()

def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)

rep('content="Version 3.92. A screen-by-screen', 'content="Version 3.93. A screen-by-screen')
rep('>3.92 (iPhone edition)<', '>3.93 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.92</span>', '<span class="cv-ver">Version 3.93</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.88</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.92</span>', '<div class="rr"><span class="rv">3.93</span><span class="rd">28 Nov 2026</span><p>Installing the App: tap a step’s picture to watch a short clip of it</p></div>\n<div class="rr"><span class="rv">3.92</span>')

# intro page of Installing the App
rep('<p class="info-lead">Install the GM Early Years App from the App Store in 7 steps. Follow them in order.</p>',
    '<p class="info-lead">Install the GM Early Years App from the App Store in 7 steps. Follow them in order. Tap the picture on a step to watch a short clip of it.</p>')

PLAY = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="16" height="16"><circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<path d="M8.2 6.6v6.8l5.4-3.4z" fill="currentColor"/></svg>')
AGAIN = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="16" height="16"><path d="M4.5 10a5.5 5.5 0 1 0 1.8-4.1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
         '<path d="M5.6 2.8v3.6h3.6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
CLIPS = {'z-in06': 'inst-1', 'z-in10': 'inst-3', 'z-in13': 'inst-4', 'z-in15': 'inst-5', 'z-in17': 'inst-6', 'z-in18': 'inst-7'}
for zid, clip in CLIPS.items():
    i = s.index(f'<input type="checkbox" class="zt" id="{zid}"'); j = s.index('</label>', i) + len('</label>')
    blk = s[i:j]
    assert blk.count('aria-label="Show the whole screen: ') == 1 and blk.count('</span><span class="zoom"') == 1
    blk = blk.replace('aria-label="Show the whole screen: ', 'aria-label="Watch a short clip of this step, then see the whole screen: ')
    blk = blk.replace(f'<label class="shot" for="{zid}"', f'<label class="shot has-clip" for="{zid}" data-clip="{clip}"')
    blk = re.sub(r'(<img [^>]*/>)</span><span class="zoom"',
                 r'\1<video class="clip" muted playsinline preload="none" width="418" height="904" aria-hidden="true"></video></span><span class="zoom"', blk)
    blk = re.sub(r'<span class="zoom" aria-hidden="true"><svg.*?</svg>Tap to enlarge</span>',
                 f'<span class="zoom" aria-hidden="true">{PLAY}Tap to watch</span>', blk)
    blk = blk.replace('<span class="zoom-close" aria-hidden="true">Tap anywhere to close</span>',
                      f'<span class="zrow"><span class="clip-again" role="button" tabindex="0">{AGAIN}<span class="ca-t">Play again</span></span>'
                      '<span class="zoom-close" aria-hidden="true">Tap anywhere to close</span></span>')
    assert 'Tap to watch' in blk and 'clip-again' in blk and '<video' in blk, zid
    s = s[:i] + blk + s[j:]

CSS = '''
/* 3.93 Installing the App: a short clip plays in the whole-screen view, then the highlighted screenshot */
.shot .clip,.shot .zrow{display:none}
.zt:checked+.shot .zrow{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.zt:checked+.shot.clip-playing .crop img{display:none}
.zt:checked+.shot.clip-playing .crop .clip{display:block;width:auto;height:auto;max-width:100%;max-height:calc(100vh - 110px);max-height:calc(100dvh - 110px);border-radius:12px;background:#fff}
.zt:checked+.shot.clip-done .crop img{animation:clipIn .4s ease-out}
@keyframes clipIn{from{opacity:0}to{opacity:1}}
.clip-again{display:none}
.zt:checked+.shot.clip-done:not(.clip-none) .clip-again{display:inline-flex;align-items:center;gap:7px;background:var(--accent);color:#fff;border-radius:999px;padding:10px 18px;font-weight:700;font-size:15px;cursor:pointer;min-height:44px;box-sizing:border-box}
.zt:checked+.shot.clip-done .zoom-close{min-height:44px;box-sizing:border-box;align-items:center}
.clip-again:focus-visible{outline:3px solid #fff;outline-offset:3px}
.shot.has-clip .zoom svg{flex:none}
@media (prefers-reduced-motion:reduce){.zt:checked+.shot.clip-done .crop img{animation:none}}
'''
rep('.zt:checked+.shot .zoom{display:none}', '.zt:checked+.shot .zoom{display:none}' + CSS)

JS = r'''<script>
/* 3.93 Installing the App: tapping a step's picture plays its clip, then shows the screenshot */
(function(){
  var d=document, shots=d.querySelectorAll('.shot.has-clip'), emb=null;
  if(!shots.length||!d.createElement('video').canPlayType) return;
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function base(){ return /\/preview\/(index\.html)?$/.test(location.pathname)?'../clips/':'clips/'; }
  function url(n){
    if(emb===null){ var e=d.getElementById('clip-data'); try{ emb=e?JSON.parse(e.textContent):{}; }catch(x){ emb={}; } }
    if(emb[n]){ var b=atob(emb[n]), a=new Uint8Array(b.length); for(var i=0;i<b.length;i++) a[i]=b.charCodeAt(i);
      return URL.createObjectURL(new Blob([a],{type:'video/mp4'})); }
    return base()+n+'.mp4';
  }
  function zt(shot){ return d.getElementById(shot.getAttribute('for')); }
  function label(shot,t){ var c=shot.querySelector('.ca-t'); if(c) c.textContent=t; }
  function done(shot){ shot.classList.remove('clip-playing'); shot.classList.add('clip-done'); }
  function stop(shot){ var v=shot.querySelector('.clip'); try{ v.pause(); }catch(x){} shot.classList.remove('clip-playing','clip-done'); }
  function play(shot){
    var v=shot.querySelector('.clip');
    if(shot.classList.contains('clip-none')){ done(shot); return; }
    if(!v.getAttribute('src')) v.src=url(shot.getAttribute('data-clip'));
    shot.classList.remove('clip-done'); label(shot,'Play again');
    try{ v.currentTime=0; }catch(x){}
    var p=v.play(); if(p&&p.catch) p.catch(function(){ done(shot); });
  }
  function sync(){ for(var i=0;i<shots.length;i++){ var z=zt(shots[i]); if(z&&!z.checked&&shots[i].className.indexOf('clip-')>-1) stop(shots[i]); } }
  Array.prototype.forEach.call(shots,function(shot){
    var v=shot.querySelector('.clip'), z=zt(shot), b=shot.querySelector('.clip-again');
    v.addEventListener('playing',function(){ if(z.checked) shot.classList.add('clip-playing'); });
    v.addEventListener('ended',function(){ done(shot); });
    v.addEventListener('error',function(){ shot.classList.add('clip-none'); done(shot); });   /* no clip (offline or saved copy): the screenshot shows as before */
    z.addEventListener('change',function(){
      if(!z.checked){ stop(shot); return; }
      if(still){ label(shot,'Play clip'); done(shot); } else play(shot);
    });
    function again(e){ e.preventDefault(); e.stopPropagation(); play(shot); }
    b.addEventListener('click',again);
    b.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' ') again(e); });
  });
  ['hashchange','popstate','pageshow'].forEach(function(t){ window.addEventListener(t,function(){ setTimeout(sync,0); }); });
  d.addEventListener('click',function(){ setTimeout(sync,0); });
  d.addEventListener('keydown',function(){ setTimeout(sync,0); });
})();
</script>
'''
k = s.rindex('</body>')
data = ''
if embed:
    m = {n: base64.b64encode(open(os.path.join(embed, n + '.mp4'), 'rb').read()).decode() for n in CLIPS.values()}
    data = '<script type="application/json" id="clip-data">' + json.dumps(m) + '</script>\n'
s = s[:k] + data + JS + s[k:]
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
