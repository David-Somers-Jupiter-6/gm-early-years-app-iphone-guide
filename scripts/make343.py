"""Guide 3.43 (from trial 3.42) – TRIAL. David, 22 Nov:
 - Question 1: No shows "Please see Who is set up with an account for more information." The page name is a link
   to that help page (in GM Early Years App help). Its Done button comes back to question 1.
 - The help page "Who the account is for" is renamed "Who is set up with an account" (title, menu card, results row).
usage: python3 make343.py v3.42.html v3.43.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
OLD, NEW = 'Who the account is for', 'Who is set up with an account'
# 1. rename the help page
m = re.search(r'<section class="screen" id="s4-who".*?</section>', s, re.S); blk = m.group(0)
for a in ('data-title="%s"', 'aria-label="%s"', '<h2 class="h2" tabindex="-1">%s</h2>'):
    assert blk.count(a % OLD) == 1, a; blk = blk.replace(a % OLD, a % NEW)
s = s[:m.start()] + blk + s[m.end():]
rep('<b>%s</b><span class="tc-s">' % OLD, '<b>%s</b><span class="tc-s">' % NEW)
rep('<p class="sum-l">%s</p>' % OLD, '<p class="sum-l">%s</p>' % NEW, 3)
rep('<p class="sum-s">Read who the account is for</p>', '<p class="sum-s">Read who is set up with an account</p>')
# 2. question 1, No
m = re.search(r'<section class="screen" id="ts1".*?</section>', s, re.S); blk = m.group(0)
a = '<div class="ans-msg msg-no ok soft" role="status"><span class="ok-ico" aria-hidden="true">i</span><p class="ok-h">That is OK. We will help.</p></div>'
assert blk.count(a) == 1
blk = blk.replace(a, '<div class="ans-msg msg-no ok soft" role="status"><span class="ok-ico" aria-hidden="true">i</span>'
                     '<p class="ok-h">Please see <a class="msg-link" href="#s4-who">%s</a> for more information.</p></div>' % NEW)
s = s[:m.start()] + blk + s[m.end():]
CSS = """/* 3.43 question 1: the No message links to the help page */
#app #ts1 .msg-no.ok{padding-top:5px!important;padding-bottom:5px!important;margin-top:3px!important;align-items:center}
#app #ts1 .msg-no .ok-h{font-size:16px!important;line-height:1.25!important}
@media screen and (max-height:640px),screen and (max-width:345px){#app #ts1 .msg-no.ok{padding-top:3px!important;padding-bottom:3px!important;margin-top:2px!important}#app #ts1 .msg-no .ok-h{font-size:15.5px!important;line-height:1.22!important}}
@media screen and (max-width:400px){#app #s4-gm .tc-t>b{letter-spacing:-.012em}}
@media screen and (max-width:380px){#app #s4-gm .tc-t>b{font-size:15.5px}}
@media screen and (max-width:345px){#app #s4-gm .tc-t>b{font-size:14.5px}#app #s4-gm .tc-s{font-size:13px!important;line-height:1.18!important}#app #s4-gm .tc-list .tc+.tc{margin-top:4px!important}#app #s4-gm .tc{padding-top:3px!important;padding-bottom:3px!important}}
#app #ts1 .msg-link{color:var(--nhs-blue,#005eb8);text-decoration:underline;text-underline-offset:2px;text-decoration-thickness:1.5px}
"""
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor); assert CSS.count('{') == CSS.count('}')
rep('Carer role v3.42', 'Carer role v3.43'); rep('Version 3.42 iPhone', 'Version 3.43 iPhone')
rep('>3.42 – REVIEW DRAFT', '>3.43 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.42</span>', '<span class="cv-ver">Version 3.43</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.38</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.42</span>', '<div class="rr"><span class="rv">3.43</span><span class="rd">22 Nov 2026</span><p>Question 1: No links to Who is set up with an account (renamed help page)</p></div>\n<div class="rr"><span class="rv">3.42</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
