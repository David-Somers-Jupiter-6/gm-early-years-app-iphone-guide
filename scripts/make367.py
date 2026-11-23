"""Guide 3.67 (from trial 3.66) – TRIAL. David, 23 Nov, question 1 (About your account) replies:
 - Yes (green tick): "That's right" removed; text "The account is set up for the child's mother or primary carer." (2 lines);
 - No (blue i): "That's OK" removed; the information, then WHO CAN HELP / Your Health Visiting team with the NHS logo
   (logo in line with the reply icon);
 - the reply icon (and the "Please tap an answer" reminder) lines up with the answer circles, and the reply text starts where the answer text starts.
usage: python3 make367.py v3.66.html v3.67.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def in_sec(i, a, b, n=1):
    global s
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (i, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
in_sec('ts1', '<p class="ok-h">That’s right</p><p class="ok-more">The account is for the child’s mother or primary carer – the account holder.</p>',
       '<p class="ok-more">The account is set up for the child’s mother or primary carer.</p>')
in_sec('ts1', '<p class="ok-h">That’s OK</p><p class="ok-more">The account is only ever set up',
       '<p class="ok-more">The account is only ever set up')
in_sec('ts1', '<span>Who can help: <strong>Your Health Visiting team</strong></span>',
       '<span class="th-t"><span class="th-k">Who can help</span><strong>Your Health Visiting team</strong></span>')
CSS = '''/* 3.67 question 1 replies: icon in line with the answer circles, text in line with the answer text */
#app #ts1 .ts-replies>.ans-msg{padding:9px 12px 9px 49px!important}
#app #ts1 .ts-replies>.ans-msg .ok-ico{left:8px!important;top:9px!important;width:28px!important;height:28px!important;margin:0!important}
#app #ts1 .ts-replies>.ans-msg>p.ok-more{margin:0!important;padding-top:3px}
#app #ts1 .ts-replies>.ans-msg>p.ok-more.ts-help{display:flex!important;align-items:center;gap:13px;margin:8px 0 0 -41px!important;padding:8px 0 0!important;border-top:1px solid rgba(0,94,184,.2)}
#app #ts1 .ts-replies>.need-ans{align-items:center;gap:13px!important;padding:10px 12px 10px 8px!important}
#app #ts1 .ts-replies>.need-ans .ni{flex:0 0 28px;width:28px!important;height:28px!important;margin:0!important;font-size:16px!important}
#app #ts1 .ts-help .ts-hi{flex:0 0 28px;width:28px!important;height:28px!important;border-radius:7px}
#app #ts1 .ts-help .th-t{display:flex;flex-direction:column;line-height:1.25}
#app #ts1 .ts-help .th-k{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#4c6272;margin-bottom:2px}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.66', 'Carer role v3.67'); rep('Version 3.66 iPhone', 'Version 3.67 iPhone')
rep('>3.66 – REVIEW DRAFT', '>3.67 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.66</span>', '<span class="cv-ver">Version 3.67</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.62</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.66</span>', '<div class="rr"><span class="rv">3.67</span><span class="rd">23 Nov 2026</span><p>Question 1: replies simplified and lined up with the answers</p></div>\n<div class="rr"><span class="rv">3.66</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
