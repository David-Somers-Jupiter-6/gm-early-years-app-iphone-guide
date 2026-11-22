"""Guide 3.60 (from trial 3.59) – TRIAL. David, 22 Nov, question 5 (Do your details match?):
 - subheading removed; body "Your GM Early Years App account must use the same contact details as your NHS login account.";
 - question "Do both accounts use the same contact details?". Example card unchanged.
usage: python3 make360.py v3.59.html v3.60.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<div class="ts-info"><h3 class="h3 ts-sub"><span class="vh">NHS login and GM Early Years App: </span>Exactly the same in both</h3><p class="q-why">Your <strong>email address</strong> and <strong>mobile number</strong> must be the same in your NHS login account and your GM Early Years App account.</p>',
    '<div class="ts-info"><p class="q-why">Your GM Early Years App account must use the same <strong>contact details</strong> as your NHS login account.</p>')
rep('<p class="q-ask" id="ask-ts4">Are your details the same in both accounts?</p>',
    '<p class="q-ask" id="ask-ts4">Do both accounts use the same contact details?</p>')
rep('Carer role v3.59', 'Carer role v3.60'); rep('Version 3.59 iPhone', 'Version 3.60 iPhone')
rep('>3.59 – REVIEW DRAFT', '>3.60 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.59</span>', '<span class="cv-ver">Version 3.60</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.55</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.59</span>', '<div class="rr"><span class="rv">3.60</span><span class="rd">22 Nov 2026</span><p>Question 5: body and question wording updated</p></div>\n<div class="rr"><span class="rv">3.59</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
