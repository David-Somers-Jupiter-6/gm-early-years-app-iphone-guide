"""Guide 2.56 (from 2.55).
- Checklist summary: the title box shows one title, "Checklist summary" (the small label
  "Checklist summary" and the title "Your checklist results" said the same thing twice).
- Questions 1 to 4: the stop messages now say "checklist summary" to match that title.
- Your Health Visiting team (both pages): each team card shows only the team name, address,
  phone number(s) and opening hours. The two extra notes are removed (Enhanced and SEND:
  referral only; Family Nurse Partnership: who it is for, and which line the number is).
usage: python3 make256.py v2.55.html v2.56.html
"""
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

def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# 1. Checklist summary title box
edit('sum', '<div class="kicker part">Checklist summary</div><h2 tabindex="-1">Your checklist results</h2>',
     '<h2 tabindex="-1">Checklist summary</h2>')

# 2. stop messages match the title
for pid in ('c1', 'c2', 'c3'):
    edit(pid, 'Your checklist results will then explain what to do next.', 'Your checklist summary will then explain what to do next.')
edit('c4', 'Select <strong>Next</strong> to see your checklist results and what to do next.',
     'Select <strong>Next</strong> to see your checklist summary and what to do next.')
assert 'checklist results' not in s

# 3. team cards: name, address, phone, hours only
for pid in ('hv', 's5-hv'):
    m = page(pid); blk = m.group(0)
    n = len(re.findall(r'<p class="hv-note">.*?</p>\n', blk))
    assert n == 2, (pid, n)
    blk = re.sub(r'<p class="hv-note">.*?</p>\n', '', blk)
    s = s[:m.start()] + blk + s[m.end():]
assert all('class="hv-note"' not in page(p).group(0) for p in ('hv', 's5-hv')) and 'class="hv-note"' in page('s5-gmdp').group(0)

# 4. NHS logo in the title box of both Health Visiting team pages (the NHS part of the guide's
#    "NHS | NHS login" badge, same size and place as on the NHS login pages)
import base64, os
NHS = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'nhs-mark.png'), 'rb').read()).decode()
IMG = '<img alt="NHS" class="nhsbadge sm nhs-mark" src="%s"/>' % NHS
edit('s5-hv', '<div class="pbox"><h2 class="h2" tabindex="-1">Your Health Visiting team</h2></div>',
     '<div class="pbox has-badge"><h2 class="h2" tabindex="-1">Your Health Visiting team</h2>' + IMG + '</div>')
m_ = page('hv'); blk = m_.group(0)
a_ = re.search(r'<div class="tp-card"><div class="tp-body"><h2 class="h2 tp-h" tabindex="-1">Your Health Visiting team</h2>.*?</div></div>', blk, re.S).group(0)
blk = blk.replace(a_, a_.replace('<div class="tp-card">', '<div class="tp-card has-badge">', 1)[:-len('</div>')] + IMG + '</div>', 1)
s = s[:m_.start()] + blk + s[m_.end():]
rep('@media print{', '''/* 2.56 NHS logo in the Section 1 title box (bottom right, as on the NHS login pages) */
#app .screen .info .ico{font-size:15px!important}   /* number circles, same as the other lists */
.tp-card.has-badge{position:relative}
.tp-card.has-badge>.nhsbadge{position:absolute;right:14px;bottom:9px;top:auto;height:22px;width:auto;margin:0;z-index:1}
@media print{''')

# ---------------------------------------------------------------- version
rep('Carer role v2.55', 'Carer role v2.56'); rep('Version 2.55 iPhone', 'Version 2.56 iPhone')
rep('<div>Version 2.55</div>', '<div>Version 2.56</div>'); rep('>2.55 – REVIEW DRAFT', '>2.56 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.53</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.55</span>', '<div class="rr"><span class="rv">2.56</span><span class="rd">16 Nov 2026</span><p>Checklist summary title; team cards show name, address, phone and hours only</p></div>\n<div class="rr"><span class="rv">2.55</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst)
