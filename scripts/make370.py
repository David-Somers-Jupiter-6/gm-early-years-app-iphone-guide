"""Guide 3.70 (from trial 3.69) – TRIAL. David, 23 Nov:
Question 3 (NHS login) laid out like questions 1 and 2:
 - title "Do you have NHS login?" (one line; was "Do you have an NHS login?"), also start page list and results page;
 - What you need: "You can only sign in to the GM Early Years App with your own NHS login account." (+ NHS login confirms who you are.);
 - question window straight under the information, no space under the question, reply slot kept so nothing moves;
 - Yes (green tick): "You need your own NHS login to use the GM Early Years App." (two lines);
 - No (STOP): "You need one to use the GM Early Years App. See Set up NHS login." (link; two lines);
 - icons in line with the answer circles; text in line with the answer text.
Questions 1-3: a reply's icon sits in the middle of its box, top to bottom; answers keep their height when chosen (bold).
usage: python3 make370.py v3.69.html v3.70.html [no-text-variant]"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
NOV = int(sys.argv[3]) if len(sys.argv) > 3 else 0
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def sec(i):
    return re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S)
def in_sec(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0)
    assert blk.count(a) == n, (i, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
T_OLD, T = 'Do you have an NHS login?', 'Do you have NHS login?'
rep('data-title="Troubleshooter · %s"' % T_OLD, 'data-title="Troubleshooter · %s"' % T)
rep('<span class="vh">Question 3 of 6: </span>%s</h2>' % T_OLD, '<span class="vh">Question 3 of 6: </span>%s</h2>' % T)
rep('<span aria-hidden="true">3</span>%s</li>' % T_OLD, '<span aria-hidden="true">3</span>%s</li>' % T)
in_sec('tsum', '<p class="sum-l">%s</p>' % T_OLD, '<p class="sum-l">%s</p>' % T, 3)
in_sec('ts2', '<p>You need your own <strong>NHS login</strong> account to use the GM Early Years App.</p>',
       '<p>You can only sign in to the GM Early Years App with your own <strong>NHS login</strong> account.</p>')
rep("var TSQ=['ts2','ts3','ts4','ts5'];", "var TSQ=['ts3','ts4','ts5'];")
m = sec('ts2'); blk = m.group(0)
a = blk.index('<p class="need-ans"'); z = blk.index('</div>\n</div>\n<input type="radio" class="nudge-t"')
blk = blk[:a] + '<div class="ts-replies">' + blk[a:z] + '</div>\n' + blk[z:]
s = s[:m.start()] + blk + s[m.end():]
in_sec('ts2', '<p class="ok-h">You have an NHS login account</p><p class="ok-more">You will use it to sign in to the GM Early Years App.</p>',
       '<p class="ok-more">You need your own NHS login to use the GM Early Years App.</p>')
NOS = ['You need one to use the GM Early Years App. See <a class="msg-link" href="#s4-setup">Set up NHS login</a>.',
       'You cannot use the GM Early Years App without one. See <a class="msg-link" href="#s4-setup">Set up NHS login</a>.',
       'You need an NHS login account first. See <a class="msg-link" href="#s4-setup">Set up NHS login</a>.']
m = sec('ts2'); blk = m.group(0)
old = re.search(r'<div class="ans-msg msg-no amber stop-msg" role="status"><div class="stop-head">(<svg class="stop-ico".*?</svg>)<h3>.*?</div>\n', blk, re.S)
svg = old.group(1).replace('width="38" height="38"', 'width="28" height="28"')
blk = blk.replace(old.group(0), '<div class="ans-msg msg-no amber stop-msg ts-stop" role="status"><span class="ok-ico ts-stopi" aria-hidden="true">%s</span><p class="ok-more">%s</p></div>\n' % (svg, NOS[NOV]))
s = s[:m.start()] + blk + s[m.end():]
a = s.index('/* 3.66 question 1:'); z = s.index('/* 3.69 question 2 copies question 1')
q3 = re.sub(r'#ts1(?=[ :.])', '#ts2', s[a:z]).replace('/* 3.66 question 1:', '/* 3.70 question 3 copies question 1 (3.66-3.68):', 1)
q3 += ('#app #ts2 .ts-help .ts-hi{position:static!important}\n'
       '#app #ts2 .ts-replies>.ans-msg.ok{padding-top:5px!important;padding-bottom:5px!important;align-items:center}\n'
       '#app #ts2 .ts-replies>.ans-msg.msg-no.stop-msg{position:relative;padding:5px 12px 5px 49px!important;margin:0!important}\n'
       '#app #ts2 .ts-replies>.ans-msg .ok-ico.ts-stopi{position:absolute!important;background:none!important;border-radius:0!important;display:block;padding:0!important}\n'
       '#app #ts2 .ts-stopi svg{display:block;width:28px;height:28px}\n'
       '#app #ts2 .ts-stop .msg-link{font-weight:700}\n'
       '#app #ts2 .ts-ask .q-ask{min-height:0!important}\n'
       '/* 3.70 questions 1-3: reply icon in the middle of its box */\n'
       '#app :is(#ts1,#ts1b,#ts2) .ts-replies>.ans-msg .ok-ico{top:50%!important;transform:translateY(-50%)}\n')
# answers keep the same height when they turn bold (a hidden bold copy reserves the room)
for i in ['ts1', 'ts1b', 'ts2']:
    m = sec(i); blk = m.group(0)
    def ghost(mm):
        t = mm.group(1)
        return '<span class="rc" aria-hidden="true"></span><span class="ans-t"><span>%s</span><span class="ans-g" aria-hidden="true">%s</span></span></label>' % (t, t)
    blk, n = re.subn(r'<span class="rc" aria-hidden="true"></span><span>([^<]*)</span></label>', ghost, blk); assert n == 2, (i, n)
    s = s[:m.start()] + blk + s[m.end():]
q3 += ('/* 3.70 questions 1-3: answer height does not change when the chosen answer turns bold */\n'
       '#app :is(#ts1,#ts1b,#ts2) .radio .ans-t{display:grid}\n'
       '#app :is(#ts1,#ts1b,#ts2) .radio .ans-t>span{grid-area:1/1}\n'
       '#app :is(#ts1,#ts1b,#ts2) .radio .ans-g{font-weight:700;visibility:hidden}\n')
z = s.index('/* 2.95 A. Troubleshooting help pages as three blocks */')
s = s[:z] + q3 + s[z:]
rep('Carer role v3.69', 'Carer role v3.70'); rep('Version 3.69 iPhone', 'Version 3.70 iPhone')
rep('>3.69 – REVIEW DRAFT', '>3.70 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.69</span>', '<span class="cv-ver">Version 3.70</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.65</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.69</span>', '<div class="rr"><span class="rv">3.70</span><span class="rd">23 Nov 2026</span><p>Question 3 laid out like questions 1 and 2; reply icons centred</p></div>\n<div class="rr"><span class="rv">3.69</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
