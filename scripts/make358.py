"""Guide 3.58 (from trial 3.57) – TRIAL. David, 22 Nov, question 1:
 - page title "Who will be set up with an account?" replaces "About your account"
   (also the start page list, the results row and the page's data-title);
 - the subheading is removed; the explanation paragraph is the body.
usage: python3 make358.py v3.57.html v3.58.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
T = 'Who will be set up with an account?'
rep('data-title="Troubleshooter · About your account"', 'data-title="Troubleshooter · %s"' % T)
rep('<span class="vh">Question 1 of 6: </span>About your account</h2>', '<span class="vh">Question 1 of 6: </span>%s</h2>' % T)
rep('<span aria-hidden="true">1</span>About your account</li>', '<span aria-hidden="true">1</span>%s</li>' % T)
rep('<p class="sum-l">About your account</p>', '<p class="sum-l">%s</p>' % T, 3)
rep('<div class="ts-info"><h3 class="h3 ts-sub"><span class="vh">GM Early Years App: </span>Who will be set up with an account?</h3><p class="q-why">Your Health Visiting',
    '<div class="ts-info"><p class="q-why">Your Health Visiting')
rep('Carer role v3.57', 'Carer role v3.58'); rep('Version 3.57 iPhone', 'Version 3.58 iPhone')
rep('>3.57 – REVIEW DRAFT', '>3.58 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.57</span>', '<span class="cv-ver">Version 3.58</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.53</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.57</span>', '<div class="rr"><span class="rv">3.58</span><span class="rd">22 Nov 2026</span><p>Question 1 titled Who will be set up with an account?; subheading removed</p></div>\n<div class="rr"><span class="rv">3.57</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
