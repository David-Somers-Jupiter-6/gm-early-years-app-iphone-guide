"""Guide 3.01 (from 3.00). David, 19 Nov: "Contact your HV team" (Section 2, `hv`) title box changed from the NHS-blue
Health Visiting team band to the GM Early Years App title box (app colours, faint ABC blocks), like About your account,
with the Stage 1 of 3 marker (first page of a section). The Contact & support copy (`s5-hv`) is unchanged.
usage: python3 make301.py v3.00.html v3.01.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
stg = re.search(r'<div class="pbox tp-stg">(<div class="stg">.*?</div>)<h2 class="h2" tabindex="-1">About your account</h2>', s, re.S).group(1)
assert 'Stage 1 of 3 · What you need' in stg
rep('<div class="pbox eyx eyx-nhs eyx-hv"><div class="eyb eyb-nhs" aria-hidden="true"><i class="eym"></i><b>Health Visiting team</b><span>Stage 1 of 3</span></div><span class="tp-n" aria-hidden="true">2</span><h2 class="h2" tabindex="-1">Contact your HV team</h2></div>',
    '<div class="pbox tp-stg">' + stg + '<h2 class="h2" tabindex="-1">Contact your HV team</h2></div>')
rep('Carer role v3.00', 'Carer role v3.01'); rep('Version 3.00 iPhone', 'Version 3.01 iPhone')
rep('<div>Version 3.00</div>', '<div>Version 3.01</div>'); rep('>3.00 – REVIEW DRAFT', '>3.01 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.98</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.00</span>', '<div class="rr"><span class="rv">3.01</span><span class="rd">19 Nov 2026</span><p>Contact your HV team: GM Early Years App title box</p></div>\n<div class="rr"><span class="rv">3.00</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
