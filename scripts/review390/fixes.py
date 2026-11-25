"""3.90 – Sign-in check questions 1 and 2 ask something real (point 3 of the problems-and-solutions doc, David 25 Nov).
Before, both asked "Does that make sense?", yet the results showed "Who is the account for? ✓" as if it had been checked.
Question 1: "Is the account for you?" – Are you the child's mother or primary carer? (Yes, I am / No, I am not)
Question 2: "Will you sign in yourself?" – Will you be the one signing in? (Yes, I will / No, someone else will)
The info cards use the wording from the mock-up. The "Please tap an answer, then tap Next." strip (need-ans) is kept
exactly as it was on both pages (David). Start page list, results rows, page titles (Search) use the new names.
Results: a No to these questions is now a real problem (✗ + Get help, counted), not a soft "i" + Read more.
usage: fixes.py src out"""
import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    c = s.count(x); assert c == n, (x[:100], c); s = s.replace(x, y)
def sec(sid):
    i = s.index(f'<section class="screen" id="{sid}"'); j = s.index('</section>', i); return i, j
def in_sec(sid, x, y, n=1):
    global s
    i, j = sec(sid); t = s[i:j]; c = t.count(x); assert c == n, (sid, x[:100], c)
    s = s[:i] + t.replace(x, y) + s[j:]
NEED = '<p class="need-ans" role="status" aria-live="polite"><span class="ni" aria-hidden="true">i</span><span>Please tap an answer, then tap <strong>Next</strong>.</span></p>'
before_need = {k: (lambda i_j: s[i_j[0]:i_j[1]].count(NEED))(sec(k)) for k in ('ts1', 'ts1b')}
assert before_need == {'ts1': 1, 'ts1b': 1}, before_need

# ---- Question 1 ----
in_sec('ts1', 'data-title="Sign-in check · Who is the account for?"', 'data-title="Sign-in check · Is the account for you?"')
in_sec('ts1', '<span class="vh">Question 1 of 6: </span>Who is the account for?</h2>', '<span class="vh">Question 1 of 6: </span>Is the account for you?</h2>')
in_sec('ts1', '<p class="abc-k">Who it is for</p><p>Your Health Visiting team sets up the account for the <strong>child’s mother or primary carer</strong>. We call this person the <strong class="nb">account holder</strong>.</p><p class="abc-k ts-k2">If it is for the wrong person</p><p>Your Health Visiting team can put it right.</p>',
           '<p class="abc-k">Who it is for</p><p>The account is for the <strong>child’s mother or primary carer</strong>. We call this person the <strong class="nb">account holder</strong>.</p><p class="abc-k ts-k2">If it is for someone else</p><p>Your Health Visiting team can put it right.</p>')
in_sec('ts1', '<p class="q-ask" id="ask-ts1">Does that make sense?</p>', '<p class="q-ask" id="ask-ts1">Are you the child’s mother or primary carer?</p>')
in_sec('ts1', '<span>Yes, that makes sense</span><span class="ans-g" aria-hidden="true">Yes, that makes sense</span>', '<span>Yes, I am</span><span class="ans-g" aria-hidden="true">Yes, I am</span>')
in_sec('ts1', '<span>No, I’m not sure</span><span class="ans-g" aria-hidden="true">No, I’m not sure</span>', '<span>No, I am not</span><span class="ans-g" aria-hidden="true">No, I am not</span>')
in_sec('ts1', '<p class="ok-more">The account is set up for the child’s mother or primary carer.</p>', '<p class="ok-more">Good – you are the account holder.</p>')

# ---- Question 2 ----
in_sec('ts1b', 'data-title="Sign-in check · Who can sign in to the account?"', 'data-title="Sign-in check · Will you sign in yourself?"')
in_sec('ts1b', '<span class="vh">Question 2 of 6: </span>Who can sign in to the account?</h2>', '<span class="vh">Question 2 of 6: </span>Will you sign in yourself?</h2>')
in_sec('ts1b', '<p class="abc-k">Who can access it</p><p>Only the <strong class="nb">account holder</strong> (the child’s mother or primary carer).</p><p class="abc-k ts-k2">How they sign in</p><p>With their own <strong class="nb">NHS login</strong>. Nobody else can sign in for them.</p>',
           '<p class="abc-k">Who can sign in</p><p>Only the <strong class="nb">account holder</strong>, with their own <strong class="nb">NHS login</strong>.</p><p class="abc-k ts-k2">Who cannot</p><p>A partner or family member cannot sign in for you.</p>')
