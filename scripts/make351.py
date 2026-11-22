"""Guide 3.51 (from trial 3.50) – TRIAL. David, 22 Nov, question 1:
 - title "About your account" (was "Who is set up with an account?"), also in the start page list and Your results;
 - subheading "Who will be set up with an account"; text "Your Health Visiting team sets up a GM Early Years App
   account for the child's mother or primary carer." then "In this guide, we call this person the account holder.";
 - question "Is it clear who will be set up with an account?";
 - No: "Please see Who will be set up with an account for more information." The help page is renamed to match
   (title, GM Early Years App help card, Your results link text).
usage: python3 make351.py v3.50.html v3.51.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b, n=1):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
T_OLD, T_NEW = 'Who is set up with an account', 'About your account'
H_NEW = 'Who will be set up with an account'
# question 1
edit('ts1', 'data-title="Troubleshooter · %s?"' % T_OLD, 'data-title="Troubleshooter · %s"' % T_NEW)
edit('ts1', '<span class="vh">Question 1 of 6: </span>%s?</h2>' % T_OLD, '<span class="vh">Question 1 of 6: </span>%s</h2>' % T_NEW)
edit('ts1', '<span class="vh">GM Early Years App: </span>The child’s mother or primary carer</h3>', '<span class="vh">GM Early Years App: </span>%s</h3>' % H_NEW)
edit('ts1', 'Your Health Visiting team sets up the GM Early Years App account for the ', 'Your Health Visiting team sets up a GM Early Years App account for the ')
edit('ts1', 'Is it clear who has been set up with a GM Early Years App account?', 'Is it clear who will be set up with an account?')
edit('ts1', '<a class="msg-link" href="#s4-who">%s</a>' % T_OLD, '<a class="msg-link" href="#s4-who">%s</a>' % H_NEW)
# start page list ("the Troubleshooter menu")
edit('ts', '<span aria-hidden="true">1</span>%s?</li>' % T_OLD, '<span aria-hidden="true">1</span>%s</li>' % T_NEW)
# Your results
edit('tsum', '<p class="sum-l">%s</p>' % T_OLD, '<p class="sum-l">%s</p>' % T_NEW, 3)
edit('tsum', '<p class="sum-s">Read who is set up with an account</p>', '<p class="sum-s">Read who will be set up with an account</p>')
# help page and its card
for a in ('data-title="%s"', 'aria-label="%s"', '<h2 class="h2" tabindex="-1">%s</h2>'):
    edit('s4-who', a % T_OLD, a % H_NEW)
edit('s4-gm', '<b>%s</b>' % T_OLD, '<b>%s</b>' % H_NEW)
assert T_OLD not in s, [s[m.start()-60:m.end()] for m in re.finditer(T_OLD, s)]
rep('Carer role v3.50', 'Carer role v3.51'); rep('Version 3.50 iPhone', 'Version 3.51 iPhone')
rep('>3.50 – REVIEW DRAFT', '>3.51 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.50</span>', '<span class="cv-ver">Version 3.51</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.46</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.50</span>', '<div class="rr"><span class="rv">3.51</span><span class="rd">22 Nov 2026</span><p>Question 1: About your account; help page Who will be set up with an account</p></div>\n<div class="rr"><span class="rv">3.50</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
