"""Guide 3.09 (from 3.08). David, 20 Nov: better Search, and a microphone button.
 - Plain-language matching: everyday words map to the guide's words (login/log in -> sign in, text -> message,
   forgot/lost -> forgotten/reset, phone -> mobile, download -> install, shortcut/icon -> Home Screen ...),
   plurals, and more everyday filler words ignored (didn't, get, my, still ...)
 - Forgiving spelling: a word found nowhere in the guide is matched to the closest word in the guide
   ("pasword" -> password), and the status line says so
 - Questions in a sentence: if no page has every word, pages with the most of the words are shown
 - Quick topic buttons under the search box (shown while the box is empty)
 - Revision history and Document control left out of search results
 - No results: "Still need help?" and Troubleshooting buttons
 - Microphone button in the search box (website in Safari only; speech goes through Apple's own speech service,
   with the iPhone's permission prompts). If voice search cannot run (Home Screen app, Claude app, permission refused,
   nothing heard), the button hides and the carer is told to use the microphone on the iPhone keyboard.
usage: python3 make309.py v3.08.html v3.09.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

MIC = ('<button type="button" class="srch-mic" id="srch-mic" aria-label="Search by voice" hidden>'
       '<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
       '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0013 0M12 17.5V21"/></svg></button>')
rep('enterkeyhint="search"/></form>', 'enterkeyhint="search"/>' + MIC + '</form>')
TOPICS = [('s4-pw', 'Forgotten password'), ('s4-activation', 'No Activation Link'), ('s4-code', 'Security code'),
          ('inst', 'Install the App'), ('a2hs', 'Add to Home Screen'), ('hv', 'Contact your HV team')]
rep('<p class="srch-status" id="srch-status" role="status" aria-live="polite">Type a word, such as <strong>password</strong>, <strong>email</strong> or <strong>link</strong>.</p>',
    '<p class="srch-status" id="srch-status" role="status" aria-live="polite">Type a word, such as <strong>password</strong>, <strong>email</strong> or <strong>link</strong>.</p>\n'
    '<div class="srch-topics"><p class="srch-tk">Popular topics</p><nav aria-label="Popular topics" class="srch-tl">' +
    ''.join('<a class="srch-tp" href="#%s">%s</a>' % t for t in TOPICS) + '</nav></div>\n'
    '<div class="srch-none" id="srch-none" hidden><a class="srch-nb" href="#s4">Troubleshooting</a><a class="srch-nb srch-nb2" href="#s4-help">Still need help?</a></div>')

# --- JavaScript ---
rep("  var STOP={'the':1,'a':1,'an':1,'to':1,'my':1,'i':1,'of':1,'and':1,'in':1,'on':1,'is':1,'for':1,'how':1,'do':1,'can':1,'what':1,'it':1,'me':1,'with':1,'am':1};",
r"""  var STOP={'the':1,'a':1,'an':1,'to':1,'my':1,'i':1,'of':1,'and':1,'in':1,'on':1,'is':1,'for':1,'how':1,'do':1,'can':1,'what':1,'it':1,'me':1,'with':1,'am':1,
    'i\'m':1,'im':1,'didn\'t':1,'didnt':1,'did':1,'don\'t':1,'dont':1,'does':1,'doesn\'t':1,'not':1,'no':1,'get':1,'got':1,'getting':1,'have':1,'has':1,'had':1,
    'haven\'t':1,'why':1,'where':1,'when':1,'will':1,'won\'t':1,'can\'t':1,'cant':1,'cannot':1,'was':1,'are':1,'be':1,'been':1,'this':1,'that':1,'there':1,
    'your':1,'you':1,'still':1,'need':1,'want':1,'please':1,'just':1,'yet':1,'any':1,'from':1,'at':1,'or':1,'but':1,'so':1,'if':1,'into':1,'up':1,'our':1,'we':1,'should':1,'would':1,'could':1,'which':1,'who':1,'about':1};
  /* everyday words -> the words the guide uses (any one of them counts) */
  var SYN={'login':['sign in','log in','login'],'logon':['sign in'],'signin':['sign in'],'log':['sign in','log in'],'sign':['sign'],'signing':['sign'],
    'password':['password'],'passcode':['password','passcode'],'pw':['password'],'pword':['password'],'pin':['code','pin'],
    'text':['text','message'],'texts':['text','message'],'sms':['text','message'],'message':['message','text'],'messages':['message','text'],
    'code':['code'],'codes':['code'],'otp':['code'],'verification':['verification','code'],'verify':['verif','code'],
    'email':['email'],'e-mail':['email'],'emails':['email'],'mail':['email'],'inbox':['email'],
    'phone':['mobile','phone'],'mobile':['mobile'],'number':['number'],'iphone':['iphone'],
    'install':['install'],'installing':['install'],'download':['download','install'],'downloading':['download','install'],
    'application':['app'],'apps':['app'],'appstore':['app store'],'store':['app store'],
    'forgot':['forgot','forgotten','reset'],'forgotten':['forgot','forgotten','reset'],'lost':['forgot','forgotten','reset'],'reset':['reset','forgot'],'remember':['forgot','forgotten'],
    'hv':['health visiting','hv'],'visitor':['health visiting'],'visitors':['health visiting'],'visiting':['health visiting'],
    'contact':['contact','call'],'call':['call','contact'],'ring':['call','contact'],'support':['support','help'],'helpline':['support','contact'],
    'shortcut':['home screen'],'icon':['icon','home screen'],'desktop':['home screen'],'homescreen':['home screen'],'bookmark':['home screen'],
    'cookie':['cookie'],'cookies':['cookie'],'surname':['name'],'married':['name has changed','name'],
    'husband':['partner'],'wife':['partner'],'dad':['partner'],'father':['partner'],'boyfriend':['partner'],'girlfriend':['partner'],
    'activation':['activation'],'activate':['activation'],'link':['link'],'links':['link'],
    'locked':['cannot sign in','locked'],'error':['error','troubleshooting','problem'],'problem':['problem','troubleshooting'],'problems':['problem','troubleshooting'],
    'faceid':['face id'],'details':['details'],'match':['match'],'wrong':['match','wrong']};
  var vocab=null;""")

rep(r"""  function words(v){ var w=norm(v).replace(/[^a-z0-9@.'\- ]/g,' ').split(' ').filter(function(x){ return x.length>0; });
    var k=w.filter(function(x){ return !STOP[x]; }); return (k.length?k:w).filter(function(x){ return x.length>1||/\d/.test(x); }); }""",
r"""  function words(v){ var w=norm(v).replace(/[^a-z0-9@.'\- ]/g,' ').split(' ').filter(function(x){ return x.length>0; });
    var k=w.filter(function(x){ return !STOP[x]; }); return (k.length?k:w).filter(function(x){ return x.length>1||/\d/.test(x); }); }
  /* each word becomes a term: the word itself, its everyday alternatives, and the singular of a plural */
  function terms(v){ return words(v).map(function(w){ var a=(SYN[w]||[w]).slice(); if(a.indexOf(w)<0&&!SYN[w]) a.push(w);
      if(!SYN[w]&&w.length>3&&/s$/.test(w)) a.push(w.slice(0,-1));
      if(!SYN[w]&&w.length>4&&/ed$/.test(w)){ a.push(w.slice(0,-2)); a.push(w.slice(0,-1)); }
      if(!SYN[w]&&w.length>5&&/ing$/.test(w)) a.push(w.slice(0,-3));
      return {w:w,alts:a}; }); }
  function dist(a,b,max){ if(Math.abs(a.length-b.length)>max) return max+1; var p=[],i,j; for(j=0;j<=b.length;j++) p[j]=j;
    for(i=1;i<=a.length;i++){ var c=[i],lo=i; for(j=1;j<=b.length;j++){ c[j]=Math.min(p[j]+1,c[j-1]+1,p[j-1]+(a[i-1]===b[j-1]?0:1)); if(c[j]<lo) lo=c[j]; } if(lo>max) return max+1; p=c; } return p[b.length]; }
  function closest(w){ if(w.length<4||/\d/.test(w)) return null; if(!vocab){ vocab={}; index.forEach(function(e){ (e.nt+' '+e.ntitle).split(/[^a-z0-9']+/).forEach(function(t){ if(t.length>=3) vocab[t]=(vocab[t]||0)+1; }); }); }
    var max=w.length>=6?2:1, best=null, bd=max+1, bn=0; for(var t in vocab){ var dd=dist(w,t,max); if(dd<bd||(dd===bd&&vocab[t]>bn)){ best=t; bd=dd; bn=vocab[t]; } } return bd<=max?best:null; }
  function hits(e,alts){ var t=0,x=0; alts.forEach(function(a){ t=Math.max(t,count(e.ntitle,a)); x=Math.max(x,count(e.nt,a)); }); return [t,x]; }""")

# revision history and document control are not useful search results for carers
rep("if(s.id==='search'||s.id==='cover') return;", "if(s.id==='search'||s.id==='cover'||s.id==='revisions'||s.id==='doc-control') return;")
old_run = s[s.find("  function run(){"):s.find("  q.addEventListener('input'")]
assert old_run.count('function run(){') == 1
NEW_RUN = r"""  var none=d.getElementById('srch-none'), mic=d.getElementById('srch-mic'), hasMic=false;
  function hint(){ st.innerHTML=hasMic?'Type, or tap the <strong>microphone</strong> and say what you need help with.'
                                     :'Type a word, such as <strong>password</strong>, <strong>email</strong> or <strong>link</strong>. To speak, use the <strong>microphone on your keyboard</strong>.'; }
  function run(){
    if(!index) build();
    var v=q.value, ts=terms(v), fixed=[];
    while(res.firstChild) res.removeChild(res.firstChild);
    none.hidden=true; pg.classList.toggle('srch-empty',!ts.length);
    if(!ts.length){ hint(); fitRes(); return; }
    /* forgiving spelling: a word found nowhere in the guide takes the closest word that is */
    ts.forEach(function(t){ if(!index.some(function(e){ var h=hits(e,t.alts); return h[0]||h[1]; })){ var c=closest(t.w); if(c){ t.alts=[c]; fixed.push(c); } } });
    var all=[], some=[];
    index.forEach(function(e){
      var n=0, score=0;
      ts.forEach(function(t){ var h=hits(e,t.alts); if(h[0]||h[1]) n++; score+=h[0]*20+Math.min(h[1],5); });
      if(n===ts.length) all.push({e:e,score:score}); else if(n>0) some.push({e:e,score:score+n*100,n:n});
    });
    var found=all, partial=false;
    if(!all.length&&ts.length>1&&some.length){ found=some; partial=true; }
    found.sort(function(a,b){ return b.score-a.score; });
    var hl=[]; ts.forEach(function(t){ t.alts.forEach(function(a){ if(hl.indexOf(a)<0) hl.push(a); }); });
    found.slice(0,40).forEach(function(f){
      var e=f.e, li=d.createElement('li'), a=d.createElement('a');
      a.className='srch-row'; a.href='#'+e.id;
      var t=d.createElement('span'); t.className='srch-t'; mark(t,e.title,hl);
      var sc=d.createElement('span'); sc.className='srch-s'; sc.textContent=e.sec;
      var x=d.createElement('span'); x.className='srch-x'; mark(x,snippet(e,hl),hl);
      a.appendChild(t); a.appendChild(sc); a.appendChild(x); li.appendChild(a); res.appendChild(li);
    });
    var lead=fixed.length?'Showing results for “'+fixed.join(' ')+'”. ':'';
    if(!found.length){ st.textContent='No pages found for “'+v.trim()+'”. Try other words, or get help:'; none.hidden=false; }
    else st.textContent=lead+(partial?'No page has all your words. These pages have some of them.':(found.length===1?'1 page found.':found.length+' pages found.'))+' Tap a page to open it.';
    res.scrollTop=0; fitRes();
  }
  /* microphone: Safari's speech recognition, website only; anything else falls back to the keyboard microphone */
  (function(){
    var SR=window.SpeechRecognition||window.webkitSpeechRecognition, rec=null, on=false, got=false, mt=0;
    var home=false; try{ home=(window.matchMedia&&window.matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true; }catch(e){}
    if(!SR||!mic||location.protocol!=='https:'||home) return;
    hasMic=true; mic.hidden=false; pg.classList.add('has-mic');
    function stop(){ on=false; pg.classList.remove('mic-on'); mic.setAttribute('aria-label','Search by voice'); clearTimeout(mt); try{ if(rec) rec.stop(); }catch(e){} }
    function off(){ stop(); hasMic=false; mic.hidden=true; pg.classList.remove('has-mic');
      st.innerHTML='Voice search is not available here. Tap the search box, then the <strong>microphone on your keyboard</strong>, to speak.'; }
    mic.addEventListener('click',function(e){
      e.preventDefault(); if(on){ stop(); if(got) run(); else hint(); return; }
      try{ rec=new SR(); }catch(x){ off(); return; }
      got=false; rec.lang='en-GB'; rec.interimResults=true; rec.continuous=false; rec.maxAlternatives=1;
      rec.onresult=function(ev){ var t=''; for(var i=0;i<ev.results.length;i++) t+=ev.results[i][0].transcript;
        q.value=t.trim(); got=true; clearTimeout(timer);
        if(ev.results[ev.results.length-1].isFinal){ stop(); run(); } else timer=setTimeout(run,150); };
      rec.onerror=function(ev){ var er=ev&&ev.error;
        if(er==='not-allowed'||er==='service-not-allowed'||er==='audio-capture') off();
        else { stop(); if(!got) st.textContent='Sorry, nothing was heard. Tap the microphone and try again.'; } };
      rec.onend=function(){ if(on){ stop(); if(got) run(); else st.textContent='Sorry, nothing was heard. Tap the microphone and try again.'; } };
      on=true; pg.classList.add('mic-on'); mic.setAttribute('aria-label','Stop listening');
      st.innerHTML='<strong>Listening…</strong> Say what you need help with.';
      mt=setTimeout(function(){ if(on&&!got) off(); else if(on){ stop(); run(); } },12000);
      try{ rec.start(); }catch(x){ off(); }
    });
  })();
  pg.classList.add('srch-empty'); hint();
"""
s = s.replace(old_run, NEW_RUN)

CSS = '''/* 3.09 Search: microphone, popular topics, no-results help */
#app #search .srch-mic{position:absolute;right:5px;top:50%;transform:translateY(-50%);width:38px;height:38px;border-radius:50%;border:0;background:var(--accentSoft);color:var(--accent2);display:flex;align-items:center;justify-content:center;padding:0;cursor:pointer;-webkit-appearance:none;appearance:none}
#app #search .srch-mic[hidden]{display:none}
#app #search .srch-mic::before{content:"";position:absolute;inset:-4px}
#app #search.has-mic .srch-q{padding-right:50px}
#app #search.has-mic .srch-q::-webkit-search-cancel-button{display:none}
#app #search.mic-on .srch-mic{background:#d5281b;color:#fff;animation:micPulse 1.2s ease-in-out infinite}
@keyframes micPulse{0%,100%{box-shadow:0 0 0 0 rgba(213,40,27,.45)}50%{box-shadow:0 0 0 8px rgba(213,40,27,0)}}
@media (prefers-reduced-motion:reduce){#app #search.mic-on .srch-mic{animation:none}}
#app #search .srch-topics{display:none;margin-top:6px}
#app #search.srch-empty .srch-topics{display:block}
#app #search.srch-empty .srch-res{border-top:0}
#app #search .srch-tk{margin:0 0 8px;font:700 13px/1.2 var(--font-head);letter-spacing:.06em;text-transform:uppercase;color:var(--sub)}
#app #search .srch-tl{display:flex;flex-wrap:wrap;gap:8px}
#app #search .srch-tp{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:22px;background:var(--accentSoft);color:var(--accent2);border:1.5px solid var(--accent);font-weight:700;font-size:16px;text-decoration:none}
#app #search .srch-none{display:flex;gap:10px;margin:8px 0}
#app #search .srch-none[hidden]{display:none}
#app #search .srch-nb{flex:1;display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:var(--r);border:2px solid var(--accent);color:var(--accent2);font-weight:700;font-size:17px;text-decoration:none;text-align:center}
#app #search .srch-nb2{background:var(--accentFill,var(--accent));border-color:var(--accentFill,var(--accent));color:#fff}
@media screen and (max-height:600px){#app #search .srch-tl{gap:6px}#app #search .srch-tp{min-height:40px;padding:0 12px;font-size:15.5px}}
@media screen and (max-width:369px){#app #search .srch-tp{padding:0 11px;font-size:15.5px}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v3.08', 'Carer role v3.09'); rep('Version 3.08 iPhone', 'Version 3.09 iPhone')
rep('<div>Version 3.08</div>', '<div>Version 3.09</div>'); rep('>3.08 – REVIEW DRAFT', '>3.09 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">3\.06</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.08</span>', '<div class="rr"><span class="rv">3.09</span><span class="rd">20 Nov 2026</span><p>Search: everyday words, spelling, popular topics, voice search</p></div>\n<div class="rr"><span class="rv">3.08</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
