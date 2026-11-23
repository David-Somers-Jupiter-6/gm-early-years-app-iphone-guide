"""Troubleshooter mock-ups from trial 3.70 (not published). Writes mock2/P.html (proposed, Q5 option A),
mock2/PB.html (Q5 option B), mock2/PM.html (questions 1 and 2 merged)."""
import re
BASE = open('/home/claude/repo/releases/GM_Early_Years_App_iPhone_v3.70.html', encoding='utf-8').read()

def build(q5='A', merged=False):
    s = BASE
    def sec(i):
        m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S); assert m, i; return m
    def in_sec(i, a, b, n=1):
        nonlocal s
        m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:70], blk.count(a))
        s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
    def sub_sec(i, f):
        nonlocal s
        m = sec(i); s = s[:m.start()] + f(m.group(0)) + s[m.end():]
    def answers(i, yes, no):
        def f(b):
            b, n = re.subn(r'(<input type="radio" class="ans ans-yes"[^>]*/><span class="rc" aria-hidden="true"></span>)<span class="ans-t"><span>[^<]*</span><span class="ans-g" aria-hidden="true">[^<]*</span></span>',
                           r'\1<span class="ans-t"><span>%s</span><span class="ans-g" aria-hidden="true">%s</span></span>' % (yes, yes), b); assert n == 1
            b, n = re.subn(r'(<input type="radio" class="ans ans-no"[^>]*/><span class="rc" aria-hidden="true"></span>)<span class="ans-t"><span>[^<]*</span><span class="ans-g" aria-hidden="true">[^<]*</span></span>',
                           r'\1<span class="ans-t"><span>%s</span><span class="ans-g" aria-hidden="true">%s</span></span>' % (no, no), b); assert n == 1
            return b
        sub_sec(i, f)
    STOP = re.search(r'<svg class="stop-ico".*?</svg>', s, re.S).group(0).replace('width="38" height="38"', 'width="28" height="28"')
    def stop(text): return '<div class="ans-msg msg-no amber stop-msg ts-stop" role="status"><span class="ok-ico ts-stopi" aria-hidden="true">%s</span><p class="ok-more">%s</p></div>' % (STOP, text)
    def tick(text): return '<div class="ans-msg msg-yes ok" role="status"><span class="ok-ico" aria-hidden="true">✓</span><p class="ok-more">%s</p></div>' % text
    def card(label, body): return '<div class="abc ts-card"><div class="abc-row"><span class="abc-ic ic-info" aria-hidden="true">i</span><div><p class="abc-k">%s</p>%s</div></div></div>' % (label, body)
    HEAD = '<div class="ts-ask"><p class="abc-k ts-ask-k"><span class="abc-ic ic-ask" aria-hidden="true">?</span>Question</p>\n'

    # 6 start page
    in_sec('ts', 'This troubleshooter should be answered by the <strong>child’s mother or primary carer</strong>, <strong>not a partner or family member</strong>.',
           'Please answer as the <strong>child’s mother or primary carer</strong> (the account holder).')
    # 4 questions 1-2
    for i in ['ts1', 'ts1b']:
        sub_sec(i, lambda b: re.sub(r'(<p class="q-ask" id="ask-ts1b?">)[^<]*(</p>)', r'\1Does that make sense?\2', b))
        answers(i, 'Yes, that makes sense', 'No, I’m not sure')
    # 3 question 3 Yes
    in_sec('ts2', '<p class="ok-more">You need your own NHS login to use the GM Early Years App.</p>', '<p class="ok-more">You will use it to sign in to the GM Early Years App.</p>')
    # 8 questions 4-6 in the new layout
    s = s.replace("var TSQ=['ts3','ts4','ts5'];", "var TSQ=[];")
    def replies(b, yes, no):
        a = b.index('<div class="ans-msg msg-yes'); z = b.index('</div>\n', b.index('<div class="ans-msg msg-no', a)) + 7
        a2 = b.index('<p class="need-ans"')
        need = b[a2:b.index('</p>', a2) + 4]
        return b[:a2] + '<div class="ts-replies">' + need + '\n' + tick(yes) + '\n' + stop(no) + '\n</div>\n' + b[z:]
    # Q4
    sub_sec('ts3', lambda b: replies(b, 'Use the same email address and password for the GM Early Years App.',
                                     'The NHS login Support team can help. See <a class="msg-link" href="#s4-cannot">Cannot sign in</a>.'))
    # Q5
    if q5 == 'A':
        info = '<p>Your GM Early Years App account must use the same <strong>mobile number</strong> and <strong>email address</strong> as your NHS login account.</p>'
        ask = 'Did you give your Health Visiting team the same mobile number and email address?'
    else:
        info = '<p>Your <strong>name</strong>, <strong>NHS number</strong>, <strong>mobile number</strong> and <strong>email address</strong> must be the same in both accounts.</p>'
        ask = 'Did you give your Health Visiting team the same details you use for NHS login?'
    def q5f(b):
        b = b.replace('<p class="q-why">Your GM Early Years App account must use the same <strong>contact details</strong> as your NHS login account.</p>', card('What must match', info))
        if q5 == 'A':
            b = re.sub(r'<div class="exc-r"><span class="exc-k">(Given name|Surname|NHS number)</span><span class="exc-v">[^<]*</span></div>', '', b)
        b = b.replace('<div class="ts-qa">', HEAD + '<div class="ts-qa">')
        b = re.sub(r'(<p class="q-ask" id="ask-ts4">)[^<]*(</p>)', r'\1%s\2' % ask, b)
        b = replies(b, 'Your details should match, so you can sign in.', 'Your details must match to sign in. See <a class="msg-link" href="#s4-problems">Details do not match</a>.')
        b = b.replace('</div>\n</div>\n<input type="radio" class="nudge-t"', '</div>\n</div>\n</div>\n<input type="radio" class="nudge-t"')
        return b
    sub_sec('ts4', q5f)
    # Q6
    def q6f(b):
        b = b.replace('<h3 class="h3 ts-sub"><span class="vh">GM Early Years App: </span>Your Activation Link</h3><p class="q-why">Your Health Visiting team sends an <strong>Activation Link</strong> by text to the mobile number on your GM Early Years App account.</p>',
                      card('How it arrives', '<p>Your Health Visiting team sends an <strong>Activation Link</strong> by text to the mobile number on your GM Early Years App account.</p>'))
        b = b.replace('<div class="ts-qa">', HEAD + '<div class="ts-qa">')
        b = replies(b, 'You have your Activation Link.', 'You need it to sign in. See <a class="msg-link" href="#s4-activation">Activation Link not received</a>.')
        b = b.replace('</div>\n</div>\n<input type="radio" class="nudge-t"', '</div>\n</div>\n</div>\n<input type="radio" class="nudge-t"')
        return b
    sub_sec('ts5', q6f)
    for i in ['ts3', 'ts4', 'ts5']:
        def gh(b):
            def g(mm):
                t = mm.group(1); return '<span class="rc" aria-hidden="true"></span><span class="ans-t"><span>%s</span><span class="ans-g" aria-hidden="true">%s</span></span></label>' % (t, t)
            return re.sub(r'<span class="rc" aria-hidden="true"></span><span>([^<]*)</span></label>', g, b)
        sub_sec(i, gh)
    if q5 == 'A' and False: pass
    answers('ts4', 'Yes, they are the same', 'No, or I’m not sure')
    # styles for questions 4-6: copy question 3's
    a = s.index('/* 3.70 question 3 copies question 1'); z = s.index('/* 3.70 questions 1-3: reply icon in the middle')
    q3 = s[a:z]
    extra = ''
    for i in ['ts3', 'ts4', 'ts5']:
        extra += re.sub(r'#ts2(?=[ :.])', '#' + i, q3)
    extra += ('#app :is(#ts3,#ts4,#ts5) .ts-replies>.ans-msg .ok-ico{top:50%!important;transform:translateY(-50%)}\n'
              '#app :is(#ts3,#ts4,#ts5) .radio .ans-t{display:grid}#app :is(#ts3,#ts4,#ts5) .radio .ans-t>span{grid-area:1/1}#app :is(#ts3,#ts4,#ts5) .radio .ans-g{font-weight:700;visibility:hidden}\n'
              '#app :is(#ts4,#ts5) .ts-ask{margin-top:6px!important;padding:5px 10px 8px!important}#app :is(#ts4,#ts5) .ts-ask .ts-ask-k{margin:0 0 2px!important}#app :is(#ts4,#ts5) .ts-ask .radio{min-height:48px!important;padding-top:9px!important;padding-bottom:9px!important}\n'
              '#app #ts4 .ts-info .ex-peek{margin-top:8px!important}\n'
              '#app :is(#ts1,#ts1b,#ts3,#ts4,#ts5) .ts-ask .q-ask{min-height:0!important}\n')
    z = s.index('/* 2.95 A. Troubleshooting help pages as three blocks */')
    s = s[:z] + extra + s[z:]
    # 7 results labels
    def resf(b):
        b = b.replace('<p class="sum-l">Account details</p>', '<p class="sum-l">Do your details match?</p>')
        b = b.replace('<p class="sum-l">Activation Link</p>', '<p class="sum-l">Has your link arrived?</p>')
        b = b.replace('The child’s mother or primary carer</p>', 'Set up for the child’s mother or primary carer</p>', 1)
        b = b.replace('Only the child’s mother or primary carer</p>', 'Only the account holder can access it</p>', 1)
        return b
    sub_sec('tsum', resf)
    if merged:
        in_sec('ts1', '<p class="abc-sub">In this guide, we call this person the <strong>account holder</strong>.</p></div></div></div>',
               '<p class="abc-sub">In this guide, we call this person the <strong>account holder</strong>.</p></div></div><div class="abc-row"><span class="abc-ic ic-info" aria-hidden="true">i</span><div><p class="abc-k">Who can access it</p><p>Only the <strong>account holder</strong> can access the account.</p></div></div></div>')
        in_sec('ts1', '<p class="ok-more">The account is set up for the child’s mother or primary carer.</p>', '<p class="ok-more">The account is for the account holder, and only they can access it.</p>')
        in_sec('ts1', 'Question 1 of 6', 'Question 1 of 5', 2)
        in_sec('ts1', '<span class="">6</span></div>', '</div>')
        z = s.index('/* 2.95 A. Troubleshooting help pages as three blocks */')
        s = s[:z] + '#app #ts1 .ts-card .abc-row:nth-child(2){background:#eef4fb!important;border-left-color:#005eb8!important;border-color:#eef4fb!important;border-left-color:#005eb8!important}\n' + s[z:]
    return s

open('/home/claude/mock2/P.html', 'w', encoding='utf-8').write(build('A'))
open('/home/claude/mock2/PB.html', 'w', encoding='utf-8').write(build('B'))
open('/home/claude/mock2/PM.html', 'w', encoding='utf-8').write(build('A', merged=True))
print('ok')
