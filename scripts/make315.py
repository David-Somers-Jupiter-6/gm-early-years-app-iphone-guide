"""Guide 3.15 (from 3.14). David, 20 Nov: the four Troubleshooting choices should go back up to the Troubleshooting
menu when you have finished with them, not sideways into the next choice.
 - NHS login account issues, GM Early Years App issues, Common sign-in problems: Next becomes "Done" and goes to the
   Troubleshooting menu (was: the next menu in the list).
 - Still need help?: Next becomes "Done" (was: Section 7). Done goes back to where you came from: Troubleshooting,
   or the topic page whose "Get help" link you tapped.
 - Troubleshooting menu: Next goes on to Section 7 · Contact & support (was: NHS login account issues), so reading
   straight through still reaches the end of the guide and nothing loops.
 - Done on a menu cuts the Back history back to the Troubleshooting menu, so Back from Troubleshooting goes to
   wherever you were before it (e.g. the cover), not back into the menu.
usage: python3 make315.py v3.14.html v3.15.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def edit(pid, pat, new):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid
    blk, n = re.subn(pat, new, m.group(0)); assert n == 1, (pid, pat)
    s = s[:m.start()] + blk + s[m.end():]

NEXT = r'<a class="nav-btn nav-next[^"]*" href="#[^"]+"[^>]*><span>[^<]*</span>'
UP = '<a class="nav-btn nav-next nav-done" href="#s4" aria-label="Done – back to Troubleshooting"><span>Done</span>'
for pid in ('s4-nhs', 's4-gm', 's4-reasons'):
    edit(pid, NEXT, UP)
edit('s4-help', NEXT, '<a class="nav-btn nav-next nav-done" href="#s4" data-start="s4-help" aria-label="Done – go back to where you were"><span>Done</span>')
edit('s4', NEXT, '<a class="nav-btn nav-next" href="#s5"><span>Next</span>')
edit('s5', r'(<a class="nav-btn nav-back[^"]*" href="#)[^"]+(")', r'\g<1>s4\2')

# Done without data-start (menus): go up to the target, cutting history back to its last visit
rep("    if(byId[id]){ trail=[id]; show(byId[id]); return true; } return false; }",
    "    var j=trail.lastIndexOf(id); if(j>=0&&byId[id]){ trail=trail.slice(0,j+1); show(byId[id]); return true; }\n"
    "    if(byId[id]){ trail=[id]; show(byId[id]); return true; } return false; }")

rep('Carer role v3.14', 'Carer role v3.15'); rep('Version 3.14 iPhone', 'Version 3.15 iPhone')
rep('>3.14 – REVIEW DRAFT', '>3.15 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.14</span>', '<span class="cv-ver">Version 3.15</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.12</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.14</span>', '<div class="rr"><span class="rv">3.15</span><span class="rd">20 Nov 2026</span><p>Troubleshooting choices finish with Done and go back to the Troubleshooting menu</p></div>\n<div class="rr"><span class="rv">3.14</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
