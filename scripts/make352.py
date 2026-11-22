"""Guide 3.52 (from 3.51) – TRIAL. David, 22 Nov: on "Who will be set up with an account", What to do reads
"If an account has been set up for the wrong person, please contact your Health Visiting team.", followed by the
Find your Health Visiting team button.
usage: python3 make352.py v3.51.html v3.52.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<p>The <strong>account holder</strong> signs in with their own NHS login. Not sure? Ask the team.</p>',
    '<p>If an account has been set up for the wrong person, please contact your <strong>Health Visiting team</strong>.</p>')
rep('Carer role v3.51', 'Carer role v3.52'); rep('Version 3.51 iPhone', 'Version 3.52 iPhone')
rep('>3.51 – REVIEW DRAFT', '>3.52 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.51</span>', '<span class="cv-ver">Version 3.52</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.47</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.51</span>', '<div class="rr"><span class="rv">3.52</span><span class="rd">22 Nov 2026</span><p>Who will be set up with an account: What to do</p></div>\n<div class="rr"><span class="rv">3.51</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