in_sec('ts1b', '<p class="q-ask" id="ask-ts1b">Does that make sense?</p>', '<p class="q-ask" id="ask-ts1b">Will you be the one signing in?</p>')
in_sec('ts1b', '<span>Yes, that makes sense</span><span class="ans-g" aria-hidden="true">Yes, that makes sense</span>', '<span>Yes, I will</span><span class="ans-g" aria-hidden="true">Yes, I will</span>')
in_sec('ts1b', '<span>No, I’m not sure</span><span class="ans-g" aria-hidden="true">No, I’m not sure</span>', '<span>No, someone else will</span><span class="ans-g" aria-hidden="true">No, someone else will</span>')
in_sec('ts1b', '<p class="ok-more">Only the account holder can access the account.</p>', '<p class="ok-more">Good – only you can sign in to your account.</p>')

# ---- Start page list ----
in_sec('ts', '<span class="tsp-t">Who is the account for?</span><a class="tsp-help" href="#s4-who" aria-label="Help with question 1: Who is the account for?">',
             '<span class="tsp-t">Is the account for you?</span><a class="tsp-help" href="#s4-who" aria-label="Help with question 1: Is the account for you?">')
in_sec('ts', '<span class="tsp-t">Who can sign in?</span><a class="tsp-help" href="#s4-2" aria-label="Help with question 2: Who can sign in?">',
             '<span class="tsp-t">Will you sign in yourself?</span><a class="tsp-help" href="#s4-2" aria-label="Help with question 2: Will you sign in yourself?">')

# ---- Results rows ----
in_sec('tsum', '<p class="sum-l">Who is the account for?</p>', '<p class="sum-l">Is the account for you?</p>', 3)
in_sec('tsum', '<p class="sum-s">The child’s mother or primary carer</p>', '<p class="sum-s">You are the account holder</p>')
in_sec('tsum', '<p class="sum-l">Who can sign in?</p>', '<p class="sum-l">Will you sign in yourself?</p>', 3)
in_sec('tsum', '<p class="sum-s">Only the child’s mother or primary carer</p>', '<p class="sum-s">Only you can sign in</p>')
# a No is now a real problem: same ✗ + Get help as questions 3–6
in_sec('tsum', '<div class="st st-no soft"><span class="sum-ico n soft" aria-hidden="true">i</span><div class="sum-t"><p class="sum-l">Is the account for you?</p><p class="sum-s">Read who will be set up with an account</p></div><a class="sum-help" href="#s4-who">Read more',
               '<div class="st st-no"><span class="sum-ico n" aria-hidden="true">✗</span><div class="sum-t"><p class="sum-l">Is the account for you?</p><p class="sum-s">Only the account holder can sign in</p></div><a class="sum-help" href="#s4-who">Get help')
in_sec('tsum', '<div class="st st-no soft"><span class="sum-ico n soft" aria-hidden="true">i</span><div class="sum-t"><p class="sum-l">Will you sign in yourself?</p><p class="sum-s">Read who can access the account</p></div><a class="sum-help" href="#s4-2">Read more',
               '<div class="st st-no"><span class="sum-ico n" aria-hidden="true">✗</span><div class="sum-t"><p class="sum-l">Will you sign in yourself?</p><p class="sum-s">Someone else cannot sign in for you</p></div><a class="sum-help" href="#s4-2">Get help')

after_need = {k: (lambda i_j: s[i_j[0]:i_j[1]].count(NEED))(sec(k)) for k in ('ts1', 'ts1b')}
assert after_need == before_need, after_need   # the hint strip is untouched
# iPhone SE in Safari: question 1's title fits on one line while 2–6 take two, so its question sat 27 px higher
# (already so in 3.89). Same title-box height on all six there, so nothing moves between the questions.
s = s.replace('</style>', '''
/* 3.90 Sign-in check questions on the shortest screens: same title-box height on every question */
@media (max-height:600px) and (max-width:389px){#app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .pbox{min-height:114px!important}}
</style>''', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
