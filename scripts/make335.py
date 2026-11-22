"""Guide 3.35 (from trial 3.34) – TRIAL. David, 22 Nov: on question 2 (Who has access?), Yes no longer says
"That is clear". It says "You are the account holder" (on the page and on Your results).
Question 4 (NHS login account): Yes "The account holder has an NHS login account"; No "The account holder needs an NHS login
account"; subheading and explanation reworded around the account holder.
Question 7: subheading "Have you received your Activation Link?" (was "Sent to you by text message").
Question 3 (Is this you?): No ("No, I am a partner or relative") says "Only the account holder can sign in to the account".
usage: python3 make335.py v3.34.html v3.35.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    assert blk.count(a) == 1, (pid, a); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
edit('ts1b', '<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">That is clear</p></div>',
             '<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">You are the account holder</p></div>')
edit('tsum', '<p class="sum-l">Who has access</p><p class="sum-s">That is clear</p>',
             '<p class="sum-l">Who has access</p><p class="sum-s">You are the account holder</p>')
edit('ts1c', '<h3>Only they can sign in</h3></div><p>Tap <strong>Next</strong> to continue.</p></div>',
             '<h3>Only the account holder can sign in to the account</h3></div></div>')
edit('tsum', '<p class="sum-l">Account holder</p><p class="sum-s">Only they can sign in</p>',
             '<p class="sum-l">Account holder</p><p class="sum-s">Only the account holder can sign in</p>')
CSS = "/* 3.35 questions 3 and 4: two-line messages stay compact */\n#app :is(#ts1c,#ts2,#ts5) .msg-no.stop-msg{padding:4px 10px!important;margin-top:4px!important}#app :is(#ts1c,#ts2,#ts5) .msg-no .stop-head{margin-bottom:0!important;align-items:center}#app :is(#ts1c,#ts2,#ts5) .msg-no .stop-ico{flex-basis:30px!important;width:30px!important;height:30px!important}#app :is(#ts1c,#ts2,#ts5) .msg-no .stop-head h3{font-size:16px!important;line-height:1.25!important}#app #ts2 .msg-yes.ok{padding-top:5px!important;padding-bottom:5px!important;margin-top:3px!important;align-items:center}#app #ts2 .msg-yes .ok-h{font-size:16px!important;line-height:1.25!important}\n"
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor)
# question 7: the subheading asks the question
edit('ts5', '<span class="vh">GM Early Years App: </span>Sent to you by text message</h3>', '<span class="vh">GM Early Years App: </span>Have you received your Activation Link?</h3>')
# question 4 (NHS login account)
edit('ts2', '<h3 class="h3 ts-sub"><span class="vh">NHS login: </span>They need their own NHS login</h3><p class="q-why">The GM Early Years App uses an <strong>NHS login</strong> account to sign in.</p>',
            '<h3 class="h3 ts-sub"><span class="vh">NHS login: </span>An NHS login account is needed</h3><p class="q-why">The account holder signs in to the GM Early Years App with their own <strong>NHS login</strong> account.</p>')
edit('ts2', '<p class="ok-h">They have NHS login</p>', '<p class="ok-h">The account holder has an NHS login account</p>')
edit('ts2', '<h3>They need NHS login first</h3></div><p>Tap <strong>Next</strong> to continue.</p></div>', '<h3>The account holder needs an NHS login account</h3></div></div>')
edit('tsum', '<p class="sum-l">NHS login account</p><p class="sum-s">They have NHS login</p>', '<p class="sum-l">NHS login account</p><p class="sum-s">The account holder has one</p>')
edit('tsum', '<p class="sum-l">NHS login account</p><p class="sum-s">They do not have NHS login yet</p>', '<p class="sum-l">NHS login account</p><p class="sum-s">The account holder needs one</p>')
rep('Carer role v3.34', 'Carer role v3.35'); rep('Version 3.34 iPhone', 'Version 3.35 iPhone')
rep('>3.34 – REVIEW DRAFT', '>3.35 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.34</span>', '<span class="cv-ver">Version 3.35</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.30</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.34</span>', '<div class="rr"><span class="rv">3.35</span><span class="rd">22 Nov 2026</span><p>Question 2: Yes says You are the account holder</p></div>\n<div class="rr"><span class="rv">3.34</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
