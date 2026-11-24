"""Title box mock-up (design review point 1). usage: tb.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
SEC = re.compile(r'<section class="screen[^"]*" id="([^"]+)"[^>]*?data-sec="([^"]*)".*?</section>', re.S)
TOPIC = {'ts1': 'Your App account', 'ts1b': 'Your App account', 'ts2': 'Your NHS login', 'ts3': 'Your NHS login', 'ts4': 'Both accounts', 'ts5': 'Both accounts'}
out = []; last = 0; added = 0
for m in SEC.finditer(s):
    i, sec = m.group(1), m.group(2); blk = m.group(0)
    if i in ('cover', 'contents'):
        continue
    a = blk.find('<div class="pbox'); b = blk.find('<div class="tp-body')
    st = a if a >= 0 and (b < 0 or a < b) else b
    if st < 0: continue
    h2 = blk.find('<h2', st)
    head = blk[st:h2]
    if i in TOPIC:
        blk2 = re.sub(r'(<div class="kicker part">)(Question \d of 6)(</div>)', lambda x: x.group(1) + TOPIC[i] + ' · ' + x.group(2) + x.group(3), blk, count=1)
    elif re.search(r'class="(kicker[^"]*|stg|tb-band|eyb[^"]*)"', head):
        blk2 = blk
        k = re.search(r'<div class="kicker part">([^<]*)</div>', head); vh = re.search(r'<span class="vh">Step (\d+) of (\d+): </span>', blk)
        if k and vh and not re.search(r'\d', k.group(1)):
            blk2 = blk.replace(k.group(0), '<div class="kicker part">%s · Step %s of %s</div>' % (k.group(1), vh.group(1), vh.group(2)), 1)
    else:
        name = sec.split(' · ', 1)[1] if ' · ' in sec else sec
        title = re.sub(r'<[^>]+>', '', blk[h2:blk.find('</h2>', h2)]).lower()
        if name.lower() in title:
            name = sec.split(' · ', 1)[0] if sec.startswith('Section') else ''
        if name:
            blk2 = blk[:h2] + '<div class="kicker tb-loc">%s</div>' % name + blk[h2:]; added += 1
        else:
            blk2 = blk
    out.append((m.start(), m.end(), blk2))
for a, b, blk2 in reversed(out):
    s = s[:a] + blk2 + s[b:]
css = '''
/* design review 1: calmer title box – no underline, fainter blocks, place shown once (in the box) */
#app .screen:not(#cover) .pbox::after,#app .screen .tp-body::after{display:none!important}
#app .screen .pbox::before,#app .screen .tp-body::before{opacity:.07!important}
#app .screen:not(#cover) .strip{display:none!important}
#app .screen .pbox .kicker.tb-loc,#app .screen .tp-body .kicker.tb-loc{display:block!important;position:absolute!important;top:20px!important;left:16px!important;right:70px!important;margin:0!important;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#app .screen .pbox.nhs-band .kicker.tb-loc,#app .screen .pbox.eyx-nhs .kicker.tb-loc{display:none!important}
#app .screen .scroll>.pbox,#app .screen .scroll>.tp-card{margin-bottom:14px!important}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok, labels added:', added)
