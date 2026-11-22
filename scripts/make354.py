"""Guide 3.54 (from trial 3.53) – TRIAL. David, 22 Nov: question 2's warning reads "A partner or family member
cannot access the account." (was "…cannot sign in to the GM Early Years App account.").
usage: python3 make354.py v3.53.html v3.54.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('A partner or family member cannot sign in to the GM Early Years App account.', 'A partner or family member cannot access the account.')
rep('Carer role v3.53', 'Carer role v3.54'); rep('Version 3.53 iPhone', 'Version 3.54 iPhone')
rep('>3.53 – REVIEW DRAFT', '>3.54 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.53</span>', '<span class="cv-ver">Version 3.54</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.49</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.53</span>', '<div class="rr"><span class="rv">3.54</span><span class="rd">22 Nov 2026</span><p>Question 2: shorter warning</p></div>\n<div class="rr"><span class="rv">3.53</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
