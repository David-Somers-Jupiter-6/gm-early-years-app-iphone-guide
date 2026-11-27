(function(){
  var d=document, root=d.documentElement;
  root.classList.add('js');
  try{ if((navigator.standalone||matchMedia('(display-mode: standalone)').matches)&&Math.max(screen.width,screen.height)>=812) root.classList.add('home-ind'); }catch(e){}
  var screens=[].slice.call(d.querySelectorAll('.screen')), ids=screens.map(function(s){return s.id});
  var HELP={help:1,contacts:1,a11y:1};
  var trail=[], pendingOpen=null, pendingHV=false;

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
    if(id==='contacts' && pendingHV){ var hv=s.querySelector('.ccard'); hv.classList.add('flash'); setTimeout(function(){ hv.classList.remove('flash'); },2600); }
    pendingHV=false;
    fitShots();
    var h=s.querySelector('h1,h2'); if(h&&trail.length>1) try{ h.focus({preventScroll:true}); }catch(e){}
  }
  /* small screens: show the highlighted part of each screenshot, full width */
  function fitShots(){
    d.querySelectorAll('.screen.on .shot img').forEach(function(i){
      var box=i.getBoundingClientRect(); if(!i.naturalWidth||!box.width) return;
      if(innerHeight>600){ i.style.objectFit=''; i.style.objectPosition=''; return; }
      var sc=box.width/i.naturalWidth, h=i.naturalHeight*sc, top=parseFloat(i.getAttribute('data-focus')||0)*h;
      top=Math.max(0,Math.min(top,h-box.height));
      i.style.objectFit='cover'; i.style.objectPosition='50% '+(-top)+'px';
    });
  }
  window.addEventListener('resize',fitShots); window.addEventListener('load',fitShots);
  window.addEventListener('hashchange',show);
  show();

  d.addEventListener('click',function(e){
    var a=e.target.closest('a'); if(!a) return;
    if(a.hasAttribute('data-open')) pendingOpen=a.getAttribute('data-open')||null;
    if(a.hasAttribute('data-hv')) pendingHV=true;
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

  /* swipe left for Next, right for Back (like turning a page) */
  var sx=null, sy=null, st=0;
  d.addEventListener('touchstart',function(e){
    var t=e.target;
    if(e.touches.length!==1 || !zoom.hidden || t.closest('select,input,textarea,.areas')){ sx=null; return; }
    sx=e.touches[0].clientX; sy=e.touches[0].clientY; st=Date.now();
  },{passive:true});
  d.addEventListener('touchend',function(e){
    if(sx===null) return;
    var dx=e.changedTouches[0].clientX-sx, dy=e.changedTouches[0].clientY-sy; sx=null;
    if(Date.now()-st>700 || Math.abs(dx)<70 || Math.abs(dx)<Math.abs(dy)*1.8) return;
    var s=d.querySelector('.screen.on'); if(!s) return;
    var btn=s.querySelector(dx<0 ? '.bnav .btn-next, .bnav .btn-start' : '.bnav .btn-back');
    if(btn) btn.click();
  },{passive:true});

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
      wrap.classList.remove('off'); sel.disabled=false; card.hidden=true; card.innerHTML='';
    });
  });
  /* if the chosen team name would be cut off, shrink the box text a little (17 down to 15 at most) */
  var meas=d.createElement('span'); meas.setAttribute('aria-hidden','true'); meas.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;font-weight:600;left:-9999px';
  d.body.appendChild(meas);
  function fitSel(){
    sel.style.fontSize=''; var o=sel.options[sel.selectedIndex]; if(!o||!sel.clientWidth) return;
    var cs=getComputedStyle(sel), avail=sel.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight)-12;
    meas.style.fontFamily=cs.fontFamily; meas.textContent=o.textContent;
    for(var fs=17; fs>=15; fs--){ meas.style.fontSize=fs+'px'; if(meas.getBoundingClientRect().width<=avail){ sel.style.fontSize=fs+'px'; return; } }
    sel.style.fontSize='15px';
  }
  window.addEventListener('resize',fitSel);
  sel.addEventListener('change',fitSel);
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
