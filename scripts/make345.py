"""Guide 3.45 (from trial 3.44) – TRIAL. David, 22 Nov: GM Early Years App help, new card order:
Who is set up with an account · Only the child's mother or primary carer can access · Partner's details used ·
Details do not match · Activation Link issues · How to install the App · Add to Home Screen.
usage: python3 make345.py v3.44.html v3.45.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
m = re.search(r'<section class="screen" id="s4-gm".*?</section>', s, re.S); blk = m.group(0)
lst = re.search(r'(<nav aria-label="GM Early Years App help" class="tc-list">)(.*?)(</nav>)', blk, re.S)
cards = dict((re.search(r'href="#([^"]+)"', c).group(1), c) for c in re.findall(r'<a class="tc [^"]+" href="#[^"]+">.*?</a>', lst.group(2), re.S))
order = ['s4-who', 's4-2', 's4-1b', 's4-problems', 's4-activation', 'inst', 'a2hs']
assert sorted(cards) == sorted(order), sorted(cards)
blk = blk.replace(lst.group(0), lst.group(1) + ''.join(cards[k] for k in order) + lst.group(3))
s = s[:m.start()] + blk + s[m.end():]
rep('Carer role v3.44', 'Carer role v3.45'); rep('Version 3.44 iPhone', 'Version 3.45 iPhone')
rep('>3.44 – REVIEW DRAFT', '>3.45 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.44</span>', '<span class="cv-ver">Version 3.45</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.40</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.44</span>', '<div class="rr"><span class="rv">3.45</span><span class="rd">22 Nov 2026</span><p>GM Early Years App help: new order</p></div>\n<div class="rr"><span class="rv">3.44</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
