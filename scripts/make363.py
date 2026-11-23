"""Guide 3.63 (from trial 3.62) – TRIAL. David, 23 Nov:
 - question 1 titled "About your account" (was "Who will be set up with an account?"),
   also in the start page list and on the results page;
 - questions 1-4: the question, hint, answers and the Yes / No reply sit together in their own
   "Question" card, in the same style as the information cards above.
usage: python3 make363.py v3.62.html v3.63.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); assert m, i; return m

T1 = 'About your account'
rep('data-title="Troubleshooter · Who will be set up with an account?"', 'data-title="Troubleshooter · %s"' % T1)
rep('<span class="vh">Question 1 of 6: </span>Who will be set up with an account?</h2>', '<span class="vh">Question 1 of 6: </span>%s</h2>' % T1)
rep('<span aria-hidden="true">1</span>Who will be set up with an account?</li>', '<span aria-hidden="true">1</span>%s</li>' % T1)
m = sec('tsum'); blk = m.group(0); assert blk.count('<p class="sum-l">Who will be set up with an account?</p>') == 3
s = s[:m.start()] + blk.replace('<p class="sum-l">Who will be set up with an account?</p>', '<p class="sum-l">%s</p>' % T1) + s[m.end():]

HEAD = '<div class="ts-ask"><p class="abc-k ts-ask-k"><span class="abc-ic ic-ask" aria-hidden="true">?</span>Question</p>\n'
for i in ['ts1', 'ts1b', 'ts2', 'ts3']:
    m = sec(i); blk = m.group(0)
    assert blk.count('<div class="ts-qa">') == 1
    blk = blk.replace('<div class="ts-qa">', HEAD + '<div class="ts-qa">')
    end = '</div>\n<input type="radio" class="nudge-t"'
    assert blk.count(end) == 1
    blk = blk.replace(end, '</div>\n' + end)
    s = s[:m.start()] + blk + s[m.end():]

CSS = '''/* 3.63 troubleshooter questions 1-4: question, answers and reply in their own card */
#app .screen .ts-ask{position:relative;margin:10px 0 0;padding:7px 11px 10px;border:1px solid var(--line);border-left:5px solid #2d5161;border-radius:14px;background:var(--surface)}
#app .screen .ts-ask .ts-ask-k{position:relative;padding-left:30px;line-height:22px!important;margin:0 0 4px!important}
#app .screen .ts-ask .abc-ic.ic-ask{position:absolute;left:0;top:0;width:22px!important;height:22px!important;font-size:13px!important;color:#fff!important;background:#2d5161!important;border-radius:50%;display:grid;place-items:center}
#app .screen .ts-ask .ts-qa{margin-top:0!important}
#app .screen .ts-ask .radios{margin-bottom:0}
#app .screen .ts-ask .ans-msg{margin-top:10px!important}
#app .screen .ts-ask .ans-msg:last-child,#app .screen .ts-ask .need-ans{margin-bottom:0!important}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')

rep('Carer role v3.62', 'Carer role v3.63'); rep('Version 3.62 iPhone', 'Version 3.63 iPhone')
rep('>3.62 – REVIEW DRAFT', '>3.63 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.62</span>', '<span class="cv-ver">Version 3.63</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.58</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.62</span>', '<div class="rr"><span class="rv">3.63</span><span class="rd">23 Nov 2026</span><p>Question 1 titled About your account; questions 1–4 in their own Question card</p></div>\n<div class="rr"><span class="rv">3.62</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
