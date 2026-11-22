"""Guide 3.56 (from trial 3.55) – TRIAL. David, 22 Nov, question 2 (Who has access?):
 - the warning "A partner or family member cannot access the account." is removed (and its styles).
usage: python3 make356.py v3.55.html v3.56.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<p class="q-why ts-warn"><span class="tw-i" aria-hidden="true">!</span><span><span class="vh">Warning: </span>A partner or family member cannot access the account.</span></p>', '')
rep('/* 3.48 question 2: warning line */\n', '')
s, n = re.subn(r'#app #ts1b \.ts-warn[^\n]*\n', '', s); assert n == 2, n
assert 'ts-warn' not in s and 'tw-i' not in s
rep('Carer role v3.55', 'Carer role v3.56'); rep('Version 3.55 iPhone', 'Version 3.56 iPhone')
rep('>3.55 – REVIEW DRAFT', '>3.56 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.55</span>', '<span class="cv-ver">Version 3.56</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.51</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.55</span>', '<div class="rr"><span class="rv">3.56</span><span class="rd">22 Nov 2026</span><p>Question 2: partner or family member warning removed</p></div>\n<div class="rr"><span class="rv">3.55</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
