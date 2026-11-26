"""3.92 – Sign-in check: the question box stays in the same place from question 4 to question 5 (David, 26 Nov).
On David's iPhone the question box on question 5 sat slightly lower than on question 4. Question 5's info area
(card + "See an example" preview, 76 px) was exactly the tallest of the six, with no spare room, so any small
difference in how Safari draws it pushed question 5's box down. The preview becomes 56 px (the two account headings
above the blue "See an example · Tap here" bar; the fade over them removed), leaving question 5 at least 19 px of
spare room at all 16 sizes, so the box is set by the other questions and stays put. The alignment also re-runs once
the guide's fonts have loaded. Question box positions are unchanged from 3.91 (iPhone SE in Safari: 2 px higher).
usage: fixes.py src out"""
import sys
s = open(sys.argv[1], encoding='utf-8').read()
css = '''
/* 3.92 question 5: smaller example preview, so question 5 is never the tallest and its question box stays put */
html body #app #ts4.screen .ts-info .ex-peek.ex-peek{height:56px!important}
html body #app #ts4.screen .ts-info .ex-peek.ex-peek::after{display:none!important}
'''
i = s.rindex('</style>'); s = s[:i] + css + s[i:]
old = "window.addEventListener('load',check); window.addEventListener('pageshow',check);"
assert s.count(old) == 1
s = s.replace(old, old + " try{ if(d.fonts&&d.fonts.ready) d.fonts.ready.then(check); }catch(e){}")
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
