"""Guide 3.59 (from trial 3.58) – TRIAL. David, 22 Nov, question 2:
 - page title "Who will be able to access the account?" replaces "Who has access?"
   (also the start page list, the results rows and the page's data-title);
 - subheading removed; body "Only the account holder (the child's mother or primary carer) can access
   the GM Early Years App account that has been set up for them.";
 - question "Is it clear that only the account holder can access the GM Early Years App account?".
usage: python3 make359.py v3.58.html v3.59.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
T = 'Who will be able to access the account?'
rep('data-title="Troubleshooter · Who has access?"', 'data-title="Troubleshooter · %s"' % T)
rep('<span class="vh">Question 2 of 6: </span>Who has access?</h2>', '<span class="vh">Question 2 of 6: </span>%s</h2>' % T)
rep('<span aria-hidden="true">2</span>Who has access?</li>', '<span aria-hidden="true">2</span>%s</li>' % T)
rep('<p class="sum-l">Who has access</p>', '<p class="sum-l">%s</p>' % T, 3)
rep('<div class="ts-info"><h3 class="h3 ts-sub"><span class="vh">GM Early Years App: </span>Who will be able to access the account?</h3><p class="q-why">Only the <strong>account holder</strong> can access',
    '<div class="ts-info"><p class="q-why">Only the <strong>account holder</strong> (the child’s mother or primary carer) can access')
rep('<p class="q-ask" id="ask-ts1b">Is it clear only the child’s mother or primary carer can access the GM Early Years App account?</p>',
    '<p class="q-ask" id="ask-ts1b">Is it clear that only the account holder can access the GM Early Years App account?</p>')
rep('Carer role v3.58', 'Carer role v3.59'); rep('Version 3.58 iPhone', 'Version 3.59 iPhone')
rep('>3.58 – REVIEW DRAFT', '>3.59 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.58</span>', '<span class="cv-ver">Version 3.59</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.54</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.58</span>', '<div class="rr"><span class="rv">3.59</span><span class="rd">22 Nov 2026</span><p>Question 2 titled Who will be able to access the account?; wording updated</p></div>\n<div class="rr"><span class="rv">3.58</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
