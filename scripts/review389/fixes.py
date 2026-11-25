"""3.89 – Sign-in check questions: the "i" in the round blue icon beside "Please tap an answer, then tap Next." sat
about 4 px above the middle (the circle was enlarged to 28 px in an earlier build but its text line stayed 22 px).
It is now centred in the circle, in light and Dark Mode, at every size.
Also (David, 25 Nov): Sign-in check start page – each of the 6 questions gets a round "?" button on the right that
opens the help page for that question. The pages are the same ones the results page opens for each question:
1 s4-who, 2 s4-2, 3 s4-setup, 4 s4-cannot, 5 s4-problems, 6 s4-activation. Back (or Done) on the help page returns
to the start page. The circle is 26 px (24 px on shorter screens, like the numbers); its tap area is the full height of its row
and 62 px wide, so neighbouring buttons never overlap.
Also (fix 12 from the problems-and-fixes doc, David 25 Nov): the 6 questions on the start page no longer sit on white
cards; they sit on the page background, so only real menus have white rows.
usage: fixes.py src out"""
import sys
s = open(sys.argv[1], encoding='utf-8').read()
css = '''
/* 3.89 hint icon: "i" centred in its 28 px circle */
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-replies>.need-ans .ni{display:grid!important;place-items:center;line-height:1!important;padding:0!important}
'''
import re
help = {1: 's4-who', 2: 's4-2', 3: 's4-setup', 4: 's4-cannot', 5: 's4-problems', 6: 's4-activation'}
i = s.index('<section class="screen" id="ts"'); j = s.index('</section>', i); sec = s[i:j]
def add(m):
    n = int(m.group(1)); q = m.group(2)
    return (f'<li><span class="tsp-n" aria-hidden="true">{n}</span><span class="tsp-t">{q}</span>'
            f'<a class="tsp-help" href="#{help[n]}" aria-label="Help with question {n}: {q}"><span aria-hidden="true">?</span></a></li>')
sec, k = re.subn(r'<li><span class="tsp-n" aria-hidden="true">(\d)</span><span class="tsp-t">([^<]+)</span></li>', add, sec)
assert k == 6, k
s = s[:i] + sec + s[j:]
css += '''
/* 3.89 Sign-in check start: "?" help button on each question */
#app #ts .tsp-list li .tsp-t{flex:1 1 auto;min-width:0}
#app #ts .tsp-list>li{position:relative!important}
#app #ts .tsp-help{flex:0 0 26px;width:26px;height:26px;margin-left:auto;border-radius:50%;display:grid;place-items:center;background:#dde9f6;color:#145a96;font:800 15px/1 var(--font-head);text-decoration:none;-webkit-tap-highlight-color:transparent}
#app #ts .tsp-help::after{content:"";position:absolute;top:0!important;bottom:0!important;height:auto!important;transform:none!important;left:auto!important;right:-14px!important;width:62px}
@media (max-height:700px){#app #ts .tsp-help{flex-basis:24px;width:24px;height:24px;font-size:14px}}
#app #ts .tsp-help:active{background:var(--accent);color:#fff}
@media (prefers-color-scheme:dark){#app #ts .tsp-help{background:#16283b;color:#8cc2f0}}
#app #ts .tsp-help:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
/* 3.89 (fix 12) the 6 questions sit on the page background: no white card, so they don't look like menu rows */
#app #ts ol.tsp-list.tsp-list{background:transparent!important;box-shadow:none!important;border:0!important}
'''
assert s.count('</style>') >= 1
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
