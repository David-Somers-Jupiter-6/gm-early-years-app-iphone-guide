(function(){
  var d=document, root=d.documentElement;
  root.classList.add('js');
  try{ if((navigator.standalone||matchMedia('(display-mode: standalone)').matches)&&Math.max(screen.width,screen.height)>=812) root.classList.add('home-ind'); }catch(e){}
  var screens=[].slice.call(d.querySelectorAll('.screen')), ids=screens.map(function(s){return s.id});
  var HELP={help:1,contacts:1,a11y:1};
  var trail=[], pendingOpen=null;

  function show(){
    var id=decodeURIComponent(location.hash.slice(1));
    if(ids.indexOf(id)<0) id='cover';
    if(trail.length>1 && trail[trail.length-2]===id) trail.pop();
    else if(trail[trail.length-1]!==id) trail.push(id);
    screens.forEach(function(s){ s.classList.toggle('on', s.id===id); });
    var s=d.getElementById(id), sc=s.querySelector('.scroll'); if(sc) sc.scrollTop=0;
    if(id==='help'){
      d.querySelectorAll('.plist details').forEach(function(x){ x.open=(pendingOpen&&x.id===pendingOpen); });
      if(pendingOpen){ var o=d.getElementById(pendingOpen); setTimeout(function(){ o&&o.scrollIntoView({block:'nearest'}); },60); }
      pendingOpen=null;
    }
    var h=s.querySelector('h1,h2'); if(h&&trail.length>1) try{ h.focus({preventScroll:true}); }catch(e){}
  }
  window.addEventListener('hashchange',show);
  show();

  d.addEventListener('click',function(e){
    var a=e.target.closest('a'); if(!a) return;
    if(a.hasAttribute('data-open')) pendingOpen=a.getAttribute('data-open')||null;
    if(a.hasAttribute('data-back') && trail.length>1){ e.preventDefault(); location.hash=trail[trail.length-2]; return; }
    if(a.hasAttribute('data-done')){
      for(var i=trail.length-1;i>=0;i--){ if(!HELP[trail[i]]){ e.preventDefault(); var t=trail[i]; trail=trail.slice(0,i); location.hash=t; return; } }
    }
  });

  /* screenshots: tap to see full size */
  var zoom=d.getElementById('zoom'), zimg=zoom.querySelector('img'), lastShot=null;
  d.querySelectorAll('.shot').forEach(function(b){
    b.addEventListener('click',function(){ var i=b.querySelector('img'); zimg.src=i.src; zimg.alt=i.alt; lastShot=b; zoom.hidden=false; zoom.setAttribute('tabindex','-1'); zoom.focus(); });
  });
  function unzoom(){ if(zoom.hidden) return; zoom.hidden=true; if(lastShot) lastShot.focus(); }
  zoom.addEventListener('click',unzoom);
  d.addEventListener('keydown',function(e){ if(e.key==='Escape') unzoom(); });
  window.addEventListener('hashchange',function(){ zoom.hidden=true; });

  /* one problem open at a time */
  d.querySelectorAll('.plist details').forEach(function(x){
    x.addEventListener('toggle',function(){ if(x.open){ d.querySelectorAll('.plist details').forEach(function(y){ if(y!==x) y.open=false; }); } });
  });

  /* Health Visiting team finder */
  var DATA=/*DATA*/null;
  var areas=d.querySelectorAll('.area'), wrap=d.querySelector('.teamwrap'), sel=d.getElementById('team'), hint=d.getElementById('ahint'), card=d.getElementById('teamcard'), area='';
  var I={
    tel:'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 3h3l2 5-2.5 1.5a11 11 0 005 5L14 12l5 2v3a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z"/></svg>',
    pin:'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0113 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/></svg>',
    clock:'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
  };
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]}); }
  areas.forEach(function(b){
    b.addEventListener('click',function(){
      area=b.getAttribute('data-area');
      areas.forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
      sel.innerHTML='<option value="">Choose your team</option>'+DATA.teams[area].map(function(t,i){ return '<option value="'+i+'">'+esc(t.o)+'</option>'; }).join('');
      hint.textContent=DATA.hints[area]||'';
      wrap.hidden=false; card.hidden=true; card.innerHTML='';
    });
  });
  sel.addEventListener('change',function(){
    var t=DATA.teams[area]&&DATA.teams[area][sel.value];
    if(!t){ card.hidden=true; card.innerHTML=''; return; }
    card.innerHTML='<h4>'+esc(t.n)+'</h4>'+
      '<a class="go" href="tel:'+esc(t.tel)+'">'+I.tel+' Call '+esc(t.td)+'</a>'+
      '<p class="row">'+I.clock+'<span>'+esc(t.h)+'</span></p>'+
      '<p class="row">'+I.pin+'<span>'+esc(t.a)+' <a class="maps" href="'+esc(t.m)+'" target="_blank" rel="noopener">Open in Maps</a></span></p>';
    card.hidden=false;
    setTimeout(function(){ card.scrollIntoView({block:'nearest',behavior:'smooth'}); },60);
  });

  /* Home Screen: keep a copy so the guide opens without a signal (website only) */
  if('serviceWorker' in navigator && location.protocol==='https:'){
    window.addEventListener('load',function(){ navigator.serviceWorker.register('sw.js').catch(function(){}); });
  }
})();
