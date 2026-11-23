"""Guide 3.71 (from trial 3.70) – TRIAL. David, 23 Nov (review of the Troubleshooter mock-ups):
 - start page: "Please answer as the child's mother or primary carer (the account holder)." first;
   "Answer Yes or No. It takes a minute or two." stays at the end;
 - questions 1-6: the question window starts at the same height on every page, and every Yes / No reply box
   is the same size (the information area and the reply slot share one height across the six questions);
 - question 1: "In this guide, we call this person the account holder." joins the first sentence (same size);
   question 1 and 2: "Does that make sense?" / "Yes, that makes sense" / "No, I'm not sure";
 - question 3: "NHS login confirms who you are." joins the first sentence; Who can help window removed;
   No answer "No, I do not have NHS login"; Yes reply "You will use it to sign in to the GM Early Years App.";
 - question 4: new layout; Who can help removed; information is about being able to sign in to NHS login;
 - question 5: new layout, version B (name, NHS number, mobile number and email address must match);
 - question 6: new layout ("How it arrives").
 - Apple text sizes: start page list and end line 16.5 -> 17 (Body), list numbers 14 -> 15 (Subheadline),
   results heading 18 -> 17 (Headline) on the Troubleshooter and Checklist results.
usage: python3 make371.py v3.70.html v3.71.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); assert m, i; return m
def in_sec(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:70], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
def sub_sec(i, f):
    global s
    m = sec(i); s = s[:m.start()] + f(m.group(0)) + s[m.end():]
def ghost(b):
    def g(mm):
        t = mm.group(1); return '<span class="rc" aria-hidden="true"></span><span class="ans-t"><span>%s</span><span class="ans-g" aria-hidden="true">%s</span></span></label>' % (t, t)
    return re.sub(r'<span class="rc" aria-hidden="true"></span><span>([^<]*)</span></label>', g, b)
def answers(i, yes, no):
    def f(b):
        for cls, t in (('ans-yes', yes), ('ans-no', no)):
            if t is None: continue
            b, n = re.subn(r'(<input type="radio" class="ans %s"[^>]*/><span class="rc" aria-hidden="true"></span>)<span class="ans-t"><span>[^<]*</span><span class="ans-g" aria-hidden="true">[^<]*</span></span>' % cls,
                           r'\1<span class="ans-t"><span>%s</span><span class="ans-g" aria-hidden="true">%s</span></span>' % (t, t), b); assert n == 1, (i, cls)
        return b
    sub_sec(i, f)
STOP = re.search(r'<svg class="stop-ico".*?</svg>', s, re.S).group(0).replace('width="38" height="38"', 'width="28" height="28"')
def stop(text): return '<div class="ans-msg msg-no amber stop-msg ts-stop" role="status"><span class="ok-ico ts-stopi" aria-hidden="true">%s</span><p class="ok-more">%s</p></div>' % (STOP, text)
def tick(text): return '<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-more">%s</p></div>' % text
def card(label, body): return '<div class="abc ts-card"><div class="abc-row"><span class="abc-ic ic-info" aria-hidden="true">i</span><div><p class="abc-k">%s</p>%s</div></div></div>' % (label, body)
HEAD = '<div class="ts-ask"><p class="abc-k ts-ask-k"><span class="abc-ic ic-ask" aria-hidden="true">?</span>Question</p>\n'
WHO_ROW = re.compile(r'<div class="abc-row"><span class="abc-ic ic-who who-nhs" aria-hidden="true"></span><div><p class="abc-k">Who can help</p><p><strong>[^<]*</strong></p></div></div>')
def replies(b, yes, no):
    a2 = b.index('<p class="need-ans"'); need = b[a2:b.index('</p>', a2) + 4]
    a = b.index('<div class="ans-msg msg-yes'); z = b.index('</div>\n', b.index('<div class="ans-msg msg-no', a)) + 7
    return b[:a2] + '<div class="ts-replies">' + need + '\n' + tick(yes) + '\n' + stop(no) + '\n</div>\n' + b[z:]

# start page
in_sec('ts', '<p class="cq-end cq-who">This troubleshooter should be answered by the <strong>child’s mother or primary carer</strong>, <strong>not a partner or family member</strong>.</p>\n', '')
in_sec('ts', '<p class="lead cq-lead">', '<p class="lead cq-who cq-first">Please answer as the <strong>child’s mother or primary carer</strong> (the account holder).</p>\n<p class="lead cq-lead">')

# question 1
in_sec('ts1', '<strong>child’s mother or primary carer</strong>.</p><p class="abc-sub">In this guide, we call this person the <strong>account holder</strong>.</p>',
       '<strong>child’s mother or primary carer</strong>. In this guide, we call this person the <strong>account holder</strong>.</p>')
for i in ['ts1', 'ts1b']:
    sub_sec(i, lambda b: re.sub(r'(<p class="q-ask" id="ask-ts1b?">)[^<]*(</p>)', r'\1Does that make sense?\2', b))
    answers(i, 'Yes, that makes sense', 'No, I’m not sure')

# question 3
in_sec('ts2', 'account.</p><p class="abc-sub">NHS login confirms who you are.</p>', 'account. NHS login confirms who you are.</p>')
sub_sec('ts2', lambda b: WHO_ROW.sub('', b, count=1))
answers('ts2', None, 'No, I do not have NHS login')
in_sec('ts2', '<p class="ok-more">You need your own NHS login to use the GM Early Years App.</p>', '<p class="ok-more">You will use it to sign in to the GM Early Years App.</p>')

# question 4
def q4(b):
    b = b.replace(re.search(r'<div class="abc ts-card">.*?</div></div></div>', b, re.S).group(0),
                  card('Signing in', '<p>You need to be able to sign in to your own <strong>NHS login</strong> account before you can use the GM Early Years App.</p>'))
    b = replies(b, 'You can use NHS login to sign in to the GM Early Years App.',
                'The NHS login Support team can help. See <a class="msg-link" href="#s4-cannot">Cannot sign in</a>.')
    return ghost(b)
sub_sec('ts3', q4)

# question 5 (version B)
def q5(b):
    b = b.replace('<p class="q-why">Your GM Early Years App account must use the same <strong>contact details</strong> as your NHS login account.</p>',
                  card('What must match', '<p>Your <strong>name</strong>, <strong>NHS number</strong>, <strong>mobile number</strong> and <strong>email address</strong> must be the same in both accounts.</p>'))
    b = b.replace('<div class="ts-qa">', HEAD + '<div class="ts-qa">')
    b = re.sub(r'(<p class="q-ask" id="ask-ts4">)[^<]*(</p>)', r'\1Did you give your Health Visiting team the same details you use for NHS login?\2', b)
    b = replies(b, 'Your details should match, so you can sign in.', 'Your details must match to sign in. See <a class="msg-link" href="#s4-problems">Details do not match</a>.')
    b = b.replace('</div>\n</div>\n<input type="radio" class="nudge-t"', '</div>\n</div>\n</div>\n<input type="radio" class="nudge-t"')
    return ghost(b)
sub_sec('ts4', q5)
answers('ts4', 'Yes, they are the same', 'No, or I’m not sure')

# question 6
def q6(b):
    b = b.replace('<h3 class="h3 ts-sub"><span class="vh">GM Early Years App: </span>Your Activation Link</h3><p class="q-why">Your Health Visiting team sends an <strong>Activation Link</strong> by text to the mobile number on your GM Early Years App account.</p>',
                  card('How it arrives', '<p>Your Health Visiting team sends an <strong>Activation Link</strong> by text to the mobile number on your GM Early Years App account.</p>'))
    b = b.replace('<div class="ts-qa">', HEAD + '<div class="ts-qa">')
    b = replies(b, 'You have your Activation Link.', 'You need it to sign in. See <a class="msg-link" href="#s4-activation">Activation Link not received</a>.')
    b = b.replace('</div>\n</div>\n<input type="radio" class="nudge-t"', '</div>\n</div>\n</div>\n<input type="radio" class="nudge-t"')
    return ghost(b)
sub_sec('ts5', q6)

# same question start and same reply size on all six questions
rep("var TSQ=['ts3','ts4','ts5'];", "var TSQ=['ts1','ts1b','ts2','ts3','ts4','ts5'];")
rep("[TSQ,['.ts-info','.ts-qa']]", "[TSQ,['.ts-info','.ts-replies']]")

# styles: questions 4-6 copy question 3; all six share the rest
a = s.index('/* 3.70 question 3 copies question 1'); z = s.index('/* 3.70 questions 1-3: reply icon in the middle')
q3css = s[a:z]
css = '/* 3.71 questions 4-6 copy question 3 */\n'
for i in ['ts3', 'ts4', 'ts5']:
    css += re.sub(r'#ts2(?=[ :.])', '#' + i, q3css)
css += '''/* 3.71 all six questions */
#app :is(#ts3,#ts4,#ts5) .ts-replies>.ans-msg .ok-ico{top:50%!important;transform:translateY(-50%)}
#app :is(#ts3,#ts4,#ts5) .radio .ans-t{display:grid}#app :is(#ts3,#ts4,#ts5) .radio .ans-t>span{grid-area:1/1}#app :is(#ts3,#ts4,#ts5) .radio .ans-g{font-weight:700;visibility:hidden}
#app :is(#ts4,#ts5) .ts-ask{margin-top:6px!important;padding:5px 10px 8px!important}#app :is(#ts4,#ts5) .ts-ask .ts-ask-k{margin:0 0 2px!important}#app :is(#ts4,#ts5) .ts-ask .radio{min-height:48px!important;padding-top:9px!important;padding-bottom:9px!important}
#app #ts4 .ts-info .ex-peek{margin-top:8px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .q-ask{min-height:0!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-replies>*{align-self:stretch!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .ts-replies>.ans-msg.ans-msg{margin:0!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-replies>.ans-msg{display:flex!important;flex-direction:column;justify-content:center;align-items:stretch!important}
#app #ts .cq-first{margin:0 0 10px!important;color:var(--ink)!important}
/* 3.71 Apple text sizes (Body 17, Subheadline 15) on the Troubleshooter start and results pages */
#app #ts .cq li,#app #ts .cq-end{font-size:17px!important}
#app #ts .cq li>span{font-size:15px!important}
#app :is(#sum,#tsum) .sm-ban b{font-size:17px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .ts-replies>.need-ans{padding-top:5px!important;padding-bottom:5px!important}
'''
z = s.index('/* 2.95 A. Troubleshooting help pages as three blocks */')
s = s[:z] + css + s[z:]

rep('Carer role v3.70', 'Carer role v3.71'); rep('Version 3.70 iPhone', 'Version 3.71 iPhone')
rep('>3.70 – REVIEW DRAFT', '>3.71 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.70</span>', '<span class="cv-ver">Version 3.71</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.66</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.70</span>', '<div class="rr"><span class="rv">3.71</span><span class="rd">23 Nov 2026</span><p>Troubleshooter: questions start at the same height; same-size replies; wording updates</p></div>\n<div class="rr"><span class="rv">3.70</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
