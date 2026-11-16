"""Guide 2.54 (from 2.53).
Checklist questions 1 to 4: the message shown after "No, or I'm not sure" is now the same short stop
message on every question, with no links. The detailed help is given once, on the checklist results
page (Get help next to each cross).
- Question 1's Get help on the results page now opens "What stopped you signing in?" (s4-problems),
  which has the NHS login set-up guidance, in place of Question 1 itself.
usage: python3 make254.py v2.53.html v2.54.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

def page(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S)
    assert m, pid
    return m

def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

STOP_SVG = re.search(r'<div class="stop-head">(<svg.*?</svg>)', page('c1').group(0), re.S).group(1)
TITLE = 'You will not be able to access a GM Early Years App account'
BODY = {
    'c1': 'Select <strong>Next</strong> to complete the checklist. Your checklist results will then explain what to do next.',
    'c2': 'Select <strong>Next</strong> to complete the checklist. Your checklist results will then explain what to do next.',
    'c3': 'Select <strong>Next</strong> to complete the checklist. Your checklist results will then explain what to do next.',
    'c4': 'Select <strong>Next</strong> to see your checklist results and what to do next.',
}
for pid, body in BODY.items():
    m = page(pid); blk = m.group(0)
    a = blk.index('<div class="ans-msg msg-no')
    z = blk.index('<input type="radio" class="nudge-t"')
    end = blk.rindex('</div>\n', a, z)            # the closing tag of the answers block stays
    new = ('<div class="ans-msg msg-no amber stop-msg" role="status"><div class="stop-head">' + STOP_SVG +
           '<h3>' + TITLE + '</h3></div><p>' + body + '</p></div>\n')
    blk = blk[:a] + new + blk[end:]
    assert blk.count('ans-msg msg-no') == 1, pid
    assert 'https://' not in blk[a:a + len(new)], pid
    s = s[:m.start()] + blk + s[m.end():]

# Question 1's Get help now goes to the NHS login set-up help in Troubleshooting
edit('sum', '<a class="sum-help" href="#c1">Get help', '<a class="sum-help" href="#s4-problems">Get help')

css = '''/* 2.54 the same short stop message after "No, or I'm not sure" on every checklist question */
.ans-msg.msg-no.stop-msg p{margin:0;font-size:17px!important;line-height:1.4!important}
.stop-msg .stop-head h3{font-size:17px;line-height:1.25}
'''
rep('@media print{', css + '@media print{')

# ---------------------------------------------------------------- version
rep('Carer role v2.53', 'Carer role v2.54'); rep('Version 2.53 iPhone', 'Version 2.54 iPhone')
rep('<div>Version 2.53</div>', '<div>Version 2.54</div>'); rep('>2.53 – REVIEW DRAFT', '>2.54 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.51</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.53</span>', '<div class="rr"><span class="rv">2.54</span><span class="rd">16 Nov 2026</span><p>Checklist: one short message after a No answer; help is on the results page</p></div>\n<div class="rr"><span class="rv">2.53</span>')
open(dst, 'w', encoding='utf-8').write(s)
print('written', dst)
