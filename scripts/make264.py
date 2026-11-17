"""Guide 2.64 (from 2.63). Checklist questions and summary - David, 17 Nov.
Each question page: the reason (q-why), then the question itself in bold on its own line
(q-ask, which also labels the answer group), then "Select one option, then select Next.", then
the two answers.
- Q1: "Do you have an NHS login account?"  Yes, I have an NHS login account / No, I have not set up an NHS login account
- Q2: reason "You will sign in to the App with your NHS login email address and password."
      "Can you sign in to your NHS login account?"
      Yes, I can sign in to my NHS login / No, I cannot sign in to my NHS login
- Q3: reason "...same email address and mobile number as your NHS login account."
      "Does your GM Early Years App account use the same email address and mobile number as your
      NHS login account?"
      Yes, my account details match / No, my account details do not match, or I'm not sure
- Q4: "Have you received an Activation Link?"
      Yes, I have my Activation Link / No, I have not received an Activation Link
- Questions 1 to 3, stop message after No: "Select Next to complete the checklist."
- Summary: instruction under the section line: "If any item below has a red cross, tap
  Get help next to it to find out what to do." The amber box at the bottom, which said the same,
  is removed.
usage: python3 make264.py v2.63.html v2.64.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b, n=1):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

Q = {
 'c1': ('<p class="q-why">You need your own NHS login account to use the GM Early Years App. NHS login confirms who you are.</p>',
        None,
        'Do you have an NHS login account?',
        ('Yes, I have NHS login', 'Yes, I have an NHS login account'),
        ('No, or I’m not sure', 'No, I have not set up an NHS login account')),
 'c2': ('<p class="q-why">You will sign in to the App with your NHS login <strong>email address</strong> and <strong>password</strong>. Not sure? Try signing in to the NHS App first.</p>',
        '<p class="q-why">You will sign in to the App with your NHS login <strong>email address</strong> and <strong>password</strong>.</p>',
        'Can you sign in to your NHS login account?',
        ('Yes, I can sign in to NHS login', 'Yes, I can sign in to my NHS login'),
        ('No, or I’m not sure', 'No, I cannot sign in to my NHS login')),
 'c3': ('<p class="q-why">Your <strong>GM Early Years App</strong> account must use the same <strong>email address</strong> and <strong>mobile number</strong> as your NHS login.</p>',
        '<p class="q-why">Your <strong>GM Early Years App</strong> account must use the same <strong>email address</strong> and <strong>mobile number</strong> as your NHS login account.</p>',
        'Does your GM Early Years App account use the same email address and mobile number as your NHS login account?',
        ('Yes, they match', 'Yes, my account details match'),
        ('No, or I’m not sure', 'No, my account details do not match, or I’m not sure')),
 'c4': ('<p class="q-why">Your Health Visiting team sends the <strong>Activation Link</strong> by text message to the <strong>mobile number</strong> on your App account.</p>',
        None,
        'Have you received an Activation Link?',
        ('Yes, I have my Activation Link', 'Yes, I have my Activation Link'),
        ('No, or I’m not sure', 'No, I have not received an Activation Link')),
}
for pid, (why, why_new, ask, yes, no) in Q.items():
    n = pid[1]
    edit(pid, why, (why_new or why) + '\n<p class="q-ask" id="ask-%s">%s</p>' % (pid, ask))
    edit(pid, 'aria-labelledby="question-%s"' % n, 'aria-labelledby="ask-%s"' % pid)
    if yes[0] != yes[1]: edit(pid, '<span>%s</span></label>' % yes[0], '<span>%s</span></label>' % yes[1])
    edit(pid, '<span>%s</span></label>' % no[0], '<span>%s</span></label>' % no[1])

# stop message after No on questions 1 to 3 (David: shorter)
for pid in ('c1', 'c2', 'c3'):
    edit(pid, '<p>Select <strong>Next</strong> to complete the checklist. Your checklist summary will then explain what to do next.</p>',
         '<p>Select <strong>Next</strong> to complete the checklist.</p>')

# summary: instruction at the top; the amber box at the bottom said the same thing
edit('sum', '<span class="pos">Page 8 of 8</span></div></div>\n',
     '<span class="pos">Page 8 of 8</span></div></div>\n<p class="sum-intro">If any item below has a red cross, tap <strong>Get help</strong> next to it to find out what to do.</p>\n')
edit('sum', '<div class="sum-msg sum-no amber"><span class="k">Some things need sorting first</span><p>Select <strong>Get help</strong> next to each cross.</p></div>\n', '')

CSS = ('/* 2.64 checklist: the question on its own line; summary instruction */\n'
 '#app .screen .q-ask{font-family:var(--font-head);font-weight:700;font-size:17px!important;line-height:1.35;color:var(--ink);margin:14px 0 6px}\n'
 '#app .screen .q-ask+.q-hint{margin-top:0}\n'
 '#app .screen .q-why{min-height:0!important;margin-bottom:0!important}\n'
 '#app .screen .sum-intro{font-size:17px!important;line-height:1.4;color:var(--ink);margin:0 0 10px}\n')
rep('@media print{', CSS + '@media print{')

rep('Carer role v2.63', 'Carer role v2.64'); rep('Version 2.63 iPhone', 'Version 2.64 iPhone')
rep('<div>Version 2.63</div>', '<div>Version 2.64</div>'); rep('>2.63 – REVIEW DRAFT', '>2.64 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.61</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.63</span>', '<div class="rr"><span class="rv">2.64</span><span class="rd">17 Nov 2026</span><p>Checklist: each question asked on its own line, new answers; summary instruction</p></div>\n<div class="rr"><span class="rv">2.63</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
