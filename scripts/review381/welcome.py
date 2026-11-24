"""3.81 review: Introduction, Contents, How this guide works. usage: welcome.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % re.escape(i), s, re.S); assert m, i; return m
def rep(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# Introduction
rep('intro', '<p class="iv-calm">If you have tried before and it did not work, it usually comes down to one small detail. This guide will help you find it, one step at a time.</p>',
    '<p class="iv-calm">If you have tried before and it did not work, it is often one small detail, like a mobile number that does not match. This guide helps you find it, step by step.</p>')
rep('intro', '<h3 class="h3">Tip: read the guide on a second screen</h3>', '<h3 class="h3">Tip: read this guide on another screen</h3>')
rep('intro', '<p class="iv-then fit-opt">Then follow the steps on your own iPhone.</p>',
    '<p class="iv-then fit-opt">Then sign in on your own iPhone. Only have your iPhone? Read each step, then do it.</p>')

# Contents
def sub(href, text):
    global s
    m = sec('contents'); blk = m.group(0)
    pat = r'(<a class="toc-row" href="#%s"><span class="gb">\d</span><span class="tt">)([^<]*)(</span>)' % href
    blk2, n = re.subn(pat, r'\1\2<small class="toc-sub">%s</small>\3' % text, blk); assert n == 1, href
    s = s[:m.start()] + blk2 + s[m.end():]
sub('ts', 'Find out what is stopping you')
sub('s4', 'Help with NHS login or the App')
sub('s5', 'Who to contact for each problem')
rep('contents', '<a class="toc-row" href="#how"><span class="gb">1</span><span class="tt">How this guide works</span><svg',
    'PLACEHOLDER')
blk = sec('contents').group(0)
a = blk.index('PLACEHOLDER'); z = blk.index('</a></div>', a) + len('</a></div>')
row = blk[a:z].replace('PLACEHOLDER', '<a class="toc-row" href="#how"><span class="gb">1</span><span class="tt">How this guide works</span><svg')
rep('contents', blk[a:z], '</div>\n<div class="toc-g">' + row[:-len('</div>')] + '</div>')

# How this guide works
rep('how', '<p class="hw-p hw-will">Here is what will happen:</p>', '<p class="hw-p hw-will">There are 3 stages:</p>')
rep('how', '<span><strong>Check what you need:</strong> your Health Visiting team, then the Troubleshooter’s 6 quick Yes or No questions</span>',
    '<span><span class="hw-k">Stage 1 · What you need</span>Find your Health Visiting team, then answer 6 quick Yes or No questions.</span>')
rep('how', '<span><strong>Sign in, one step at a time,</strong> with a picture of each screen</span>',
    '<span><span class="hw-k">Stage 2 · How to sign in</span>Follow the steps one at a time, with a picture of each screen.</span>')
rep('how', '<span><strong>Get the right help</strong> if something is not right: who to contact and what to do</span>',
    '<span><span class="hw-k">Stage 3 · Who can help</span>If something is not right, see who to contact and what to do.</span>')
rep('how', '</ol>\n</div>', '</ol>\n<div class="push" aria-hidden="true"></div>\n<div class="tip nav-tip" role="note"><p>The stage you are on is shown at the top of each page, so you always know where you are.</p></div>\n</div>')

css = ('#app #contents .toc-sub{display:block;font-size:15px;font-weight:400;line-height:1.3;color:var(--sub);margin-top:1px}\n'
       '#app #how .hw-k{display:block;font:700 13px/1.3 var(--font-head);letter-spacing:.06em;text-transform:uppercase;color:var(--accent2,#8a1450);margin:0 0 3px}\n'
       '#app #how .hw-list li>span:last-child{font-weight:400}\n')
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
