import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)

STRIP = re.compile(r'<div class="strip" aria-hidden="true">(<div class="strip-row">.*?</div>)<div class="prog"><i style="width:[\d.]+%"></i></div></div>\n?')
secs = list(re.finditer(r'<section class="screen[^"]*" id="([^"]+)".*?</section>', s, re.S))
out = []; last = 0; counts = {'tp': 0, 'step': 0, 'bar': 0}
for m in secs:
    pid = m.group(1); b = m.group(0)
    if pid != 'cover':
        sm = STRIP.search(b); assert sm, pid
        strip = '<div class="strip" aria-hidden="true">' + sm.group(1) + '</div>'
        b = b[:sm.start()] + b[sm.end():]
        if 'class="tp-card"' in b:
            b, n = re.subn(r'(<div class="tp-card"><div class="tp-body">.*?</div></div>)', lambda x: x.group(1) + '\n' + strip, b, count=1, flags=re.S)
            assert n == 1, pid; counts['tp'] += 1
        elif 'class="step-head' in b:
            stp = re.search(r'<div class="stepper[^"]*" aria-hidden="true">.*?</div>\s*', b, re.S)
            stepper = ''
            if stp:
                stepper = stp.group(0).strip(); b = b[:stp.start()] + b[stp.end():]
            hm = re.search(r'<div class="step-head[^"]*"><span class="badge" aria-hidden="true">(.*?)</span><div>(<div class="kicker[^"]*">.*?</div>)(<h2[^>]*>.*?</h2>)</div></div>', b, re.S)
            assert hm, pid
            box = ('<div class="pbox has-n">' + stepper + '<span class="tp-n" aria-hidden="true">' + hm.group(1) + '</span>'
                   + hm.group(2) + hm.group(3) + '</div>\n' + strip)
            b = b[:hm.start()] + box + b[hm.end():]; counts['step'] += 1
        else:
            hm = re.search(r'(<h2 class="h2" tabindex="-1">.*?</h2>)\s*(?:<div class="bar"></div>|<div class="bar-row"><div class="bar"></div>(<img[^>]*class="nhsbadge sm"[^>]*/?>)</div>)', b, re.S)
            if not hm:
                hm = re.search(r'<div class="title-row">(<h2 class="h2" tabindex="-1">.*?</h2>)\s*(<img[^>]*class="nhsbadge"[^>]*/?>)</div>\s*<div class="bar"></div>', b, re.S)
            assert hm, pid
            img = (hm.group(2) or '').replace('class="nhsbadge"', 'class="nhsbadge sm"')
            box = '<div class="pbox' + (' has-badge' if img else '') + '">' + hm.group(1) + img + '</div>\n' + strip
            b = b[:hm.start()] + box + b[hm.end():]; counts['bar'] += 1
    out.append(s[last:m.start()]); out.append(b); last = m.end()
s = ''.join(out) + s[last:]
print(counts)

css = '''/* 2.48 layout C: no header after the cover; every page opens with a blue box (progress, label, title);
   a quiet section line sits under the box; no thin bar and no page counter */
.jsnav .app:not(:has(#cover.on)) .hdr,html:not(.jsnav) .app:has(.stage>.screen:target:not(#cover)) .hdr{display:none}
#cover .strip{display:none}
.scroll .strip{background:none;border:0;padding:0;margin:10px 0 14px}
.scroll .strip .strip-row{color:var(--accent2)}
.scroll .strip .pos{color:var(--sub)}
.menu-btn .count{display:none!important}
.screen:not(#cover) .scroll{padding-top:16px}
.tp-card{margin-bottom:0!important}
.pbox{position:relative;overflow:hidden;border-radius:14px;padding:12px 16px 18px;background:linear-gradient(135deg,var(--headerBg) 0%,var(--accent) 100%);box-shadow:0 2px 8px rgba(15,76,138,.18);color:#fff}
.pbox::after{content:"";position:absolute;left:16px;bottom:9px;width:44px;height:4px;border-radius:2px;background:var(--headerSub)}
.pbox .tp-n{font-size:104px;bottom:-26px}
.pbox .kicker,.pbox .kicker.part{position:relative;z-index:1;color:var(--headerSub)!important;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin:0 0 1px}
.pbox h2,.pbox h2.h2{position:relative;z-index:1;color:#fff!important;font-family:var(--font-head);font-weight:800;font-size:21.5px!important;line-height:1.2;margin:0;max-width:100%}
.pbox.has-n h2{max-width:86%}
.pbox h2:focus{outline:none}
.pbox.has-badge{padding-bottom:34px}
.pbox.has-badge .nhsbadge{position:absolute;right:14px;bottom:9px;top:auto;transform:none;height:22px;width:auto;margin:0}
.pbox .stepper,.screen .pbox .stepper.chk-steps,.screen[data-sec^="Section 3"] .pbox .stepper{position:relative;z-index:1;margin:0 0 12px!important}
.pbox .stepper span{background:rgba(255,255,255,.28)!important}
.pbox .stepper span.d{background:#5fd38d!important}
.pbox .stepper span.c{background:#fff!important}
.pbox .stepper span.bad{background:#ff7a6e!important}
.screen:has(.ans-yes:checked) .pbox .stepper span.cur{background:#5fd38d!important}
.screen:has(.ans-no:checked) .pbox .stepper span.cur{background:#ff7a6e!important}
'''
rep('@media print{', css + '@media print{')
pcss = '''
  .pbox{background:none!important;box-shadow:none!important;padding:0!important;color:inherit}
  .pbox h2,.pbox h2.h2{color:#16314f!important}
  .pbox .kicker,.pbox .kicker.part{color:var(--sub)!important}
  .pbox::after,.pbox .tp-n{display:none!important}
  .pbox .nhsbadge{position:static!important;transform:none!important;margin-top:6px!important}'''
rep('@media print{', '@media print{' + pcss)
# version
rep('Carer role v2.47', 'Carer role v2.48'); rep('Version 2.47 iPhone', 'Version 2.48 iPhone')
rep('<div>Version 2.47</div>', '<div>Version 2.48</div>'); rep('>2.47 – REVIEW DRAFT', '>2.48 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.45</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.47</span>', '<div class="rr"><span class="rv">2.48</span><span class="rd">16 Nov 2026</span><p>New page layout: header on the cover only; every page opens with a blue title box</p></div>\n<div class="rr"><span class="rv">2.47</span>')
open(dst, 'w', encoding='utf-8').write(s)
