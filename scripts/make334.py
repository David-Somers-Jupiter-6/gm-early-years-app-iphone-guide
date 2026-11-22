"""Guide 3.34 (from trial 3.33) – TRIAL. David, 22 Nov:
 - Question 1 asks "Is it clear who has been set up with a GM Early Years App account?"
 - The explanation adds "This troubleshooter should be answered by the child's mother or primary carer, not a partner
   or family member." (Yes stays "That is clear": a longer message would make the page scroll on smaller iPhones.)
 - New page in GM Early Years App help, "Who the account is for", in the same style as "A partner is signing in".
   Question 1's Read more on Your results now opens it (it used to open About your account).
 - Fix (since 3.31): the No answers on questions 1 and 2 said "That is clear". They say "That is OK. We will help."
usage: python3 make334.py v3.33.html v3.34.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>\n?' % re.escape(pid), s, re.S)
    assert m, pid
    return m
def put(pid, new):
    global s
    m = page(pid); s = s[:m.start()] + new + s[m.end():]
def edit(pid, a, b, n=1):
    blk = page(pid).group(0); assert blk.count(a) == n, (pid, a[:80], blk.count(a)); put(pid, blk.replace(a, b))

MUM = 'child’s mother or primary carer'

# 1. Question 1
edit('ts1', '<p class="q-ask" id="ask-ts1">Is it clear who the GM Early Years App account is for?</p>',
            '<p class="q-ask" id="ask-ts1">Is it clear who has been set up with a GM Early Years App account?</p>')
for pid in ('ts1', 'ts1b'):   # fix: the soft No message
    edit(pid, '<div class="ans-msg msg-no ok soft" role="status"><span class="ok-ico" aria-hidden="true">i</span><p class="ok-h">That is clear</p></div>',
              '<div class="ans-msg msg-no ok soft" role="status"><span class="ok-ico" aria-hidden="true">i</span><p class="ok-h">That is OK. We will help.</p></div>')

edit('ts1', '<p class="q-why">Your Health Visiting team sets up the GM Early Years App account for the <strong>child’s mother or primary carer</strong>.</p></div>',
            '<p class="q-why">Your Health Visiting team sets up the account for the <strong>child’s mother or primary carer</strong>.</p>'
            '<p class="q-why ts-who">This troubleshooter should be answered by the <strong>child’s mother or primary carer</strong>, <strong>not a partner or family member</strong>.</p></div>')

# 2. Your results: question 1's Read more opens the new page
edit('tsum', '<p class="sum-s">Read who the account is for</p></div><a class="sum-help" href="#acct">',
             '<p class="sum-s">Read who the account is for</p></div><a class="sum-help" href="#s4-who">')

# 3. New page, modelled on "A partner is signing in"
p2 = page('s4-2').group(0)
new = p2.replace('id="s4-2"', 'id="s4-who"').replace('data-start="s4-2"', 'data-start="s4-who"')
new = new.replace('data-title="A partner is signing in" aria-label="A partner is signing in"',
                  'data-title="Who the account is for" aria-label="Who the account is for"')
new = new.replace('<h2 class="h2" tabindex="-1">A partner is signing in</h2>', '<h2 class="h2" tabindex="-1">Who the account is for</h2>')
new = new.replace('Here is what to do instead.', 'Here is how it works.')
old_rows = re.search(r'<div class="abc">.*?</div></div></div></div>\n', new, re.S).group(0)
btn = re.search(r'<div class="hv-card sp-card abc-links">.*?</a></div>', old_rows, re.S).group(0)
do_ic = re.search(r'<span class="abc-ic ic-do" aria-hidden="true">(<svg.*?</svg>)</span>', old_rows, re.S).group(1)
rows = ('<div class="abc">'
  '<div class="abc-row"><span class="abc-ic ic-issue" aria-hidden="true">i</span><div><p class="abc-k">Who it is for</p>'
  '<p>Your Health Visiting team creates the App account for the <strong>%s</strong>.</p></div></div>'
  '<div class="abc-row"><span class="abc-ic ic-who who-nhs" aria-hidden="true"></span><div><p class="abc-k">Who can help</p>'
  '<p><strong>Your Health Visiting team</strong></p></div></div>'
  '<div class="abc-row"><span class="abc-ic ic-do" aria-hidden="true">%s</span><div><p class="abc-k">What to do</p>'
  '<p>The %s signs in with their own NHS login. Not sure who it is for? Ask the team.</p>%s</div></div>'
  '</div>\n') % (MUM, do_ic, MUM, btn)
new = new.replace(old_rows, rows)
assert new.count('s4-2') == 0 and 'Who the account is for' in new
m = page('s4-problems'); s = s[:m.start()] + new + s[m.start():]

# 4. GM Early Years App help: card for the new page, first of the Health Visiting team topics
gm = page('s4-gm').group(0)
person = ('<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="3.8"/><path d="M4.5 20.5c.9-4 3.8-6.2 7.5-6.2s6.6 2.2 7.5 6.2"/></svg>')
chev = re.search(r'<span class="tc-c">(<svg.*?</svg>)</span>', gm, re.S).group(1)
card = ('<a class="tc tc-hv" href="#s4-who"><span class="tc-tile">%s</span><span class="tc-t"><b>Who the account is for</b>'
        '<span class="tc-s">For the %s</span></span><span class="tc-c">%s</span></a>') % (person, MUM, chev)
i = gm.index('<a class="tc tc-hv" href="#s4-problems">'); gm = gm[:i] + card + gm[i:]
put('s4-gm', gm)

# 5. CSS: seven cards – a little tighter on short screens
NEW_CSS = """/* 3.34 GM Early Years App help has seven topics */
#app #s4-gm .tc-list .tc+.tc{margin-top:6px}
#app #s4-gm .tc{padding-top:6px;padding-bottom:6px}
#app #s4-gm.tight .tc{padding-top:4px;padding-bottom:4px}
#app #s4-gm.tight .tc-list .tc+.tc{margin-top:5px}
@media screen and (max-width:370px){#app #s4-gm .tc{gap:8px;padding-left:8px;padding-right:4px}#app #s4-gm .tc-tile{flex-basis:32px;height:32px}#app #s4-gm .tc-t>b{font-size:15.5px}#app #s4-gm .tc-s{font-size:13.5px;line-height:1.2}#app #s4-gm .tc-c{flex-basis:16px}}
@media screen and (max-height:600px){#app #s4-gm .tc-tile{flex-basis:32px;height:32px}#app #s4-gm .tc-t>b{font-size:15.5px;line-height:1.18}#app #s4-gm .tc-s{font-size:14px;line-height:1.2}}
"""
anchor = '/* 2.88 Step 1:'
assert s.count(anchor) == 1; s = s.replace(anchor, NEW_CSS + anchor); assert NEW_CSS.count('{') == NEW_CSS.count('}')

# 6. Section 6 numbering (in page order) and whole-guide counters
k = iter(range(1, 100)); s, n = re.subn(r'<span class="pos">Page \d+ of 49</span>', lambda m: '<span class="pos">Page %d of 50</span>' % next(k), s)
assert n == 50, n
ids = re.findall(r'<section class="screen(?: cover)?" id="([^"]+)"', s)
assert ids[:4] == ['cover', 'intro', 'contents', 'how'] and ids[-1] == 'search'; T = len(ids) - 1
for idx, pid in enumerate(ids, 1):
    blk = page(pid).group(0)
    nb = re.sub(r'\(page \d+ of \d+\)', f'(page {idx} of {T})', blk)
    nb = re.sub(r'<span class="count">\d+ / \d+</span>', f'<span class="count">{idx} / {T}</span>', nb)
    if nb != blk: put(pid, nb)

rep('Carer role v3.33', 'Carer role v3.34'); rep('Version 3.33 iPhone', 'Version 3.34 iPhone')
rep('>3.33 – REVIEW DRAFT', '>3.34 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.33</span>', '<span class="cv-ver">Version 3.34</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.29</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.33</span>', '<div class="rr"><span class="rv">3.34</span><span class="rd">22 Nov 2026</span><p>Question 1 reworded; new page Who the account is for; No messages on questions 1 and 2 fixed</p></div>\n<div class="rr"><span class="rv">3.33</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, T)
