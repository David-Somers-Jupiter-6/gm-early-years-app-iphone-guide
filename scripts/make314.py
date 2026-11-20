"""Guide 3.14 (from 3.13) – LIVE. David, 20 Nov: review the other Troubleshooting pages for the same issue as 3.13
(topics running on into the next topic) and fix them the same way.
 - NHS login account issues (s4-nhs): 8 topics ran on into each other, and the last one ran into GM Early Years App
   issues. The last page of each topic now has Done (step-h-tip, s4-setup, s4-cannot, s4-pw, s4-code, s4-email,
   s4-mobile, s4-name).
 - Common sign-in problems (s4-reasons): 3 topics ran on, and the last one ran into Still need help?
   Done on s4-problems, s4-1b, s4-2.
 - Done goes back to the page you were on before the topic started: the menu if you chose it there, or the Checklist
   summary or Search if you came from there. Opened directly (no history) it goes to the menu, and Back there goes to Troubleshooting. This also fixes 3.13:
   Back on a menu after Done no longer steps back into the topic you just finished.
 - Menus no longer run into their first topic (that made a loop now that topics return to the menu).
   Next on a menu goes to the next menu: Troubleshooting > NHS login account issues > GM Early Years App issues >
   Common sign-in problems > Still need help? > Section 7.
 - Opened directly (no history), Back on a topic's first page goes to its menu, and Back on a menu goes to
   Troubleshooting.
usage: python3 make314.py v3.13.html v3.14.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def page(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S)
    assert m, pid
    return m

def edit(pid, fn):
    global s
    m = page(pid); blk = fn(m.group(0)); s = s[:m.start()] + blk + s[m.end():]

def set_back(pid, back):
    def f(blk):
        blk, n = re.subn(r'(<a class="nav-btn nav-back[^"]*" href="#)[^"]+(")', r'\g<1>%s\2' % back, blk)
        assert n == 1, (pid, 'back'); return blk
    edit(pid, f)

def set_next(pid, nxt):
    def f(blk):
        blk, n = re.subn(r'(<a class="nav-btn nav-next[^"]*" href="#)[^"]+(")', r'\g<1>%s\2' % nxt, blk)
        assert n == 1, (pid, 'next'); return blk
    edit(pid, f)

ARIA = 'Done – go back to where you chose this topic'
def set_done(pid, menu, start):
    def f(blk):
        blk, n = re.subn(r'<a class="nav-btn nav-next[^"]*" href="#[^"]+"[^>]*><span>[^<]*</span>',
                         '<a class="nav-btn nav-next nav-done" href="#%s" data-start="%s" aria-label="%s"><span>Done</span>' % (menu, start, ARIA), blk)
        assert n == 1, (pid, 'done'); return blk
    edit(pid, f)

# GM Early Years App issues (3.13 Done buttons get the smarter Done)
set_done('inst-7-tip', 's4-gm', 'inst'); set_done('a2hs', 's4-gm', 'a2hs'); set_done('s4-activation-2', 's4-gm', 's4-activation')
# NHS login account issues
set_done('step-h-tip', 's4-nhs', 'step-a')
for pid in ('s4-setup', 's4-cannot', 's4-pw', 's4-code', 's4-email', 's4-mobile', 's4-name'):
    set_done(pid, 's4-nhs', pid); set_back(pid, 's4-nhs')
# Common sign-in problems
for pid in ('s4-problems', 's4-1b', 's4-2'):
    set_done(pid, 's4-reasons', pid); set_back(pid, 's4-reasons')
# menus: Next goes to the next menu; Back (no history) goes to Troubleshooting
set_next('s4-nhs', 's4-gm'); set_next('s4-gm', 's4-reasons'); set_next('s4-reasons', 's4-help')
for pid in ('s4-nhs', 's4-gm', 's4-reasons', 's4-help'):
    set_back(pid, 's4')

# Done: return to the page before the topic started (menu, Checklist summary, Search); otherwise open the menu
rep("function goBack(fallbackId){",
    "function done(a,id){ var st=a.getAttribute('data-start'), k=st?trail.lastIndexOf(st):-1;\n"
    "    if(k>0&&byId[trail[k-1]]){ trail=trail.slice(0,k); show(byId[trail[k-1]]); return true; }\n"
    "    if(byId[id]){ trail=[id]; show(byId[id]); return true; } return false; }\n"
    "  function goBack(fallbackId){")
rep("if(a.classList.contains('nav-back')||a.hasAttribute('data-hist')) goBack(id); else go(id);",
    "if(a.classList.contains('nav-done')&&done(a,id)) return;\n"
    "    if(a.classList.contains('nav-back')||a.hasAttribute('data-hist')) goBack(id); else go(id);")

rep('Carer role v3.13', 'Carer role v3.14'); rep('Version 3.13 iPhone', 'Version 3.14 iPhone')
rep('>3.13 – REVIEW DRAFT', '>3.14 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.13</span>', '<span class="cv-ver">Version 3.14</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.11</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.13</span>', '<div class="rr"><span class="rv">3.14</span><span class="rd">20 Nov 2026</span><p>All Troubleshooting topics finish with Done and go back to where you chose them</p></div>\n<div class="rr"><span class="rv">3.13</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
