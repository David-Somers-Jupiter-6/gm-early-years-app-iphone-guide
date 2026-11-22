"""Guide 3.61 (from trial 3.60) – TRIAL. David, 22 Nov, question 3 (was "NHS login account"):
 - title "Do you have an NHS login?" (also the start page list, results rows and data-title);
 - subheading removed; body "You need your own NHS login account to use the GM Early Years App. NHS login confirms who you are.";
 - answers "Yes, I have an NHS login account" / "No, I have not set up an NHS login account". Question unchanged.
usage: python3 make361.py v3.60.html v3.61.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
T = 'Do you have an NHS login?'
rep('data-title="Troubleshooter · NHS login account"', 'data-title="Troubleshooter · %s"' % T)
rep('<span class="vh">Question 3 of 6: </span>NHS login account</h2>', '<span class="vh">Question 3 of 6: </span>%s</h2>' % T)
rep('<span aria-hidden="true">3</span>NHS login account</li>', '<span aria-hidden="true">3</span>%s</li>' % T)
# results rows on the Troubleshooter results page only (the Checklist summary keeps its own label)
m = re.search(r'<section class="screen[^"]*" id="tsum".*?</section>', s, re.S); blk = m.group(0)
blk2, n = re.subn(r'<p class="sum-l">NHS login account</p>', '<p class="sum-l">%s</p>' % T, blk); assert n == 3, n
s = s[:m.start()] + blk2 + s[m.end():]
rep('<div class="ts-info"><h3 class="h3 ts-sub"><span class="vh">NHS login: </span>An NHS login account is needed</h3><p class="q-why">You sign in to the GM Early Years App with your own <strong>NHS login</strong> account.</p></div>',
    '<div class="ts-info"><p class="q-why">You need your own <strong>NHS login</strong> account to use the GM Early Years App. NHS login confirms who you are.</p></div>')
rep('<span>Yes, I have NHS login</span></label>\n<label class="radio"><input type="radio" class="ans ans-no" name="ans-ts2"/><span class="rc" aria-hidden="true"></span><span>No, or I’m not sure</span>',
    '<span>Yes, I have an NHS login account</span></label>\n<label class="radio"><input type="radio" class="ans ans-no" name="ans-ts2"/><span class="rc" aria-hidden="true"></span><span>No, I have not set up an NHS login account</span>')
rep('Carer role v3.60', 'Carer role v3.61'); rep('Version 3.60 iPhone', 'Version 3.61 iPhone')
rep('>3.60 – REVIEW DRAFT', '>3.61 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.60</span>', '<span class="cv-ver">Version 3.61</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.56</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.60</span>', '<div class="rr"><span class="rv">3.61</span><span class="rd">22 Nov 2026</span><p>Question 3 titled Do you have an NHS login?; wording and answers updated</p></div>\n<div class="rr"><span class="rv">3.60</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
