"""Guide 3.73 (from trial 3.72) – TRIAL. David, 23 Nov, Troubleshooter questions 1-6:
 - the ? QUESTION label, the question, "Tap an answer, then tap Next.", the answer boxes and the reply boxes
   are in the same place on all six questions (question text and answer heights are now shared too).
usage: python3 make373.py v3.72.html v3.73.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep("[TSQ,['.ts-info','.ts-replies']]", "[TSQ,['.ts-info','.ts-qa','.radios','.ts-replies']]")
CSS = '''/* 3.73 questions 1-6: question text and answers share one height so everything below lines up */
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .ts-qa{margin:0!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .radios{align-content:start;margin-top:0!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask p.q-hint{margin:2px 0 6px!important;padding:0!important}
'''
rep('/* 2.95 A. Troubleshooting help pages as three blocks */', CSS + '/* 2.95 A. Troubleshooting help pages as three blocks */')
rep('Carer role v3.72', 'Carer role v3.73'); rep('Version 3.72 iPhone', 'Version 3.73 iPhone')
rep('>3.72 – REVIEW DRAFT', '>3.73 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.72</span>', '<span class="cv-ver">Version 3.73</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.68</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.72</span>', '<div class="rr"><span class="rv">3.73</span><span class="rd">23 Nov 2026</span><p>Troubleshooter: question, hint, answers and replies line up on all six questions</p></div>\n<div class="rr"><span class="rv">3.72</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
