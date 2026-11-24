"""3.87 navigation fixes for the Sign-in check results. usage: nav_fix.py src out
1. Results page: the bottom button is always Next and always goes to Section 4 Signing in (#s3), whatever the answers
   (it used to say Done and go to Support when anything was red, and Back from Support then went to "You are signed in").
2. Side trips: when a Sign-in check, Signing in or Support page sends you to a Health Visiting team or Contacts page
   (hv, s5-hv, s5-2, s5-gmdp) through a link on the page, that page's right-hand button becomes
   "Done" and takes you back to where you were (as the GMDP help page already does). Reached any other way
   (Contents, Search, Next/Back in page order) those pages work as before."""
import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:100], s.count(x)); s = s.replace(x, y)
ARROW = '<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
# 1. results page: one Next, always to Signing in
i = s.index('id="tsum"'); j = s.index('</section>', i)
sec = s[i:j]
a = sec.index('<div class="nx">'); b = sec.index('</div></nav>', a)
new_nx = '<div class="nx"><a class="nav-btn nav-next tsum-next" href="#s3" aria-label="Next – Signing in to the GM Early Years App"><span>Next</span>' + ARROW + '</a>'
sec2 = sec[:a] + new_nx + sec[b:]
sec2 = sec2.replace('<input type="radio" class="nudge-t" id="nw-tsum" name="nw-tsum" tabindex="-1" aria-hidden="true"/>\n', '')
s = s[:i] + sec2 + s[j:]
# 2. side-trip Done buttons
TRIP = ['hv', 's5-hv', 's5-2', 's5-gmdp']
for pid in TRIP:
    i = s.index(f'id="{pid}" data-sec='); j = s.index('</section>', i)
    sec = s[i:j]; k = sec.rindex('</nav>')
    done = (f'<a class="nav-btn nav-next nav-done trip-done" href="#{pid}" data-start="{pid}" '
            f'aria-label="Done – go back to where you were"><span>Done</span>{ARROW}</a>')
    s = s[:i] + sec[:k] + done + sec[k:] + s[j:]
css = '''
/* 3.87 results page: always one Next to Signing in */
#app #tsum .bnav .tsum-next{display:inline-flex!important}
/* 3.87 side trips: Done takes you back to where you were */
#app .bnav .trip-done{display:none!important}
#app .screen.trip .bnav .trip-done{display:inline-flex!important}
#app .screen.trip .bnav .nav-next:not(.trip-done){display:none!important}
'''
s = s.replace('</style>', css + '</style>', 1)
js = '''
<script>
/* 3.87 side trips: a Health Visiting team or Contacts page opened by a link on a Sign-in check, Signing in or
   Support page gets a Done button back to where you were; reached any other way it works as before */
(function(){
  var TRIP={'hv':1,'s5-hv':1,'s5-2':1,'s5-gmdp':1};
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href^="#"]'); if(!a) return;
    var id=a.getAttribute('href').slice(1); if(!TRIP[id]) return;
    var t=document.getElementById(id), cur=document.querySelector('.screen.on'); if(!t||!cur||t===cur) return;
    var sec=cur.getAttribute('data-sec')||'';
    var fromPage=!a.closest('.bnav') && /^Section [345]\\b/.test(sec) && !t.classList.contains('trip-keep');
    t.classList.toggle('trip', fromPage);
  }, true);
})();
</script>
'''
s = s.replace('</body>', js + '</body>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
