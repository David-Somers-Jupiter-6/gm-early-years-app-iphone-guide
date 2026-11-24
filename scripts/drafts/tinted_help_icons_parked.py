"""How page tinted numbers + tinted help-block icons. usage: extra.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
i = s.index('#app #s4 .tc-nhsmark{background:#005eb8 url('); NHS = re.compile(r'url\(([^)]*)\)').search(s, i).group(1)
css = '''
/* How this guide works: numbers as pink tinted squares, like Contents */
#app :is(#how,#roadmap) :is(.hw-n,.rm-dot){width:28px!important;height:28px!important;border-radius:8px!important;border:0!important;background:var(--tp-bg)!important;color:var(--tp-fg)!important}
/* help-block icons as soft tints, each keeping its own meaning */
html{--ti-amber-bg:#fbecc7;--ti-amber:#8a5300;--ti-green-bg:#dcefe3;--ti-green:#00703c;--ti-slate-bg:#e3e9ec;--ti-slate:#2d5161}
@media (prefers-color-scheme:dark){html{--ti-amber-bg:#3a2c10;--ti-amber:#f5c36a;--ti-green-bg:#123224;--ti-green:#7fd6a2;--ti-slate-bg:#24323a;--ti-slate:#b7cbd6}}
#app .screen .abc-ic{box-shadow:none!important}
#app .screen .abc-ic.ic-issue{background:var(--ti-amber-bg)!important;color:var(--ti-amber)!important}
#app .screen .abc-ic.ic-info,#app .screen .ts-card .abc-ic.ic-info{background:var(--tb-bg)!important;color:var(--tb-fg)!important}
#app .screen .abc-ic.ic-do{background:var(--ti-green-bg)!important;color:var(--ti-green)!important}
#app .screen .abc-ic.ic-do svg{color:var(--ti-green)!important;stroke:var(--ti-green)!important}
#app .screen .abc-ic.ic-ask,#app .screen .ts-ask .abc-ic.ic-ask{background:var(--ti-slate-bg)!important;color:var(--ti-slate)!important}
#app .screen .ts-card .abc-ic.ic-info{background:#fff!important}
@media (prefers-color-scheme:dark){#app .screen .ts-card .abc-ic.ic-info{background:#0d1a27!important}}
/* tinted icons are a touch larger, so they hold their own at small size */
#app .screen .abc-k>.abc-ic,#app .screen .abc-row .abc-ic:not(.ts-hi){width:22px!important;height:22px!important;font-size:13px!important}
#app .screen .abc-ic.who-nhs{background:var(--tb-bg)!important;background-image:none!important}
#app .screen .abc-ic.who-nhs::after{content:"";position:absolute;inset:0;background:var(--tb-fg);-webkit-mask:url(NHS) center/78% auto no-repeat;mask:url(NHS) center/78% auto no-repeat}
#app .screen .abc-ic.who-gm{background:var(--tp-bg)!important}
'''.replace('url(NHS)', 'url(%s)' % NHS)
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
