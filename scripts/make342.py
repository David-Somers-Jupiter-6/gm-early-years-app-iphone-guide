"""Guide 3.42 (from trial 3.41) – TRIAL. David, 22 Nov: on question 1 (Who is set up with an account?), Yes shows
"Yes, the child's mother or primary carer" (was "That is clear"). Compact two-line message, as on question 4.
usage: python3 make342.py v3.41.html v3.42.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
m = re.search(r'<section class="screen" id="ts1".*?</section>', s, re.S); blk = m.group(0)
a = '<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">That is clear</p></div>'
assert blk.count(a) == 1
blk = blk.replace(a, '<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-h">Yes, the child’s mother or primary carer</p></div>')
s = s[:m.start()] + blk + s[m.end():]
CSS = "/* 3.42 question 1: two-line Yes message stays compact */\n#app #ts1 .msg-yes.ok{padding-top:5px!important;padding-bottom:5px!important;margin-top:3px!important;align-items:center}#app #ts1 .msg-yes .ok-h{font-size:16px!important;line-height:1.25!important}\n"
anchor = '/* 2.88 Step 1:'; assert s.count(anchor) == 1; s = s.replace(anchor, CSS + anchor)
rep('Carer role v3.41', 'Carer role v3.42'); rep('Version 3.41 iPhone', 'Version 3.42 iPhone')
rep('>3.41 – REVIEW DRAFT', '>3.42 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.41</span>', '<span class="cv-ver">Version 3.42</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.37</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.41</span>', '<div class="rr"><span class="rv">3.42</span><span class="rd">22 Nov 2026</span><p>Question 1: Yes says Yes, the child’s mother or primary carer</p></div>\n<div class="rr"><span class="rv">3.41</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
