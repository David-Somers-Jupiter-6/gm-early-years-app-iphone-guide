"""3.84 mock-up: shorter Who can help reply (Q1, Q2), shorter results labels, Troubleshooter renamed,
Next taps: no double page-turns, Next kept above the Home Screen gesture area. usage: mock384.py src out [name]"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read(); NAME = sys.argv[3] if len(sys.argv) > 3 else 'Sign-in check'
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
# 1 Who can help reply on questions 1 and 2: two lines
old = '<span class="th-k">Who can help</span><span>Contact <a class="msg-link" href="#hv">Your Health Visiting team</a></span>'
n = s.count(old); assert n == 2, n
rep(old, '<span class="th-k">Who can help · contact</span><span><a class="msg-link" href="#hv">Your Health Visiting team</a></span>', 2)
# 2 results labels: at most two lines
for a, b in [('Who can sign in to the account?', 'Who can sign in?'), ('Do you have an NHS login account?', 'Do you have NHS login?'),
             ('Can you sign in to your NHS login account?', 'Can you sign in to NHS login?'), ('Are your details the same in both accounts?', 'Do your details match?'),
             ('Has your Activation Link arrived?', 'Has your link arrived?')]:
    rep('<p class="sum-l">%s</p>' % a, '<p class="sum-l">%s</p>' % b, 3)
# 3 new name for the Troubleshooter (visible text only, not styles or scripts)
parts = re.split(r'(<style.*?</style>|<script.*?</script>)', s, flags=re.S)
for k in range(0, len(parts), 2):
    p = parts[k]
    p = p.replace('Return to the Troubleshooter', 'Return to the ' + NAME.lower() if NAME[0].isupper() and ' ' in NAME else 'Return to the ' + NAME)
    p = p.replace('Troubleshooter results', NAME + ' results').replace('Troubleshooter question', NAME + ' question').replace('Troubleshooter', NAME)
    parts[k] = p
s = ''.join(parts)
# 4a Next: ignore a second tap that arrives while the page is still changing
rep("  function act(a){\n    if(!a){ nudge(); return; }\n    if(a.classList.contains('off')) return;",
    "  var lastNav=0;\n  function act(a){\n    if(!a){ nudge(); return; }\n    if(a.classList.contains('off')) return;\n    var now=Date.now(); if(now-lastNav<450) return; lastNav=now;")
# 4b Home Screen on iPhones with a home indicator: keep the bottom bar above the swipe-up area
rep("root.classList.add('jsnav');", "root.classList.add('jsnav'); try{ if((navigator.standalone||matchMedia('(display-mode: standalone)').matches)&&Math.max(screen.width,screen.height)>=812) root.classList.add('home-ind'); }catch(e){}")
css = '''
/* 3.84 Who can help reply on questions 1-2: label and link on two lines */
#app :is(#ts1,#ts1b) .ts-help .th-k{white-space:nowrap}
#app :is(#ts1,#ts1b) .ts-help .msg-link{white-space:nowrap}
/* 3.84 Home Screen on iPhones with a home indicator: the bottom bar sits above the swipe-up area */
html.home-ind .bnav{padding-bottom:21px!important}
/* 3.84 Your results on short screens: six answered rows fit */
@media screen and (max-height:700px){#app #tsum .sum-list>li{padding-top:0!important;padding-bottom:0!important}#app #tsum .sum-list .st{min-height:0!important;padding-top:4px!important;padding-bottom:4px!important}#app #tsum .sum-list>li+li{margin-top:5px!important}}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok', NAME)
