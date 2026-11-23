"""Guide 3.72 (from trial 3.71) – TRIAL. David, 23 Nov, questions 1 and 2, No reply:
 - the NHS logo is placed exactly like the green tick (centre in line with the answer circles) and
   WHO CAN HELP / Contact Your Health Visiting team starts where the answer text starts
   (no negative margin or flex offset, so every browser places it the same way).
usage: python3 make372.py v3.71.html v3.72.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
CSS = '''/* 3.72 questions 1-2 No reply: NHS logo placed like the tick, text in line with the answers */
#app :is(#ts1,#ts1b) .ts-replies>.ans-msg.ts-noreply{position:relative!important;padding-left:49px!important}
#app :is(#ts1,#ts1b) .ts-replies>.ans-msg.ts-noreply>p.ok-more.ts-help{display:block!important;margin:0!important;padding:0!important;border:0!important;gap:0!important}
#app :is(#ts1,#ts1b) .ans-msg.ts-noreply .ts-help .ts-hi{position:absolute!important;left:8px!important;top:50%!important;transform:translateY(-50%);width:28px!important;height:28px!important;margin:0!important}
#app :is(#ts1,#ts1b) .ans-msg.ts-noreply .ts-help .th-t{display:flex!important;flex-direction:column;margin:0!important;padding:0!important}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.71', 'Carer role v3.72'); rep('Version 3.71 iPhone', 'Version 3.72 iPhone')
rep('>3.71 – REVIEW DRAFT', '>3.72 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.71</span>', '<span class="cv-ver">Version 3.72</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.67</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.71</span>', '<div class="rr"><span class="rv">3.72</span><span class="rd">23 Nov 2026</span><p>Questions 1–2: No reply logo and text lined up with the answers</p></div>\n<div class="rr"><span class="rv">3.71</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
