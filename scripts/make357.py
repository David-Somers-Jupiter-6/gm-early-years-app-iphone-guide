"""Guide 3.57 (from trial 3.56) – TRIAL. David, 22 Nov, question 1 (About your account):
 - subheading "Who will be set up with an account?" (question mark added);
 - explanation is one paragraph: "Your Health Visiting team sets up a GM Early Years App account for the
   child's mother or primary carer. In this guide, we call this person the account holder.";
 - question "Is it clear who will be set up with a GM Early Years App account?".
usage: python3 make357.py v3.56.html v3.57.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep('<span class="vh">GM Early Years App: </span>Who will be set up with an account</h3><p class="q-why">Your Health Visiting team sets up a GM Early Years App account for the <strong>child’s mother or primary carer</strong>.</p><p class="q-why ts-who">In this guide, we call this person the <strong>account holder</strong>.</p>',
    '<span class="vh">GM Early Years App: </span>Who will be set up with an account?</h3><p class="q-why">Your Health Visiting team sets up a GM Early Years App account for the <strong>child’s mother or primary carer</strong>. In this guide, we call this person the <strong>account holder</strong>.</p>')
rep('<p class="q-ask" id="ask-ts1">Is it clear who will be set up with an account?</p>',
    '<p class="q-ask" id="ask-ts1">Is it clear who will be set up with a GM Early Years App account?</p>')
rep('Carer role v3.56', 'Carer role v3.57'); rep('Version 3.56 iPhone', 'Version 3.57 iPhone')
rep('>3.56 – REVIEW DRAFT', '>3.57 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.56</span>', '<span class="cv-ver">Version 3.57</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.52</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.56</span>', '<div class="rr"><span class="rv">3.57</span><span class="rd">22 Nov 2026</span><p>Question 1: wording of explanation and question updated</p></div>\n<div class="rr"><span class="rv">3.56</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
