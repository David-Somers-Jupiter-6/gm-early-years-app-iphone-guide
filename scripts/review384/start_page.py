"""Sign-in check start page layouts. usage: tsp.py src out A|B"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read(); V = sys.argv[3]
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % re.escape(i), s, re.S); assert m, i; return m
def rin(i, a, b):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == 1, (i, a[:80], blk.count(a)); s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
PERSON = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4 20c1.2-4 4.4-6 8-6s6.8 2 8 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
Q = ['Who is the account for?', 'Who can sign in?', 'Do you have NHS login?',
     'Can you sign in to NHS login?', 'Do your details match?', 'Has your Activation Link arrived?']
m = sec('ts').group(0)
a = m.index('<p class="lead cq-who cq-first">'); z = m.index('</p>', m.index('<p class="cq-end">')) + 4
old = m[a:z]
who = ('<div class="tsp-who"><span class="tsp-wi">%s</span><div><p class="tsp-k">Who should answer</p>'
       '<p class="tsp-v">The <strong>child’s mother or primary carer</strong> (the account holder)</p></div></div>\n' % PERSON)
lead = '<p class="tsp-lead">Answer <strong>6 quick questions</strong>. At the end, you will see what is stopping you and what to do next.</p>\n'
def row(n): return '<li><span class="tsp-n" aria-hidden="true">%d</span><span class="tsp-t">%s</span></li>' % (n, Q[n - 1])
end = '<p class="tsp-end fit-opt"><span class="tsp-ci">%s</span><span>Answer <strong>Yes</strong> or <strong>No</strong>. It takes about 2 minutes.</span></p>' % CLOCK
if V == 'A':
    body = who + lead + '<ol class="tsp-list">' + ''.join(row(n) for n in range(1, 7)) + '</ol>\n' + end
else:
    def grp(title, ns): return '<p class="tsp-gh">%s</p><ol class="tsp-list" start="%d">%s</ol>\n' % (title, ns[0], ''.join(row(n) for n in ns))
    body = (who + lead + grp('Your App account', [1, 2]) + grp('Your NHS login', [3, 4]) + grp('Both accounts', [5, 6]) + end)
rin('ts', old, body)
css = '''
#app #ts .tsp-who{display:flex;gap:12px;align-items:center;margin:2px 0 12px;padding:11px 14px;border-radius:14px;background:var(--surface);border:1px solid var(--line)}
#app #ts .tsp-wi{flex:0 0 36px;height:36px;border-radius:50%;display:grid;place-items:center;background:#f6e3ec;color:#a3124d}
#app #ts .tsp-k{margin:0 0 1px;font:700 12px/1.2 var(--font-head);letter-spacing:.08em;text-transform:uppercase;color:var(--sub)}
#app #ts .tsp-v{margin:0;font-size:17px;line-height:1.35;color:var(--ink)}
#app #ts .tsp-lead{margin:0 0 14px;font-size:17px;line-height:1.45;color:var(--ink)}
#app #ts .tsp-list{list-style:none;margin:0;padding:0 14px;border-radius:14px;background:var(--surface);border:1px solid var(--line);box-shadow:0 1px 2px rgba(16,40,70,.04),0 3px 10px rgba(16,40,70,.05)}
#app #ts .tsp-list li{display:flex;align-items:center;gap:14px;min-height:50px;padding:7px 0;font-size:17px;line-height:1.3;color:var(--ink);font-weight:400}
#app #ts .tsp-list li+li{border-top:1px solid var(--line)}
#app #ts .tsp-n{flex:0 0 28px;height:28px;border-radius:50%;display:grid;place-items:center;font:700 15px/1 var(--font-head);background:#f6e3ec;color:#a3124d}
#app #ts .tsp-end{display:flex;align-items:center;gap:8px;margin:14px 0 0;font-size:15px;color:var(--sub)}
#app #ts .tsp-ci{color:var(--sub);display:flex}
#app #ts .tsp-gh{margin:10px 2px 4px;font:700 12px/1.2 var(--font-head);letter-spacing:.08em;text-transform:uppercase;color:var(--sub)}
#app #ts .tsp-gh:first-of-type{margin-top:0}
#app #ts .tsp-lead+.tsp-gh{margin-top:0}
#app #ts .tsp-gh~.tsp-list li{min-height:44px;padding:4px 0}
#app #ts .tsp-gh~.tsp-list{box-shadow:none}
@media (prefers-color-scheme:dark){#app #ts :is(.tsp-wi,.tsp-n){background:#3a1a2c;color:#ff9ec4}}
@media screen and (max-height:700px){
#app #ts .tsp-end{display:none}
#app #ts .tsp-gh{display:none}#app #ts .tsp-list+.tsp-gh+.tsp-list{margin-top:6px}
#app #ts .tsp-who{padding:8px 12px;margin-bottom:8px}#app #ts .tsp-wi{flex-basis:30px;height:30px}
#app #ts .tsp-lead{margin-bottom:8px;line-height:1.35}
#app #ts .tsp-list li{min-height:40px;padding:4px 0}#app #ts .tsp-gh~.tsp-list li{min-height:38px;padding:3px 0}
#app #ts .tsp-gh{margin:7px 2px 3px}#app #ts .tsp-n{flex-basis:24px;height:24px;font-size:13px}
#app #ts .tsp-end{margin-top:8px}
}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok', V)
