"""Design review 5: fixed rules for shape and spacing.
Corners: 16 (screenshots), 12 (cards and panels), 8 (small items), capsules for buttons.
Cards: shadow only in light, a hairline border only in Dark Mode. Answer boxes and inputs: border only.
Left stripes kept only where they signal a status (answers, warnings). Spacing on an 8 step (16/8/4).
usage: tokens.py src out"""
import sys
s = open(sys.argv[1], encoding='utf-8').read()
A = '#app .screen '
CARD = ':is(.abc-row,.stuck,.ts-ask,.tp-card,.toc-g,.st-list,ul.nd,ul.iv,.tsp-list,.tc-list,.tr-list,.wc-list)'
CALL = ':is(.tip,.hv-card,.hv-find,.need-ans,.ans-msg,.amber,.st-mail,.jr-n)'
css = f'''
/* DR5 shape and spacing rules */
html{{--r-lg:16px;--r-md:12px;--r-sm:8px;--card-sh:0 1px 2px rgba(16,40,70,.05),0 2px 8px rgba(16,40,70,.06)}}
/* corners */
{A}{CARD},{A}{CALL},{A}li.st-row{{border-radius:var(--r-md)!important}}
{A}label.shot{{border-radius:var(--r-lg)!important}}
{A}:is(.abc-ic.who-nhs,.chip,.gb,.tc-tile,.tr-i,.tsp-n,.hw-n,.wc-tile,.sp-warn){{border-radius:var(--r-sm)!important}}
#app .menu-btn{{border-radius:var(--r-md)!important}}
/* cards: shadow, no border */
{A}{CARD}{{border:0!important;box-shadow:var(--card-sh)!important}}
{A}label.shot{{border:0!important}}
/* white cards lose the thick left stripe; padding made even */
{A}.abc-row{{padding-left:12px!important;padding-right:12px!important}}
{A}.ts-ask{{padding-left:12px!important;padding-right:12px!important}}
/* blue tips and help cards: tint only, no stripe */
{A}:is(.tip,.hv-card){{border-left:0!important;padding-left:14px!important;padding-right:14px!important}}
/* answer boxes and inputs: border, no shadow */
{A}:is(label.radio,select){{box-shadow:none!important}}
/* Dark Mode: no shadows, a hairline border instead */
@media (prefers-color-scheme:dark){{
{A}{CARD},{A}label.shot{{box-shadow:none!important;border:1px solid rgba(255,255,255,.12)!important}}
}}
/* spacing on an 8 step: 16 between groups, 8 between related items, 4 from a label to its content */
#app .screen .scroll>.pbox,#app .screen .scroll>.tp-card{{margin-bottom:16px!important}}
{A}:is(.info-lead,.hw-p,.iv-calm,.tsp-lead){{margin-bottom:16px!important}}
#app #s3 .jr{{margin-bottom:16px!important}}
{A}.info-lead.ci1-for{{margin-bottom:0!important}}
{A}.calm{{margin-bottom:8px!important}}
{A}.step-body>p+p{{margin-top:8px!important}}
{A}.abc+.hv-card,{A}.info-lead+.hv-card,{A}.hv-card+.hv-card{{margin-top:8px!important}}
{A}.abc{{margin-top:0!important}}
{A}.ts-info .ts-ask,{A}.ts-info+.ts-ask{{margin-top:8px!important}}
{A}.tsp-list+.tsp-gh{{margin-top:16px!important}}
{A}.tsp-gh{{margin-bottom:4px!important}}
{A}.pg-h{{margin-bottom:4px!important}}
{A}.jr-k{{margin-bottom:4px!important}}
/* short screens keep the tighter title gap */
@media (max-height:700px){{#app .screen .scroll>.pbox,#app .screen .scroll>.tp-card{{margin-bottom:12px!important}}
{A}:is(.info-lead,.hw-p,.iv-calm,.tsp-lead){{margin-bottom:12px!important}}{A}.tsp-list+.tsp-gh{{margin-top:12px!important}}}}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
