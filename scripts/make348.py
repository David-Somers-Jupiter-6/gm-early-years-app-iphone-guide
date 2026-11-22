"""Guide 3.48 (from trial 3.47) – TRIAL. David, 22 Nov, question 2 (Who has access?):
 - "In this guide, we call this person the account holder." is replaced with a warning:
   "A partner or family member cannot sign in to the account."
 - No: "See Only the account holder can access for help." (shorter, so it fits on two lines).
usage: python3 make348.py v3.47.html v3.48.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % pid, s, re.S); blk = m.group(0)
    assert blk.count(a) == 1, (pid, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
blk = re.search(r'<section class="screen" id="ts1b".*?</section>', s, re.S).group(0)
old = re.search(r'<p class="q-why[^"]*">In this guide, we call this person the <strong>account holder</strong>\.</p>', blk).group(0)
edit('ts1b', old, '<p class="q-why ts-warn"><span class="tw-i" aria-hidden="true">!</span><span><span class="vh">Warning: </span>A partner or family member cannot sign in to the account.</span></p>')
edit('ts1b', '<p class="ok-h">Please see <a class="msg-link" href="#s4-2">Only the account holder can access</a> for more information.</p>',
             '<p class="ok-h">See <a class="msg-link" href="#s4-2">Only the account holder can access</a> for help.</p>')
CSS = """/* 3.48 question 2: warning line */
#app #ts1b .ts-warn{display:flex;align-items:flex-start;gap:8px;margin-top:6px!important;padding:6px 10px;border-radius:8px;background:var(--amberBg,#fff4d6);border-left:4px solid var(--hl,#ffb81c);font-weight:700;color:var(--ink)}
#app #ts1b .ans-msg.ok{padding-top:4px!important;padding-bottom:4px!important;margin-top:3px!important;align-items:center}#app #ts1b .ans-msg .ok-h{font-size:16px!important;line-height:1.22!important}
#app #ts1b .ts-warn .tw-i{flex:0 0 20px;height:20px;margin-top:2px;border-radius:50%;background:#d5281b;color:#fff;font:700 13px/20px var(--font-head,Arial);text-align:center}
"""
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor); assert CSS.count('{') == CSS.count('}')
rep('Carer role v3.47', 'Carer role v3.48'); rep('Version 3.47 iPhone', 'Version 3.48 iPhone')
rep('>3.47 – REVIEW DRAFT', '>3.48 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.47</span>', '<span class="cv-ver">Version 3.48</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.43</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.47</span>', '<div class="rr"><span class="rv">3.48</span><span class="rd">22 Nov 2026</span><p>Question 2: partner warning; shorter No message</p></div>\n<div class="rr"><span class="rv">3.47</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
