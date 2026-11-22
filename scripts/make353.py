"""Guide 3.53 (from trial 3.52) – TRIAL. David, 22 Nov, question 2 (Who has access?):
 - subheading "Who will be able to access the account?" (was "…the GM Early Years App account?");
 - text "Only the account holder can access the GM Early Years App account that has been set up for them."
usage: python3 make353.py v3.52.html v3.53.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<span class="vh">GM Early Years App: </span>Who will be able to access the GM Early Years App account?</h3>',
    '<span class="vh">GM Early Years App: </span>Who will be able to access the account?</h3>')
rep('<p class="q-why">Only the <strong>child’s mother or primary carer</strong> can access the GM Early Years App account that has been set up for them.</p>',
    '<p class="q-why">Only the <strong>account holder</strong> can access the GM Early Years App account that has been set up for them.</p>')
rep('Carer role v3.52', 'Carer role v3.53'); rep('Version 3.52 iPhone', 'Version 3.53 iPhone')
rep('>3.52 – REVIEW DRAFT', '>3.53 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.52</span>', '<span class="cv-ver">Version 3.53</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.48</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.52</span>', '<div class="rr"><span class="rv">3.53</span><span class="rd">22 Nov 2026</span><p>Question 2: subheading and account holder wording</p></div>\n<div class="rr"><span class="rv">3.52</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
