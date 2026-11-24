"""3.86 fit fixes for every iPhone size. usage: fit386.py src out
1. Sign-in check questions on shorter screens (Safari, 760 px high and under): the "?" icon sits on the question's
   own line (the separate "Question" label row goes), and "Tap an answer, then tap Next." gives way, so the reply
   after Yes or No shows above the bottom bar.
2. Safety net on every page: if a reply or message would still open below the bottom bar (smallest iPhones), the page
   scrolls just enough to show it."""
import sys
s = open(sys.argv[1], encoding='utf-8').read()
Q = ':is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5)'
css = f'''
/* 3.86: Sign-in check questions fit on shorter screens */
@media (max-height:760px){{
html body #app {Q} .ts-ask p.ts-ask-k.ts-ask-k{{position:absolute!important;left:10px!important;top:9px!important;width:22px!important;height:22px!important;padding:0!important;margin:0!important;font-size:0!important;line-height:0!important;color:transparent!important;overflow:visible}}
html body #app {Q} .ts-ask p.ts-ask-k.ts-ask-k .abc-ic{{left:0!important;top:0!important;font-size:13px!important;line-height:22px!important;color:#fff!important}}
html body #app {Q} .ts-ask .ts-qa.ts-qa{{padding-left:30px!important;min-height:24px}}
html body #app {Q} .ts-ask .q-hint.q-hint{{display:none!important}}
}}
@media screen and (max-height:650px){{
html body #app {Q} .ts-ask label.radio{{min-height:44px!important;padding-top:6px!important;padding-bottom:6px!important}}
html body #app {Q} .ts-ask .ts-replies{{margin-top:6px!important}}
}}
/* 3.86: Sign-in check start page: the compact list (as on shorter screens) also on 701-730 px high (iPhone 11/XR Safari) */
@media screen and (min-height:701px) and (max-height:730px){{
#app #ts .tsp-list>li{{min-height:40px!important;padding-top:4px!important;padding-bottom:4px!important}}
#app #ts .scroll .tsp-gh:not(.pbox *){{font-size:13px!important;line-height:1.15!important;margin-top:3px!important;margin-bottom:2px!important}}
}}
/* 3.86: smallest screens (iPhone SE in Safari): the location label sits above the title instead of over it */
@media screen and (max-height:600px){{
#app .screen .pbox .kicker.tb-loc,#app .screen .tp-body .kicker.tb-loc{{position:static!important;margin:0 0 2px!important;padding-right:56px}}
#app #contents .toc-row .toc-sub,#app #contents .toc-g small{{display:none!important}}
#app #contents .toc-g.toc-tiles{{display:none!important}}
#app #cover .cover-photo{{height:206px!important;min-height:0!important;max-height:206px!important;flex:0 0 206px!important}}
#app #s4-nhs .tr-list>li,#app #s4-nhs .tr-list>a,#app #s4-nhs .tr-list .tr{{min-height:43px!important}}
#app #s4-nhs .scroll>.pbox{{margin-bottom:8px!important}}
#app #s4-nhs .info-lead{{margin-bottom:2px!important}}
#app #ts .tsp-who{{padding-top:6px!important;padding-bottom:6px!important}}
#app #doc-control .dcgrid{{row-gap:4px!important}}
#app #doc-control .dc{{padding-top:5px!important;padding-bottom:5px!important}}
}}
'''
js = '''
<script>
/* 3.86: if a reply or message opens below the bottom bar, scroll just enough to show it */
(function(){
  function show(sc){
    var on=document.querySelector('.screen.on'); if(!on) return;
    var nav=on.querySelector('.bnav'); if(!nav) return;
    var navTop=nav.getBoundingClientRect().top, low=0;
    on.querySelectorAll('.ts-replies > *, .need-ans').forEach(function(e){
      if(!e.getClientRects().length || getComputedStyle(e).display=='none') return;
      var b=e.getBoundingClientRect().bottom; if(b>low) low=b; });
    if(low>navTop-6) window.scrollBy({top:low-navTop+10, behavior: sc ? 'auto' : 'smooth'});
  }
  document.addEventListener('change', function(ev){ if(ev.target && ev.target.matches('input.ans, input.nudge-t')) setTimeout(show, 60); }, true);
  document.addEventListener('click', function(ev){ if(ev.target && ev.target.closest && ev.target.closest('.bnav .go-wait, .bnav label.nav-next')) setTimeout(show, 80); }, true);
})();
</script>
'''
s = s.replace('</style>', css + '</style>', 1)
assert s.count('</body>') == 1
s = s.replace('</body>', js + '</body>')
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
