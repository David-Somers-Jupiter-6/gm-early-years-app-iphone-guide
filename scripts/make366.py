"""Guide 3.66 (from trial 3.65) – TRIAL. David, 23 Nov, question 1 (About your account):
 - the question window moves up under "Who it is for" (question 1 no longer shares heights with questions 2-6);
 - no space between the question and "Tap an answer, then tap Next.";
 - the space for the reply is kept at the bottom of the question window from the start, so nothing moves
   when Yes or No is tapped (the Yes reply, No reply and "Please tap an answer" share one slot).
usage: python3 make366.py v3.65.html v3.66.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep("var TSQ=['ts1','ts1b','ts2','ts3','ts4','ts5'];", "var TSQ=['ts1b','ts2','ts3','ts4','ts5'];")
m = re.search(r'<section class="screen[^"]*" id="ts1".*?</section>', s, re.S); blk = m.group(0)
a = blk.index('<p class="need-ans"'); z = blk.index('</div>\n</div>\n<input type="radio" class="nudge-t"')
blk = blk[:a] + '<div class="ts-replies">' + blk[a:z] + '</div>\n' + blk[z:]
s = s[:m.start()] + blk + s[m.end():]
CSS = '''/* 3.66 question 1: question window straight under the information; reply slot kept from the start */
#app #ts1 .ts-ask .q-ask{margin-bottom:0!important}
#app #ts1 .ts-ask .q-hint{margin-top:2px!important}
#app #ts1 .ts-replies{display:grid;margin-top:8px}
#app #ts1 .ts-replies>*{grid-area:1/1;visibility:hidden;margin:0!important;align-self:start}
#app #ts1 .ts-replies>.ans-msg{display:block!important}
#app #ts1 .ts-replies>.need-ans{display:flex!important}
#app #ts1:has(.ans-yes:checked) .ts-replies>.msg-yes,#app #ts1:has(.ans-no:checked) .ts-replies>.msg-no{visibility:visible}
#app #ts1.nudge:not(:has(.ans:checked)) .ts-replies>.need-ans{visibility:visible}
html:not(.jsnav) #app #ts1:has(.nudge-t:checked):not(:has(.ans:checked)) .ts-replies>.need-ans{visibility:visible}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.65', 'Carer role v3.66'); rep('Version 3.65 iPhone', 'Version 3.66 iPhone')
rep('>3.65 – REVIEW DRAFT', '>3.66 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.65</span>', '<span class="cv-ver">Version 3.66</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.61</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.65</span>', '<div class="rr"><span class="rv">3.66</span><span class="rd">23 Nov 2026</span><p>Question 1: question moved up; reply space kept so nothing moves</p></div>\n<div class="rr"><span class="rv">3.65</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
