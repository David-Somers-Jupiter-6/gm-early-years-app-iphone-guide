"""Design review 4: capitals only in the title box; bold only for on-screen names, headings and warnings.
usage: cb.py src out unbold.json   (unbold.json: {section_id: [indexes of <strong>/<b> to unbold]})"""
import re, sys, json
s = open(sys.argv[1], encoding='utf-8').read(); un = json.load(open(sys.argv[3]))
SEC = re.compile(r'<section class="screen[^"]*" id="([^"]+)".*?</section>', re.S)
TAG = re.compile(r'<(strong|b)(?=[\s>])([^>]*)>')
out = []; total = 0
for m in SEC.finditer(s):
    idx = set(un.get(m.group(1), []))
    if not idx: continue
    blk = m.group(0); k = -1
    def f(t):
        global total
        nonlocal_k[0] += 1
        if nonlocal_k[0] in idx:
            total_[0] += 1
            a = t.group(2)
            if 'class="' in a: return '<%s%s>' % (t.group(1), a.replace('class="', 'class="nb ', 1))
            return '<%s class="nb"%s>' % (t.group(1), a)
        return t.group(0)
    nonlocal_k = [-1]; total_ = [0]
    blk2 = TAG.sub(f, blk); total += total_[0]
    assert total_[0] == len(idx), (m.group(1), total_[0], len(idx))
    out.append((m.start(), m.end(), blk2))
for a, b, blk2 in reversed(out): s = s[:a] + blk2 + s[b:]
LBL = '.abc-k,.th-k,.k,.lbl,.dk,.toc-st,.hw-k,.tsp-gh,.tsp-k,.jr-k,.srch-tk,.q-count,.eyebrow,.tag,.pill,.m-sec'
css = '''
/* design review 4: capitals only for the one label in the title box; labels on the page in sentence case */
#app .screen:not(#cover) .scroll :is(LBL):not(.pbox *,.tp-body *,.tp-card *){text-transform:none!important;letter-spacing:0!important;font-size:15px!important;font-weight:600!important}
#app .screen .scroll :is(.toc-st,.tsp-gh,.srch-tk):not(.pbox *){font-size:15px!important;font-weight:600!important;color:var(--sub)!important}
#app .screen .scroll .lbl:not(.pbox *){font-size:15px!important}
/* bold only where it names something on screen: emphasis words go back to regular */
#app .screen :is(strong,b).nb{font-weight:inherit!important}
@media screen and (max-height:700px){#app .screen .scroll :is(.toc-st,.tsp-gh):not(.pbox *){font-size:13px!important;line-height:1.15!important;margin-top:3px!important;margin-bottom:2px!important}}
'''.replace('LBL', LBL)
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok, unbolded', total)
