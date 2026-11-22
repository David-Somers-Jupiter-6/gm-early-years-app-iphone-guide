"""Guide 3.44 (from trial 3.43) – TRIAL. David, 22 Nov, question 2 (Who has access?):
 - subheading "Who will be able to access the account?" (was "Account access");
 - Yes: "Yes, the child's mother or primary carer" (was "You are the account holder");
 - No: "Please see Only the child's mother or primary carer can access for more information.", linking to that page;
 - the help page "A partner is signing in" is renamed "Only the child's mother or primary carer can access"
   (title, GM Early Years App help card; card line now "Not a partner or family member").
No layout fitting in this build (David: get the content in place first).
usage: python3 make344.py v3.43.html v3.44.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    assert blk.count(a) == 1, (pid, a[:80]); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
MUM = 'child’s mother or primary carer'
OLD, NEW = 'A partner is signing in', 'Only the %s can access' % MUM
# help page rename
for a in ('data-title="%s"', 'aria-label="%s"', '<h2 class="h2" tabindex="-1">%s</h2>'):
    edit('s4-2', a % OLD, a % NEW)
edit('s4-gm', '<b>%s</b><span class="tc-s">Only the named carer can sign in</span>' % OLD,
              '<b>%s</b><span class="tc-s">Not a partner or family member</span>' % NEW)
# question 2
edit('ts1b', '<span class="vh">GM Early Years App: </span>Account access</h3>', '<span class="vh">GM Early Years App: </span>Who will be able to access the account?</h3>')
edit('ts1b', '<p class="ok-h">You are the account holder</p>', '<p class="ok-h">Yes, the %s</p>' % MUM)
edit('ts1b', '<p class="ok-h">That is OK. We will help.</p>',
     '<p class="ok-h">Please see <a class="msg-link" href="#s4-2">%s</a> for more information.</p>' % NEW)
CSS = "/* 3.44 question 2: link in the No message */\n#app #ts1b .msg-link{color:var(--nhs-blue,#005eb8);text-decoration:underline;text-underline-offset:2px;text-decoration-thickness:1.5px}\n"
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor)
rep('Carer role v3.43', 'Carer role v3.44'); rep('Version 3.43 iPhone', 'Version 3.44 iPhone')
rep('>3.43 – REVIEW DRAFT', '>3.44 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.43</span>', '<span class="cv-ver">Version 3.44</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.39</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.43</span>', '<div class="rr"><span class="rv">3.44</span><span class="rd">22 Nov 2026</span><p>Question 2 wording; No links to the renamed partner page</p></div>\n<div class="rr"><span class="rv">3.43</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
