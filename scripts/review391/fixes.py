"""3.91 – Sign-in check polish (David, 26 Nov).
1. Start page (ts): the 6 questions are in pairs (1–2 your App account, 3–4 your NHS login, 5–6 both accounts).
   The dividers sat inside each pair (between 1 and 2, 3 and 4, 5 and 6). Now there is no divider inside a pair and
   one divider below question 2 and one below question 4, in the middle of the gap between the pairs.
2. Questions 1–6, layout with the "?" icon beside the question (screens up to 760 px high): the question's first line
   sat 5.5 px (1.5 px on screens up to 640 px high) below the middle of the "?" icon. The space above the question is
   reduced so the first line is centred on the icon, as "i" and "Who it is for" are above it; everything below moves
   up by the same amount on all six questions, so they still line up.
usage: fixes.py src out"""
import sys
s = open(sys.argv[1], encoding='utf-8').read()
css = '''
/* 3.91 Sign-in check start: one divider below question 2 and below question 4 (between the pairs), none inside a pair */
#app #ts.screen .tsp-list.tsp-list>li+li{background:none!important}
#app #ts.screen .tsp-list.tsp-list:has(~ .tsp-list){position:relative!important;overflow:visible!important}
#app #ts.screen .tsp-list.tsp-list:has(~ .tsp-list)::after{content:"";position:absolute;left:0;right:0;bottom:-3.5px;height:1px;background:var(--line);pointer-events:none}
/* 3.91 Sign-in check questions: first line of the question centred on the "?" icon (layout with the icon beside it) */
@media (max-height:760px){html body #app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .ts-qa.ts-qa.ts-qa{padding-top:.5px!important}}
@media (max-height:640px){html body #app :is(#ts1,#ts1b,#ts2,#ts3,#ts4,#ts5) .ts-ask .ts-qa.ts-qa.ts-qa{padding-top:4.5px!important}}
'''
i = s.rindex('</style>'); s = s[:i] + css + s[i:]
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
