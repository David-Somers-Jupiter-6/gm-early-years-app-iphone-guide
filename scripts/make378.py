"""Guide 3.78 (from trial 3.77). David, 23 Nov:
 - Contents lists itself: Cover page, Introduction, Contents, How this guide works (the Contents row is marked
   as the current page).
usage: python3 make378.py v3.77.html v3.78.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
CHEV = '<svg class="chev" aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M7 4l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LIST = '<svg aria-hidden="true" viewBox="0 0 20 20" width="17" height="17"><path d="M5 6h10M5 10h10M5 14h10" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
intro_row = '<a class="toc-row" href="#intro"><span class="gb" aria-hidden="true">i</span><span class="tt">Introduction</span>' + CHEV + '</a>'
rep(intro_row, intro_row + '\n<a class="toc-row" href="#contents" aria-current="page"><span class="gb" aria-hidden="true">' + LIST + '</span><span class="tt">Contents</span>' + CHEV + '</a>')
rep('Carer role v3.77', 'Carer role v3.78'); rep('Version 3.77 iPhone', 'Version 3.78 iPhone')
rep('>3.77 – REVIEW DRAFT', '>3.78 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.77</span>', '<span class="cv-ver">Version 3.78</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.73</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.77</span>', '<div class="rr"><span class="rv">3.78</span><span class="rd">23 Nov 2026</span><p>Contents lists the Contents page</p></div>\n<div class="rr"><span class="rv">3.77</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
